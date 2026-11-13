import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router-dom'
import { renderWithApp } from '../test/renderWithApp'
import GrowthPlanPage from './GrowthPlanPage'
import * as guidesApi from '../api/guides'
import * as plansApi from '../api/growthPlans'
import type { ApiError } from '../api/errors'
import { makePlan, makeTopic } from '../components/growth/testFixtures'

vi.mock('../api/guides', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/guides')>()
  return { ...actual, getCatalog: vi.fn(), startStudy: vi.fn() }
})
vi.mock('../api/growthPlans', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/growthPlans')>()
  return {
    ...actual,
    listGrowthPlans: vi.fn(),
    getGrowthPlan: vi.fn(),
    updateGrowthPlan: vi.fn(),
    deleteGrowthPlan: vi.fn(),
    addGrowthGoal: vi.fn(),
    updateGrowthGoal: vi.fn(),
    deleteGrowthGoal: vi.fn(),
    addGrowthCheckIn: vi.fn(),
  }
})

const guides = vi.mocked(guidesApi)
const api = vi.mocked(plansApi)

function renderPage(route = '/growth/p1') {
  return renderWithApp(
    <Routes>
      <Route path="/growth" element={<p>the list of plans</p>} />
      <Route path="/growth/:planId" element={<GrowthPlanPage />} />
      <Route path="/study/:studyId" element={<p>the study</p>} />
    </Routes>,
    { route },
  )
}

beforeEach(() => {
  vi.clearAllMocks()
  api.listGrowthPlans.mockResolvedValue([])
})

