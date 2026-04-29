import { useState } from 'react'
import { 
  MessageCircle, 
  CheckCircle, 
  Clock, 
  XCircle,
  ChevronDown,
  ChevronUp,
  Loader2,
  AlertTriangle,
  TrendingUp,
  HelpCircle
} from 'lucide-react'
import { 
  useActiveThreads, 
  useThreadStats,
  useThreadActions
} from '../hooks/useReflections'
import { OpenThread } from '../api/reflections'

const THREAD_TYPE_ICONS: Record<string, React.ReactNode> = {
  struggle: <AlertTriangle className="w-5 h-5" />,
  commitment: <CheckCircle className="w-5 h-5" />,
  question: <HelpCircle className="w-5 h-5" />,
  relationship: <MessageCircle className="w-5 h-5" />,
  decision: <Clock className="w-5 h-5" />,
  confession: <MessageCircle className="w-5 h-5" />,
}

const THREAD_TYPE_COLORS: Record<string, string> = {
  struggle: 'text-red-500 bg-red-500/10',
  commitment: 'text-green-500 bg-green-500/10',
  question: 'text-blue-500 bg-blue-500/10',
  relationship: 'text-purple-500 bg-purple-500/10',
  decision: 'text-yellow-500 bg-yellow-500/10',
  confession: 'text-pink-500 bg-pink-500/10',
}

const STATUS_COLORS: Record<string, string> = {
  open: 'bg-blue-500/10 text-blue-500',
  following_up: 'bg-yellow-500/10 text-yellow-500',
  progressing: 'bg-green-500/10 text-green-500',
  resolved: 'bg-gray-500/10 text-gray-500',
  deferred: 'bg-orange-500/10 text-orange-500',
  dropped: 'bg-red-500/10 text-red-500',
}

export default function ThreadsPage() {
  const { data: threads, isLoading } = useActiveThreads()
  const { data: stats } = useThreadStats()
  const [filter, setFilter] = useState<string>('all')

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-accent-primary" />
      </div>
    )
  }

  const filteredThreads = threads?.filter((thread) => {
    if (filter === 'all') return true
    return thread.thread_type === filter
  })

  return (
    <div className="min-h-screen bg-bg-primary p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-text-primary">Open Threads</h1>
            <p className="text-text-secondary mt-1">
              Track your struggles, commitments, and growth areas
            </p>
          </div>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <StatCard label="Open" value={stats.open || 0} color="blue" />
            <StatCard label="Following Up" value={stats.following_up || 0} color="yellow" />
            <StatCard label="Progressing" value={stats.progressing || 0} color="green" />
            <StatCard label="Resolved" value={stats.resolved || 0} color="gray" />
          </div>
        )}

        {/* Filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          {['all', 'struggle', 'commitment', 'question', 'relationship', 'decision'].map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === type
                  ? 'bg-accent-primary text-white'
                  : 'bg-bg-secondary text-text-primary hover:bg-bg-secondary/80'
              }`}
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>

        {/* Threads List */}
        <div className="space-y-4">
          {filteredThreads && filteredThreads.length > 0 ? (
            filteredThreads.map((thread) => (
              <ThreadCard key={thread.id} thread={thread} />
            ))
          ) : (
            <div className="text-center py-16">
              <TrendingUp className="w-16 h-16 text-text-secondary mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-text-primary mb-2">
                No Active Threads
              </h2>
              <p className="text-text-secondary">
                Threads are automatically detected from your reflections
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function StatCard({ label, value, color }: { label: string; value: number; color: string }) {
  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-500/10 text-blue-500',
    yellow: 'bg-yellow-500/10 text-yellow-500',
    green: 'bg-green-500/10 text-green-500',
    gray: 'bg-gray-500/10 text-gray-500',
  }

  return (
    <div className="bg-bg-secondary rounded-lg p-4">
      <div className={`text-3xl font-bold ${colorClasses[color]?.split(' ')[1] || 'text-text-primary'}`}>
        {value}
      </div>
      <div className="text-sm text-text-secondary">{label}</div>
    </div>
  )
}

function ThreadCard({ thread }: { thread: OpenThread }) {
  const [expanded, setExpanded] = useState(false)
  const { resolve, defer, drop } = useThreadActions(thread.id)
  const [showResolveInput, setShowResolveInput] = useState(false)
  const [resolutionNote, setResolutionNote] = useState('')

  const handleResolve = () => {
    resolve.mutate(resolutionNote)
    setShowResolveInput(false)
    setResolutionNote('')
  }

  return (
    <div className="bg-bg-secondary rounded-xl overflow-hidden">
      <div
        className="p-4 cursor-pointer flex items-start gap-4"
        onClick={() => setExpanded(!expanded)}
      >
        <div className={`p-2 rounded-lg ${THREAD_TYPE_COLORS[thread.thread_type]}`}>
          {THREAD_TYPE_ICONS[thread.thread_type]}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_COLORS[thread.status]}`}>
              {thread.status.replace('_', ' ')}
            </span>
            <span className="text-xs text-text-secondary">
              {thread.days_since_mentioned} days ago
            </span>
          </div>
          <p className="text-text-primary font-medium truncate">{thread.summary}</p>
          {thread.related_life_area && (
            <span className="text-xs text-accent-primary">{thread.related_life_area}</span>
          )}
        </div>

        <button className="p-1 text-text-secondary">
          {expanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
      </div>

      {expanded && (
        <div className="px-4 pb-4 border-t border-border-primary pt-4">
          {thread.original_context && (
            <div className="mb-4 p-3 bg-bg-primary rounded-lg">
              <p className="text-sm text-text-secondary italic">"{thread.original_context}"</p>
            </div>
          )}

          <div className="flex items-center gap-2 text-sm text-text-secondary mb-4">
            <span>Follow-ups: {thread.followup_count}</span>
            <span>•</span>
            <span>Skipped: {thread.skip_count}</span>
          </div>

          {showResolveInput ? (
            <div className="space-y-3">
              <textarea
                value={resolutionNote}
                onChange={(e) => setResolutionNote(e.target.value)}
                placeholder="How did you resolve this? (optional)"
                rows={3}
                className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary resize-none"
              />
              <div className="flex gap-2">
                <button
                  onClick={() => setShowResolveInput(false)}
                  className="flex-1 py-2 bg-bg-primary text-text-primary rounded-lg font-medium"
                >
                  Cancel
                </button>
                <button
                  onClick={handleResolve}
                  disabled={resolve.isPending}
                  className="flex-1 py-2 bg-green-500 text-white rounded-lg font-medium hover:bg-green-500/90 disabled:opacity-50"
                >
                  {resolve.isPending ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : 'Mark Resolved'}
                </button>
              </div>
            </div>
          ) : (
            <div className="flex gap-2">
              <button
                onClick={() => setShowResolveInput(true)}
                className="flex-1 py-2 bg-green-500 text-white rounded-lg font-medium hover:bg-green-500/90 flex items-center justify-center gap-2"
              >
                <CheckCircle className="w-4 h-4" />
                Resolve
              </button>
              <button
                onClick={() => defer.mutate(7)}
                disabled={defer.isPending}
                className="flex-1 py-2 bg-bg-primary text-text-primary rounded-lg font-medium hover:bg-bg-primary/80 flex items-center justify-center gap-2"
              >
                <Clock className="w-4 h-4" />
                Defer 7 days
              </button>
              <button
                onClick={() => drop.mutate()}
                disabled={drop.isPending}
                className="py-2 px-4 bg-red-500/10 text-red-500 rounded-lg font-medium hover:bg-red-500/20"
              >
                <XCircle className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
