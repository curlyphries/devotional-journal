import client, { AI_TIMEOUT_MS } from './client'
import { unwrapList } from './pagination'

/** An AI-written review of one week or month of journaling. */
export interface GrowthReview {
  id: string
  period_type: 'week' | 'month'
  period_start: string
  period_end: string
  content: string
  /** Which AI wrote it, e.g. provider "ollama", model "llama3.1:8b". */
  provider: string
  model: string
  created_at: string
}

/** Most recent reviews first (first page). */
export const getGrowthReviews = async (): Promise<GrowthReview[]> => {
  const response = await client.get('/reviews/')
  return unwrapList<GrowthReview>(response.data)
}

export const generateGrowthReview = async (periodType: 'week' | 'month' = 'week'): Promise<GrowthReview> => {
  const response = await client.post('/reviews/generate/', { period_type: periodType }, { timeout: AI_TIMEOUT_MS })
  return response.data
}
