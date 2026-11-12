import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { MutationCache, QueryCache, QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import { AuthProvider } from './context/AuthContext'
import { ToastProvider, getToast } from './components/Toast'
import { toApiError } from './api/errors'
import './i18n'
import './styles/index.css'

/** Retry once, and only when the server might answer differently next time. */
function shouldRetry(failureCount: number, error: unknown): boolean {
  if (failureCount >= 1) return false
  const apiError = toApiError(error)
  if (apiError.code === 'TIMEOUT') return false
  return apiError.status === 0 || apiError.status >= 500
}

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    // Queries render their own inline error state; only opted-in ones toast.
    onError: (error, query) => {
      if (query.meta?.toastOnError) getToast().fromError(error)
    },
  }),
  mutationCache: new MutationCache({
    // Safety net: a mutation that does not handle its own failure still tells the user.
    onError: (error, _variables, _context, mutation) => {
      if (mutation.options.onError || mutation.meta?.silent) return
      getToast().fromError(error)
    },
  }),
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      retry: shouldRetry,
    },
  },
})

const basename = import.meta.env.VITE_BASE_PATH ?? '/devotional-journal/'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter basename={basename}>
        <ToastProvider>
          <AuthProvider>
            <App />
          </AuthProvider>
        </ToastProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
