import { useId, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useInfiniteQuery } from '@tanstack/react-query'
import { Plus, Filter, Loader2, Book, BookOpen, Lightbulb, MessageSquareText, ScrollText } from 'lucide-react'
import { getJournalEntriesPage } from '../api/journal'
import InlineError from '../components/InlineError'
import { parseJournalContent } from '../lib/journalContent'
import { MOODS, getMood, moodLabelKey } from '../lib/moods'
import { formatDate } from '../lib/dates'

export default function JournalHistoryPage() {
  const { t, i18n } = useTranslation()
  const [filterMood, setFilterMood] = useState('')
  const filterId = useId()

  const query = useInfiniteQuery({
    queryKey: ['journalEntries', 'history', filterMood],
    queryFn: ({ pageParam }) =>
      getJournalEntriesPage({ page: pageParam, ...(filterMood ? { mood: filterMood } : {}) }),
    initialPageParam: 1,
    getNextPageParam: (lastPage, allPages) => (lastPage.next ? allPages.length + 1 : undefined),
  })

  const entries = query.data?.pages.flatMap((page) => page.results) ?? []
  const total = query.data?.pages[0]?.count ?? 0

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold text-text-primary">{t('journal.history')}</h1>

        <div className="flex flex-wrap items-center gap-3">
          <Link to="/audit" className="btn-secondary flex items-center gap-2 text-sm">
            <ScrollText className="w-4 h-4" aria-hidden="true" />
            {t('audit.navLabel')}
          </Link>
          <Link to="/journal/new" className="btn-primary flex items-center gap-2">
            <Plus className="w-4 h-4" aria-hidden="true" />
            {t('journal.newEntry')}
          </Link>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <label htmlFor={filterId} className="flex items-center gap-2 text-text-secondary text-sm">
          <Filter className="w-4 h-4" aria-hidden="true" />
          {t('journal.filterByMood')}
        </label>
        <select
          id={filterId}
          value={filterMood}
          onChange={(e) => setFilterMood(e.target.value)}
          className="input py-1 px-3"
        >
          <option value="">{t('journal.allMoods')}</option>
          {MOODS.map((mood) => (
            <option key={mood.id} value={mood.id}>
              {t(moodLabelKey(mood.id))}
            </option>
          ))}
        </select>
        {query.isSuccess && total > 0 && (
          <span className="text-sm text-text-secondary">{t('journal.showing', { shown: entries.length, total })}</span>
        )}
      </div>

      <div className="space-y-4">
        {query.isLoading ? (
          <div className="flex items-center justify-center py-12" role="status">
            <Loader2 className="w-8 h-8 text-accent-primary animate-spin" aria-hidden="true" />
            <span className="sr-only">{t('common.loading')}</span>
          </div>
        ) : query.isError && entries.length === 0 ? (
          <InlineError error={query.error} title={t('journal.listFailed')} onRetry={() => query.refetch()} />
        ) : entries.length === 0 ? (
          <div className="card text-center py-12">
            <BookOpen className="w-10 h-10 text-text-secondary mx-auto mb-3" aria-hidden="true" />
            <p className="text-text-primary font-medium">
              {filterMood ? t('journal.noEntriesForMood') : t('journal.emptyTitle')}
            </p>
            {!filterMood && <p className="text-text-secondary mt-1 max-w-md mx-auto">{t('journal.emptyBody')}</p>}
            {filterMood ? (
              <button type="button" className="btn-secondary mt-4" onClick={() => setFilterMood('')}>
                {t('journal.clearFilter')}
              </button>
            ) : (
              <Link to="/journal/new" className="btn-primary mt-4 inline-flex items-center gap-2">
                <Plus className="w-4 h-4" aria-hidden="true" />
                {t('journal.firstEntry')}
              </Link>
            )}
          </div>
        ) : (
          <ul className="space-y-4">
            {entries.map((entry) => {
              // The server strips metadata from previews; parse anyway so an
              // older server (or a legacy entry) never leaks a raw block.
              const parsed = parseJournalContent(entry.content_preview || '')
              const mood = getMood(entry.mood_tag)

              return (
                <li key={entry.id}>
                  <Link
                    to={`/journal/${entry.id}`}
                    className="card block hover:border-accent-secondary transition-colors focus:outline-none focus:ring-2 focus:ring-accent-primary"
                  >
                    <div className="flex items-start justify-between gap-3 mb-3">
                      <div className="min-w-0">
                        <span className="text-sm text-text-secondary">
                          {formatDate(entry.date, i18n.language, {
                            weekday: 'long',
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                          })}
                        </span>

                        {parsed.planTitle && (
                          <div className="flex flex-wrap items-center gap-2 mt-1 text-xs">
                            <Book className="w-3 h-3 text-accent-primary" aria-hidden="true" />
                            <span className="text-accent-primary">
                              {parsed.planTitle}
                              {parsed.dayNumber ? ` • ${t('journal.day', { day: parsed.dayNumber })}` : ''}
                            </span>
                            {parsed.passage && <span className="text-text-secondary">• {parsed.passage}</span>}
                          </div>
                        )}

                        {parsed.theme && (
                          <div className="flex items-center gap-1 mt-1">
                            <Lightbulb className="w-3 h-3 text-text-secondary" aria-hidden="true" />
                            <span className="text-text-secondary text-xs italic">{parsed.theme}</span>
                          </div>
                        )}
                      </div>

                      {mood && (
                        <span className={`text-xs px-2 py-1 rounded flex-shrink-0 ${mood.badgeClass}`}>
                          <span aria-hidden="true">{mood.emoji}</span> {t(moodLabelKey(mood.id))}
                        </span>
                      )}
                    </div>

                    <p className="text-text-primary line-clamp-2 break-words">
                      {parsed.userContent || t('journal.noPreview')}
                    </p>

                    {(entry.scripture_reference || entry.has_feedback) && (
                      <div className="flex flex-wrap items-center gap-2 mt-3">
                        {entry.scripture_reference && (
                          <span className="inline-flex items-center gap-1.5 rounded-full border border-accent-secondary px-2.5 py-0.5 text-xs text-text-primary">
                            <BookOpen className="w-3 h-3 text-accent-primary" aria-hidden="true" />
                            {entry.scripture_reference}
                          </span>
                        )}
                        {entry.has_feedback && (
                          <span className="inline-flex items-center gap-1.5 rounded-full border border-border px-2.5 py-0.5 text-xs text-text-secondary">
                            <MessageSquareText className="w-3 h-3" aria-hidden="true" />
                            {t('journal.hasFeedback')}
                          </span>
                        )}
                      </div>
                    )}
                  </Link>
                </li>
              )
            })}
          </ul>
        )}

        {query.isError && entries.length > 0 && (
          <InlineError error={query.error} title={t('journal.moreFailed')} onRetry={() => query.fetchNextPage()} />
        )}

        {query.hasNextPage && !query.isError && (
          <div className="flex justify-center">
            <button
              type="button"
              className="btn-secondary inline-flex items-center gap-2"
              onClick={() => query.fetchNextPage()}
              disabled={query.isFetchingNextPage}
            >
              {query.isFetchingNextPage && <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />}
              {query.isFetchingNextPage ? t('common.loading') : t('journal.loadMore')}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
