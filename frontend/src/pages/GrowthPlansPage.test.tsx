import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes, useLocation } from 'react-router-dom'
import { renderWithApp } from '../test/renderWithApp'
import GrowthPlansPage from './GrowthPlansPage'
import * as guidesApi from '../api/guides'
import * as plansApi from '../api/growthPlans'
import * as profileApi from '../api/profile'
import * as promptsApi from '../api/prompts'
import type { ApiError } from '../api/errors'
import { catalog, makePlan, makeProfile } from '../components/growth/testFixtures'

vi.mock('../api/guides', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/guides')>()
  return { ...actual, getCatalog: vi.fn(), startStudy: vi.fn() }
})
vi.mock('../api/growthPlans', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/growthPlans')>()
  return { ...actual, listGrowthPlans: vi.fn(), createGrowthPlan: vi.fn() }
})
vi.mock('../api/profile', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/profile')>()
  return { ...actual, getGrowthProfile: vi.fn() }
})
vi.mock('../api/prompts', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/prompts')>()
  return { ...actual, getAiStatus: vi.fn() }
})

const guides = vi.mocked(guidesApi)
const api = vi.mocked(plansApi)
const profile = vi.mocked(profileApi)
const prompts = vi.mocked(promptsApi)

/** Stand-in for the plan page: shows where we landed and what was carried along. */
function Landed() {
  const location = useLocation()
  return (
    <p>
      landed on {location.pathname} {JSON.stringify(location.state)}
    </p>
  )
}

function renderPage(route = '/growth') {
  return renderWithApp(
    <Routes>
      <Route path="/growth" element={<GrowthPlansPage />} />
      <Route path="/growth/:planId" element={<Landed />} />
    </Routes>,
    { route },
  )
}

beforeEach(() => {
  vi.clearAllMocks()
  guides.getCatalog.mockResolvedValue(catalog)
  profile.getGrowthProfile.mockResolvedValue(makeProfile())
  prompts.getAiStatus.mockResolvedValue({
    backend: 'anthropic',
    model: 'claude',
    reachable: true,
    configured: true,
    local: false,
  })
})

