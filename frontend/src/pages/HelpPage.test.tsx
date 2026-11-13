import { describe, it, expect, afterEach } from 'vitest'
import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router-dom'
import { renderWithApp } from '../test/renderWithApp'
import HelpPage from './HelpPage'
import OnboardingTour from '../components/OnboardingTour'

afterEach(() => {
  window.sessionStorage.clear()
})

function renderHelp() {
  return renderWithApp(
    <Routes>
      <Route path="/help" element={<HelpPage />} />
      <Route path="/" element={<OnboardingTour open={false} onClose={() => undefined} />} />
    </Routes>,
    { route: '/help' }
  )
}

describe('HelpPage', () => {
  it('has deep-linkable sections and explains every error code', () => {
    const { container } = renderHelp()
    for (const id of ['quick-start', 'where', 'feedback', 'study', 'voice', 'privacy', 'troubleshooting']) {
      expect(container.querySelector(`#${id}`)).not.toBeNull()
    }
    for (const code of [
      'AI_UNAVAILABLE', 'AI_TIMEOUT', 'AI_NOT_CONFIGURED', 'AI_CONSENT_REQUIRED', 'AI_BAD_RESPONSE',
      'AI_URL_NOT_ALLOWED', 'SCRIPTURE_UNAVAILABLE', 'VALIDATION_ERROR', 'NOT_AUTHENTICATED',
      'PERMISSION_DENIED', 'NOT_FOUND', 'RATE_LIMITED', 'SERVER_ERROR',
    ]) {
      expect(container.querySelector(`#code-${code}`)).not.toBeNull()
    }
    expect(screen.getByRole('link', { name: 'Open the Audit log' })).toHaveAttribute('href', '/audit')
    // No untranslated keys leak into the page.
    expect(container.textContent).not.toMatch(/help\.[a-zA-Z]+\./)
    expect(container.textContent).not.toMatch(/@/)
  })

  it('explains the study guide, the growth profile and growth plans, and links to each', () => {
    renderHelp()
    expect(
      screen.getByRole('heading', { name: 'Bible study guide, your profile and growth plans' })
    ).toBeInTheDocument()
    expect(screen.getByText(/the reasons are always shown/i)).toBeInTheDocument()
    expect(screen.getByText(/not a diagnosis/i)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Open the Bible study guide' })).toHaveAttribute('href', '/study')
    expect(screen.getByRole('link', { name: 'Open my profile' })).toHaveAttribute('href', '/profile')
    expect(screen.getByRole('link', { name: 'Open growth plans' })).toHaveAttribute('href', '/growth')
    // "Where things are" lists the three new destinations.
    expect(screen.getByRole('link', { name: /^Bible study guide/ })).toHaveAttribute('href', '/study')
    expect(screen.getByRole('link', { name: /^My profile/ })).toHaveAttribute('href', '/profile')
    expect(screen.getByRole('link', { name: /^Growth plans/ })).toHaveAttribute('href', '/growth')
  })

  it('"Replay the tour" goes home and starts the tour', async () => {
    const user = userEvent.setup()
    renderHelp()
    await user.click(screen.getByRole('button', { name: 'Replay the tour' }))
    expect(await screen.findByRole('dialog', { name: 'Welcome to your Devotional Journal' })).toBeInTheDocument()
  })
})
