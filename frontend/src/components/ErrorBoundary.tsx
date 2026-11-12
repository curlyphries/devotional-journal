import { Component, ErrorInfo, ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { AlertTriangle, RefreshCw } from 'lucide-react'

interface ErrorBoundaryProps {
  children: ReactNode
  /** When this value changes (e.g. the route path) the boundary clears its error. */
  resetKey?: string
}

interface ErrorBoundaryState {
  error: Error | null
}

function ErrorFallback({ error }: { error: Error }) {
  const { t } = useTranslation()
  return (
    <div className="max-w-xl mx-auto py-8 px-4">
      <div role="alert" className="card">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-6 h-6 text-red-400 shrink-0 mt-0.5" aria-hidden="true" />
          <div className="min-w-0">
            <h1 className="text-lg font-semibold text-text-primary">{t('errors.boundaryTitle')}</h1>
            <p className="text-text-secondary mt-2">{t('errors.boundaryBody')}</p>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-3 mt-5">
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="btn-primary inline-flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" aria-hidden="true" />
            {t('errors.reload')}
          </button>
          <Link to="/help" className="text-accent-primary hover:underline">
            {t('errors.goHelp')}
          </Link>
        </div>
        <details className="mt-5 text-sm">
          <summary className="cursor-pointer text-text-secondary">{t('errors.technicalDetails')}</summary>
          <pre className="mt-2 p-3 rounded-lg bg-bg-elevated text-text-secondary text-xs whitespace-pre-wrap break-words">
            {error.message || String(error)}
          </pre>
        </details>
      </div>
    </div>
  )
}

/** Catches render errors below it so one broken page does not blank the whole app. */
export default class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Unhandled render error:', error, info.componentStack)
  }

  componentDidUpdate(prevProps: ErrorBoundaryProps) {
    if (this.state.error && prevProps.resetKey !== this.props.resetKey) {
      this.setState({ error: null })
    }
  }

  render() {
    if (this.state.error) return <ErrorFallback error={this.state.error} />
    return this.props.children
  }
}
