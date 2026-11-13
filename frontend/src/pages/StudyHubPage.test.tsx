import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes, useParams } from 'react-router-dom'
import { renderWithApp } from '../test/renderWithApp'
import StudyHubPage from './StudyHubPage'
import * as guidesApi from '../api/guides'
import type { Catalog, Recommendations, Study, TopicCard } from '../api/guides'

vi.mock('../api/guides', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/guides')>()
  return {
    ...actual,
    getCatalog: vi.fn(),
    getRecommendations: vi.fn(),
    getProfileBasics: vi.fn(),
    setLifeStage: vi.fn(),
    getStudies: vi.fn(),
    startStudy: vi.fn(),
  }
})

const api = vi.mocked(guidesApi)

function topic(overrides: Partial<TopicCard>): TopicCard {
  return {
    key: 'anxiety',
    category: 'peace',
    title: 'When worry will not stop',
    summary: 'Handing your fears to God, one at a time.',
    lesson_count: 4,
    stages: ['teen', 'young_adult', 'adult', 'senior'],
    traits: ['trust'],
    sensitive: false,
    stage_note: null,
    enrollment: null,
    ...overrides,
  }
}

const anxiety = topic({ stage_note: 'For full lives: when the list never ends.' })
const rest = topic({
  key: 'rest',
  title: 'Rest for the weary',
  summary: 'Sabbath, sleep and the God who never slumbers.',
  stages: ['adult', 'senior'],
})
const grief = topic({
  key: 'grief',
  category: 'refuge',
  title: 'Grief and the God who weeps',
  summary: 'Lament, loss and hope that does not hurry you.',
  stages: ['adult', 'senior'],
  sensitive: true,
})
const bullying = topic({
  key: 'bullying',
  category: 'refuge',
  title: 'When someone is unkind',
  summary: 'What to do when you are picked on.',
  stages: ['child', 'teen'],
  lesson_count: 1,
})

const catalog: Catalog = {
  life_stages: [
    { key: 'child', title: 'Child (6-11), with a grown-up', note: 'Short, concrete lessons meant to be read together with a parent or guardian.' },
    { key: 'teen', title: 'Teen (12-17)', note: 'Honest about pressure, identity and questions.' },
    { key: 'young_adult', title: 'Young adult (18-29)', note: 'For years of big decisions: calling, relationships, direction.' },
    { key: 'adult', title: 'Adult (30-59)', note: 'For full lives: work, family, responsibility, weariness.' },
    { key: 'senior', title: 'Senior (60+)', note: 'For a season of looking back, letting go and leaving a legacy.' },
  ],
  situations: [],
  faith_backgrounds: [],
  categories: [
    { key: 'peace', title: 'Peace', summary: 'When your mind will not rest.', topics: [anxiety, rest] },
    { key: 'refuge', title: 'Refuge', summary: 'When life hurts and you need somewhere safe.', topics: [grief, bullying] },
  ],
  traits: [],
  assessment: { scale: '', items: [] },
}

const noRecommendations: Recommendations = { based_on: { entries_considered: 0, has_profile: false }, results: [] }

const activeStudy: Study = {
  id: 's-1',
  topic: { key: 'anxiety', title: 'When worry will not stop', category: 'peace', sensitive: false },
  life_stage: 'adult',
  status: 'active',
  current_lesson: 2,
  lesson_count: 4,
  completed_lessons: [1],
  progress_percent: 25,
  started_at: '2026-11-10T09:00:00Z',
  completed_at: null,
}

function StudyStub() {
  const { studyId } = useParams()
  return <p>Reader for study {studyId}</p>
}

function renderHub() {
  return renderWithApp(
    <Routes>
      <Route path="/study" element={<StudyHubPage />} />
      <Route path="/study/:studyId" element={<StudyStub />} />
    </Routes>,
    { route: '/study' }
  )
}

beforeEach(() => {
  vi.clearAllMocks()
  api.getCatalog.mockResolvedValue(catalog)
  api.getRecommendations.mockResolvedValue(noRecommendations)
  api.getProfileBasics.mockResolvedValue({ exists: true, life_stage: 'adult' })
  api.getStudies.mockResolvedValue([])
})

