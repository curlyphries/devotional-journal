import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { renderWithApp } from '../test/renderWithApp'
import ProfilePage from './ProfilePage'
import * as guidesApi from '../api/guides'
import * as profileApi from '../api/profile'
import * as promptsApi from '../api/prompts'
import type { ApiError } from '../api/errors'
import { DISCLAIMER, catalog, makeFullProfile, makeProfile } from '../components/growth/testFixtures'

vi.mock('../api/guides', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/guides')>()
  return { ...actual, getCatalog: vi.fn(), startStudy: vi.fn() }
})
vi.mock('../api/profile', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/profile')>()
  return {
    ...actual,
    getGrowthProfile: vi.fn(),
    updateGrowthProfile: vi.fn(),
    submitAssessment: vi.fn(),
    generateProfileInsights: vi.fn(),
    sendInsightFeedback: vi.fn(),
    eraseGrowthProfile: vi.fn(),
  }
})
vi.mock('../api/prompts', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/prompts')>()
  return { ...actual, getAiStatus: vi.fn() }
})

const guides = vi.mocked(guidesApi)
const api = vi.mocked(profileApi)
const prompts = vi.mocked(promptsApi)

beforeEach(() => {
  vi.clearAllMocks()
  guides.getCatalog.mockResolvedValue(catalog)
  prompts.getAiStatus.mockResolvedValue({
    backend: 'ollama',
    model: 'llama3.1:8b',
    reachable: true,
    configured: true,
    local: true,
  })
})

