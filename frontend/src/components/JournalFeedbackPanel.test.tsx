import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AxiosError, type AxiosResponse } from 'axios'
import { renderWithApp } from '../test/renderWithApp'
import JournalFeedbackPanel from './JournalFeedbackPanel'
import * as journalApi from '../api/journal'
import type { JournalFeedback } from '../api/journal'

vi.mock('../api/journal', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/journal')>()
  return {
    ...actual,
    getJournalFeedback: vi.fn(),
    generateJournalFeedback: vi.fn(),
    rateJournalFeedback: vi.fn(),
  }
})

const api = vi.mocked(journalApi)

function notFound(): AxiosError {
  const response = {
    status: 404,
    statusText: 'Not Found',
    headers: {},
    config: {},
    data: { error: 'No feedback yet.', code: 'NOT_FOUND', request_id: 'abc12345' },
  } as unknown as AxiosResponse
  return new AxiosError('Request failed with status code 404', 'ERR_BAD_REQUEST', undefined, undefined, response)
}

const okFeedback: JournalFeedback = {
  id: 'fb-1',
  entry_id: 'entry-1',
  entry_date: '2026-11-12',
  created_at: '2026-11-12T15:04:05Z',
  status: 'ok',
  is_spiritual: false,
  themes: ['work stress', 'patience'],
  reflection: 'It sounds like work has been heavy this week.',
  scripture: {
    reference: 'Philippians 4:6-7',
    book: 'Philippians',
    chapter: 4,
    verse_start: 6,
    verse_end: 7,
    text: 'In nothing be anxious, but in everything, by prayer and petition with thanksgiving…',
    translation: 'WEB',
    translation_name: 'World English Bible',
    verified: true,
    source: 'bolls',
  },
  why_this_passage: 'You wrote about worry over deadlines; Paul speaks to anxiety directly.',
  meditation_prompt: 'What would it look like to hand this deadline to God?',
  christlike_step: 'Pray for your manager by name before the meeting.',
  growth_note: 'This echoes what you wrote last week about rest.',
  helpful: null,
  audit: {
    provider: 'ollama',
    model: 'llama3.1:8b',
    local: true,
    prompt_version: 'journal-feedback-v1',
    duration_ms: 8421,
    inputs_used: ['entry_text', 'mood', 'recent_themes'],
    recent_themes: ['anxiety', 'work'],
    candidates: [
      { reference: 'Philippians 4:6-7', reason: 'Speaks to anxiety.', outcome: 'selected' },
      { reference: 'Hezekiah 3:1', reason: 'Suggested by the model.', outcome: 'not_found' },
    ],
    selection_rule: 'First suggested passage whose text could be retrieved from the Bible source.',
    fallback_reason: null,
    threads_detected: [{ type: 'struggle', summary: 'Pressure at work' }],
  },
}