describe('StudyHubPage', () => {
  it('asks who the studies are for on a first visit, then opens the library', async () => {
    api.getProfileBasics.mockResolvedValue({ exists: false, life_stage: null })
    api.setLifeStage.mockResolvedValue({ exists: true, life_stage: 'adult' })
    const user = userEvent.setup()
    renderHub()

    expect(await screen.findByRole('heading', { name: 'First, who is this for?' })).toBeInTheDocument()
    // Every life stage is offered with its note.
    for (const stage of catalog.life_stages) {
      const button = screen.getByRole('button', { name: new RegExp(`^${stage.title.replace(/[()+]/g, '\\$&')}`) })
      expect(within(button).getByText(stage.note)).toBeInTheDocument()
    }
    expect(screen.getByRole('link', { name: 'Tell us more about you' })).toHaveAttribute('href', '/profile')
    // The library waits until they have chosen (or skipped).
    expect(screen.queryByRole('heading', { name: 'Find a study' })).not.toBeInTheDocument()
    expect(screen.queryByText(rest.title)).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: /^Adult \(30-59\)/ }))
    expect(api.setLifeStage).toHaveBeenCalledWith('adult')

    expect(await screen.findByRole('heading', { name: 'Find a study' })).toBeInTheDocument()
    expect(screen.getByLabelText('Who is this for?')).toHaveValue('adult')
    expect(screen.getByRole('heading', { name: rest.title })).toBeInTheDocument()
    // Suggestions and stage notes depend on the life stage, so they are fetched again.
    await waitFor(() => expect(api.getCatalog).toHaveBeenCalledTimes(2))
    expect(api.getRecommendations).toHaveBeenCalledTimes(2)
  })

  it('lets a first-time visitor skip the question and see every study', async () => {
    api.getProfileBasics.mockResolvedValue({ exists: false, life_stage: null })
    const user = userEvent.setup()
    renderHub()

    await user.click(await screen.findByRole('button', { name: 'Not now — show me every study' }))
    expect(api.setLifeStage).not.toHaveBeenCalled()
    expect(screen.getByRole('heading', { name: rest.title })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: bullying.title })).toBeInTheDocument()
    expect(screen.getByText('Showing studies for every age.')).toBeInTheDocument()
  })

  it('always shows why each study is suggested', async () => {
    api.getRecommendations.mockResolvedValue({
      based_on: { entries_considered: 5, has_profile: true },
      results: [
        {
          topic: anxiety,
          score: 9,
          reasons: ['Your recent entries mention “anxiety” 3 times.', 'You said you are caring for someone.'],
        },
      ],
    })
    renderHub()

    const suggested = (await screen.findByRole('heading', { name: 'Suggested for you' })).closest('section')!
    const card = (await within(suggested).findByRole('heading', { name: anxiety.title })).closest('article')!
    expect(within(card).getByText('Why this is suggested')).toBeInTheDocument()
    expect(within(card).getByText('Your recent entries mention “anxiety” 3 times.')).toBeVisible()
    expect(within(card).getByText('You said you are caring for someone.')).toBeVisible()
    expect(within(card).getByText('For full lives: when the list never ends.')).toBeInTheDocument()
    expect(within(card).getByRole('button', { name: `Start: ${anxiety.title}` })).toBeInTheDocument()
    expect(within(suggested).getByText(/Based on 5 recent journal entries\./)).toBeInTheDocument()
    expect(within(suggested).getByText(/Your profile was used too\./)).toBeInTheDocument()
  })

  it('explains how suggestions improve when there are none yet', async () => {
    renderHub()
    expect(await screen.findByText('No suggestions yet')).toBeInTheDocument()
    expect(screen.getByText(/Suggestions get better as you journal and fill in your profile/)).toBeInTheDocument()
  })

  it('filters by category, by search, and by age', async () => {
    const user = userEvent.setup()
    renderHub()

    // Default: only studies written for the person's life stage (adult).
    expect(await screen.findByRole('heading', { name: anxiety.title })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: rest.title })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: grief.title })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: bullying.title })).not.toBeInTheDocument()
    expect(screen.getByText('3 studies')).toBeInTheDocument()
    // A sensitive topic carries a care marker.
    const griefCard = screen.getByRole('heading', { name: grief.title }).closest('article')!
    expect(within(griefCard).getByText('Handled with care')).toBeInTheDocument()
    expect(within(griefCard).getByText('4 lessons')).toBeInTheDocument()

    // "I need…" chips.
    const chips = screen.getByRole('group', { name: 'I need…' })
    await user.click(within(chips).getByRole('button', { name: 'Refuge' }))
    expect(within(chips).getByRole('button', { name: 'Refuge' })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('heading', { name: grief.title })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: anxiety.title })).not.toBeInTheDocument()
    expect(screen.getAllByText('When life hurts and you need somewhere safe.').length).toBeGreaterThan(0)
    expect(screen.getByText('1 study')).toBeInTheDocument()

    await user.click(within(chips).getByRole('button', { name: 'Everything' }))
    expect(screen.getByRole('heading', { name: anxiety.title })).toBeInTheDocument()

    // Search looks at titles and summaries.
    const search = screen.getByRole('searchbox', { name: 'Search studies' })
    await user.type(search, 'sleep')
    expect(screen.getByRole('heading', { name: rest.title })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: anxiety.title })).not.toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: grief.title })).not.toBeInTheDocument()

    await user.clear(search)
    await user.type(search, 'zzz')
    expect(screen.getByText('No studies match')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Clear search and filters' }))
    expect(screen.getByText('3 studies')).toBeInTheDocument()

    // Every age.
    await user.click(screen.getByRole('checkbox', { name: 'Show studies for every age' }))
    const bullyingCard = screen.getByRole('heading', { name: bullying.title }).closest('article')!
    expect(within(bullyingCard).getByText('1 lesson')).toBeInTheDocument()
    expect(screen.getByText('4 studies')).toBeInTheDocument()
  })

  it('starts a study and opens it', async () => {
    api.startStudy.mockResolvedValue({ ...activeStudy, id: 's-9', topic: { ...activeStudy.topic, key: 'rest', title: rest.title } })
    const user = userEvent.setup()
    renderHub()

    await user.click(await screen.findByRole('button', { name: `Start: ${rest.title}` }))
    expect(api.startStudy).toHaveBeenCalledWith('rest')
    expect(await screen.findByText('Reader for study s-9')).toBeInTheDocument()
  })

  it('says so when a study cannot be started, and stays on the page', async () => {
    api.startStudy.mockRejectedValue({
      code: 'SERVER_ERROR',
      message: 'The study service is down.',
      suggestion: 'Try again in a minute.',
      status: 500,
    })
    const user = userEvent.setup()
    renderHub()

    await user.click(await screen.findByRole('button', { name: `Start: ${rest.title}` }))
    const alert = await screen.findByRole('alert')
    expect(within(alert).getByText(/The study service is down\./)).toBeInTheDocument()
    expect(within(alert).getByText('Try again in a minute.')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Find a study' })).toBeInTheDocument()
  })

  it('offers to continue studies in progress and keeps completed ones tucked away', async () => {
    const completed: Study = {
      ...activeStudy,
      id: 's-2',
      topic: { key: 'rest', title: rest.title, category: 'peace', sensitive: false },
      status: 'completed',
      current_lesson: 4,
      completed_lessons: [1, 2, 3, 4],
      progress_percent: 100,
      completed_at: '2026-10-01T12:00:00Z',
    }
    api.getStudies.mockResolvedValue([activeStudy, completed])
    api.getCatalog.mockResolvedValue({
      ...catalog,
      categories: [
        {
          ...catalog.categories[0],
          topics: [
            { ...anxiety, enrollment: { id: 's-1', status: 'active', current_lesson: 2, completed_lessons: [1] } },
            { ...rest, enrollment: { id: 's-2', status: 'completed', current_lesson: 4, completed_lessons: [1, 2, 3, 4] } },
          ],
        },
        catalog.categories[1],
      ],
    })
    api.startStudy.mockResolvedValue({ ...activeStudy, id: 's-3' })
    const user = userEvent.setup()
    renderHub()

    const section = (await screen.findByRole('heading', { name: 'Continue' })).closest('section')!
    expect(within(section).getByRole('heading', { name: activeStudy.topic.title })).toBeInTheDocument()
    expect(within(section).getByText('Lesson 2 of 4')).toBeInTheDocument()
    expect(within(section).getByRole('progressbar')).toHaveAttribute('aria-valuenow', '25')
    expect(within(section).getByRole('link', { name: `Continue: ${activeStudy.topic.title}` })).toHaveAttribute(
      'href',
      '/study/s-1'
    )

    // Catalog cards reflect enrolment.
    const find = screen.getByRole('heading', { name: 'Find a study' }).closest('section')!
    const inProgress = within(find).getByRole('heading', { name: anxiety.title }).closest('article')!
    expect(within(inProgress).getByText('In progress')).toBeInTheDocument()
    const done = within(find).getByRole('heading', { name: rest.title }).closest('article')!
    expect(within(done).getByText('Completed')).toBeInTheDocument()

    // Completed studies are collapsed by default.
    const summary = screen.getByText('Completed studies (1)')
    const details = summary.closest('details')!
    expect(details).not.toHaveAttribute('open')
    await user.click(summary)
    await user.click(within(details).getByRole('button', { name: `Study again: ${rest.title}` }))
    expect(api.startStudy).toHaveBeenCalledWith('rest')
    expect(await screen.findByText('Reader for study s-3')).toBeInTheDocument()
  })

  it('shows what went wrong, with a retry, when the catalog cannot be loaded', async () => {
    api.getCatalog
      .mockRejectedValueOnce({ code: 'SERVER_ERROR', message: 'Catalog exploded.', suggestion: 'Try again.', status: 500 })
      .mockResolvedValue(catalog)
    const user = userEvent.setup()
    renderHub()

    const alert = await screen.findByRole('alert')
    expect(within(alert).getByText("The studies couldn't be loaded")).toBeInTheDocument()
    expect(within(alert).getByText('Catalog exploded.')).toBeInTheDocument()
    await user.click(within(alert).getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('heading', { name: 'Find a study' })).toBeInTheDocument()
  })
})