describe('ProfilePage first run', () => {
  it('walks through the four steps and saves each one', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValue(makeProfile())
    renderWithApp(<ProfilePage />)

    // Step 1: about you
    expect(await screen.findByRole('heading', { level: 2, name: 'About you' })).toBeInTheDocument()
    expect(screen.getByText('Step 1 of 4')).toBeInTheDocument()
    await user.click(screen.getByRole('radio', { name: /^Adult/ }))
    await user.click(screen.getByRole('button', { name: 'Parent' }))
    await user.click(screen.getByRole('radio', { name: 'New to faith' }))

    const afterAbout = makeProfile({ exists: true, life_stage: 'adult', situations: ['parent'], faith_background: 'new' })
    api.updateGrowthProfile.mockResolvedValueOnce(afterAbout)
    await user.click(screen.getByRole('button', { name: 'Next' }))
    await waitFor(() =>
      expect(api.updateGrowthProfile).toHaveBeenCalledWith({
        situations: ['parent'],
        life_stage: 'adult',
        faith_background: 'new',
      }),
    )

    // Step 2: what you are looking for. The first save must not end the setup.
    expect(await screen.findByRole('heading', { level: 2, name: 'What you are looking for' })).toBeInTheDocument()
    expect(screen.getByText('Step 2 of 4')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Anxiety' }))
    await user.click(screen.getByRole('button', { name: 'Patience' }))
    expect(screen.getByText('Staying steady when things are slow or hard.')).toBeInTheDocument()

    api.updateGrowthProfile.mockResolvedValueOnce({ ...afterAbout, needs: ['anxiety'], desired_traits: ['patience'] })
    await user.click(screen.getByRole('button', { name: 'Next' }))
    await waitFor(() =>
      expect(api.updateGrowthProfile).toHaveBeenLastCalledWith({ needs: ['anxiety'], desired_traits: ['patience'] }),
    )

    // Step 3: a look inward, under its two headings, with the scale shown once
    expect(await screen.findByRole('heading', { level: 2, name: 'A quick look inward' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 3, name: 'Your walk with God' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 3, name: 'How you are doing inside' })).toBeInTheDocument()
    expect(screen.getAllByText(catalog.assessment.scale)).toHaveLength(1)
    const prayer = screen.getByRole('radiogroup', { name: 'I pray most days.' })
    await user.click(within(prayer).getByRole('radio', { name: '4 out of 5' }))

    api.submitAssessment.mockResolvedValueOnce(afterAbout)
    await user.click(screen.getByRole('button', { name: 'Next' }))
    await waitFor(() => expect(api.submitAssessment).toHaveBeenCalledWith({ answers: { prayer: 4 }, trait_ratings: {} }))

    // Step 4: self-rating, the chosen characteristic first and the rest behind "rate more"
    expect(await screen.findByRole('heading', { level: 2, name: 'How you see yourself today' })).toBeInTheDocument()
    expect(screen.queryByRole('radiogroup', { name: 'Kindness' })).not.toBeInTheDocument()
    await user.click(within(screen.getByRole('radiogroup', { name: 'Patience' })).getByRole('radio', { name: '2 out of 5' }))
    await user.click(screen.getByRole('button', { name: /Rate more characteristics/ }))
    expect(screen.getByRole('radiogroup', { name: 'Kindness' })).toBeInTheDocument()

    api.submitAssessment.mockResolvedValueOnce(makeFullProfile())
    await user.click(screen.getByRole('button', { name: 'Finish' }))
    await waitFor(() =>
      expect(api.submitAssessment).toHaveBeenLastCalledWith({ answers: { prayer: 4 }, trait_ratings: { patience: 2 } }),
    )

    // Finished: the profile itself is shown
    expect(await screen.findByRole('heading', { level: 2, name: 'What the app notices' })).toBeInTheDocument()
    expect(screen.queryByText(/Step \d of \d/)).not.toBeInTheDocument()
  })

  it('lets every step be skipped without saving it, and still creates the profile at the end', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValue(makeProfile())
    api.updateGrowthProfile.mockResolvedValue(makeProfile({ exists: true }))
    renderWithApp(<ProfilePage />)

    await screen.findByRole('heading', { level: 2, name: 'About you' })
    for (let step = 0; step < 3; step += 1) {
      await user.click(screen.getByRole('button', { name: 'Skip this step' }))
    }
    expect(screen.getByText('Step 4 of 4')).toBeInTheDocument()
    expect(api.updateGrowthProfile).not.toHaveBeenCalled()

    await user.click(screen.getByRole('button', { name: 'Skip this step' }))
    await waitFor(() =>
      expect(api.updateGrowthProfile).toHaveBeenCalledWith({ situations: [], needs: [], desired_traits: [] }),
    )
    expect(api.submitAssessment).not.toHaveBeenCalled()
    expect(await screen.findByRole('heading', { level: 2, name: 'Your data' })).toBeInTheDocument()
  })

  it('skips the inward steps for a child and says plainly why', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValue(makeProfile())
    renderWithApp(<ProfilePage />)

    await screen.findByRole('heading', { level: 2, name: 'About you' })
    await user.click(screen.getByRole('radio', { name: /^Child/ }))

    const child = makeProfile({ exists: true, life_stage: 'child', profiling_enabled: false })
    api.updateGrowthProfile.mockResolvedValue(child)
    await user.click(screen.getByRole('button', { name: 'Next' }))
    await waitFor(() => expect(api.updateGrowthProfile).toHaveBeenCalledWith({ situations: [], life_stage: 'child' }))

    expect(await screen.findByRole('heading', { level: 2, name: 'What you are looking for' })).toBeInTheDocument()
    expect(screen.getByText('Step 2 of 2')).toBeInTheDocument()
    expect(screen.getByText(/the app only uses age to choose gentler, simpler lessons/)).toBeInTheDocument()

    // The second step is the last one: no look inward, no self-rating.
    await user.click(screen.getByRole('button', { name: 'Finish' }))
    await waitFor(() => expect(api.updateGrowthProfile).toHaveBeenLastCalledWith({ needs: [], desired_traits: [] }))
    expect(api.submitAssessment).not.toHaveBeenCalled()

    // The profile view hides the inner-life picture and the AI reflection, with the explanation.
    expect(await screen.findByRole('heading', { level: 2, name: 'No profile is built for a child' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'How you are doing inside' })).not.toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'What the app notices' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Write my reflection' })).not.toBeInTheDocument()
    expect(screen.getByText(DISCLAIMER)).toBeInTheDocument()
  })

  it('keeps the person on the step and shows the error when a save fails', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValue(makeProfile())
    const failure: ApiError = { code: 'SERVER_ERROR', message: 'The server had a problem.', status: 500 }
    api.updateGrowthProfile.mockRejectedValue(failure)
    renderWithApp(<ProfilePage />)

    await screen.findByRole('heading', { level: 2, name: 'About you' })
    await user.click(screen.getByRole('button', { name: 'Next' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('The server had a problem.')
    expect(screen.getByText('Step 1 of 4')).toBeInTheDocument()
  })
})

