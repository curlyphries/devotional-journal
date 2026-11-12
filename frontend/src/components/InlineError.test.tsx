import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '../i18n'
import InlineError from './InlineError'

const apiError = {
  code: 'SCRIPTURE_UNAVAILABLE',
  message: 'The Bible text source is unreachable.',
  suggestion: 'Try again in a few minutes.',
  requestId: 'abc123',
  status: 503,
}

describe('InlineError', () => {
  it('renders message, suggestion, code and reference as an alert', () => {
    render(<InlineError error={apiError} />)

    const alert = screen.getByRole('alert')
    expect(alert).toHaveTextContent("This couldn't be loaded")
    expect(alert).toHaveTextContent('The Bible text source is unreachable.')
    expect(alert).toHaveTextContent('Try again in a few minutes.')
    expect(alert).toHaveTextContent('SCRIPTURE_UNAVAILABLE · ref abc123')
  })

  it('uses the given title and has no retry button unless onRetry is passed', () => {
    render(<InlineError error={apiError} title="Couldn't load your reviews" />)

    expect(screen.getByText("Couldn't load your reviews")).toBeInTheDocument()
    expect(screen.queryByRole('button')).not.toBeInTheDocument()
  })

  it('calls onRetry when "Try again" is clicked', async () => {
    const onRetry = vi.fn()
    render(<InlineError error={apiError} onRetry={onRetry} />)

    await userEvent.click(screen.getByRole('button', { name: 'Try again' }))
    expect(onRetry).toHaveBeenCalledTimes(1)
  })

  it('normalises anything thrown, including plain Errors', () => {
    render(<InlineError error={new Error('boom')} />)

    expect(screen.getByRole('alert')).toHaveTextContent('boom')
    expect(screen.getByRole('alert')).toHaveTextContent('CLIENT_ERROR')
  })
})
