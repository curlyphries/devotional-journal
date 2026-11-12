import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import { AlertTriangle, CheckCircle2, Info, X } from 'lucide-react'
import { toApiError } from '../api/errors'

type ToastKind = 'success' | 'error' | 'info'

interface ToastItem {
  id: number
  kind: ToastKind
  message: string
  suggestion?: string
  code?: string
  requestId?: string
}

interface ToastOptions {
  suggestion?: string
  code?: string
  requestId?: string
}

export interface ToastApi {
  success: (message: string) => void
  info: (message: string) => void
  /** Show an error with an optional "what to do" line and reference. */
  error: (message: string, options?: ToastOptions) => void
  /** Show whatever a request threw, normalised through toApiError. */
  fromError: (err: unknown, fallbackMessage?: string) => void
}

const noop: ToastApi = {
  success: () => undefined,
  info: () => undefined,
  error: () => undefined,
  fromError: () => undefined,
}

const ToastContext = createContext<ToastApi>(noop)

/**
 * Module-level handle so non-React code (the QueryClient's global error
 * handlers) can raise a toast. Set by the mounted ToastProvider.
 */
let activeToast: ToastApi = noop
export function getToast(): ToastApi {
  return activeToast
}

const DURATION_MS: Record<ToastKind, number> = { success: 4000, info: 5000, error: 9000 }
const MAX_VISIBLE = 4

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([])
  const nextId = useRef(1)
  const timers = useRef(new Map<number, ReturnType<typeof setTimeout>>())

  const dismiss = useCallback((id: number) => {
    setItems((current) => current.filter((item) => item.id !== id))
    const timer = timers.current.get(id)
    if (timer) {
      clearTimeout(timer)
      timers.current.delete(id)
    }
  }, [])

  const push = useCallback(
    (kind: ToastKind, message: string, options: ToastOptions = {}) => {
      const id = nextId.current++
      setItems((current) => {
        // Collapse repeats so one failing query does not stack identical toasts.
        if (current.some((item) => item.kind === kind && item.message === message)) return current
        return [...current.slice(-(MAX_VISIBLE - 1)), { id, kind, message, ...options }]
      })
      timers.current.set(
        id,
        setTimeout(() => dismiss(id), DURATION_MS[kind]),
      )
    },
    [dismiss],
  )

  const api = useMemo<ToastApi>(
    () => ({
      success: (message) => push('success', message),
      info: (message) => push('info', message),
      error: (message, options) => push('error', message, options),
      fromError: (err, fallbackMessage) => {
        const apiError = toApiError(err)
        push('error', fallbackMessage ? `${fallbackMessage} ${apiError.message}` : apiError.message, {
          suggestion: apiError.suggestion,
          code: apiError.code,
          requestId: apiError.requestId,
        })
      },
    }),
    [push],
  )

  useEffect(() => {
    activeToast = api
    const pending = timers.current
    return () => {
      activeToast = noop
      pending.forEach((timer) => clearTimeout(timer))
      pending.clear()
    }
  }, [api])

  return (
    <ToastContext.Provider value={api}>
      {children}
      <div
        className="fixed z-[100] bottom-4 inset-x-4 sm:inset-x-auto sm:right-4 sm:w-96 flex flex-col gap-2 pointer-events-none"
        aria-live="polite"
      >
        {items.map((item) => (
          <div
            key={item.id}
            role={item.kind === 'error' ? 'alert' : 'status'}
            className={`pointer-events-auto rounded-xl border bg-bg-elevated shadow-lg p-4 flex gap-3 ${
              item.kind === 'error'
                ? 'border-danger'
                : item.kind === 'success'
                  ? 'border-success'
                  : 'border-border'
            }`}
          >
            <span className="mt-0.5 shrink-0" aria-hidden="true">
              {item.kind === 'error' ? (
                <AlertTriangle className="w-5 h-5 text-red-400" />
              ) : item.kind === 'success' ? (
                <CheckCircle2 className="w-5 h-5 text-green-400" />
              ) : (
                <Info className="w-5 h-5 text-text-secondary" />
              )}
            </span>
            <div className="min-w-0 flex-1 text-sm">
              <p className="text-text-primary font-medium break-words">{item.message}</p>
              {item.suggestion && (
                <p className="text-text-secondary mt-1 break-words">{item.suggestion}</p>
              )}
              {(item.code || item.requestId) && (
                <p className="text-text-secondary/80 mt-1 text-xs font-mono break-all">
                  {[item.code, item.requestId && `ref ${item.requestId}`].filter(Boolean).join(' · ')}
                </p>
              )}
            </div>
            <button
              type="button"
              onClick={() => dismiss(item.id)}
              className="shrink-0 text-text-secondary hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary rounded"
              aria-label="Dismiss notification"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast(): ToastApi {
  return useContext(ToastContext)
}