describe('ProfilePage profile view', () => {
  it('shows neutral bars, the support note, both trait lists and the disclaimer', async () => {
    api.getGrowthProfile.mockResolvedValue(
      makeFullProfile({ support: { message: 'If things feel heavy, talk to someone you trust today.' } }),
    )
    renderWithApp(<ProfilePage />)

    expect(await screen.findByRole('heading', { level: 1, name: 'My growth profile' })).toBeInTheDocument()
    expect(await screen.findByText('If things feel heavy, talk to someone you trust today.')).toBeInTheDocument()

    // Practices: a bar per item, "Not answered" where there is no score
    const prayer = screen.getByRole('meter', { name: 'Prayer' })
    expect(prayer).toHaveAttribute('aria-valuenow', '4')
    expect(prayer).toHaveAttribute('aria-valuemax', '5')
    expect(screen.queryByRole('meter', { name: 'Bible reading' })).not.toBeInTheDocument()
    const walk = screen.getByRole('region', { name: 'Your walk with God' })
    expect(within(walk).getByText('Bible reading')).toBeInTheDocument()
    expect(within(walk).getByText('Not answered')).toBeInTheDocument()
    expect(screen.getByRole('meter', { name: 'Peace' })).toHaveAttribute('aria-valuenow', '2')

    // Described in words, never as good/bad
    expect(within(screen.getByRole('list', { name: 'Strong today' })).getByText('Kindness')).toBeInTheDocument()
    expect(within(screen.getByRole('list', { name: 'Room to grow' })).getByText('Patience')).toBeInTheDocument()

    // Counts, moods, lesson averages, threads
    expect(screen.getByText('Journal entries with feedback')).toBeInTheDocument()
    expect(screen.getByText('12')).toBeInTheDocument()
    expect(screen.getByText('Grateful')).toBeInTheDocument()
    expect(screen.getByText('4.2 of 5')).toBeInTheDocument()
    expect(screen.getByText(/You have 2 open threads/)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'See your threads' })).toHaveAttribute('href', '/threads')

    // History, newest first
    const rows = within(screen.getByRole('table')).getAllByRole('row')
    expect(rows).toHaveLength(3)
    expect(rows[1]).toHaveTextContent('4.0')
    expect(rows[1]).toHaveTextContent('2.5')
    expect(screen.getByRole('button', { name: 'Retake the look inward' })).toBeInTheDocument()

    // The reflection, what it is based on, and where it was written
    expect(screen.getByText('You are showing up steadily, even in a tiring season.')).toBeInTheDocument()
    expect(screen.getByText('You rated “I pray most days” 4 of 5.')).toBeInTheDocument()
    expect(screen.getByText('ollama · llama3.1:8b')).toBeInTheDocument()
    expect(screen.getByText('on your network')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Start a growth plan for Patience' })).toHaveAttribute(
      'href',
      '/growth?trait=patience',
    )
    expect(screen.getByText(DISCLAIMER)).toBeInTheDocument()

    // Easy ways out
    expect(screen.getByRole('button', { name: 'Erase my profile' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'See the audit log' })).toHaveAttribute('href', '/audit')
    expect(screen.getByRole('link', { name: 'How studies and the profile work' })).toHaveAttribute('href', '/help#study')
  })

  it('saves the free-text note', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValue(makeFullProfile())
    api.updateGrowthProfile.mockResolvedValue(makeFullProfile({ about_me: 'I work nights. I am not a parent.' }))
    renderWithApp(<ProfilePage />)

    const box = await screen.findByLabelText('Anything you want the app to know, or that it has gotten wrong?')
    expect(box).toHaveValue('I work nights.')
    await user.type(box, ' I am not a parent.')
    await user.click(screen.getByRole('button', { name: 'Save' }))

    await waitFor(() =>
      expect(api.updateGrowthProfile).toHaveBeenCalledWith({ about_me: 'I work nights. I am not a parent.' }),
    )
  })

  it('posts insight feedback and clears it on a second click', async () => {
    const user = userEvent.setup()
    const profile = makeFullProfile()
    const withAnswer = (accurate: boolean | null) =>
      makeFullProfile({
        insights: {
          ...profile.insights!,
          items: profile.insights!.items.map((item) => (item.id === 'i1' ? { ...item, accurate } : item)),
        },
      })
    api.getGrowthProfile.mockResolvedValue(profile)
    renderWithApp(<ProfilePage />)

    const group = await screen.findByRole('group', { name: 'Is this right? Prayer is a steady habit' })
    const right = () => within(group).getByRole('button', { name: "That's right" })
    const notMe = () => within(group).getByRole('button', { name: "That's not me" })
    expect(right()).toHaveAttribute('aria-pressed', 'false')

    api.sendInsightFeedback.mockResolvedValueOnce(withAnswer(true))
    await user.click(right())
    await waitFor(() => expect(api.sendInsightFeedback).toHaveBeenLastCalledWith('i1', true))
    await waitFor(() => expect(right()).toHaveAttribute('aria-pressed', 'true'))
    expect(within(group).getByText('Saved: you said this is right.')).toBeInTheDocument()

    // Clicking the chosen answer again clears it
    api.sendInsightFeedback.mockResolvedValueOnce(withAnswer(null))
    await user.click(right())
    await waitFor(() => expect(api.sendInsightFeedback).toHaveBeenLastCalledWith('i1', null))
    await waitFor(() => expect(right()).toHaveAttribute('aria-pressed', 'false'))

    api.sendInsightFeedback.mockResolvedValueOnce(withAnswer(false))
    await user.click(notMe())
    await waitFor(() => expect(api.sendInsightFeedback).toHaveBeenLastCalledWith('i1', false))
    await waitFor(() => expect(notMe()).toHaveAttribute('aria-pressed', 'true'))
    expect(within(group).getByText('Saved: you said this is not you.')).toBeInTheDocument()
  })

  it('says where the AI runs before writing, and treats "not enough yet" as guidance', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValue(makeFullProfile({ insights: null }))
    const notEnough: ApiError = {
      code: 'VALIDATION_ERROR',
      message: 'There is not enough to reflect on yet.',
      suggestion: 'Take the look inward or finish a lesson first, then try again.',
      status: 400,
    }
    api.generateProfileInsights.mockRejectedValue(notEnough)
    renderWithApp(<ProfilePage />)

    expect(await screen.findByText(/The AI runs on your own network \(ollama · llama3.1:8b\)/)).toBeInTheDocument()
    expect(screen.getByText(DISCLAIMER)).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Write my reflection' }))

    expect(await screen.findByText('Take the look inward or finish a lesson first, then try again.')).toBeInTheDocument()
    expect(screen.getByText('There is not enough to go on yet')).toBeInTheDocument()
    // Guidance, not an error
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Write my reflection' })).toBeInTheDocument()
  })

  it('shows a real AI failure as an error with its suggestion and a retry', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValue(makeFullProfile({ insights: null }))
    const unavailable: ApiError = {
      code: 'AI_UNAVAILABLE',
      message: 'The AI provider is not responding.',
      suggestion: 'Check that your local model server is running.',
      status: 503,
    }
    api.generateProfileInsights.mockRejectedValueOnce(unavailable).mockResolvedValueOnce(makeFullProfile())
    renderWithApp(<ProfilePage />)

    await user.click(await screen.findByRole('button', { name: 'Write my reflection' }))
    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('The AI provider is not responding.')
    expect(alert).toHaveTextContent('Check that your local model server is running.')

    await user.click(within(alert).getByRole('button', { name: 'Try again' }))
    expect(await screen.findByText('You are showing up steadily, even in a tiring season.')).toBeInTheDocument()
  })

  it('erases the profile after confirmation and returns to first run', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValueOnce(makeFullProfile()).mockResolvedValue(makeProfile())
    api.eraseGrowthProfile.mockResolvedValue(undefined)
    renderWithApp(<ProfilePage />)

    await user.click(await screen.findByRole('button', { name: 'Erase my profile' }))
    const dialog = screen.getByRole('dialog', { name: 'Erase your growth profile?' })
    expect(dialog).toHaveTextContent('Your journal entries, your studies and your growth plans are kept.')
    expect(api.eraseGrowthProfile).not.toHaveBeenCalled()

    await user.click(within(dialog).getByRole('button', { name: 'Erase my profile' }))
    await waitFor(() => expect(api.eraseGrowthProfile).toHaveBeenCalledTimes(1))

    expect(await screen.findByText('Step 1 of 4')).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Your data' })).not.toBeInTheDocument()
  })

  it('does not erase when the dialog is cancelled', async () => {
    const user = userEvent.setup()
    api.getGrowthProfile.mockResolvedValue(makeFullProfile())
    renderWithApp(<ProfilePage />)

    await user.click(await screen.findByRole('button', { name: 'Erase my profile' }))
    await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Cancel' }))

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(api.eraseGrowthProfile).not.toHaveBeenCalled()
  })
})
