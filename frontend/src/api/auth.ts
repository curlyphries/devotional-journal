import client from './client'

export interface User {
  id: string
  email: string
  display_name: string
  language_preference: 'en' | 'es' | 'bilingual'
  timezone: string
  ai_provider?: string
  ai_api_key_set?: boolean
  ai_model?: string
  ai_base_url?: string
  created_at: string
  last_active_at: string | null
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  expires_in: number
}

export interface AITestResult {
  success: boolean
  message?: string
  error?: string
  status_code?: number
}

export const requestMagicLink = async (email: string): Promise<void> => {
  await client.post('/auth/magic-link/request/', { email })
}

export const devLogin = async (email?: string): Promise<AuthTokens> => {
  const response = await client.post('/auth/dev-login/', { email })
  return response.data
}

export const verifyMagicLink = async (token: string): Promise<AuthTokens> => {
  const response = await client.post('/auth/magic-link/verify/', { token })
  return response.data
}

export const getProfile = async (): Promise<User> => {
  const response = await client.get('/me/')
  return response.data
}

export const updateProfile = async (data: Partial<User> & { ai_api_key?: string }): Promise<User> => {
  const response = await client.patch('/me/', data)
  return response.data
}

export const testAIConnection = async (data: {
  provider: string
  api_key?: string
  model?: string
  base_url?: string
}): Promise<AITestResult> => {
  const response = await client.post('/auth/test-ai/', data)
  return response.data
}

export const logout = async (): Promise<void> => {
  await client.post('/auth/logout/')
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}