describe('GrowthPlansPage', () => {
  it('lists plans with the stage label, percent and a check-in marker', async () => {
    api.listGrowthPlans.mockResolvedValue([
      makePlan(),
      makePlan({
        id: 'p2',
        trait: { key: 'kindness', title: 'Kindness', definition: 'Doing good to others.' },
        status: 'paused',
        why: '',
        progress: { ...makePlan().progress, percent: 60, stage_label: 'Holding steady', check_in_due: true },
      }),
    ])
    renderPage()

    expect(screen.getByRole('heading', { level: 1, name: 'Growth plans' })).toBeInTheDocument()
    const items = await screen.findAllByRole('listitem')
    const first = items.find((item) => within(item).queryByRole('heading', { name: 'Patience' }))!
    const second = items.find((item) => within(item).queryByRole('heading', { name: 'Kindness' }))!

    expect(within(first).getByRole('link', { name: 'Patience' })).toHaveAttribute('href', '/growth/p1')
    expect(within(first).getByText('I snap at my kids when I am tired.')).toBeInTheDocument()
    const meter = within(first).getByRole('meter', { name: 'Building the habit' })
    expect(meter).toHaveAttribute('aria-valuenow', '35')
    expect(meter).toHaveAttribute('aria-valuetext', '35%')
    expect(within(first).getByText('Check-in due')).toBeInTheDocument()
    expect(within(first).getByRole('link', { name: 'Open the plan for Patience' })).toHaveAttribute('href', '/growth/p1')

    // A paused plan says so, and does not nag about a check-in
    expect(within(second).getByText('Paused')).toBeInTheDocument()
    expect(within(second).getByRole('meter', { name: 'Holding steady' })).toHaveAttribute('aria-valuenow', '60')
    expect(within(second).queryByText('Check-in due')).not.toBeInTheDocument()

    // The start form stays out of the way until asked for
    expect(screen.queryByRole('heading', { name: 'Start a plan' })).not.toBeInTheDocument()
    await userEvent.setup().click(screen.getByRole('button', { name: 'Start another plan' }))
    expect(screen.getByRole('heading', { name: 'Start a plan' })).toBeInTheDocument()
  })

  it('preselects the characteristic from ?trait= and posts the full payload', async () => {
    const user = userEvent.setup()
    api.listGrowthPlans.mockResolvedValue([])
    const created = makePlan({
      id: 'p9',
      personalize_error: { code: 'AI_UNAVAILABLE', message: 'The AI is not responding.', suggestion: 'Try later.' },
    })
    api.createGrowthPlan.mockResolvedValue(created)
    renderPage('/growth?trait=patience')

    const chip = await screen.findByRole('button', { name: 'Patience' })
    expect(chip).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByText('Staying steady when things are slow or hard.')).toBeInTheDocument()

    await user.type(screen.getByLabelText(/Why does this matter to you\?/), 'I snap when tired.')
    const baseline = screen.getByRole('radiogroup', { name: 'Where are you today?' })
    await user.click(within(baseline).getByRole('radio', { name: '2 out of 5' }))

    // AI tailoring is off unless asked for, and says where it would run
    const tailor = screen.getByRole('checkbox', { name: 'Tailor the goals to me with AI' })
    expect(tailor).not.toBeChecked()
    expect(screen.getByText(/The AI is a cloud service \(anthropic · claude\), so this is sent to it\./)).toBeInTheDocument()
    await user.click(tailor)

    await user.click(screen.getByRole('button', { name: 'Start my plan for Patience' }))

    await waitFor(() =>
      expect(api.createGrowthPlan).toHaveBeenCalledWith({
        trait: 'patience',
        why: 'I snap when tired.',
        baseline_rating: 2,
        personalize: true,
      }),
    )
    // Goes to the new plan, carrying the "could not tailor" notice with it
    const landed = await screen.findByText(/landed on \/growth\/p9/)
    expect(landed).toHaveTextContent('The AI is not responding.')
  })

  it('sends only the characteristic when nothing else is filled in', async () => {
    const user = userEvent.setup()
    api.listGrowthPlans.mockResolvedValue([])
    api.createGrowthPlan.mockResolvedValue(makePlan({ id: 'p3' }))
    renderPage()

    expect(await screen.findByText('You have not started a growth plan yet')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Start this plan' })).toBeDisabled()

    await user.click(await screen.findByRole('button', { name: 'Kindness' }))
    await user.click(screen.getByRole('button', { name: 'Start my plan for Kindness' }))

    await waitFor(() => expect(api.createGrowthPlan).toHaveBeenCalledWith({ trait: 'kindness' }))
    expect(await screen.findByText(/landed on \/growth\/p3/)).toBeInTheDocument()
  })

  it('suggests the characteristics from the profile when there are no plans', async () => {
    const user = userEvent.setup()
    api.listGrowthPlans.mockResolvedValue([])
    profile.getGrowthProfile.mockResolvedValue(makeProfile({ exists: true, desired_traits: ['humility'] }))
    renderPage()

    expect(await screen.findByText('In your profile you said you want to grow in:')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Start a plan for Humility' }))

    expect(screen.getByRole('button', { name: 'Humility' })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByText('Seeing yourself truthfully before God.')).toBeInTheDocument()
  })

  it('points at the existing plan instead of starting a duplicate', async () => {
    api.listGrowthPlans.mockResolvedValue([makePlan()])
    renderPage('/growth?trait=patience')

    expect(await screen.findByText('You already have an active plan for Patience.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Open that plan' })).toHaveAttribute('href', '/growth/p1')
    expect(screen.queryByRole('button', { name: /Start my plan/ })).not.toBeInTheDocument()
  })

  it('shows the server message when the plan cannot be started', async () => {
    const user = userEvent.setup()
    api.listGrowthPlans.mockResolvedValue([])
    const failure: ApiError = {
      code: 'VALIDATION_ERROR',
      message: 'You already have an active plan for this characteristic.',
      suggestion: 'Open it from your list of plans.',
      status: 400,
    }
    api.createGrowthPlan.mockRejectedValue(failure)
    renderPage('/growth?trait=courage')

    await user.click(await screen.findByRole('button', { name: 'Start my plan for Courage' }))

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('You already have an active plan for this characteristic.')
    expect(alert).toHaveTextContent('Open it from your list of plans.')
  })

  it('shows an error with retry when the plans cannot be loaded', async () => {
    const failure: ApiError = { code: 'SERVER_ERROR', message: 'The server had a problem.', status: 500 }
    api.listGrowthPlans.mockRejectedValue(failure)
    renderPage()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('Your growth plans could not be loaded')
    expect(within(alert).getByRole('button', { name: 'Try again' })).toBeInTheDocument()
  })
})
