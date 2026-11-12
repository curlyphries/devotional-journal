import client from './client'
import type { StudyGuide } from './devotional'
import type { Paginated } from './pagination'

export interface JournalEntry {
  id: string
  date: string
  mood_tag: string
  /** List only. Any metadata block is already stripped by the server. */
  content_preview?: string
  focus_themes?: string[]
  /** List only: whether feedback has been generated for this entry. */
  has_feedback?: boolean
  /** List only: the scripture given in this entry's feedback, if any. */
  scripture_reference?: string | null
  decrypted_content?: string
  plan_enrollment?: string
  plan_day?: string
  reflection_prompts_used?: string[]
  is_private?: boolean
  created_at: string
  updated_at?: string
}

export interface CreateJournalEntry {
  date: string
  content: string
  mood_tag?: string
  plan_enrollment?: string
  plan_day?: string
  is_private?: boolean
}

export interface JournalFilters {
  date_from?: string
  date_to?: string
  mood?: string
  page?: number
}

/** Accept both a bare array (older servers) and the paginated `{results}` shape. */
function toPage<T>(data: unknown): Paginated<T> {
  if (Array.isArray(data)) {
    return { count: data.length, next: null, previous: null, results: data as T[] }
  }
  const body = (typeof data === 'object' && data !== null ? data : {}) as Partial<Paginated<T>>
  const results = Array.isArray(body.results) ? body.results : []
  return {
    count: typeof body.count === 'number' ? body.count : results.length,
    next: body.next ?? null,
    previous: body.previous ?? null,
    results,
  }
}

/** One page (20 entries) of the journal, newest first. */
export const getJournalEntriesPage = async (filters?: JournalFilters): Promise<Paginated<JournalEntry>> => {
  const response = await client.get('/journal/', { params: filters })
  return toPage<JournalEntry>(response.data)
}

/** The entries of one page as a plain array (first page unless `page` is given). */
export const getJournalEntries = async (filters?: JournalFilters): Promise<JournalEntry[]> => {
  return (await getJournalEntriesPage(filters)).results
}

export const getJournalEntry = async (entryId: string): Promise<JournalEntry> => {
  const response = await client.get(`/journal/${entryId}/`)
  return response.data
}

export const createJournalEntry = async (data: CreateJournalEntry): Promise<JournalEntry> => {
  const response = await client.post('/journal/', data)
  return response.data
}

export const updateJournalEntry = async (entryId: string, data: Partial<CreateJournalEntry>): Promise<JournalEntry> => {
  const response = await client.patch(`/journal/${entryId}/`, data)
  return response.data
}

export const deleteJournalEntry = async (entryId: string): Promise<void> => {
  await client.delete(`/journal/${entryId}/`)
}

export const generateJournalDeepDive = async (entryId: string, context?: string): Promise<StudyGuide> => {
  const response = await client.post(`/journal/${entryId}/deep-dive/`, {
    context: context || '',
  })
  return response.data
}

// ---------------------------------------------------------------------------
// Feedback: the response to an entry, its scripture, and the decision record.
// ---------------------------------------------------------------------------

export interface FeedbackScripture {
  reference: string
  book: string
  chapter: number
  verse_start: number | null
  verse_end: number | null
  /** Fetched from the Bible source — never written by the AI. */
  text: string
  translation: string
  translation_name: string
  verified: boolean
  source: string
}

export type CandidateOutcome = 'selected' | 'not_found' | 'not_used' | 'invalid'

export interface FeedbackCandidate {
  reference: string
  reason: string
  outcome: CandidateOutcome | string
}

export interface FeedbackFallbackReason {
  code: string
  message: string
  suggestion?: string | null
}

export interface FeedbackAudit {
  provider: string
  model: string
  local: boolean
  prompt_version: string
  duration_ms: number
  inputs_used: string[]
  recent_themes: string[]
  candidates: FeedbackCandidate[]
  selection_rule: string
  fallback_reason: FeedbackFallbackReason | null
  threads_detected: { type: string; summary: string }[]
}

export interface JournalFeedback {
  id: string
  entry_id: string
  entry_date: string
  created_at: string
  /** "ok" = written by the AI; "fallback" = AI unavailable, passage picked by built-in rules. */
  status: 'ok' | 'fallback'
  is_spiritual: boolean
  themes: string[]
  reflection: string
  scripture: FeedbackScripture | null
  why_this_passage: string
  meditation_prompt: string
  christlike_step: string
  growth_note: string
  helpful: boolean | null
  audit: FeedbackAudit
}

export interface ThemeCount {
  theme: string
  count: number
  last_seen: string
}

export interface ThemesSummary {
  themes: ThemeCount[]
  entries_with_feedback: number
}

/** Local models can take up to ~90s; the default client timeout is far shorter. */
export const FEEDBACK_TIMEOUT_MS = 120_000

/** Existing feedback for an entry. Rejects with a 404 (code NOT_FOUND) when none exists yet. */
export const getJournalFeedback = async (entryId: string): Promise<JournalFeedback> => {
  const response = await client.get(`/journal/${entryId}/feedback/`)
  return response.data
}

/** Generate feedback (or return the existing one unless `regenerate`). */
export const generateJournalFeedback = async (
  entryId: string,
  options?: { regenerate?: boolean }
): Promise<JournalFeedback> => {
  const response = await client.post(
    `/journal/${entryId}/feedback/`,
    options?.regenerate ? { regenerate: true } : {},
    { timeout: FEEDBACK_TIMEOUT_MS }
  )
  return response.data
}

/** The audit log: every feedback decision, newest first. */
export const getFeedbackLog = async (page = 1): Promise<Paginated<JournalFeedback>> => {
  const response = await client.get('/journal/feedback/', { params: { page } })
  return toPage<JournalFeedback>(response.data)
}

export const rateJournalFeedback = async (
  feedbackId: string,
  helpful: boolean | null
): Promise<JournalFeedback> => {
  const response = await client.post(`/journal/feedback/${feedbackId}/rate/`, { helpful })
  return response.data
}

export const getJournalThemes = async (): Promise<ThemesSummary> => {
  const response = await client.get('/journal/themes/')
  const body = (response.data ?? {}) as Partial<ThemesSummary>
  return {
    themes: Array.isArray(body.themes) ? body.themes : [],
    entries_with_feedback: body.entries_with_feedback ?? 0,
  }
}
