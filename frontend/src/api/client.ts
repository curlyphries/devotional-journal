/// <reference types="vite/client" />
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

/** Default request timeout. Override per request: `client.post(url, body, { timeout: AI_TIMEOUT_MS })`. */
export const DEFAULT_TIMEOUT_MS = 30_000
/** Timeout for calls that wait on an AI model (local models can take over a minute). */
export const AI_TIMEOUT_MS = 120_000

const client = axios.create({
  baseURL: API_URL,
  timeout: DEFAULT_TIMEOUT_MS,
  headers: {
    'Content-Type': 'application/json',
  },
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function clearTokens(): void {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

function redirectToLogin(): void {
  const loginPath = (import.meta.env.BASE_URL || '/') + 'login'
  // Already on a public page: a redirect would only loop or lose what the user typed.
  if (/\/(login|welcome|auth\/[a-z]+)\/?$/.test(window.location.pathname)) return
  window.location.href = loginPath
}

// Single-flight refresh: concurrent 401s wait on the same refresh request.
let refreshPromise: Promise<string> | null = null

function refreshAccessToken(refreshToken: string): Promise<string> {
  if (!refreshPromise) {
    refreshPromise = axios
      .post(
        `${API_URL}/auth/refresh/`,
        { refresh_token: refreshToken },
        { timeout: DEFAULT_TIMEOUT_MS },
      )
      .then((response) => {
        const { access_token, refresh_token: newRefreshToken } = response.data
        localStorage.setItem('access_token', access_token)
        if (newRefreshToken) localStorage.setItem('refresh_token', newRefreshToken)
        return access_token as string
      })
      .finally(() => {
        refreshPromise = null
      })
  }
  return refreshPromise
}

type RetriableConfig = InternalAxiosRequestConfig & { _retry?: boolean }

client.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetriableConfig | undefined
    const url = originalRequest?.url ?? ''
    // A 401 from the sign-in endpoints means "bad credentials", not "session expired".
    const isAuthEndpoint = /\/auth\/(magic-link|dev-login|google|refresh)\//.test(url)

    if (error.response?.status === 401 && originalRequest && !originalRequest._retry && !isAuthEndpoint) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        clearTokens()
        redirectToLogin()
        return Promise.reject(error)
      }

      let accessToken: string
      try {
        accessToken = await refreshAccessToken(refreshToken)
      } catch {
        clearTokens()
        redirectToLogin()
        return Promise.reject(error)
      }
      originalRequest.headers.Authorization = `Bearer ${accessToken}`
      return client(originalRequest)
    }

    return Promise.reject(error)
  },
)

export { client as apiClient }
export default client
