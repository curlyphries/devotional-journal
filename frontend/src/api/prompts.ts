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

/** Where AI features run right now, and whether they can run at all. */
export interface AiStatus {
  backend: string
  model: string | null
  reachable: boolean
  configured: boolean
  /** Whose settings are in effect: the user's own provider or the server default. */
  source?: 'user' | 'server'
  /** True when the model runs on the server/your network rather than a cloud service. */
  local?: boolean
  /** The server default is a cloud AI and the user has not allowed it yet. */
  consent_required?: boolean
  code?: string | null
  suggestion?: string | null
}

export async function getAiStatus(): Promise<AiStatus> {
  const response = await apiClient.get('/prompts/ai-status/')
  return response.data
}
