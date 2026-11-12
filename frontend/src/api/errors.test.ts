import { describe, it, expect } from 'vitest'
import { AxiosError, AxiosHeaders, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'
import { isApiError, toApiError } from './errors'

const config = { headers: new AxiosHeaders() } as InternalAxiosRequestConfig

function httpError(status: number, data: unknown, headers: Record<string, string> = {}): AxiosError {
  const response = { status, data, headers, statusText: '', config } as AxiosResponse
  return new AxiosError('Request failed', AxiosError.ERR_BAD_RESPONSE, config, {}, response)
}

describe('toApiError', () => {
  it('reads the backend error envelope', () => {
    const result = toApiError(
      httpError(503, {
        error: 'The AI provider is not responding.',
        code: 'AI_UNAVAILABLE',
        suggestion: 'Start Ollama and try again.',
        request_id: 'a1b2c3d4',
        details: { ai_base_url: ['Not allowed.'] },
      }),
    )

    expect(result).toEqual({
      code: 'AI_UNAVAILABLE',
      message: 'The AI provider is not responding.',
      suggestion: 'Start Ollama and try again.',
      requestId: 'a1b2c3d4',
      status: 503,
      details: { ai_base_url: ['Not allowed.'] },
    })
  })

  it('falls back to the X-Request-ID header and a built-in suggestion', () => {
    const result = toApiError(
      httpError(404, { error: 'Entry not found', code: 'NOT_FOUND' }, { 'x-request-id': 'hdr-42' }),
    )

    expect(result.requestId).toBe('hdr-42')
    expect(result.suggestion).toMatch(/deleted/i)
  })

  it('maps a request that never reached the server to NETWORK_ERROR', () => {
    const result = toApiError(new AxiosError('Network Error', AxiosError.ERR_NETWORK, config, {}))

    expect(result.code).toBe('NETWORK_ERROR')
    expect(result.status).toBe(0)
    expect(result.message).toBe('Could not reach the server.')
    expect(result.suggestion).toBeTruthy()
  })

  it('maps an aborted request to TIMEOUT', () => {
    const result = toApiError(new AxiosError('timeout of 30000ms exceeded', AxiosError.ECONNABORTED, config, {}))

    expect(result.code).toBe('TIMEOUT')
    expect(result.status).toBe(0)
    expect(result.message).toBe('The request timed out.')
  })

  it.each([
    [400, 'VALIDATION_ERROR'],
    [401, 'NOT_AUTHENTICATED'],
    [403, 'PERMISSION_DENIED'],
    [404, 'NOT_FOUND'],
    [429, 'RATE_LIMITED'],
    [500, 'SERVER_ERROR'],
    [502, 'SERVER_ERROR'],
  ])('derives the code from HTTP %i when the body has none', (status, code) => {
    // e.g. a proxy's HTML error page
    const result = toApiError(httpError(status, '<html>Bad Gateway</html>'))

    expect(result.code).toBe(code)
    expect(result.status).toBe(status)
    expect(result.message).toBe(`Request failed (${status}).`)
  })

  it('accepts DRF-style {detail} bodies', () => {
    expect(toApiError(httpError(403, { detail: 'You do not have permission.' })).message).toBe(
      'You do not have permission.',
    )
  })

  it('wraps non-request errors and passes ApiErrors through unchanged', () => {
    const wrapped = toApiError(new Error('boom'))
    expect(wrapped).toMatchObject({ code: 'CLIENT_ERROR', message: 'boom', status: 0 })
    expect(isApiError(wrapped)).toBe(true)
    expect(toApiError(wrapped)).toBe(wrapped)
    expect(toApiError(undefined).code).toBe('CLIENT_ERROR')
  })
})
