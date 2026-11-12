import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen } from '@testing-library/react'
import { renderWithApp } from '../test/renderWithApp'
import AuditLogPage from './AuditLogPage'
import * as journalApi from '../api/journal'
import type { JournalFeedback } from '../api/journal'

vi.mock('../api/journal', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/journal')>()
  return { ...actual, getFeedbackLog: vi.fn(), getJournalThemes: vi.fn() }
})

const api = vi.mocked(journalApi)

const item: JournalFeedback = {
  id: 'fb-1',
  entry_id: 'entry-1',
  entry_date: '2026-11-12',
  created_at: '2026-11-12T15:04:05Z',
  status: 'fallback',
  is_spiritual: true,
  themes: ['anxiety'],
  reflection: '',
  scripture: {
    reference: 'Psalm 23:1', book: 'Psalms', chapter: 23, verse_start: 1, verse_end: 1,
    text: 'Yahweh is my shepherd', translation: 'WEB', translation_name: 'World English Bible',
    verified: true, source: 'local',
  },
  why_this_passage: '',
  meditation_prompt: '',
  christlike_step: '',
  growth_note: '',
  helpful: null,
  audit: {
    provider: 'none', model: '', local: true, prompt_version: 'journal-feedback-v1', duration_ms: 12,
    inputs_used: ['entry_text'], recent_themes: [], candidates: [], selection_rule: 'Keyword match.',
    fallback_reason: { code: 'AI_UNAVAILABLE', message: 'Ollama is not running.' }, threads_detected: [],
  },
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe('AuditLogPage', () => {
  it('lists decisions with status, where it ran, and themes over time', async () => {
    api.getFeedbackLog.mockResolvedValue({ count: 1, next: null, previous: null, results: [item] })
    api.getJournalThemes.mockResolvedValue({
      themes: [{ theme: 'anxiety', count: 4, last_seen: '2026-11-10' }],
      entries_with_feedback: 12,
    })
    renderWithApp(<AuditLogPage />)

    expect(screen.getByRole('heading', { name: 'Why you received each scripture' })).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Psalm 23:1' })).toBeInTheDocument()
    expect(screen.getByText('Built-in rules')).toBeInTheDocument()
    expect(screen.getByText('Ollama is not running.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'View the entry' })).toHaveAttribute('href', '/journal/entry-1')
    expect(await screen.findByText(/across 12 entries with feedback/)).toBeInTheDocument()
    expect(screen.getByText('4')).toBeInTheDocument()
  })

  it('shows an empty state with a link to write an entry', async () => {
    api.getFeedbackLog.mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
    api.getJournalThemes.mockResolvedValue({ themes: [], entries_with_feedback: 0 })
    renderWithApp(<AuditLogPage />)

    expect(await screen.findByText('Nothing recorded yet')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Write an entry' })).toHaveAttribute('href', '/journal/new')
  })
})
