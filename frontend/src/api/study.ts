import client from './client'
import type { StudyGuide } from './devotional'

export type StudySessionStatus = 'active' | 'completed' | 'archived'

export interface StudyGuideSession {
  id: string
  source_type: 'devotional_passage' | 'journal_entry'
  source_reference: string
  source_passage: string | null
  source_journal_entry: string | null
  source_passage_reference: string
  source_journal_date: string
  guide_data: StudyGuide
  completed_days: number[]
  day_notes: Record<string, string>
  status: StudySessionStatus
  started_at: string
  last_activity_at: string
  completed_at: string | null
  total_days: number
  next_day: number | null
  progress_percentage: number
}

export interface StudySessionSummary {
  total_sessions: number
  active_sessions: number
  completed_sessions: number
  archived_sessions: number
  average_progress_percentage: number
}

export const getStudySessions = async (status?: StudySessionStatus): Promise<StudyGuideSession[]> => {
  const params = status ? { status } : {}
  const response = await client.get('/study-sessions/', { params })
  return response.data
}

export const getStudySessionSummary = async (): Promise<StudySessionSummary> => {
  const response = await client.get('/study-sessions/summary/')
  return response.data
}

export const markStudySessionDay = async (
  sessionId: string,
  payload: { day: number; completed?: boolean; note?: string }
): Promise<StudyGuideSession> => {
  const response = await client.post(`/study-sessions/${sessionId}/mark_day/`, payload)
  return response.data
}

export const archiveStudySession = async (sessionId: string): Promise<StudyGuideSession> => {
  const response = await client.post(`/study-sessions/${sessionId}/archive/`)
  return response.data
}

export const resumeStudySession = async (sessionId: string): Promise<StudyGuideSession> => {
  const response = await client.post(`/study-sessions/${sessionId}/resume/`)
  return response.data
}
