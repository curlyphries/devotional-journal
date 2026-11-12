import axios from 'axios'

/**
 * Normalised API error.
 *
 * The backend returns every 4xx/5xx as:
 *   { error: string, code: string, suggestion?: string, request_id?: string, details?: object }
 * Anything else (network down, timeout, a proxy HTML page) is mapped onto the
 * same shape here so the UI has one thing to render.
 */
export interface ApiError {
  /** Machine-readable code, e.g. AI_UNAVAILABLE. See docs/TROUBLESHOOTING.md. */
  code: string
  /** Human-readable description of what went wrong. */
  message: string
  /** What the user can do about it, when known. */
  suggestion?: string
  /** Server request id — quote this when reporting a problem. */
  requestId?: string
  /** HTTP status, or 0 when the request never reached the server. */
  status: number
  /** Per-field validation messages, when the server sent them. */
  details?: Record<string, unknown>
}

const FALLBACK_SUGGESTIONS: Record<string, string> = {
  NETWORK_ERROR:
    'Check that you are connected to the network (and to the mesh/VPN if this is a private instance), then try again.',
  TIMEOUT: 'The server took too long to answer. Try again; AI features can be slow on local models.',
  NOT_AUTHENTICATED: 'Sign in again.',
  PERMISSION_DENIED: 'You do not have access to this item.',
  NOT_FOUND: 'This item may have been deleted. Go back and refresh the list.',
  RATE_LIMITED: 'Wait a few minutes before trying again.',
  SERVER_ERROR: 'Try again. If it keeps happening, report it with the reference shown.',
  AI_UNAVAILABLE: 'Check Settings → AI Provider, or make sure your local model server is running.',
  AI_NOT_CONFIGURED: 'Choose an AI provider in Settings → AI Provider.',
  AI_CONSENT_REQUIRED:
    'This server uses a cloud AI. Allow it in Settings → AI Provider, or configure your own local provider.',
}

function codeFromStatus(status: number): string {
  if (status === 400 || status === 422) return 'VALIDATION_ERROR'
  if (status === 401) return 'NOT_AUTHENTICATED'
  if (status === 403) return 'PERMISSION_DENIED'
  if (status === 404) return 'NOT_FOUND'
  if (status === 429) return 'RATE_LIMITED'
  return 'SERVER_ERROR'
}

export function isApiError(value: unknown): value is ApiError {
  return (
    typeof value === 'object' &&
    value !== null &&
    // An AxiosError also carries string `code`/`message` and (axios >= 1.7) a
    // numeric `status`, so it would pass the shape check below and be shown raw
    // ("Request failed with status code 503", ERR_BAD_RESPONSE).
    !axios.isAxiosError(value) &&
    typeof (value as ApiError).code === 'string' &&
    typeof (value as ApiError).message === 'string' &&
    typeof (value as ApiError).status === 'number'
  )
}

/** Convert anything thrown by a request into an ApiError. Never throws. */
export function toApiError(err: unknown): ApiError {
  if (isApiError(err)) return err

  if (axios.isAxiosError(err)) {
    if (!err.response) {
      const timedOut = err.code === 'ECONNABORTED' || err.code === 'ETIMEDOUT'
      const code = timedOut ? 'TIMEOUT' : 'NETWORK_ERROR'
      return {
        code,
        message: timedOut ? 'The request timed out.' : 'Could not reach the server.',
        suggestion: FALLBACK_SUGGESTIONS[code],
        status: 0,
      }
    }

    const { status, data, headers } = err.response
    const body = (typeof data === 'object' && data !== null ? data : {}) as Record<string, unknown>
    const code = typeof body.code === 'string' ? body.code : codeFromStatus(status)
    const message =
      (typeof body.error === 'string' && body.error) ||
      (typeof body.detail === 'string' && body.detail) ||
      (typeof body.message === 'string' && body.message) ||
      `Request failed (${status}).`
    const suggestion =
      (typeof body.suggestion === 'string' && body.suggestion) || FALLBACK_SUGGESTIONS[code]
    const requestId =
      (typeof body.request_id === 'string' && body.request_id) ||
      (headers?.['x-request-id'] as string | undefined)
    const details =
      typeof body.details === 'object' && body.details !== null
        ? (body.details as Record<string, unknown>)
        : undefined

    return { code, message, suggestion, requestId, status, details }
  }

  const message = err instanceof Error ? err.message : 'Something unexpected happened.'
  return {
    code: 'CLIENT_ERROR',
    message,
    suggestion: 'Reload the page. If it keeps happening, report it.',
    status: 0,
  }
}
