import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useInfiniteQuery, useQuery } from '@tanstack/react-query'
import { BookOpen, Cloud, HardDrive, Loader2, PenLine, ScrollText, ShieldCheck } from 'lucide-react'
import { getFeedbackLog, getJournalThemes } from '../api/journal'
import DecisionRecord, { useWhereItRan } from '../components/DecisionRecord'
import InlineError from '../components/InlineError'
import { formatDate } from '../lib/dates'

/** Every scripture the app has given, and the record of how each was chosen. */
export default function AuditLogPage() {
  const { t, i18n } = useTranslation()
  const whereItRan = useWhereItRan()

  const log = useInfiniteQuery({
    queryKey: ['feedbackLog'],
    queryFn: ({ pageParam }) => getFeedbackLog(pageParam),
    initialPageParam: 1,
    getNextPageParam: (lastPage, allPages) => (lastPage.next ? allPages.length + 1 : undefined),
  })

  const themes = useQuery({ queryKey: ['journalThemes'], queryFn: getJournalThemes })

  const items = log.data?.pages.flatMap((page) => page.results) ?? []
  const total = log.data?.pages[0]?.count ?? 0
  const topThemes = (themes.data?.themes ?? []).slice(0, 12)

  return (
    <div className="space-y-6">
      <header>
        <div className="flex items-center gap-2">
          <ScrollText className="w-6 h-6 text-accent-primary" aria-hidden="true" />
          <h1 className="text-2xl font-bold text-text-primary">{t('audit.title')}</h1>
        </div>
        <p className="mt-2 max-w-3xl text-text-secondary leading-relaxed">{t('audit.intro')}</p>
        <p className="mt-2 max-w-3xl text-text-secondary leading-relaxed">
          {t('audit.introPrivacy')}{' '}
          <Link to="/help#feedback" className="text-accent-primary underline-offset-2 hover:underline">
            {t('audit.learnMore')}
          </Link>
        </p>
      </header>

      {/* Themes over time */}
      <section className="card" aria-labelledby="themes-heading">
        <h2 id="themes-heading" className="text-lg font-semibold text-text-primary">{t('audit.themes.title')}</h2>
        {themes.isLoading ? (
          <p className="mt-2 text-sm text-text-secondary" role="status">{t('common.loading')}</p>
        ) : themes.isError ? (
          <InlineError className="mt-3" error={themes.error} title={t('audit.themes.failed')} onRetry={() => themes.refetch()} />
        ) : topThemes.length === 0 ? (
          <p className="mt-2 text-sm text-text-secondary">{t('audit.themes.empty')}</p>
        ) : (
          <>
            <p className="mt-1 text-sm text-text-secondary">
              {t('audit.themes.subtitle', { count: themes.data?.entries_with_feedback ?? 0 })}
            </p>
            <ul className="mt-3 flex flex-wrap gap-2">
              {topThemes.map((theme) => (
                <li
                  key={theme.theme}
                  className="inline-flex items-center gap-2 rounded-full border border-border bg-bg-elevated px-3 py-1 text-sm text-text-primary"
                  title={t('audit.themes.lastSeen', { date: formatDate(theme.last_seen, i18n.language) })}
                >
                  {theme.theme}
                  <span className="rounded-full bg-accent-primary/20 px-1.5 text-xs font-medium text-text-primary">
                    <span className="sr-only">{t('audit.themes.times')} </span>
                    {theme.count}
                  </span>
                </li>
              ))}
            </ul>
          </>
        )}
      </section>

      <section aria-labelledby="decisions-heading" className="space-y-4">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 id="decisions-heading" className="text-lg font-semibold text-text-primary">{t('audit.decisions')}</h2>
          {log.isSuccess && total > 0 && (
            <span className="text-sm text-text-secondary">{t('journal.showing', { shown: items.length, total })}</span>
          )}
        </div>

        {log.isLoading ? (
          <div className="flex items-center justify-center py-12" role="status">
            <Loader2 className="w-8 h-8 text-accent-primary animate-spin" aria-hidden="true" />
            <span className="sr-only">{t('common.loading')}</span>
          </div>
        ) : log.isError && items.length === 0 ? (
          <InlineError error={log.error} title={t('audit.failed')} onRetry={() => log.refetch()} />
        ) : items.length === 0 ? (
          <div className="card text-center py-12">
            <BookOpen className="w-10 h-10 text-text-secondary mx-auto mb-3" aria-hidden="true" />
            <p className="text-text-primary font-medium">{t('audit.emptyTitle')}</p>
            <p className="text-text-secondary mt-1 max-w-md mx-auto">{t('audit.emptyBody')}</p>
            <Link to="/journal/new" className="btn-primary mt-4 inline-flex items-center gap-2">
              <PenLine className="w-4 h-4" aria-hidden="true" />
              {t('audit.writeEntry')}
            </Link>
          </div>
        ) : (
          <ul className="space-y-4">
            {items.map((item) => {
              const where = whereItRan(item)
              const isFallback = item.status === 'fallback'
              return (
                <li key={item.id} className="card space-y-3 p-4 sm:p-6">
                  <div className="flex flex-wrap items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="text-sm text-text-secondary">{formatDate(item.entry_date, i18n.language)}</p>
                      <h3 className="text-lg font-semibold text-text-primary">
                        {item.scripture ? item.scripture.reference : t('audit.noScripture')}
                      </h3>
                      {item.scripture && (
                        <p className="flex flex-wrap items-center gap-2 text-sm text-text-secondary">
                          {item.scripture.translation_name || item.scripture.translation}
                          {item.scripture.verified && (
                            <span className="inline-flex items-center gap-1 text-xs text-text-primary">
                              <ShieldCheck className="w-3.5 h-3.5 text-success" aria-hidden="true" />
                              {t('audit.verified')}
                            </span>
                          )}
                        </p>
                      )}
                    </div>
                    <span
                      className={`rounded-full border px-2.5 py-0.5 text-xs font-medium ${
                        isFallback
                          ? 'border-accent-secondary bg-accent-secondary/15 text-text-primary'
                          : 'border-success bg-success/20 text-text-primary'
                      }`}
                    >
                      {isFallback ? t('audit.status.fallback') : t('audit.status.ok')}
                    </span>
                  </div>

                  {item.themes?.length > 0 && (
                    <ul className="flex flex-wrap gap-2" aria-label={t('feedback.themes')}>
                      {item.themes.map((theme) => (
                        <li key={theme} className="rounded-full border border-border bg-bg-elevated px-2.5 py-0.5 text-xs text-text-primary">
                          {theme}
                        </li>
                      ))}
                    </ul>
                  )}

                  <p className="flex flex-wrap items-center gap-2 text-sm text-text-secondary">
                    {where.noAi || where.local ? (
                      <HardDrive className="w-4 h-4" aria-hidden="true" />
                    ) : (
                      <Cloud className="w-4 h-4" aria-hidden="true" />
                    )}
                    <span className="break-all">{where.engine}</span>
                    <span className="rounded-full border border-border px-2 py-0.5 text-xs">{where.location}</span>
                  </p>

                  <DecisionRecord feedback={item} showLogLink={false} />

                  <Link
                    to={`/journal/${item.entry_id}`}
                    className="inline-block text-sm text-accent-primary underline-offset-2 hover:underline"
                  >
                    {t('audit.viewEntry')}
                  </Link>
                </li>
              )
            })}
          </ul>
        )}

        {log.isError && items.length > 0 && (
          <InlineError error={log.error} title={t('audit.failed')} onRetry={() => log.fetchNextPage()} />
        )}

        {log.hasNextPage && !log.isError && (
          <div className="flex justify-center">
            <button
              type="button"
              className="btn-secondary inline-flex items-center gap-2"
              onClick={() => log.fetchNextPage()}
              disabled={log.isFetchingNextPage}
            >
              {log.isFetchingNextPage && <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />}
              {log.isFetchingNextPage ? t('common.loading') : t('journal.loadMore')}
            </button>
          </div>
        )}
      </section>
    </div>
  )
}
