import { createContext, useCallback, useContext, useState, useEffect, ReactNode } from 'react'
import { User, getProfile, logout as apiLogout } from '../api/auth'
import { clearTokens } from '../api/client'
import { toApiError } from '../api/errors'
import { applyProfileLanguage } from '../i18n/language'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (accessToken: string, refreshToken: string) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Stable identities: pages list these in effect deps, and a changing `login`
  // would re-run the OAuth code exchange with an already-used code.
  const refreshUser = useCallback(async () => {
    try {
      const userData = await getProfile()
      setUser(userData)
      applyProfileLanguage(userData.language_preference)
    } catch (err) {
      setUser(null)
      // Keep the session when the server was merely unreachable; a reload restores it.
      const status = toApiError(err).status
      if (status === 401 || status === 403) clearTokens()
    }
  }, [])

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      refreshUser().finally(() => setIsLoading(false))
    } else {
      setIsLoading(false)
    }
  }, [refreshUser])

  const login = useCallback(async (accessToken: string, refreshToken: string) => {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
    // Awaited so callers can navigate to a private route as soon as this resolves.
    await refreshUser()
  }, [refreshUser])

  const logout = useCallback(async () => {
    try {
      await apiLogout()
    } catch {
      // The server could not be told; local sign-out still happens below.
    } finally {
      clearTokens()
      setUser(null)
    }
  }, [])

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
