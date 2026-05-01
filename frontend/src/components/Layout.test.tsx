import type { ReactNode } from 'react'
import { describe, it, expect, vi } from 'vitest'
import { screen } from '@testing-library/react'
import { render } from '../test/utils'
import Layout from './Layout'

vi.mock('../context/AuthContext', () => ({
  AuthProvider: ({ children }: { children: ReactNode }) => children,
  useAuth: () => ({
    user: { display_name: 'Test User', email: 'test@example.com' },
    logout: vi.fn(),
  }),
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
  }),
}))

describe('Layout', () => {
  it('renders the app name', () => {
    render(<Layout />)
    expect(screen.getByText('Devotional Journal')).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<Layout />)
    expect(screen.getByText('nav.dashboard')).toBeInTheDocument()
    expect(screen.getByText('nav.journal')).toBeInTheDocument()
    expect(screen.getByText('nav.settings')).toBeInTheDocument()
  })
})
