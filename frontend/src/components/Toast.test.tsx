import { describe, it, expect } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AxiosError, AxiosHeaders, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'
import { ToastProvider, getToast, useToast } from './Toast'

const config = { headers: new AxiosHeaders() } as InternalAxiosRequestConfig

function aiDownError(): AxiosError {
  const response = {
    status: 503,
    data: {
      error: 'The AI provider is not responding.',
      code: 'AI_UNAVAILABLE',
      suggestion: 'Check that Ollama is running.',
      request_id: 'req-123',
    },
    headers: {},
    statusText: '',
    config,
  } as AxiosResponse
  return new AxiosError('Request failed', AxiosError.ERR_BAD_RESPONSE, config, {}, response)
}

function Trigger() {
  const toast = useToast()
  return (
    <>
      <button onClick={() => toast.fromError(aiDownError())}>fail</button>
      <button onClick={() => toast.success('Saved.')}>ok</button>
    </>
  )
}

describe('Toast', () => {
  it('fromError shows the message, the suggestion and the reference', async () => {
    render(
      <ToastProvider>
        <Trigger />
      </ToastProvider>,
    )

    await userEvent.click(screen.getByText('fail'))

    const alert = screen.getByRole('alert')
    expect(alert).toHaveTextContent('The AI provider is not responding.')
    expect(alert).toHaveTextContent('Check that Ollama is running.')
    expect(alert).toHaveTextContent('AI_UNAVAILABLE')
    expect(alert).toHaveTextContent('ref req-123')
  })

  it('does not stack identical errors and can be dismissed', async () => {
    render(
      <ToastProvider>
        <Trigger />
      </ToastProvider>,
    )

    await userEvent.click(screen.getByText('fail'))
    await userEvent.click(screen.getByText('fail'))
    expect(screen.getAllByRole('alert')).toHaveLength(1)

    await userEvent.click(screen.getByRole('button', { name: 'Dismiss notification' }))
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('shows success messages as a status, not an alert', async () => {
    render(
      <ToastProvider>
        <Trigger />
      </ToastProvider>,
    )

    await userEvent.click(screen.getByText('ok'))
    expect(screen.getByRole('status')).toHaveTextContent('Saved.')
  })

  it('getToast() reaches the mounted provider from non-React code', () => {
    render(
      <ToastProvider>
        <div />
      </ToastProvider>,
    )

    act(() => getToast().fromError(aiDownError(), 'Could not save.'))

    expect(screen.getByRole('alert')).toHaveTextContent('Could not save. The AI provider is not responding.')
  })
})
