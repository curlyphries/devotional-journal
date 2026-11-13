import client, { clearTokens } from './client'

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
  /** Lets the server's default cloud AI read journal text when the user has no provider of their own. */
  allow_server_cloud_ai?: boolean
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

/**
 * How this server gets a sign-in link to a person:
 *  - "email": a mail server is configured;
 *  - "log": no mail server — the link is written to the server log for the administrator;
 *  - "unavailable": neither, so email sign-in cannot work here.
 */
export type SigninDelivery = 'email' | 'log' | 'unavailable'

export interface AuthMethods {
  email: { delivery: SigninDelivery }
  /** Google sign-in is configured on this server. */
  google: boolean
  /** Asking for a link with a new address creates an account. */
  signup: boolean
}

/** Which ways of signing in this server offers. */
export const getAuthMethods = async (): Promise<AuthMethods> => {
  const response = await client.get('/auth/methods/')
  return response.data
}

/** Ask for a sign-in link. Resolves to how the link is being delivered. */
export const requestMagicLink = async (email: string): Promise<SigninDelivery> => {
  const response = await client.post('/auth/magic-link/request/', { email })
  return response.data?.delivery ?? 'email'
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
  const refreshToken = localStorage.getItem('refresh_token')
  try {
    // Best effort: the server-side token is revoked when reachable.
    if (refreshToken) await client.post('/auth/logout/', { refresh_token: refreshToken })
  } finally {
    // Signing out must always work locally, even offline or with an expired session.
    clearTokens()
  }
}