const fallbackFeedback: JournalFeedback = {
  ...okFeedback,
  id: 'fb-2',
  status: 'fallback',
  growth_note: '',
  audit: {
    ...okFeedback.audit,
    provider: 'none',
    model: '',
    local: true,
    candidates: [{ reference: 'Philippians 4:6-7', reason: 'Keyword: anxious', outcome: 'selected' }],
    fallback_reason: {
      code: 'AI_UNAVAILABLE',
      message: 'Could not reach Ollama at http://localhost:11434.',
      suggestion: 'Make sure Ollama is running.',
    },
  },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe('JournalFeedbackPanel', () => {
  it('renders AI feedback with the verified badge and the decision record', async () => {
    api.getJournalFeedback.mockResolvedValue(okFeedback)
    renderWithApp(<JournalFeedbackPanel entryId="entry-1" />)

    expect(await screen.findByText(okFeedback.reflection)).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Philippians 4:6-7' })).toBeInTheDocument()
    expect(screen.getByText(/In nothing be anxious/)).toBeInTheDocument()
    expect(screen.getByText('Verified against World English Bible')).toBeInTheDocument()
    expect(screen.getByText('work stress')).toBeInTheDocument()

    expect(screen.getByRole('heading', { name: 'Why this passage' })).toBeInTheDocument()
    expect(screen.getByText(okFeedback.meditation_prompt)).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'A step toward Christlikeness' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'How this connects to your journey' })).toBeInTheDocument()
    // The entry was not about faith: a gentle note says that is fine.
    expect(screen.getByText(/Everyday entries are welcome/)).toBeInTheDocument()

    expect(screen.getByRole('link', { name: /Open in Bible/ })).toHaveAttribute(
      'href',
      '/bible?passage=Philippians%204%3A6-7'
    )

    // Decision record: where it ran, inputs, every candidate and its outcome.
    expect(screen.getByText('Why this scripture? — decision record')).toBeInTheDocument()
    expect(screen.getByText('ollama · llama3.1:8b')).toBeInTheDocument()
    expect(screen.getByText('on your network')).toBeInTheDocument()
    expect(screen.getByText('The text of your entry')).toBeInTheDocument()
    const rejected = screen.getByText('Hezekiah 3:1').closest('li')!
    expect(within(rejected).getByText('Not found in the Bible')).toBeInTheDocument()
    expect(screen.getByText('Selected')).toBeInTheDocument()
    expect(screen.getByText('8.4 s')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'See all decisions' })).toHaveAttribute('href', '/audit')

    expect(screen.queryByText(/chosen by built-in rules/)).not.toBeInTheDocument()
    expect(api.generateJournalFeedback).not.toHaveBeenCalled()
  })

  it('renders the fallback banner and retries with the AI', async () => {
    api.getJournalFeedback.mockResolvedValue(fallbackFeedback)
    api.generateJournalFeedback.mockResolvedValue(okFeedback)
    const user = userEvent.setup()
    renderWithApp(<JournalFeedbackPanel entryId="entry-1" />)

    expect(await screen.findByText(/chosen by built-in rules/)).toBeInTheDocument()
    expect(screen.getAllByText(/Could not reach Ollama/).length).toBeGreaterThan(0)
    expect(screen.getByText('Make sure Ollama is running.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Check AI settings' })).toHaveAttribute('href', '/settings')
    expect(screen.queryByRole('heading', { name: 'How this connects to your journey' })).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Try again with AI' }))
    expect(api.generateJournalFeedback).toHaveBeenCalledWith('entry-1', { regenerate: true })
    await waitFor(() => expect(screen.queryByText(/chosen by built-in rules/)).not.toBeInTheDocument())
  })

  it('generates feedback when none exists and autoGenerate is set', async () => {
    api.getJournalFeedback.mockRejectedValue(notFound())
    let finish: (feedback: JournalFeedback) => void = () => undefined
    api.generateJournalFeedback.mockReturnValue(
      new Promise<JournalFeedback>((resolve) => {
        finish = resolve
      })
    )
    renderWithApp(<JournalFeedbackPanel entryId="entry-1" autoGenerate />)

    // Calm progress state while the model works.
    expect(await screen.findByText('Reading your entry…')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveAttribute('aria-live', 'polite')
    expect(api.generateJournalFeedback).toHaveBeenCalledTimes(1)
    expect(api.generateJournalFeedback).toHaveBeenCalledWith('entry-1', { regenerate: false })

    finish(okFeedback)
    expect(await screen.findByText(okFeedback.reflection)).toBeInTheDocument()
    expect(api.generateJournalFeedback).toHaveBeenCalledTimes(1)
  })

  it('waits for the user to ask when autoGenerate is off', async () => {
    api.getJournalFeedback.mockRejectedValue(notFound())
    api.generateJournalFeedback.mockResolvedValue(okFeedback)
    const user = userEvent.setup()
    renderWithApp(<JournalFeedbackPanel entryId="entry-1" />)

    const button = await screen.findByRole('button', { name: 'Get feedback' })
    expect(api.generateJournalFeedback).not.toHaveBeenCalled()
    await user.click(button)
    expect(await screen.findByText(okFeedback.reflection)).toBeInTheDocument()
  })

  it('shows the error with its code when generation fails, and can retry', async () => {
    api.getJournalFeedback.mockRejectedValue(notFound())
    const failure = {
      code: 'VALIDATION_ERROR',
      message: 'This entry is empty.',
      suggestion: 'Write something first.',
      requestId: 'req-777',
      status: 400,
    }
    api.generateJournalFeedback.mockRejectedValueOnce(failure).mockResolvedValueOnce(okFeedback)
    const user = userEvent.setup()
    renderWithApp(<JournalFeedbackPanel entryId="entry-1" autoGenerate />)

    const alert = await screen.findByRole('alert')
    expect(within(alert).getByText('This entry is empty.')).toBeInTheDocument()
    expect(within(alert).getByText('Write something first.')).toBeInTheDocument()
    expect(within(alert).getByText(/VALIDATION_ERROR/)).toBeInTheDocument()
    expect(within(alert).getByText(/req-777/)).toBeInTheDocument()

    await user.click(within(alert).getByRole('button'))
    expect(await screen.findByText(okFeedback.reflection)).toBeInTheDocument()
  })

  it('saves a helpful rating and reflects it', async () => {
    api.getJournalFeedback.mockResolvedValue(okFeedback)
    api.rateJournalFeedback.mockResolvedValue({ ...okFeedback, helpful: true })
    const user = userEvent.setup()
    renderWithApp(<JournalFeedbackPanel entryId="entry-1" />)

    const yes = await screen.findByRole('button', { name: 'Yes' })
    expect(yes).toHaveAttribute('aria-pressed', 'false')
    await user.click(yes)
    expect(api.rateJournalFeedback).toHaveBeenCalledWith('fb-1', true)
    await waitFor(() => expect(screen.getByRole('button', { name: 'Yes' })).toHaveAttribute('aria-pressed', 'true'))
  })

  it('asks before replacing feedback on Regenerate', async () => {
    api.getJournalFeedback.mockResolvedValue(okFeedback)
    api.generateJournalFeedback.mockResolvedValue({ ...okFeedback, reflection: 'A fresh reflection.' })
    const user = userEvent.setup()
    renderWithApp(<JournalFeedbackPanel entryId="entry-1" />)

    await user.click(await screen.findByRole('button', { name: 'Regenerate' }))
    expect(api.generateJournalFeedback).not.toHaveBeenCalled()
    expect(screen.getByText('Replace the current feedback with a new one?')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Replace' }))
    expect(api.generateJournalFeedback).toHaveBeenCalledWith('entry-1', { regenerate: true })
    expect(await screen.findByText('A fresh reflection.')).toBeInTheDocument()
  })
})
