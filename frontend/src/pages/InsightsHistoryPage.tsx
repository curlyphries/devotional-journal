import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { format, isValid, parseISO } from 'date-fns'
import { Link } from 'react-router-dom'
import { 
  BookOpen, 
  Calendar, 
  ChevronLeft,
  Sparkles,
  ExternalLink,
  Loader2,
  Filter
} from 'lucide-react'
import { useTranslation } from 'react-i18next'
import client from '../api/client'
import { unwrapList } from '../api/pagination'
import { getFeedbackLog } from '../api/journal'
import InlineError from '../components/InlineError'

interface DailyReflection {
  id: string
  date: string
  scripture_reference: string
  ai_insight: string
  scripture_themes: string[]
  area_scores: Record<string, number>
}

const fetchReflections = async (): Promise<DailyReflection[]> => {
  const response = await client.get('/reflections/')
  return unwrapList<DailyReflection>(response.data)
}

/** Format a YYYY-MM-DD date without the timezone shift `new Date('2026-11-12')` causes. */
function formatDay(isoDate: string): string {
  const parsed = parseISO(isoDate)
  return isValid(parsed) ? format(parsed, 'MMMM d, yyyy') : isoDate
}

export default function InsightsHistoryPage() {
  const [viewMode, setViewMode] = useState<'reflections' | 'journal'>('reflections')
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null)

  const { t } = useTranslation()
  const reflectionsQuery = useQuery({
    queryKey: ['reflections-history'],
    queryFn: fetchReflections,
    enabled: viewMode === 'reflections'
  })

  const reflections = reflectionsQuery.data ?? []

  // Feedback given on journal entries, newest first (first page of the audit log).
  const feedbackQuery = useQuery({
    queryKey: ['journal-feedback-log', 1],
    queryFn: () => getFeedbackLog(1),
    enabled: viewMode === 'journal'
  })
  const feedbackItems = feedbackQuery.data?.results ?? []
  const feedbackTotal = feedbackQuery.data?.count ?? 0

  // Get all unique themes
  const allThemes = Array.from(
    new Set(
      reflections.flatMap(r => r.scripture_themes || [])
    )
  ).sort()

  // Filter reflections by theme
  const filteredReflections = selectedTheme
    ? reflections.filter(r => r.scripture_themes?.includes(selectedTheme))
    : reflections

  const isLoading = viewMode === 'reflections' ? reflectionsQuery.isLoading : feedbackQuery.isLoading

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            to="/"
            className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
            Back
          </Link>
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-amber-500" />
            <h1 className="text-2xl font-bold text-text-primary">Devotional Insights History</h1>
          </div>
        </div>
      </div>

      {/* View Mode Toggle */}
      <div className="flex gap-2">
        <button
          onClick={() => setViewMode('reflections')}
          className={`px-4 py-2 rounded-lg transition-colors ${
            viewMode === 'reflections'
              ? 'bg-purple-500 text-white'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            Daily Reflections
          </div>
        </button>
        <button
          onClick={() => setViewMode('journal')}
          className={`px-4 py-2 rounded-lg transition-colors ${
            viewMode === 'journal'
              ? 'bg-amber-500 text-white'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            Journal Insights
          </div>
        </button>
      </div>

      {/* Theme Filter */}
      {viewMode === 'reflections' && allThemes.length > 0 && (
        <div className="card">
          <div className="flex items-center gap-2 mb-3">
            <Filter className="w-4 h-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-400">Filter by Theme</span>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedTheme(null)}
              className={`px-3 py-1 rounded-full text-sm transition-colors ${
                selectedTheme === null
                  ? 'bg-purple-500 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              All
            </button>
            {allThemes.map(theme => (
              <button
                key={theme}
                onClick={() => setSelectedTheme(theme)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  selectedTheme === theme
                    ? 'bg-purple-500 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {theme}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-amber-500 animate-spin" />
        </div>
      )}

      {/* Reflections View */}
      {viewMode === 'reflections' && !isLoading && reflectionsQuery.isError && (
        <InlineError error={reflectionsQuery.error} onRetry={() => reflectionsQuery.refetch()} />
      )}
      {viewMode === 'reflections' && !isLoading && !reflectionsQuery.isError && (
        <div className="space-y-4">
          {filteredReflections.length === 0 ? (
            <div className="card text-center py-12">
              <Sparkles className="w-12 h-12 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400">No devotional insights yet</p>
              <p className="text-sm text-gray-500 mt-2">
                Complete daily reflections to build your insights history
              </p>
            </div>
          ) : (
            filteredReflections.map(reflection => (
              <div key={reflection.id} className="card hover:border-purple-500/30 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                      <BookOpen className="w-5 h-5 text-purple-400" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">
                        {formatDay(reflection.date)}
                      </p>
                      {reflection.scripture_reference && (
                        <Link
                          to={`/bible?passage=${encodeURIComponent(reflection.scripture_reference)}`}
                          className="text-amber-400 hover:text-amber-300 font-medium flex items-center gap-1"
                        >
                          {reflection.scripture_reference}
                          <ExternalLink className="w-3 h-3" />
                        </Link>
                      )}
                    </div>
                  </div>
                  {reflection.scripture_themes && reflection.scripture_themes.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {reflection.scripture_themes.slice(0, 3).map(theme => (
                        <span
                          key={theme}
                          className="px-2 py-0.5 bg-purple-500/20 text-purple-300 text-xs rounded"
                        >
                          {theme}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {reflection.ai_insight && (
                  <div className="mt-4 p-4 bg-gray-800/50 rounded-lg border border-purple-500/20">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles className="w-4 h-4 text-amber-400" />
                      <span className="text-sm font-medium text-amber-400">AI Insight</span>
                    </div>
                    <div className="text-gray-300 text-sm whitespace-pre-wrap leading-relaxed">
                      {reflection.ai_insight}
                    </div>
                  </div>
                )}

                <Link
                  to={`/reflection/${reflection.id}`}
                  className="mt-4 text-purple-400 hover:text-purple-300 text-sm flex items-center gap-1"
                >
                  View full reflection
                  <ChevronLeft className="w-4 h-4 rotate-180" />
                </Link>
              </div>
            ))
          )}
        </div>
      )}

      {/* Journal feedback view: one card per entry that has received feedback */}
      {viewMode === 'journal' && !isLoading && feedbackQuery.isError && (
        <InlineError
          error={feedbackQuery.error}
          title={t('insights.feedbackLoadFailed')}
          onRetry={() => feedbackQuery.refetch()}
        />
      )}
      {viewMode === 'journal' && !isLoading && !feedbackQuery.isError && (
        <div className="space-y-4">
          {feedbackItems.length === 0 ? (
            <div className="card text-center py-12">
              <Sparkles className="w-12 h-12 text-text-secondary mx-auto mb-4" aria-hidden="true" />
              <p className="text-text-primary">{t('insights.feedbackEmptyTitle')}</p>
              <p className="text-sm text-text-secondary mt-2">{t('insights.feedbackEmptyBody')}</p>
              <Link to="/journal/new" className="btn-primary inline-block mt-4">
                {t('insights.writeEntry')}
              </Link>
            </div>
          ) : (
            feedbackItems.map((item) => (
              <div key={item.id} className="card">
                <div className="flex items-start gap-3 mb-3">
                  <div className="w-10 h-10 bg-bg-elevated rounded-lg flex items-center justify-center shrink-0">
                    <Calendar className="w-5 h-5 text-accent-primary" aria-hidden="true" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm text-text-secondary">{formatDay(item.entry_date)}</p>
                    {item.scripture?.reference ? (
                      <Link
                        to={`/bible?passage=${encodeURIComponent(item.scripture.reference)}`}
                        className="text-accent-primary hover:underline font-medium inline-flex items-center gap-1"
                      >
                        {item.scripture.reference}
                        <ExternalLink className="w-3 h-3" aria-hidden="true" />
                      </Link>
                    ) : (
                      <p className="text-text-secondary text-sm">{t('insights.noScripture')}</p>
                    )}
                  </div>
                </div>

                {item.reflection && (
                  <p className="text-text-primary text-sm leading-relaxed line-clamp-4">{item.reflection}</p>
                )}

                <Link
                  to={`/journal/${item.entry_id}`}
                  className="mt-4 text-accent-primary hover:underline text-sm inline-flex items-center gap-1"
                >
                  {t('insights.viewEntry')}
                  <ChevronLeft className="w-4 h-4 rotate-180" aria-hidden="true" />
                </Link>
              </div>
            ))
          )}
          {feedbackTotal > feedbackItems.length && (
            <p className="text-sm text-text-secondary text-center">
              {t('insights.showingOf', { shown: feedbackItems.length, total: feedbackTotal })}{' '}
              <Link to="/audit" className="text-accent-primary hover:underline">
                {t('insights.seeAll')}
              </Link>
            </p>
          )}
        </div>
      )}
    </div>
  )
}
