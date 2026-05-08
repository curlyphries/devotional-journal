import { Component, ErrorInfo, ReactNode } from 'react'
import { AlertTriangle } from 'lucide-react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
  /** Logging label — shown in console alongside the stack so issues are findable. */
  label?: string
}

interface State {
  error: Error | null
}

/**
 * Tiny error boundary so a runtime crash inside one page does not blank the
 * entire layout (nav, FAB, etc.). Used to wrap individual route elements.
 */
export default class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null }

  static getDerivedStateFromError(error: Error): State {
    return { error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error(`[ErrorBoundary${this.props.label ? ` · ${this.props.label}` : ''}]`, error, info.componentStack)
  }

  reset = () => this.setState({ error: null })

  render() {
    if (this.state.error) {
      if (this.props.fallback) return this.props.fallback
      return (
        <div className="card border-red-500/30 bg-red-500/5">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-500/15 flex items-center justify-center shrink-0">
              <AlertTriangle className="w-5 h-5 text-red-400" aria-hidden="true" />
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-text-primary font-semibold mb-1">Something went wrong on this page</h2>
              <p className="text-text-secondary text-sm mb-3">
                The rest of the app still works — open the browser console for details.
              </p>
              <pre className="text-xs text-red-300 bg-bg-elevated rounded p-2 overflow-auto max-h-40">
                {this.state.error.message}
              </pre>
              <button
                onClick={this.reset}
                className="mt-3 text-sm text-amber-400 hover:text-amber-300"
              >
                Try again
              </button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
