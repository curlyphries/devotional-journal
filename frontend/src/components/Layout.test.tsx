import type { ReactNode } from 'react'
import { describe, it, expect, vi } from 'vitest'
import { screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
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
    t: (key: string, fallback?: string) => fallback ?? key,
    i18n: {
      language: 'en',
      changeLanguage: vi.fn(),
    },
  }),
}))

describe('Layout', () => {
  it('renders the app name', () => {
    render(<Layout />)
    expect(screen.getByText('Devotional Journal')).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<Layout />)
    expect(screen.getByRole('link', { name: 'nav.dashboard' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'nav.journal' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'nav.study' })).toHaveAttribute('href', '/study')
    expect(screen.getByRole('link', { name: 'nav.settings' })).toBeInTheDocument()
  })

  it('keeps the tour targets in the bar on every screen size', () => {
    const { container } = render(<Layout />)
    for (const id of ['language', 'help', 'fab']) {
      expect(container.querySelectorAll(`[data-tour-id="${id}"]`)).toHaveLength(1)
    }
  })

  it('gives Study, My profile and Growth plans their tour ids, on desktop and in the phone menu', async () => {
    const { container } = render(<Layout />)
    expect(container.querySelectorAll('[data-tour-id="nav-study"]')).toHaveLength(1)

    await userEvent.click(screen.getByRole('button', { name: 'nav.more' }))
    expect(container.querySelector('#nav-more-menu [data-tour-id="nav-profile"]')).toHaveAttribute('href', '/profile')
    expect(container.querySelector('#nav-more-menu [data-tour-id="nav-growth"]')).toHaveAttribute('href', '/growth')
    await userEvent.keyboard('{Escape}')

    await userEvent.click(screen.getByRole('button', { name: 'nav.openMenu' }))
    for (const id of ['nav-study', 'nav-profile', 'nav-growth']) {
      expect(container.querySelector(`#nav-mobile-menu [data-tour-id="${id}"]`)).not.toBeNull()
    }
  })

  it('opens the "More" menu with the secondary pages and closes it on Escape', async () => {
    render(<Layout />)
    const more = screen.getByRole('button', { name: 'nav.more' })
    expect(more).toHaveAttribute('aria-expanded', 'false')

    await userEvent.click(more)
    expect(more).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('link', { name: 'nav.reflection' })).toHaveAttribute('href', '/reflection')
    expect(screen.getByRole('link', { name: 'nav.threads' })).toHaveAttribute('href', '/threads')
    expect(screen.getByRole('link', { name: 'nav.profile' })).toHaveAttribute('href', '/profile')
    expect(screen.getByRole('link', { name: 'nav.growth' })).toHaveAttribute('href', '/growth')
    expect(screen.getByRole('link', { name: 'nav.readingPlans' })).toHaveAttribute('href', '/plans')

    await userEvent.keyboard('{Escape}')
    expect(more).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByRole('link', { name: 'nav.threads' })).not.toBeInTheDocument()
    expect(more).toHaveFocus()
  })

  it('has a phone menu button that lists every page and sign-out', async () => {
    render(<Layout />)
    const toggle = screen.getByRole('button', { name: 'nav.openMenu' })
    expect(toggle).toHaveAttribute('aria-expanded', 'false')

    await userEvent.click(toggle)

    expect(screen.getByRole('button', { name: 'nav.closeMenu' })).toHaveAttribute('aria-expanded', 'true')
    const menu = document.getElementById('nav-mobile-menu')!
    const labels = within(menu).getAllByRole('link').map((link) => link.textContent)
    expect(labels).toEqual([
      'nav.dashboard', 'nav.journal', 'nav.study', 'nav.focus', 'nav.progress',
      'nav.profile', 'nav.growth', 'nav.readingPlans',
      'nav.reflection', 'nav.threads', 'nav.insights', 'audit.navLabel', 'nav.settings',
    ])
    expect(within(menu).getByRole('button', { name: 'auth.logout' })).toBeInTheDocument()

    await userEvent.keyboard('{Escape}')
    expect(document.getElementById('nav-mobile-menu')).toBeNull()
  })
})
