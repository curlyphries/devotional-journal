import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ChevronRight, Cloud, HardDrive, ListChecks } from 'lucide-react'
import type { JournalFeedback } from '../api/journal'
import { formatDateTime } from '../lib/dates'

const KNOWN_INPUTS = [
  'entry_text', 'mood', 'active_focus', 'recent_themes', 'open_threads', 'recent_passages',
  'life_stage', 'growth_focus', 'entry_date', 'language',
]
const KNOWN_OUTCOMES = ['selected', 'not_found', 'not_used', 'invalid']

const OUTCOME_CLASS: Record<string, string> = {
  selected: 'bg-success/25 text-text-primary border-success',
  not_found: 'bg-danger/20 text-text-primary border-danger',
  invalid: 'bg-danger/20 text-text-primary border-danger',
  not_used: 'bg-bg-elevated text-text-secondary border-border',
}

function humanize(value: string): string {
  return value.replace(/[_-]+/g, ' ')
}

/** "Ollama · llama3.1:8b", or a plain sentence when no AI was involved. */
export function useWhereItRan() {
  const { t } = useTranslation()
  return (feedback: Pick<JournalFeedback, 'status' | 'audit'>) => {
    const { provider, model, local } = feedback.audit
    const noAi = !provider || provider === 'none'
    return {
      noAi,
      local,
      engine: noAi ? t('audit.noAi') : [provider, model].filter(Boolean).join(' · '),
      location: noAi ? t('audit.onServer') : local ? t('audit.local') : t('audit.cloud'),
    }
  }
}

interface DecisionRecordProps {
  feedback: JournalFeedback
  /** Show the "See all decisions" link (hidden on the audit page itself). */
  showLogLink?: boolean
  defaultOpen?: boolean
}

/**
 * Expandable record of how a scripture was chosen: where the AI ran, what it
 * was given, every passage it suggested and what happened to each.
 */
