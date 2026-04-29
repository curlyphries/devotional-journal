import client from './client'
import type { StudyGuide } from './devotional'

export interface JournalEntry {
  id: string
  date: string
  mood_tag: string
  content_preview?: string
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

export const getJournalEntries = async (filters?: {
  date_from?: string
  date_to?: string
  mood?: string
}): Promise<JournalEntry[]> => {
  const response = await client.get('/journal/', { params: filters })
  return response.data
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