describe('GrowthPlanPage', () => {
  it('shows the plan: why, progress, scripture, and how Jesus showed it', async () => {
    api.getGrowthPlan.mockResolvedValue(makePlan())
    renderPage()

    expect(await screen.findByRole('heading', { level: 1, name: 'Patience' })).toBeInTheDocument()
    expect(api.getGrowthPlan).toHaveBeenCalledWith('p1')
    expect(screen.getByText('Staying steady when things are slow or hard.')).toBeInTheDocument()
    expect(screen.getByText('I snap at my kids when I am tired.')).toBeInTheDocument()

    const progress = screen.getByRole('region', { name: 'Progress status' })
    expect(within(progress).getByRole('meter', { name: 'Building the habit' })).toHaveAttribute('aria-valuenow', '35')
    expect(within(progress).getByText('You are twelve days in and practising regularly.')).toBeInTheDocument()
    expect(within(progress).getByText('Day 12 of 90')).toBeInTheDocument()
    expect(within(progress).getByText('From 2 to 3')).toBeInTheDocument()
    expect(within(progress).getByText('1 of 4 done')).toBeInTheDocument()

    const scripture = screen.getByRole('region', { name: 'In Scripture' })
    expect(within(scripture).getByRole('link', { name: 'Open James 1:2-4 in the Bible' })).toHaveAttribute(
      'href',
      '/bible?passage=James%201%3A2-4',
    )
    expect(within(scripture).getByRole('heading', { name: 'How Jesus showed it' })).toBeInTheDocument()
    expect(within(scripture).getByText('He made time for the children when others were in a hurry.')).toBeInTheDocument()
    expect(within(scripture).getByRole('link', { name: 'Open Mark 10:13-16 in the Bible' })).toBeInTheDocument()

    // A study the person is already in links straight to it
    const studies = screen.getByRole('region', { name: 'Studies that build this' })
    expect(within(studies).getByRole('link', { name: 'Continue the study “Anxiety”' })).toHaveAttribute('href', '/study/s1')

    expect(screen.getByText('Goals from the standard plan.')).toBeInTheDocument()
    expect(screen.queryByText(/could not be tailored by AI/)).not.toBeInTheDocument()
  })

  it('keeps short-term and long-term goals in separate groups, finished ones folded below', async () => {
    api.getGrowthPlan.mockResolvedValue(makePlan())
    renderPage()

    const short = await screen.findByRole('region', { name: 'Short-term goals' })
    const long = screen.getByRole('region', { name: 'Long-term goals' })

    expect(within(short).getByText('Pause and breathe before answering')).toBeInTheDocument()
    expect(within(short).getByText('Complete two lessons on patience')).toBeInTheDocument()
    expect(within(short).queryByText('Finish the patience study')).not.toBeInTheDocument()
    expect(within(short).getByText('45% done')).toBeInTheDocument()
    expect(within(short).getByText('2 / 5')).toBeInTheDocument()
    expect(within(short).getByText('Practice')).toBeInTheDocument()

    expect(within(long).getByText('Finish the patience study')).toBeInTheDocument()
    expect(within(long).queryByText('Pause and breathe before answering')).not.toBeInTheDocument()

    // The finished goal sits in the collapsed group at the bottom of its own horizon
    const finished = within(long).getByText('Finished or skipped (1)').closest('details')!
    expect(finished).not.toHaveAttribute('open')
    expect(within(finished).getByText('Pray for patience each morning')).toBeInTheDocument()
    expect(within(finished).getByRole('button', { name: 'Reopen “Pray for patience each morning”' })).toBeInTheDocument()
    expect(within(short).queryByText(/Finished or skipped/)).not.toBeInTheDocument()
  })

  it('adds one to a manual goal, and offers no +1 on an automatic goal', async () => {
    const user = userEvent.setup()
    const plan = makePlan()
    api.getGrowthPlan.mockResolvedValue(plan)
    api.updateGrowthGoal.mockResolvedValue(
      makePlan({ goals: plan.goals.map((goal) => (goal.id === 'g1' ? { ...goal, progress_count: 3, percent: 60 } : goal)) }),
    )
    renderPage()

    const short = await screen.findByRole('region', { name: 'Short-term goals' })
    expect(
      within(short).queryByRole('button', { name: 'Add one to “Complete two lessons on patience”' }),
    ).not.toBeInTheDocument()
    expect(within(short).getByText('Counts automatically as you complete lessons.')).toBeInTheDocument()

    await user.click(within(short).getByRole('button', { name: 'Add one to “Pause and breathe before answering”' }))

    await waitFor(() => expect(api.updateGrowthGoal).toHaveBeenCalledWith('p1', 'g1', { add: 1 }))
    expect(await within(short).findByText('3 / 5')).toBeInTheDocument()
  })

  it('marks a goal done, and shows the error when a goal change fails', async () => {
    const user = userEvent.setup()
    api.getGrowthPlan.mockResolvedValue(makePlan())
    const failure: ApiError = { code: 'SERVER_ERROR', message: 'The server had a problem.', status: 500 }
    api.updateGrowthGoal.mockRejectedValue(failure)
    renderPage()

    await user.click(await screen.findByRole('button', { name: 'Mark “Pause and breathe before answering” as done' }))

    await waitFor(() => expect(api.updateGrowthGoal).toHaveBeenCalledWith('p1', 'g1', { status: 'done' }))
    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('The goal could not be updated.')
    expect(alert).toHaveTextContent('The server had a problem.')
  })

  it('adds a goal of the person’s own', async () => {
    const user = userEvent.setup()
    api.getGrowthPlan.mockResolvedValue(makePlan())
    api.addGrowthGoal.mockResolvedValue(makePlan())
    renderPage()

    await user.click(await screen.findByRole('button', { name: 'Add a goal' }))
    await user.type(screen.getByLabelText('Goal'), 'Thank one person each day')
    await user.click(screen.getByRole('radio', { name: 'Long-term' }))
    const count = screen.getByLabelText('How many times?')
    await user.clear(count)
    await user.type(count, '10')
    await user.click(screen.getByRole('button', { name: 'Add goal' }))

    await waitFor(() =>
      expect(api.addGrowthGoal).toHaveBeenCalledWith('p1', {
        title: 'Thank one person each day',
        horizon: 'long',
        target_count: 10,
        days: 90,
      }),
    )
  })

  it('prompts for a check-in when one is due and posts the rating and note', async () => {
    const user = userEvent.setup()
    const plan = makePlan()
    api.getGrowthPlan.mockResolvedValue(plan)
    api.addGrowthCheckIn.mockResolvedValue(
      makePlan({
        checkins: [{ id: 'c2', date: '2026-11-13', rating: 4, note: 'Held my tongue twice.' }, ...plan.checkins],
        progress: { ...plan.progress, check_in_due: false },
      }),
    )
    renderPage()

    const section = await screen.findByRole('region', { name: 'Check-ins' })
    expect(within(section).getByText('Check-in due')).toBeInTheDocument()
    expect(within(section).getByText('When were you patient this week, and when were you not?')).toBeInTheDocument()
    // Earlier check-ins are listed
    expect(within(section).getByText('Better at bedtime.')).toBeInTheDocument()
    expect(within(section).getByRole('img', { name: '3 of 5' })).toBeInTheDocument()

    const save = within(section).getByRole('button', { name: 'Save check-in' })
    expect(save).toBeDisabled()
    const rating = within(section).getByRole('radiogroup', { name: 'How true is this of you this week?' })
    await user.click(within(rating).getByRole('radio', { name: '4 out of 5' }))
    await user.type(within(section).getByLabelText(/Anything you want to remember\?/), 'Held my tongue twice.')
    await user.click(save)

    await waitFor(() =>
      expect(api.addGrowthCheckIn).toHaveBeenCalledWith('p1', { rating: 4, note: 'Held my tongue twice.' }),
    )
    // The new check-in appears and the prompt steps back
    expect(await within(section).findByText('Held my tongue twice.')).toBeInTheDocument()
    await waitFor(() => expect(within(section).queryByText('Check-in due')).not.toBeInTheDocument())
    expect(within(section).getByRole('button', { name: 'Check in now' })).toBeInTheDocument()
  })

  it('pauses and resumes the plan', async () => {
    const user = userEvent.setup()
    api.getGrowthPlan.mockResolvedValue(makePlan())
    renderPage()

    api.updateGrowthPlan.mockResolvedValueOnce(makePlan({ status: 'paused' }))
    await user.click(await screen.findByRole('button', { name: 'Pause' }))
    await waitFor(() => expect(api.updateGrowthPlan).toHaveBeenLastCalledWith('p1', { status: 'paused' }))

    const resume = await screen.findByRole('button', { name: 'Resume' })
    expect(screen.queryByRole('button', { name: 'Pause' })).not.toBeInTheDocument()
    expect(screen.getByText('Paused')).toBeInTheDocument()

    api.updateGrowthPlan.mockResolvedValueOnce(makePlan({ status: 'active' }))
    await user.click(resume)
    await waitFor(() => expect(api.updateGrowthPlan).toHaveBeenLastCalledWith('p1', { status: 'active' }))
    expect(await screen.findByRole('button', { name: 'Pause' })).toBeInTheDocument()
  })

  it('marks the plan complete', async () => {
    const user = userEvent.setup()
    api.getGrowthPlan.mockResolvedValue(makePlan())
    api.updateGrowthPlan.mockResolvedValue(makePlan({ status: 'completed' }))
    renderPage()

    await user.click(await screen.findByRole('button', { name: 'Mark complete' }))

    await waitFor(() => expect(api.updateGrowthPlan).toHaveBeenCalledWith('p1', { status: 'completed' }))
    expect(await screen.findByRole('button', { name: 'Reopen plan' })).toBeInTheDocument()
  })

  it('deletes the plan only after confirmation, then returns to the list', async () => {
    const user = userEvent.setup()
    api.getGrowthPlan.mockResolvedValue(makePlan())
    api.deleteGrowthPlan.mockResolvedValue(undefined)
    renderPage()

    await user.click(await screen.findByRole('button', { name: 'Delete' }))
    const dialog = screen.getByRole('dialog', { name: 'Delete this growth plan?' })
    expect(api.deleteGrowthPlan).not.toHaveBeenCalled()

    await user.click(within(dialog).getByRole('button', { name: 'Delete plan' }))
    await waitFor(() => expect(api.deleteGrowthPlan).toHaveBeenCalledWith('p1'))
    expect(await screen.findByText('the list of plans')).toBeInTheDocument()
  })

  it('shows the personalize notice as information and says the goals are the standard ones', async () => {
    api.getGrowthPlan.mockResolvedValue(
      makePlan({
        personalize_error: {
          code: 'AI_UNAVAILABLE',
          message: 'The AI provider is not responding.',
          suggestion: 'Check Settings → AI Provider.',
        },
      }),
    )
    renderPage()

    const notice = await screen.findByRole('note')
    expect(notice).toHaveTextContent('The goals could not be tailored by AI, so the standard plan was used')
    expect(notice).toHaveTextContent('The AI provider is not responding.')
    expect(notice).toHaveTextContent('Check Settings → AI Provider.')
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(screen.getByText('Goals from the standard plan.')).toBeInTheDocument()
  })

  it('says when the goals were written by AI', async () => {
    api.getGrowthPlan.mockResolvedValue(makePlan({ goal_source: 'ai' }))
    renderPage()

    expect(await screen.findByText('Goals written by AI for you.')).toBeInTheDocument()
  })

  it('starts a study that is not yet started and goes to it', async () => {
    const user = userEvent.setup()
    api.getGrowthPlan.mockResolvedValue(makePlan({ topics: [makeTopic({ key: 'waiting', title: 'Waiting well' })] }))
    guides.startStudy.mockResolvedValue({
      id: 's7',
      topic: { key: 'waiting', title: 'Waiting well', category: 'peace', sensitive: false },
      life_stage: 'adult',
      status: 'active',
      current_lesson: 1,
      lesson_count: 5,
      completed_lessons: [],
      progress_percent: 0,
      started_at: '2026-11-13T10:00:00Z',
      completed_at: null,
    })
    renderPage()

    await user.click(await screen.findByRole('button', { name: 'Start the study “Waiting well”' }))

    await waitFor(() => expect(guides.startStudy).toHaveBeenCalledWith('waiting'))
    expect(await screen.findByText('the study')).toBeInTheDocument()
  })

  it('shows a not-found state for a plan that no longer exists', async () => {
    const missing: ApiError = { code: 'NOT_FOUND', message: 'Not found.', status: 404 }
    api.getGrowthPlan.mockRejectedValue(missing)
    renderPage('/growth/gone')

    expect(await screen.findByRole('heading', { level: 1, name: 'Plan not found' })).toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(screen.getAllByRole('link', { name: 'All growth plans' })[0]).toHaveAttribute('href', '/growth')
  })

  it('shows an error with retry when the plan cannot be loaded', async () => {
    const failure: ApiError = { code: 'SERVER_ERROR', message: 'The server had a problem.', status: 500 }
    api.getGrowthPlan.mockRejectedValue(failure)
    renderPage()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('This plan could not be loaded')
    expect(within(alert).getByRole('button', { name: 'Try again' })).toBeInTheDocument()
  })
})
