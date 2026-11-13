import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router-dom'
import { renderWithApp } from '../../test/renderWithApp'
import StudyDashboardCard from './StudyDashboardCard'
import * as guidesApi from '../../api/guides'
import type { Study, TopicCard } from '../../api/guides'

vi.mock('../../api/guides', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../api/guides')>()
  return { ...actual, getStudies: vi.fn(), getRecommendations: vi.fn(), startStudy: vi.fn() }
})

const api = vi.mocked(guidesApi)

const active: Study = {
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

const rest: TopicCard = {
  key: 'rest',
  category: 'peace',
  title: 'Rest for the weary',
  summary: 'Sabbath, sleep and the God who never slumbers.',
  lesson_count: 3,
  stages: ['adult'],
  traits: [],
  sensitive: false,
  stage_note: null,
  enrollment: null,
}

function renderCard() {
  return renderWithApp(
    <Routes>
      <Route path="/" element={<StudyDashboardCard />} />
      <Route path="/study/:studyId" element={<p>Reader</p>} />
    </Routes>
  )
}

beforeEach(() => {
  vi.clearAllMocks()
  api.getStudies.mockResolvedValue([])
  api.getRecommendations.mockResolvedValue({ based_on: { entries_considered: 0, has_profile: false }, results: [] })
})

describe('StudyDashboardCard', () => {
  it('offers to continue the study in progress', async () => {
    api.getStudies.mockResolvedValue([active])
    renderCard()

    expect(await screen.findByText('Continue: When worry will not stop')).toBeInTheDocument()
    expect(screen.getByText('Lesson 2 of 4')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue' })).toHaveAttribute('href', '/study/s-1')
    // Nothing else is needed when there is a study to continue.
    expect(api.getRecommendations).not.toHaveBeenCalled()
  })

  it('otherwise offers the top suggestion with its first reason, and starts it', async () => {
    api.getRecommendations.mockResolvedValue({
      based_on: { entries_considered: 4, has_profile: true },
      results: [{ topic: rest, score: 8, reasons: ['Your recent entries mention “tired” 4 times.', 'Second reason.'] }],
    })
    api.startStudy.mockResolvedValue({ ...active, id: 's-5' })
    const user = userEvent.setup()
    renderCard()

    expect(await screen.findByText('Suggested for you: Rest for the weary')).toBeInTheDocument()
    expect(screen.getByText(/Your recent entries mention “tired” 4 times\./)).toBeInTheDocument()
    expect(screen.queryByText(/Second reason/)).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Start: Rest for the weary' }))
    expect(api.startStudy).toHaveBeenCalledWith('rest')
    expect(await screen.findByText('Reader')).toBeInTheDocument()
  })

  it('falls back to "Find a study" when there is nothing to suggest', async () => {
    renderCard()
    expect(await screen.findByText('Find a study')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Browse studies' })).toHaveAttribute('href', '/study')
  })

  it('still shows the plain link, and no error, when the study service fails', async () => {
    api.getStudies.mockRejectedValue({ code: 'SERVER_ERROR', message: 'Down.', status: 500 })
    api.getRecommendations.mockRejectedValue({ code: 'SERVER_ERROR', message: 'Down.', status: 500 })
    renderCard()

    expect(await screen.findByText('Find a study')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Browse studies' })).toHaveAttribute('href', '/study')
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })
})
