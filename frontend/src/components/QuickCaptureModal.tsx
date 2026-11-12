import { useEffect, useId, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { X, Save, Loader2, Sparkles } from 'lucide-react'
import { createJournalEntry, type CreateJournalEntry } from '../api/journal'
import { toApiError } from '../api/errors'
import { buildJournalContent } from '../lib/journalContent'
import { MOODS, moodLabelKey } from '../lib/moods'
import { todayLocalISO } from '../lib/dates'
import { useDialogFocus } from '../hooks/useDialogFocus'
import { useToast } from './Toast'
import DictationButton from './DictationButton'

interface QuickCaptureModalProps {
  isOpen: boolean
  onClose: () => void
  activeFocus?: {
    intention: string
    themes: string[]
  }
}

/**
 * Jot (or dictate) a thought from anywhere in the app. Saving creates a
 * journal entry and opens it so the feedback and scripture are shown.
 */
export default function QuickCaptureModal({ isOpen, onClose, activeFocus }: QuickCaptureModalProps) {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const toast = useToast()
  const titleId = useId()
  const textId = useId()
  const moodLabelId = useId()
  const dialogRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const [content, setContent] = useState('')
  const [selectedMood, setSelectedMood] = useState('')

  const createMutation = useMutation({
    mutationFn: (data: CreateJournalEntry) => createJournalEntry(data),
    onSuccess: (entry) => {
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      queryClient.invalidateQueries({ queryKey: ['profile'] })
      setContent('')
      setSelectedMood('')
      toast.success(t('journal.saved'))
      onClose()
      navigate(`/journal/${entry.id}?feedback=1`)
    },
    onError: (err) => toast.fromError(err, t('journal.saveFailed')),
  })

  const isSaving = createMutation.isPending
  // The text stays in the box if the dialog is dismissed, so nothing typed is lost.
  useDialogFocus(dialogRef, isOpen, isSaving ? undefined : onClose)

  useEffect(() => {
    if (isOpen) textareaRef.current?.focus()
  }, [isOpen])

  const { reset } = createMutation
  useEffect(() => {
    if (!isOpen) reset()
  }, [isOpen, reset])

  const handleSave = () => {
    if (!content.trim() || isSaving) return

    // Tag with the active focus, if there is one.
    const meta = activeFocus
      ? { focus_intention: activeFocus.intention, focus_themes: activeFocus.themes, capture_type: 'quick' }
      : { capture_type: 'quick' }

    createMutation.mutate({
      date: todayLocalISO(),
      content: buildJournalContent(meta, content.trim()),
      mood_tag: selectedMood || undefined,
    })
  }

  if (!isOpen) return null

  const saveError = createMutation.isError ? toApiError(createMutation.error) : null

  return (
    <div
      className="fixed inset-0 bg-black/60 flex items-end sm:items-center justify-center z-50 p-0 sm:p-4"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget && !isSaving) onClose()
      }}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        tabIndex={-1}
        className="bg-bg-surface rounded-t-2xl sm:rounded-2xl border border-border w-full max-w-lg shadow-2xl max-h-[95vh] overflow-y-auto focus:outline-none"
      >
        <div className="flex items-center justify-between p-4 border-b border-border">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-accent-primary" aria-hidden="true" />
            <h2 id={titleId} className="text-lg font-semibold text-text-primary">{t('journal.quick.title')}</h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-2 hover:bg-bg-elevated rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-accent-primary"
            aria-label={t('common.close')}
          >
            <X className="w-5 h-5 text-text-secondary" aria-hidden="true" />
          </button>
        </div>

        <div className="p-4 space-y-4">
          {activeFocus && (
            <div className="bg-bg-elevated border border-border rounded-lg p-3">
              <p className="text-text-secondary text-xs font-medium uppercase tracking-wider mb-1">
                {t('journal.quick.taggedWithFocus')}
              </p>
              <p className="text-text-primary text-sm">{activeFocus.intention}</p>
            </div>
          )}

          <div>
            <label htmlFor={textId} className="block text-sm font-medium text-text-primary mb-2">
              {t('journal.quick.label')}
            </label>
            <textarea
              id={textId}
              ref={textareaRef}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder={t('journal.quick.placeholder')}
              className="input w-full resize-y font-serif"
              rows={4}
            />
            <DictationButton className="mt-3" value={content} onChange={setContent} textareaRef={textareaRef} />
          </div>

          <div>
            <p id={moodLabelId} className="text-sm text-text-secondary mb-2">{t('journal.moodQuestion')}</p>
            <div className="flex flex-wrap gap-2" role="group" aria-labelledby={moodLabelId}>
              {MOODS.map((mood) => (
                <button
                  key={mood.id}
                  type="button"
                  aria-label={t(moodLabelKey(mood.id))}
                  title={t(moodLabelKey(mood.id))}
                  aria-pressed={selectedMood === mood.id}
                  onClick={() => setSelectedMood(selectedMood === mood.id ? '' : mood.id)}
                  className={`px-3 py-2 rounded-lg border transition-colors focus:outline-none focus:ring-2 focus:ring-accent-primary ${
                    selectedMood === mood.id
                      ? 'border-accent-primary bg-accent-primary/20'
                      : 'border-border hover:border-text-secondary'
                  }`}
                >
                  <span aria-hidden="true">{mood.emoji}</span>
                </button>
              ))}
            </div>
          </div>

          {saveError && (
            <div role="alert" className="rounded-lg border border-danger bg-danger/10 p-3 text-sm">
              <p className="font-medium text-text-primary">{t('journal.saveFailed')}</p>
              <p className="text-text-primary">{saveError.message}</p>
              {saveError.suggestion && <p className="text-text-secondary">{saveError.suggestion}</p>}
              <p className="mt-1 text-xs font-mono text-text-secondary">
                {saveError.code}
                {saveError.requestId ? ` · ${saveError.requestId}` : ''}
              </p>
            </div>
          )}

          <p className="text-xs text-text-secondary">{t('journal.afterSaveHint')}</p>
        </div>

        <div className="flex gap-3 p-4 border-t border-border">
          <button type="button" onClick={onClose} disabled={isSaving} className="btn-secondary flex-1">
            {t('journal.quick.later')}
          </button>
          <button
            type="button"
            onClick={handleSave}
            disabled={isSaving || !content.trim()}
            className="btn-primary flex-1 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {isSaving ? (
              <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
            ) : (
              <Save className="w-4 h-4" aria-hidden="true" />
            )}
            {isSaving ? t('journal.saving') : t('common.save')}
          </button>
        </div>
      </div>
    </div>
  )
}
