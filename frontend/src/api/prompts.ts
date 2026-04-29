/**
 * LLM Prompts API
 */
import { apiClient } from './client'

export interface GeneratePromptsRequest {
  passage: string
  reference: string
  language: 'en' | 'es' | 'bilingual'
  context?: string
}

export interface GeneratePromptsResponse {
  prompts: string[]
}

export async function generatePrompts(
  data: GeneratePromptsRequest
): Promise<GeneratePromptsResponse> {
  const response = await apiClient.post('/prompts/generate/', data)
  return response.data
}
