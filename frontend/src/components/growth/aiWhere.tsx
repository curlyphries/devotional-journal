import { useTranslation } from 'react-i18next'
import { Cloud, HardDrive } from 'lucide-react'
import { useAiStatus } from '../../hooks/useAiStatus'

/**
 * One sentence saying where an AI request made now would run — on the person's
 * own network or at a cloud provider — so they know before they press the button.
 */
export function useAiWhereSentence(): string {
  const { t } = useTranslation()
  const { data: status } = useAiStatus()
  if (!status || !status.configured) return t('growth.ai.whereUnknown')
  const engine = [status.backend, status.model].filter(Boolean).join(' · ')
  return status.local ? t('growth.ai.whereLocal', { engine }) : t('growth.ai.whereCloud', { engine })
}

interface AiRanLineProps {
  provider: string
  model: string
  local: boolean
  className?: string
}

/** "ollama · llama3.1 · on your network": where a finished piece of AI writing was produced. */
export function AiRanLine({ provider, model, local, className = '' }: AiRanLineProps) {
  const { t } = useTranslation()
  const engine = [provider, model].filter(Boolean).join(' · ')
  return (
    <p className={`flex flex-wrap items-center gap-2 text-sm text-text-primary ${className}`}>
      {local ? (
        <HardDrive className="h-4 w-4 text-text-secondary" aria-hidden="true" />
      ) : (
        <Cloud className="h-4 w-4 text-text-secondary" aria-hidden="true" />
      )}
      <span className="sr-only">{t('audit.record.where')}: </span>
      <span className="break-all">{engine || t('growth.ai.unknownEngine')}</span>
      <span className="rounded-full border border-border px-2 py-0.5 text-xs text-text-secondary">
        {local ? t('audit.local') : t('audit.cloud')}
      </span>
    </p>
  )
}