export default function DecisionRecord({ feedback, showLogLink = true, defaultOpen = false }: DecisionRecordProps) {
  const { t, i18n } = useTranslation()
  const whereItRan = useWhereItRan()
  const { audit } = feedback
  const where = whereItRan(feedback)
  const candidates = audit.candidates ?? []
  const inputs = audit.inputs_used ?? []
  const recentThemes = audit.recent_themes ?? []
  const threads = audit.threads_detected ?? []

  const inputLabel = (input: string) =>
    KNOWN_INPUTS.includes(input) ? t(`audit.inputs.${input}`) : humanize(input)
  const outcomeLabel = (outcome: string) =>
    KNOWN_OUTCOMES.includes(outcome) ? t(`audit.outcomes.${outcome}`) : humanize(outcome)

  return (
    <details className="group rounded-xl border border-border bg-bg-elevated/40" open={defaultOpen}>
      <summary className="flex cursor-pointer list-none items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium text-text-primary hover:bg-bg-elevated focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary [&::-webkit-details-marker]:hidden">
        <ChevronRight className="h-4 w-4 flex-shrink-0 text-text-secondary transition-transform group-open:rotate-90" aria-hidden="true" />
        <ListChecks className="h-4 w-4 flex-shrink-0 text-accent-primary" aria-hidden="true" />
        <span>{t('audit.record.summary')}</span>
      </summary>

      <div className="space-y-5 border-t border-border px-4 py-4 text-sm">
        <section>
          <h4 className="mb-1 text-xs font-semibold uppercase tracking-wider text-text-secondary">
            {t('audit.record.where')}
          </h4>
          <p className="flex flex-wrap items-center gap-2 text-text-primary">
            {where.noAi || where.local ? (
              <HardDrive className="h-4 w-4 text-text-secondary" aria-hidden="true" />
            ) : (
              <Cloud className="h-4 w-4 text-text-secondary" aria-hidden="true" />
            )}
            <span className="break-all">{where.engine}</span>
            <span className="rounded-full border border-border px-2 py-0.5 text-xs text-text-secondary">
              {where.location}
            </span>
          </p>
          <p className="mt-1 text-xs text-text-secondary">
            {where.noAi
              ? t('audit.record.whereNoAi')
              : where.local
                ? t('audit.record.whereLocal')
                : t('audit.record.whereCloud')}
          </p>
        </section>

        {audit.fallback_reason && (
          <section>
            <h4 className="mb-1 text-xs font-semibold uppercase tracking-wider text-text-secondary">
              {t('audit.record.fallback')}
            </h4>
            <p className="text-text-primary">{audit.fallback_reason.message}</p>
            <p className="text-xs text-text-secondary">
              {audit.fallback_reason.code}
            </p>
          </section>
        )}

        <section>
          <h4 className="mb-1 text-xs font-semibold uppercase tracking-wider text-text-secondary">
            {t('audit.record.inputs')}
          </h4>
          {inputs.length > 0 ? (
            <ul className="flex flex-wrap gap-2">
              {inputs.map((input) => (
                <li key={input} className="rounded-full border border-border px-2.5 py-0.5 text-xs text-text-primary">
                  {inputLabel(input)}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-text-secondary">{t('audit.record.none')}</p>
          )}
        </section>

        {recentThemes.length > 0 && (
          <section>
            <h4 className="mb-1 text-xs font-semibold uppercase tracking-wider text-text-secondary">
              {t('audit.record.recentThemes')}
            </h4>
            <p className="text-text-primary">{recentThemes.join(', ')}</p>
          </section>
        )}

        <section>
          <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-text-secondary">
            {t('audit.record.candidates')}
          </h4>
          {candidates.length > 0 ? (
            <ol className="space-y-2">
              {candidates.map((candidate, index) => (
                <li key={`${candidate.reference}-${index}`} className="rounded-lg border border-border bg-bg-surface p-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="font-medium text-text-primary">{candidate.reference}</span>
                    <span
                      className={`rounded-full border px-2 py-0.5 text-xs ${OUTCOME_CLASS[candidate.outcome] ?? OUTCOME_CLASS.not_used}`}
                    >
                      {outcomeLabel(candidate.outcome)}
                    </span>
                  </div>
                  {candidate.reason && <p className="mt-1 text-text-secondary">{candidate.reason}</p>}
                </li>
              ))}
            </ol>
          ) : (
            <p className="text-text-secondary">{t('audit.record.noCandidates')}</p>
          )}
        </section>

        {audit.selection_rule && (
          <section>
            <h4 className="mb-1 text-xs font-semibold uppercase tracking-wider text-text-secondary">
              {t('audit.record.rule')}
            </h4>
            <p className="text-text-primary">{audit.selection_rule}</p>
          </section>
        )}

        {threads.length > 0 && (
          <section>
            <h4 className="mb-1 text-xs font-semibold uppercase tracking-wider text-text-secondary">
              {t('audit.record.threads')}
            </h4>
            <ul className="space-y-1">
              {threads.map((thread, index) => (
                <li key={index} className="text-text-primary">
                  <span className="text-text-secondary">{humanize(thread.type)}: </span>
                  {thread.summary}
                </li>
              ))}
            </ul>
          </section>
        )}

        <dl className="grid grid-cols-1 gap-x-6 gap-y-2 text-xs sm:grid-cols-3">
          <div>
            <dt className="text-text-secondary">{t('audit.record.duration')}</dt>
            <dd className="text-text-primary">
              {t('audit.record.seconds', { seconds: (Math.max(0, audit.duration_ms ?? 0) / 1000).toFixed(1) })}
            </dd>
          </div>
          <div>
            <dt className="text-text-secondary">{t('audit.record.promptVersion')}</dt>
            <dd className="break-all text-text-primary">{audit.prompt_version || '—'}</dd>
          </div>
          <div>
            <dt className="text-text-secondary">{t('audit.record.generatedAt')}</dt>
            <dd className="text-text-primary">{formatDateTime(feedback.created_at, i18n.language)}</dd>
          </div>
        </dl>

        {showLogLink && (
          <p>
            <Link to="/audit" className="text-accent-primary underline-offset-2 hover:underline">
              {t('audit.record.seeAll')}
            </Link>
          </p>
        )}
      </div>
    </details>
  )
}
