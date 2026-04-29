import { ChangeEvent, FormEvent, useCallback, useEffect, useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { Bookmark, BookOpen, ChevronDown, ChevronUp, Clock, Loader2, Sparkles, Target, Trash2 } from 'lucide-react'
import client from '../api/client'
import { useCreateFocusIntention } from '../hooks/useDevotional'

interface ExplorePassage {
  reference: string
  book: string
  chapter: number
  verse_start: number
  verse_end: number
  text: string
  reason: string
}

interface ExplorePlan {
  id: string
  title: string
  description: string
  category: string
  total_days: number
}

interface ExploreResult {
  id?: string
  passages: ExplorePassage[]
  prompts: string[]
  category: string
  summary: string
  plans: ExplorePlan[]
  created_at?: string
  is_bookmarked?: boolean
  user_input?: string
}

interface HistoryItem {
  id: string
  user_input: string
  summary: string
  category: string
  passage_count: number
  is_bookmarked: boolean
  created_at: string
}

const QUICK_TOPICS = [
  'anxiety and fear',
  'discipline and consistency',
  'marriage conflict',
  'purpose and direction',
  'forgiveness',
  'hope in suffering',
]

function timeAgo(dateStr: string): string {
  const now = new Date()
  const date = new Date(dateStr)
  const diffMs = now.getTime() - date.getTime()
  const mins = Math.floor(diffMs / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}d ago`
  return date.toLocaleDateString()
}

export default function HeartPromptExplorer() {
  const navigate = useNavigate()
  const createFocus = useCreateFocusIntention()
  const [mindInput, setMindInput] = useState('')
  const [focusError, setFocusError] = useState('')
  const [guidance, setGuidance] = useState<ExploreResult | null>(null)
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [showHistory, setShowHistory] = useState(false)
  const [loadingHistory, setLoadingHistory] = useState(false)
  const [loadingRestore, setLoadingRestore] = useState<string | null>(null)

  const fetchHistory = useCallback(async () => {
    setLoadingHistory(true)
    try {
      const res = await client.get('/prompts/explorations/')
      setHistory(res.data || [])
    } catch {
      // Silently fail — history is a convenience, not critical
    } finally {
      setLoadingHistory(false)
    }
  }, [])

  useEffect(() => {
    fetchHistory()
  }, [fetchHistory])

  const guidanceMutation = useMutation<ExploreResult, Error, string>({
    mutationFn: async (rawInput: string) => {
      const input = rawInput.trim()
      if (!input) {
        throw new Error('Please share what is on your mind first.')
      }

      const response = await client.post('/prompts/explore/', { input })

      if (response.data?.error) {
        throw new Error(response.data.error)
      }

      return response.data as ExploreResult
    },
    onSuccess: (data: ExploreResult) => {
      setGuidance(data)
      // Refresh history list to include the new entry
      fetchHistory()
    },
  })

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setFocusError('')
    setGuidance(null)
    await guidanceMutation.mutateAsync(mindInput)
  }

  const handleRestore = async (explorationId: string) => {
    setLoadingRestore(explorationId)
    try {
      const res = await client.get(`/prompts/explorations/${explorationId}/`)
      const data = res.data as ExploreResult
      setGuidance(data)
      setMindInput(data.user_input || '')
      setShowHistory(false)
    } catch {
      // Ignore
    } finally {
      setLoadingRestore(null)
    }
  }

  const handleBookmark = async (explorationId: string) => {
    try {
      const res = await client.post(`/prompts/explorations/${explorationId}/bookmark/`)
      const newBookmarked = res.data?.is_bookmarked
      // Update local history state
      setHistory((prev: HistoryItem[]) =>
        prev.map((h: HistoryItem) =>
          h.id === explorationId ? { ...h, is_bookmarked: newBookmarked } : h
        )
      )
      // Update current guidance if it matches
      if (guidance?.id === explorationId) {
        setGuidance((prev: ExploreResult | null) => prev ? { ...prev, is_bookmarked: newBookmarked } : prev)
      }
    } catch {
      // Ignore
    }
  }

  const handleDelete = async (explorationId: string) => {
    try {
      await client.delete(`/prompts/explorations/${explorationId}/`)
      setHistory((prev: HistoryItem[]) => prev.filter((h: HistoryItem) => h.id !== explorationId))
      if (guidance?.id === explorationId) {
        setGuidance(null)
      }
    } catch {
      // Ignore
    }
  }

  const handleCreateFocus = async () => {
    const intention = mindInput.trim()
    if (!intention) return

    setFocusError('')
    try {
      await createFocus.mutateAsync({
        period_type: 'week',
        intention,
      })
      navigate('/devotional')
    } catch {
      setFocusError('Unable to create focus right now. You may already have an active weekly focus.')
    }
  }

  return (
    <div className="card bg-gradient-to-br from-indigo-900/20 via-gray-900 to-purple-900/20 border border-indigo-500/30">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-indigo-300" />
          <h2 className="text-lg font-semibold text-white">Speak Your Mind</h2>
        </div>
        {history.length > 0 && (
          <button
            type="button"
            onClick={() => setShowHistory(!showHistory)}
            className="flex items-center gap-1 text-xs text-indigo-300 hover:text-indigo-200 transition-colors"
          >
            <Clock className="w-3.5 h-3.5" />
            <span>{history.length} past {history.length === 1 ? 'search' : 'searches'}</span>
            {showHistory ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        )}
      </div>

      {showHistory && (
        <div className="mb-4 space-y-1.5 max-h-48 overflow-y-auto rounded-lg border border-gray-700 bg-gray-900/50 p-2">
          {loadingHistory && <p className="text-xs text-gray-400 p-2">Loading...</p>}
          {history.map((item: HistoryItem) => (
            <div
              key={item.id}
              className="flex items-center gap-2 group"
            >
              <button
                type="button"
                onClick={() => handleRestore(item.id)}
                disabled={loadingRestore === item.id}
                className="flex-1 text-left px-3 py-2 rounded-md hover:bg-gray-800 transition-colors"
              >
                <div className="flex items-center gap-2">
                  {loadingRestore === item.id ? (
                    <Loader2 className="w-3 h-3 animate-spin text-indigo-300 shrink-0" />
                  ) : (
                    <Sparkles className="w-3 h-3 text-indigo-400 shrink-0" />
                  )}
                  <span className="text-sm text-gray-200 truncate">{item.user_input}</span>
                </div>
                <div className="flex items-center gap-2 mt-0.5 ml-5">
                  <span className="text-xs text-gray-500">{timeAgo(item.created_at)}</span>
                  <span className="text-xs text-gray-600">·</span>
                  <span className="text-xs text-gray-500">{item.passage_count} passages</span>
                  {item.summary && (
                    <>
                      <span className="text-xs text-gray-600">·</span>
                      <span className="text-xs text-gray-400 truncate">{item.summary}</span>
                    </>
                  )}
                </div>
              </button>
              <button
                type="button"
                onClick={() => handleBookmark(item.id)}
                className="p-1 opacity-60 hover:opacity-100 transition-opacity shrink-0"
                title={item.is_bookmarked ? 'Remove bookmark' : 'Bookmark'}
              >
                <Bookmark className={`w-3.5 h-3.5 ${item.is_bookmarked ? 'text-amber-400 fill-amber-400' : 'text-gray-500'}`} />
              </button>
              <button
                type="button"
                onClick={() => handleDelete(item.id)}
                className="p-1 opacity-0 group-hover:opacity-60 hover:!opacity-100 transition-opacity shrink-0"
                title="Delete"
              >
                <Trash2 className="w-3.5 h-3.5 text-red-400" />
              </button>
            </div>
          ))}
        </div>
      )}

      <p className="text-sm text-gray-300 mb-4">
        Share what you are wrestling with, curious about, or studying. Our AI will find relevant scripture, generate reflection prompts, and recommend reading plans. Your results are saved automatically.
      </p>

      <form onSubmit={handleSubmit} className="space-y-3">
        <textarea
          value={mindInput}
          onChange={(event: ChangeEvent<HTMLTextAreaElement>) => setMindInput(event.target.value)}
          placeholder="Example: I want to understand the book of Romans and the concept of hope, or I'm struggling with anger at work..."
          className="w-full h-24 px-3 py-2 bg-gray-900/70 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-indigo-400 resize-none"
        />

        <div className="flex flex-wrap gap-2">
          {QUICK_TOPICS.map((topic: string) => (
            <button
              key={topic}
              type="button"
              onClick={() => setMindInput(topic)}
              className="text-xs px-2 py-1 rounded-md bg-gray-800 text-gray-300 hover:text-white hover:bg-gray-700"
            >
              {topic}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            type="submit"
            disabled={guidanceMutation.isPending || mindInput.trim().length < 3}
            className="px-4 py-2 rounded-lg bg-indigo-500 text-white hover:bg-indigo-400 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {guidanceMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
            {guidanceMutation.isPending ? 'Thinking...' : 'Ask the Bible Agent'}
          </button>

          <button
            type="button"
            disabled={!mindInput.trim() || createFocus.isPending}
            onClick={handleCreateFocus}
            className="px-4 py-2 rounded-lg bg-purple-500/20 text-purple-300 border border-purple-500/40 hover:bg-purple-500/30 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {createFocus.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Target className="w-4 h-4" />}
            Set as Weekly Focus
          </button>

          <button
            type="button"
            disabled={!mindInput.trim()}
            onClick={() => navigate(`/devotional?intention=${encodeURIComponent(mindInput.trim())}&period=week`)}
            className="px-4 py-2 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30 transition-colors disabled:opacity-50"
          >
            Open in Devotional
          </button>
        </div>
      </form>

      {focusError && <p className="text-red-300 text-sm mt-3">{focusError}</p>}
      {guidanceMutation.error && <p className="text-red-300 text-sm mt-3">{guidanceMutation.error.message}</p>}

      {guidance && (
        <div className="mt-5 space-y-5">
          <div className="flex items-center justify-between">
            {guidance.summary && (
              <p className="text-sm text-gray-300 italic border-l-2 border-indigo-500/50 pl-3 flex-1">
                {guidance.summary}
              </p>
            )}
            {guidance.id && (
              <button
                type="button"
                onClick={() => handleBookmark(guidance.id as string)}
                className="ml-3 p-1.5 rounded hover:bg-gray-800 transition-colors shrink-0"
                title={guidance.is_bookmarked ? 'Remove bookmark' : 'Bookmark this exploration'}
              >
                <Bookmark className={`w-4 h-4 ${guidance.is_bookmarked ? 'text-amber-400 fill-amber-400' : 'text-gray-500'}`} />
              </button>
            )}
          </div>

          <div>
            <h3 className="text-sm font-semibold text-indigo-300 mb-2">Relevant Scriptures</h3>
            <div className="space-y-2">
              {guidance.passages.map((passage: ExplorePassage) => (
                <div key={`${passage.book}-${passage.chapter}-${passage.verse_start}`} className="p-3 rounded-lg bg-gray-900/70 border border-gray-700">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-amber-400 text-sm font-medium">{passage.reference}</p>
                    <button
                      type="button"
                      onClick={() => navigate(`/bible?passage=${encodeURIComponent(passage.reference)}`)}
                      className="text-xs text-indigo-300 hover:text-indigo-200"
                    >
                      Open
                    </button>
                  </div>
                  {passage.text && (
                    <p className="text-sm text-gray-200 mt-1 leading-relaxed">{passage.text}</p>
                  )}
                  {passage.reason && (
                    <p className="text-xs text-gray-400 mt-2 italic">{passage.reason}</p>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-indigo-300 mb-2">Reflection Prompts</h3>
            <ul className="space-y-2">
              {guidance.prompts.map((prompt: string, index: number) => (
                <li key={`${index}-${prompt}`} className="text-sm text-gray-200 flex gap-2">
                  <span className="text-indigo-300 shrink-0">•</span>
                  <span>{prompt}</span>
                </li>
              ))}
            </ul>
          </div>

          {guidance.plans.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold text-indigo-300">Recommended Plans</h3>
                <button
                  type="button"
                  onClick={() => navigate(`/plans?category=${encodeURIComponent(guidance.category)}`)}
                  className="text-xs text-indigo-300 hover:text-indigo-200"
                >
                  Browse Category
                </button>
              </div>
              <div className="space-y-2">
                {guidance.plans.map((plan: ExplorePlan) => (
                  <button
                    key={plan.id}
                    type="button"
                    onClick={() => navigate('/plans')}
                    className="w-full text-left p-3 rounded-lg bg-gray-900/70 border border-gray-700 hover:border-indigo-500/50 transition-colors"
                  >
                    <div className="flex items-center gap-2 text-white">
                      <BookOpen className="w-4 h-4 text-indigo-300" />
                      <span className="font-medium">{plan.title}</span>
                      <span className="text-xs text-gray-500 ml-auto">{plan.total_days} days</span>
                    </div>
                    {plan.description && <p className="text-sm text-gray-300 mt-1">{plan.description}</p>}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
