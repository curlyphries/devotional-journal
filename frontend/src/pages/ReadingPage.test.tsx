import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes, useParams } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import '../i18n'
import { ToastProvider } from '../components/Toast'
import ReadingPage from './ReadingPage'
import { advanceDay, getPlanDetail, getTodayReading } from '../api/plans'
import { getPassage } from '../api/bible'
import { createJournalEntry } from '../api/journal'

vi.mock('../api/plans', async (importOriginal) => ({
  ...(await importOriginal<typeof import('../api/plans')>()),
  getTodayReading: vi.fn(),
  getPlanDetail: vi.fn(),
  advanceDay: vi.fn(),
}))
vi.mock('../api/bible', async (importOriginal) => ({
  ...(await importOriginal<typeof import('../api/bible')>()),
  getPassage: vi.fn(),
}))
vi.mock('../api/journal', () => ({
  createJournalEntry: vi.fn(),
}))

const plan = {
  id: 'plan-1',
  title: 'Psalms Journey',
  description: '',
  duration_days: 30,
  category: 'general',
  is_premium: false,
  is_public: true,
  is_owned: false,
}
const enrollment = {
  id: 'enr-1',
  plan,
  started_at: '2026-11-01T00:00:00Z',
  current_day: 7,
  completed_at: null,
  is_active: true,
  progress_percentage: 23,
}

function JournalEntryStub() {
  const { entryId } = useParams()
  return <div>journal entry {entryId}</div>
}

function renderPage() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })
  return render(
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <MemoryRouter initialEntries={['/reading/enr-1']}>
          <Routes>
            <Route path="/reading/:enrollmentId" element={<ReadingPage />} />
            <Route path="/journal/:entryId" element={<JournalEntryStub />} />
            <Route path="/" element={<div>dashboard</div>} />
          </Routes>
        </MemoryRouter>
      </ToastProvider>
    </QueryClientProvider>,
  )
}

describe('ReadingPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(getTodayReading).mockResolvedValue({
      enrollment,
      day: { day_number: 7, passages: ['Psalm 23:1-6'], theme: 'The Lord is my shepherd' },
    })
    vi.mocked(getPlanDetail).mockResolvedValue({
      ...plan,
      days: [
        { id: 'day-6', day_number: 6, passages: ['Psalm 19'], theme: 'Glory' },
        { id: 'day-7', day_number: 7, passages: ['Psalm 23:1-6'], theme: 'The Lord is my shepherd' },
      ],
    })
    vi.mocked(getPassage).mockResolvedValue({
      source: 'bolls',
      translation: { code: 'KJV', name: 'King James Version', language: 'en' },
      book: 'Psalm',
      chapter: 23,
      verses: [],
      full_text: 'The LORD is my shepherd; I shall not want.',
    })
    vi.mocked(advanceDay).mockResolvedValue({ message: 'Advanced to day 8', enrollment })
    vi.mocked(createJournalEntry).mockResolvedValue({
      id: 'entry-9',
      date: '2026-11-12',
      mood_tag: 'grateful',
      created_at: '2026-11-12T10:00:00Z',
    })
  })

  it('shows the real plan, day, passage text and theme from the API', async () => {
    renderPage()

    expect(await screen.findByText('Day 7 of 30 · Psalms Journey')).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 1, name: 'The Lord is my shepherd' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 2, name: 'Psalm 23:1-6' })).toBeInTheDocument()
    expect(await screen.findByText('The LORD is my shepherd; I shall not want.')).toBeInTheDocument()

    expect(getTodayReading).toHaveBeenCalledWith('enr-1')
    expect(getPassage).toHaveBeenCalledWith('Psalm', 23, 'KJV', 1, 6)
  })

  it('saves what was written as a journal entry, completes the day and opens the entry', async () => {
    renderPage()
    const box = await screen.findByLabelText('Journal Entry')
    // Wait for the plan detail, which supplies the day id the entry links to.
    await waitFor(() => expect(getPlanDetail).toHaveBeenCalledWith('plan-1'))
    await screen.findByText('The LORD is my shepherd; I shall not want.')

    await userEvent.type(box, 'He restores my soul.')
    await userEvent.click(screen.getByRole('button', { name: /Grateful/ }))
    await userEvent.click(screen.getByRole('button', { name: 'Save entry and complete day' }))

    expect(await screen.findByText('journal entry entry-9')).toBeInTheDocument()
    expect(createJournalEntry).toHaveBeenCalledTimes(1)
    expect(createJournalEntry).toHaveBeenCalledWith({
      date: expect.stringMatching(/^\d{4}-\d{2}-\d{2}$/),
      content: 'He restores my soul.',
      mood_tag: 'grateful',
      plan_enrollment: 'enr-1',
      plan_day: 'day-7',
    })
    expect(advanceDay).toHaveBeenCalledWith('enr-1')
  })

  it('only marks the day complete when nothing was written', async () => {
    renderPage()

    await userEvent.click(await screen.findByRole('button', { name: 'Mark day complete' }))

    expect(await screen.findByText('dashboard')).toBeInTheDocument()
    expect(createJournalEntry).not.toHaveBeenCalled()
    expect(advanceDay).toHaveBeenCalledWith('enr-1')
  })

  it('keeps the entry when completing the day fails, and says so', async () => {
    vi.mocked(advanceDay).mockRejectedValue(new Error('advance failed'))
    renderPage()

    await userEvent.type(await screen.findByLabelText('Journal Entry'), 'Still here.')
    await userEvent.click(screen.getByRole('button', { name: 'Save entry and complete day' }))

    expect(await screen.findByText('journal entry entry-9')).toBeInTheDocument()
    expect(screen.getByRole('alert')).toHaveTextContent(
      'Your entry was saved, but the day could not be marked complete.',
    )
  })

  it('shows an error with a retry when the reading cannot be loaded', async () => {
    vi.mocked(getTodayReading).mockRejectedValue({
      code: 'NOT_FOUND',
      message: 'Enrollment not found',
      status: 404,
    })
    renderPage()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent("Today's reading couldn't be loaded")
    expect(alert).toHaveTextContent('Enrollment not found')
    expect(screen.getByRole('button', { name: 'Try again' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Browse reading plans' })).toHaveAttribute('href', '/plans')
  })

  it('says so when the day has no passages', async () => {
    vi.mocked(getTodayReading).mockResolvedValue({
      enrollment,
      day: { day_number: 7, passages: [], theme: '' },
    })
    renderPage()

    expect(await screen.findByText('This day has no passages assigned.')).toBeInTheDocument()
    expect(getPassage).not.toHaveBeenCalled()
  })
})
