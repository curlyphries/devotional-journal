import { useCallback, type RefObject } from 'react'
import { useTranslation } from 'react-i18next'
import { Mic, MicOff, Square } from 'lucide-react'
import { speechLanguageFor, useSpeechToText } from '../hooks/useSpeechToText'

/**
 * Insert dictated text into `value` at the textarea's cursor (replacing any
 * selection), or at the end when the textarea is not available. Adds the
 * spacing a typist would.
 */
export function insertDictatedText(
  value: string,
  text: string,
  selectionStart?: number | null,
  selectionEnd?: number | null
): { value: string; cursor: number } {
  const start = Math.min(selectionStart ?? value.length, value.length)
  const end = Math.min(Math.max(selectionEnd ?? start, start), value.length)
  const before = value.slice(0, start)
  const after = value.slice(end)
  const lead = before && !/\s$/.test(before) ? ' ' : ''
  const trail = after && !/^[\s.,;:!?]/.test(after) ? ' ' : ''
  const inserted = `${lead}${text}${trail}`
  return { value: before + inserted + after, cursor: before.length + inserted.length }
}

interface DictationButtonProps {
  /** Current text of the field being dictated into. */
  value: string
  onChange: (value: string) => void
  /** The textarea, so text lands at the cursor. Optional: falls back to appending. */
  textareaRef?: RefObject<HTMLTextAreaElement>
  /** Hide the privacy note (e.g. when it is already shown nearby). */
  hidePrivacyNote?: boolean
  className?: string
}

/**
 * Microphone button for voice entry. Speech is turned into text by the
 * browser; this app receives only the text, and only saves it when the user
 * saves the entry.
 */
export default function DictationButton({
  value,
  onChange,
  textareaRef,
  hidePrivacyNote = false,
  className = '',
}: DictationButtonProps) {
  const { t, i18n } = useTranslation()

  const handleFinalText = useCallback(
    (text: string) => {
      const textarea = textareaRef?.current
      // Read the live DOM value: several phrases can arrive before React re-renders.
      const current = textarea ? textarea.value : value
      const focused = textarea && document.activeElement === textarea
      const result = insertDictatedText(
        current,
        text,
        focused ? textarea.selectionStart : null,
        focused ? textarea.selectionEnd : null
      )
      onChange(result.value)
      if (textarea && focused) {
        requestAnimationFrame(() => {
          try {
            textarea.setSelectionRange(result.cursor, result.cursor)
          } catch {
            // The textarea may have unmounted; nothing to restore.
          }
        })
      }
    },
    [onChange, textareaRef, value]
  )

  const { supported, listening, interim, error, toggle } = useSpeechToText({
    lang: speechLanguageFor(i18n.language),
    onFinalText: handleFinalText,
  })

  const label = !supported
    ? t('voice.unsupportedLabel')
    : listening
      ? t('voice.stop')
      : t('voice.start')

  return (
    <div className={className}>
      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={toggle}
          disabled={!supported}
          aria-pressed={listening}
          aria-describedby={!supported ? 'dictation-unsupported' : undefined}
          title={!supported ? t('voice.unsupported') : label}
          className={`inline-flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-accent-primary focus:ring-offset-2 focus:ring-offset-bg-primary disabled:cursor-not-allowed disabled:opacity-60 ${
            listening
              ? 'border-danger bg-danger/20 text-text-primary'
              : 'border-border bg-bg-elevated text-text-primary hover:border-accent-primary'
          }`}
        >
          {!supported ? (
            <MicOff className="h-4 w-4" aria-hidden="true" />
          ) : listening ? (
            <>
              <span className="relative flex h-3 w-3" aria-hidden="true">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75" />
                <span className="relative inline-flex h-3 w-3 rounded-full bg-red-500" />
              </span>
              <Square className="h-3.5 w-3.5" aria-hidden="true" />
            </>
          ) : (
            <Mic className="h-4 w-4" aria-hidden="true" />
          )}
          {label}
        </button>

        {listening && (
          <span className="text-sm text-text-secondary" role="status">
            {t('voice.listening')}
          </span>
        )}
      </div>

      {listening && interim && (
        <p className="mt-2 text-sm italic text-text-secondary/80" aria-hidden="true">
          {interim}…
        </p>
      )}

      {!supported && (
        <p id="dictation-unsupported" className="mt-2 text-xs text-text-secondary">
          {t('voice.unsupported')}
        </p>
      )}

      {error && (
        <p className="mt-2 text-sm text-red-300" role="alert">
          {t(error.messageKey)}
        </p>
      )}

      {supported && !hidePrivacyNote && (
        <p className="mt-2 text-xs leading-relaxed text-text-secondary">{t('voice.privacy')}</p>
      )}
    </div>
  )
}
