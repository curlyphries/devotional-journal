import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AxiosError, type AxiosResponse } from 'axios'
import { renderWithApp } from '../test/renderWithApp'
import LoginPage from './LoginPage'
import * as authApi from '../api/auth'
import type { AuthMethods } from '../api/auth'

vi.mock('../api/auth', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/auth')>()
  return { ...actual, getAuthMethods: vi.fn(), requestMagicLink: vi.fn(), devLogin: vi.fn() }
})
vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({ isAuthenticated: false, login: vi.fn() }),
}))

const api = vi.mocked(authApi)

const methods = (overrides: Partial<AuthMethods> = {}): AuthMethods => ({
  email: { delivery: 'email' },
  google: true,
  signup: false,
  ...overrides,
})

async function askForLink(user: ReturnType<typeof userEvent.setup>, address = 'me@example.org') {
  const open = screen.queryByRole('button', { name: 'Continue with email' })
  if (open) await user.click(open)
  await user.type(await screen.findByLabelText('Email'), address)
  await user.click(screen.getByRole('button', { name: /send/i }))
}

beforeEach(() => {
  vi.clearAllMocks()
  api.getAuthMethods.mockResolvedValue(methods())
  api.requestMagicLink.mockResolvedValue('email')
})

describe('LoginPage', () => {
  it('with a mail server: says the link was emailed and what to do if it does not arrive', async () => {
    const user = userEvent.setup()
    renderWithApp(<LoginPage />)

    await askForLink(user)

    expect(api.requestMagicLink).toHaveBeenCalledWith('me@example.org')
    expect(await screen.findByRole('heading', { name: 'Check your email' })).toBeInTheDocument()
    expect(screen.getByText(/If me@example.org has an account here/)).toBeInTheDocument()
    expect(screen.getByText(/spam or junk folder/)).toBeInTheDocument()
    // Accounts are not created by asking: say so, so nobody waits for a mail that will never come.
    expect(screen.getByText(/may be no account for that address yet/)).toBeInTheDocument()
  })

  it('without a mail server: does not say "check your email"', async () => {
    api.getAuthMethods.mockResolvedValue(methods({ email: { delivery: 'log' }, google: false }))
    api.requestMagicLink.mockResolvedValue('log')
    const user = userEvent.setup()
    renderWithApp(<LoginPage />)

    // Email is the only way in, so its form is already open and the page says how it works here.
    expect(await screen.findByText(/This server does not send email/)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Continue with Google' })).not.toBeInTheDocument()

    await askForLink(user)

    expect(await screen.findByRole('heading', { name: 'Ask your administrator for the link' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Check your email' })).not.toBeInTheDocument()
    expect(screen.getByText('python manage.py signin_link me@example.org')).toBeInTheDocument()
  })

  it('shows Google only when the server has it configured', async () => {
    renderWithApp(<LoginPage />)
    expect(await screen.findByRole('button', { name: 'Continue with Google' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Continue with email' })).toBeInTheDocument()
  })

  it('keeps both options when the server cannot say what it offers', async () => {
    api.getAuthMethods.mockRejectedValue(new Error('offline'))
    renderWithApp(<LoginPage />)
    await waitFor(() => expect(api.getAuthMethods).toHaveBeenCalled())
    expect(screen.getByRole('button', { name: 'Continue with Google' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Continue with email' })).toBeInTheDocument()
  })

  it('shows the real reason and the remedy when a link cannot be sent', async () => {
    const response = {
      status: 503,
      statusText: 'Service Unavailable',
      headers: {},
      config: {},
      data: {
        error: 'This server cannot send sign-in links: no mail server is set up.',
        code: 'SIGNIN_EMAIL_NOT_CONFIGURED',
        suggestion: 'Ask the administrator to configure the mail server.',
        request_id: 'abc123',
      },
    } as unknown as AxiosResponse
    api.requestMagicLink.mockRejectedValue(
      new AxiosError('Request failed with status code 503', 'ERR_BAD_RESPONSE', undefined, undefined, response)
    )
    const user = userEvent.setup()
    renderWithApp(<LoginPage />)

    await askForLink(user)

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('no mail server is set up')
    expect(alert).toHaveTextContent('Ask the administrator to configure the mail server.')
    expect(screen.queryByRole('heading', { name: 'Check your email' })).not.toBeInTheDocument()
  })

  it('tells someone who may sign up by email to check for a typo instead', async () => {
    api.getAuthMethods.mockResolvedValue(methods({ signup: true }))
    const user = userEvent.setup()
    renderWithApp(<LoginPage />)
    await screen.findByRole('button', { name: 'Continue with Google' })
    await askForLink(user)
    expect(await screen.findByText(/Check the address for a typo/)).toBeInTheDocument()
  })

  it('no longer claims end-to-end encryption', async () => {
    renderWithApp(<LoginPage />)
    expect(await screen.findByText('Journal encrypted at rest')).toBeInTheDocument()
    expect(screen.queryByText(/end-to-end/i)).not.toBeInTheDocument()
  })
})
