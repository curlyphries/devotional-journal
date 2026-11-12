import { useEffect, useId, useMemo, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate, useParams, useSearchParams, Link } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  ChevronLeft, Save, Trash2, Book, Lightbulb, Loader2, ExternalLink, Highlighter,
  Sparkles, MessageSquare, Target, X,
} from 'lucide-react'
import {
  createJournalEntry, updateJournalEntry, deleteJournalEntry, getJournalEntry, generateJournalDeepDive,
  type CreateJournalEntry,
} from '../api/journal'
import { getHighlights, VerseHighlight } from '../api/highlights'
import { getPassage, Verse } from '../api/bible'
import { getActiveFocusIntentions } from '../api/devotional'
import type { StudyGuide } from '../api/devotional'
import client from '../api/client'
import ThreadPromptCard from '../components/ThreadPromptCard'
import JournalFeedbackPanel from '../components/JournalFeedbackPanel'
import DictationButton from '../components/DictationButton'
import InlineError from '../components/InlineError'
import ConfirmDialog from '../components/ConfirmDialog'
import { useToast } from '../components/Toast'
import { buildJournalContent, parseJournalContent, type JournalMeta } from '../lib/journalContent'
import { MOODS, moodLabelKey } from '../lib/moods'
import { formatDate, todayLocalISO } from '../lib/dates'

const HIGHLIGHT_COLORS: Record<string, string> = {
  yellow: 'rgba(234, 179, 8, 0.3)',
  green: 'rgba(34, 197, 94, 0.3)',
  blue: 'rgba(59, 130, 246, 0.3)',
  pink: 'rgba(236, 72, 153, 0.3)',
  orange: 'rgba(249, 115, 22, 0.3)',
}

const PUBLIC_DOMAIN_TRANSLATIONS = ['KJV', 'ASV', 'WEB', 'YLT', 'DBY', 'WBT']

const isPublicDomainTranslation = (code: string): boolean =>
  PUBLIC_DOMAIN_TRANSLATIONS.includes(code.toUpperCase())

function parsePassageReference(ref: string): { book: string; chapter: number } | null {
  const match = ref.match(/^(\w+)\s*(\d+)/)
  if (match) {
    return { book: match[1].toUpperCase(), chapter: parseInt(match[2], 10) }
  }
  return null
}

function metaText(meta: JournalMeta, key: string): string | undefined {
  const value = meta[key]
  if (typeof value === 'string' && value.trim()) return value
  if (typeof value === 'number') return String(value)
  return undefined
}

/**
 * Write a new entry (`/journal/new`) or view and edit a saved one
 * (`/journal/:entryId`). Saved entries show their feedback underneath;
 * `?feedback=1` (set right after saving) generates it straight away.
 */
export default function JournalPage() {
  const { entryId } = useParams()
  // Both routes render this component; the key gives each entry fresh state.
  return <JournalEditor key={entryId ?? 'new'} entryId={entryId} />
}

function JournalEditor({ entryId }: { entryId?: string }) {
  const { t, i18n } = useTranslation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const toast = useToast()
  const [searchParams] = useSearchParams()
  const isEditing = !!entryId
  const dateId = useId()
  const textId = useId()
  const moodLabelId = useId()
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Context handed over by the Bible reader / reading plan when starting a new entry.
  const passageContext = useMemo(
    () => ({
      passage: searchParams.get('passage'),
      theme: searchParams.get('theme'),
      planTitle: searchParams.get('planTitle'),
      dayNumber: searchParams.get('dayNumber'),
      aiInsight: searchParams.get('aiInsight'),
      translation: searchParams.get('translation') || 'KJV',
    }),
    [searchParams]
  )
  const autoGenerateFeedback = searchParams.get('feedback') === '1'

  const [date, setDate] = useState(todayLocalISO())
  const [text, setText] = useState('')
  const [selectedMood, setSelectedMood] = useState('')
  // Metadata stored with a saved entry — kept whole so nothing is dropped on re-save.
  const [savedMeta, setSavedMeta] = useState<JournalMeta>({})
  const [savedText, setSavedText] = useState('')
  const [entryChanged, setEntryChanged] = useState(false)
  const [confirmDelete, setConfirmDelete] = useState(false)
  const [highlightInsight, setHighlightInsight] = useState('')
  const [highlightError, setHighlightError] = useState<unknown>(null)
  const [loadingHighlightInsight, setLoadingHighlightInsight] = useState(false)
  const [showDeepDive, setShowDeepDive] = useState(false)

  const entryQuery = useQuery({
    queryKey: ['journalEntry', entryId],
    queryFn: () => getJournalEntry(entryId!),
    enabled: isEditing,
    retry: false,
  })

  // Fill the editor once, when the entry first arrives. Later refetches must
  // not overwrite what the user is typing.
  const loadedRef = useRef(false)
  useEffect(() => {
    const entry = entryQuery.data
    if (!entry || loadedRef.current) return
    loadedRef.current = true
    const parsed = parseJournalContent(entry.decrypted_content || '')
    setDate(entry.date)
    setText(parsed.userContent)
    setSavedText(parsed.userContent)
    setSavedMeta(parsed.meta)
    setSelectedMood(entry.mood_tag || '')
  }, [entryQuery.data])

  const parsedRef = !isEditing && passageContext.passage ? parsePassageReference(passageContext.passage) : null

  const { data: highlights = [] } = useQuery({
    queryKey: ['highlights', parsedRef?.book, parsedRef?.chapter],
    queryFn: () => getHighlights({ book: parsedRef!.book, chapter: parsedRef!.chapter }),
    enabled: !!parsedRef,
  })

  const { data: passageData } = useQuery({
    queryKey: ['passage', parsedRef?.book, parsedRef?.chapter],
    queryFn: () => getPassage(parsedRef!.book, parsedRef!.chapter, 'KJV'),
    enabled: !!parsedRef,
  })

  const { data: activeFocus = [] } = useQuery({
    queryKey: ['activeFocus'],
    queryFn: getActiveFocusIntentions,
    staleTime: 5 * 60 * 1000,
  })

  const { data: pendingPrompts = [] } = useQuery({
    queryKey: ['pendingThreadPrompts'],
    queryFn: async () => {
      const response = await client.get('/thread-prompts/pending/')
      const data = response.data
      return Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : []
    },
    staleTime: 0,
    enabled: !isEditing,
  })

  // What is shown in the context banners: stored metadata for a saved entry,
  // the URL context for a new one.
  const display = isEditing
    ? {
        planTitle: metaText(savedMeta, 'planTitle'),
        dayNumber: metaText(savedMeta, 'dayNumber'),
        theme: metaText(savedMeta, 'theme'),
        passage: metaText(savedMeta, 'passage'),
        aiInsight: metaText(savedMeta, 'aiInsight'),
      }
    : {
        planTitle: passageContext.planTitle || undefined,
        dayNumber: passageContext.dayNumber || undefined,
        theme: passageContext.theme || undefined,
        passage: passageContext.passage || undefined,
        aiInsight: passageContext.aiInsight || undefined,
      }

  const getVerseText = (verseNum: number): string => {
    if (!passageData?.verses) return ''
    const verse = passageData.verses.find((v: Verse) => v.verse === verseNum)
    return verse?.text || ''
  }

  const generateHighlightInsight = async () => {
    if (highlights.length === 0 || !passageData) return

    setLoadingHighlightInsight(true)
    setHighlightError(null)
    try {
      const highlightContext = highlights.map((h: VerseHighlight) => {
        const verseText = getVerseText(h.verse_start)
        return `Verse ${h.verse_start}: "${verseText}"${h.note ? ` (User's note: "${h.note}")` : ''}`
      }).join('\n\n')

      const focusContext = activeFocus.length > 0
        ? `\n\nIMPORTANT - The reader has set a personal spiritual focus: "${activeFocus[0].intention_text}". Their focus themes include: ${activeFocus[0].themes.join(', ')}. Please connect these highlighted verses to their personal focus.`
        : ''

      const prompt = `Based on these highlighted verses from ${passageContext.passage} and the user's personal notes, provide a thoughtful reflection that:
1. Connects the themes across the highlighted verses
2. Incorporates the user's notes and observations
3. Suggests how these insights might apply to daily life
4. Offers a brief prayer or meditation prompt
${activeFocus.length > 0 ? '5. Include a "Connection to Your Focus" section' : ''}

Highlighted verses and notes:
${highlightContext}

${passageContext.theme ? `Today's theme: "${passageContext.theme}"` : ''}${focusContext}`

      const response = await client.post(
        '/crew/ask-agent/',
        {
          agent: 'scripture',
          prompt,
          context: {
            passage: passageContext.passage,
            theme: passageContext.theme,
            highlights: highlights.length,
            userFocus: activeFocus.length > 0 ? activeFocus[0].intention_text : null,
            focusThemes: activeFocus.length > 0 ? activeFocus[0].themes : [],
          },
        },
        { timeout: 120_000 }
      )
      setHighlightInsight(response.data.response)
    } catch (err) {
      setHighlightError(err)
    } finally {
      setLoadingHighlightInsight(false)
    }
  }

  const invalidateLists = () => {
    queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
    queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
    queryClient.invalidateQueries({ queryKey: ['profile'] })
  }

  const createMutation = useMutation({
    mutationFn: (data: CreateJournalEntry) => createJournalEntry(data),
    onSuccess: (entry) => {
      invalidateLists()
      toast.success(t('journal.saved'))
      // Stay with the entry so the user sees their feedback and scripture.
      navigate(`/journal/${entry.id}?feedback=1`, { replace: true })
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof updateJournalEntry>[1] }) =>
      updateJournalEntry(id, data),
    onSuccess: () => {
      invalidateLists()
      queryClient.invalidateQueries({ queryKey: ['journalEntry', entryId] })
      toast.success(t('journal.saved'))
      if (text.trim() !== savedText.trim()) setEntryChanged(true)
      setSavedText(text)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteJournalEntry(id),
    onSuccess: () => {
      invalidateLists()
      queryClient.removeQueries({ queryKey: ['journalEntry', entryId] })
      toast.success(t('journal.deleted'))
      navigate('/journal', { replace: true })
    },
    onError: (err) => {
      setConfirmDelete(false)
      toast.fromError(err, t('journal.deleteFailed'))
    },
  })

  const deepDiveMutation = useMutation<StudyGuide, unknown, void>({
    mutationFn: () => generateJournalDeepDive(entryId!),
  })
  const deepDiveGuide = deepDiveMutation.data ?? null

  const handleSave = () => {
    if (!text.trim()) return

    if (isEditing && entryId) {
      updateMutation.mutate({
        id: entryId,
        data: {
          date,
          // Whatever metadata the entry was saved with goes back unchanged.
          content: buildJournalContent(savedMeta, text),
          mood_tag: selectedMood || undefined,
        },
      })
      return
    }

    const meta: JournalMeta = passageContext.passage
      ? {
          planTitle: passageContext.planTitle,
          dayNumber: passageContext.dayNumber,
          theme: passageContext.theme,
          passage: passageContext.passage,
          aiInsight: passageContext.aiInsight,
          highlights: highlights.map((h: VerseHighlight) => ({ verse: h.verse_start, note: h.note || null })),
        }
      : {}

    createMutation.mutate({
      date,
      content: buildJournalContent(meta, text),
      mood_tag: selectedMood || undefined,
    })
  }

  const openDeepDive = () => {
    if (!entryId) return
    setShowDeepDive(true)
    deepDiveMutation.reset()
    deepDiveMutation.mutate()
  }

  const closeDeepDive = () => {
    setShowDeepDive(false)
    deepDiveMutation.reset()
  }

  // Esc closes the study-guide dialog.
  useEffect(() => {
    if (!showDeepDive) return
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setShowDeepDive(false)
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [showDeepDive])

  const isSaving = createMutation.isPending || updateMutation.isPending
  const saveError = createMutation.error ?? updateMutation.error
  const isDirty = isEditing && text !== savedText

  const backButton = (
    <button
      type="button"
      onClick={() => (isEditing ? navigate('/journal') : navigate(-1))}
      className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
    >
      <ChevronLeft className="w-5 h-5" aria-hidden="true" />
      {t('common.back')}
    </button>
  )

  if (isEditing && entryQuery.isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]" role="status">
        <Loader2 className="w-8 h-8 text-accent-primary animate-spin" aria-hidden="true" />
        <span className="sr-only">{t('common.loading')}</span>
      </div>
    )
  }

  // A failed load must never fall through to an empty editor: saving that
  // would overwrite the real entry.
  if (isEditing && (entryQuery.isError || !entryQuery.data)) {
    return (
      <div className="space-y-6">
        {backButton}
        <InlineError
          error={entryQuery.error ?? new Error(t('journal.loadFailed'))}
          title={t('journal.loadFailed')}
          onRetry={() => entryQuery.refetch()}
        />
        <p className="text-sm text-text-secondary">
          <Link to="/journal" className="text-accent-primary hover:underline">{t('journal.backToHistory')}</Link>
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-3">
        {backButton}

        {isEditing && (
          <button
            type="button"
            onClick={() => setConfirmDelete(true)}
            disabled={deleteMutation.isPending}
            className="flex items-center gap-2 text-red-300 hover:text-red-200 transition-colors"
          >
            <Trash2 className="w-5 h-5" aria-hidden="true" />
            {t('common.delete')}
          </button>
        )}
      </div>

      {/* Active focus */}
      {!isEditing && activeFocus.length > 0 && (
        <div className="bg-bg-surface border border-border rounded-xl p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-accent-primary/15 rounded-lg flex items-center justify-center flex-shrink-0">
              <Target className="w-5 h-5 text-accent-primary" aria-hidden="true" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-text-secondary text-xs font-medium uppercase tracking-wider mb-1">{t('journal.yourFocus')}</p>
              <p className="text-text-primary font-medium">{activeFocus[0].intention_text}</p>
              {activeFocus[0].themes.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-2">
                  {activeFocus[0].themes.slice(0, 4).map((theme: string) => (
                    <span key={theme} className="px-2 py-0.5 bg-bg-elevated border border-border text-text-secondary text-xs rounded">
                      {theme}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Quick check-in on open threads */}
      {!isEditing && pendingPrompts.length > 0 && <ThreadPromptCard prompts={pendingPrompts} />}

      {/* Passage this entry is about */}
      {display.passage && (
        <div className="bg-bg-surface border border-accent-secondary/60 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 bg-accent-primary/15 rounded-lg flex items-center justify-center flex-shrink-0">
              <Book className="w-5 h-5 text-accent-primary" aria-hidden="true" />
            </div>
            <div className="flex-1 min-w-0">
              {display.planTitle && (
                <p className="text-text-secondary text-xs uppercase tracking-wider mb-1">
                  {display.planTitle}
                  {display.dayNumber ? ` • ${t('journal.day', { day: display.dayNumber })}` : ''}
                </p>
              )}
              <Link
                to={`/bible?passage=${encodeURIComponent(display.passage)}`}
                className="text-text-primary font-semibold hover:text-accent-primary transition-colors inline-flex items-center gap-2"
              >
                {display.passage}
                <ExternalLink className="w-4 h-4" aria-hidden="true" />
              </Link>
              {display.theme && (
                <p className="text-text-secondary text-sm mt-1 flex items-center gap-1">
                  <Lightbulb className="w-3 h-3" aria-hidden="true" />
                  {display.theme}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {display.aiInsight && (
        <div className="bg-bg-surface border border-border rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-4 h-4 text-accent-primary" aria-hidden="true" />
            <span className="text-text-primary font-semibold text-sm">{t('journal.aiInsight')}</span>
          </div>
          <p className="text-text-secondary text-sm leading-relaxed whitespace-pre-wrap">{display.aiInsight}</p>
        </div>
      )}

      {/* Highlights from the passage being journaled about */}
      {highlights.length > 0 && !isEditing && (
        <div className="bg-bg-surface border border-border rounded-xl p-4">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div className="flex items-center gap-2">
              <Highlighter className="w-4 h-4 text-accent-primary" aria-hidden="true" />
              <span className="text-text-primary font-semibold text-sm">{t('journal.highlights.title')}</span>
            </div>
            {isPublicDomainTranslation(passageContext.translation) ? (
              <button
                type="button"
                onClick={generateHighlightInsight}
                disabled={loadingHighlightInsight || !passageData}
                className="btn-secondary flex items-center gap-1.5 px-3 py-1.5 text-xs disabled:opacity-50"
              >
                {loadingHighlightInsight ? (
                  <Loader2 className="w-3 h-3 animate-spin" aria-hidden="true" />
                ) : (
                  <Sparkles className="w-3 h-3" aria-hidden="true" />
                )}
                {loadingHighlightInsight ? t('journal.highlights.generating') : t('journal.highlights.getInsight')}
              </button>
            ) : (
              <span className="text-xs text-text-secondary">{t('journal.highlights.publicDomainOnly')}</span>
            )}
          </div>
          <div className="space-y-3">
            {highlights.map((h: VerseHighlight) => (
              <div
                key={h.id}
                className="p-3 rounded-lg"
                style={{ backgroundColor: HIGHLIGHT_COLORS[h.color] || HIGHLIGHT_COLORS.yellow }}
              >
                <div className="flex items-start gap-2">
                  <span className="text-text-primary font-bold text-sm flex-shrink-0">v{h.verse_start}</span>
                  <p className="text-text-primary text-sm font-serif leading-relaxed">
                    {getVerseText(h.verse_start) || t('common.loading')}
                  </p>
                </div>
                {h.note && (
                  <div className="flex items-start gap-1 mt-2 pt-2 border-t border-white/10">
                    <MessageSquare className="w-3 h-3 text-text-primary mt-0.5 flex-shrink-0" aria-hidden="true" />
                    <p className="text-text-primary text-sm italic">{h.note}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {highlightError !== null && (
            <InlineError
              className="mt-4"
              error={highlightError}
              title={t('journal.highlights.failed')}
              onRetry={generateHighlightInsight}
            />
          )}

          {highlightInsight && (
            <div className="mt-4 pt-4 border-t border-border">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-4 h-4 text-accent-primary" aria-hidden="true" />
                <span className="text-text-primary font-semibold text-sm">{t('journal.highlights.reflection')}</span>
              </div>
              <p className="text-text-secondary text-sm leading-relaxed whitespace-pre-wrap">{highlightInsight}</p>
            </div>
          )}
        </div>
      )}

      <div className="card">
        <h1 className="text-2xl font-bold text-text-primary mb-1">
          {isEditing
            ? t('journal.yourEntry')
            : display.passage
              ? t('journal.reflectionTitle')
              : t('journal.newEntry')}
        </h1>
        <p className="text-sm text-text-secondary mb-6">
          {isEditing
            ? formatDate(date, i18n.language, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
            : t('journal.newEntryHint')}
        </p>

        <div className="mb-6">
          <label htmlFor={dateId} className="block text-sm font-medium text-text-primary mb-2">
            {t('journal.date')}
          </label>
          <input
            id={dateId}
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="input"
          />
        </div>

        <div className="mb-6">
          <label htmlFor={textId} className="block text-sm font-medium text-text-primary mb-2">
            {display.passage ? t('journal.yourReflection') : t('journal.entryLabel')}
          </label>
          {display.theme && !isEditing && (
            <p className="text-text-secondary text-sm mb-3">{t('journal.themeHint', { theme: display.theme })}</p>
          )}
          <textarea
            id={textId}
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={
              display.passage
                ? t('journal.placeholderPassage', { passage: display.passage })
                : t('journal.placeholder')
            }
            className="input w-full h-64 resize-y font-serif"
          />
          <DictationButton className="mt-3" value={text} onChange={setText} textareaRef={textareaRef} />
        </div>

        <div className="mb-6">
          <p id={moodLabelId} className="block text-sm font-medium text-text-primary mb-3">
            {t('journal.moodQuestion')}
          </p>
          <div className="flex flex-wrap gap-2" role="group" aria-labelledby={moodLabelId}>
            {MOODS.map((mood) => (
              <button
                key={mood.id}
                type="button"
                aria-pressed={selectedMood === mood.id}
                onClick={() => setSelectedMood(selectedMood === mood.id ? '' : mood.id)}
                className={`px-4 py-2 rounded-lg border transition-colors ${
                  selectedMood === mood.id
                    ? 'border-accent-primary bg-accent-primary/10 text-accent-primary'
                    : 'border-border text-text-secondary hover:border-text-secondary'
                }`}
              >
                <span className="mr-2" aria-hidden="true">{mood.emoji}</span>
                {t(moodLabelKey(mood.id))}
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={handleSave}
            disabled={isSaving || !text.trim()}
            className="btn-primary flex items-center gap-2 disabled:opacity-60"
          >
            {isSaving ? <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" /> : <Save className="w-4 h-4" aria-hidden="true" />}
            {isSaving ? t('journal.saving') : isEditing ? t('journal.saveChanges') : t('journal.saveAndFeedback')}
          </button>
          {isEditing && (
            <button
              type="button"
              onClick={openDeepDive}
              disabled={deepDiveMutation.isPending}
              className="btn-secondary flex items-center gap-2 disabled:opacity-60"
            >
              {deepDiveMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" /> : <Sparkles className="w-4 h-4" aria-hidden="true" />}
              {t('journal.deepDive.button')}
            </button>
          )}
          {display.passage && (
            <button
              type="button"
              onClick={() => navigate(`/bible?passage=${encodeURIComponent(display.passage!)}`)}
              className="btn-secondary"
            >
              {t('journal.backToReading')}
            </button>
          )}
          {isDirty && <span className="text-sm text-text-secondary">{t('journal.unsaved')}</span>}
        </div>

        {!isEditing && <p className="mt-3 text-xs text-text-secondary">{t('journal.afterSaveHint')}</p>}

        {saveError && <InlineError className="mt-4" error={saveError} title={t('journal.saveFailed')} onRetry={handleSave} />}
      </div>

      {isEditing && entryId && (
        <JournalFeedbackPanel
          entryId={entryId}
          autoGenerate={autoGenerateFeedback}
          entryChanged={entryChanged}
          onGenerated={() => setEntryChanged(false)}
        />
      )}

      <ConfirmDialog
        open={confirmDelete}
        title={t('journal.deleteTitle')}
        message={t('journal.deleteMessage')}
        confirmLabel={t('common.delete')}
        destructive
        busy={deleteMutation.isPending}
        onConfirm={() => entryId && deleteMutation.mutate(entryId)}
        onCancel={() => setConfirmDelete(false)}
      />

      {showDeepDive && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="deep-dive-title"
            className="bg-bg-surface rounded-xl p-6 max-w-3xl w-full border border-border max-h-[90vh] overflow-y-auto"
          >
            <div className="flex items-start justify-between gap-3 mb-4">
              <div>
                <h2 id="deep-dive-title" className="text-xl font-semibold text-text-primary">{t('journal.deepDive.title')}</h2>
                <p className="text-text-secondary mt-1">{t('journal.deepDive.subtitle')}</p>
              </div>
              <button
                type="button"
                onClick={closeDeepDive}
                className="p-2 text-text-secondary hover:text-text-primary"
                aria-label={t('common.close')}
                autoFocus
              >
                <X className="w-4 h-4" aria-hidden="true" />
              </button>
            </div>

            {deepDiveMutation.isPending && (
              <div className="py-12 text-center" role="status">
                <Loader2 className="w-8 h-8 animate-spin text-accent-primary mx-auto" aria-hidden="true" />
                <p className="text-text-secondary mt-3">{t('journal.deepDive.loading')}</p>
              </div>
            )}

            {deepDiveMutation.isError && (
              <InlineError
                error={deepDiveMutation.error}
                title={t('journal.deepDive.failed')}
                onRetry={() => deepDiveMutation.mutate()}
              />
            )}

            {deepDiveGuide && !deepDiveMutation.isPending && (
              <div className="space-y-6">
                {deepDiveGuide.study_session_id && (
                  <div className="bg-bg-elevated border border-border rounded-lg p-4 flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="text-text-primary text-sm font-medium">{t('journal.deepDive.tracking')}</p>
                      <p className="text-text-secondary text-xs mt-1">
                        {t('journal.deepDive.progress', {
                          percent: deepDiveGuide.study_progress?.progress_percentage ?? 0,
                        })}
                      </p>
                    </div>
                    <button type="button" onClick={() => navigate('/progress')} className="btn-secondary px-3 py-1.5 text-sm">
                      {t('journal.deepDive.openTracker')}
                    </button>
                  </div>
                )}

                <div className="bg-bg-elevated border border-border rounded-lg p-4">
                  <h3 className="text-text-primary font-semibold mb-2">{deepDiveGuide.title}</h3>
                  <p className="text-text-primary text-sm leading-relaxed">{deepDiveGuide.insight_summary}</p>
                </div>

                {deepDiveGuide.analytical_insights?.length > 0 && (
                  <div>
                    <h4 className="text-sm text-text-secondary font-medium mb-2">{t('journal.deepDive.insights')}</h4>
                    <ul className="space-y-2 list-disc pl-5 text-text-primary text-sm">
                      {deepDiveGuide.analytical_insights.map((insight, index) => (
                        <li key={index}>{insight}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {deepDiveGuide.heart_check_questions?.length > 0 && (
                  <div>
                    <h4 className="text-sm text-text-secondary font-medium mb-2">{t('journal.deepDive.questions')}</h4>
                    <ul className="space-y-2 list-disc pl-5 text-text-primary text-sm">
                      {deepDiveGuide.heart_check_questions.map((question, index) => (
                        <li key={index}>{question}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {deepDiveGuide.study_plan?.length > 0 && (
                  <div>
                    <h4 className="text-sm text-text-secondary font-medium mb-3">{t('journal.deepDive.plan')}</h4>
                    <div className="space-y-3">
                      {deepDiveGuide.study_plan.map((day) => (
                        <div key={day.day} className="bg-bg-elevated border border-border rounded-lg p-4">
                          <p className="text-text-primary text-sm font-semibold">
                            {t('journal.day', { day: day.day })}: {day.focus}
                          </p>
                          <p className="text-text-secondary text-xs mt-1">{t('journal.deepDive.scripture')}: {day.scripture}</p>
                          <p className="text-text-primary text-sm mt-2">
                            <span className="text-text-secondary">{t('journal.deepDive.practice')}:</span> {day.practice}
                          </p>
                          <p className="text-text-primary text-sm mt-1">
                            <span className="text-text-secondary">{t('journal.deepDive.journalPrompt')}:</span> {day.journal_prompt}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="bg-bg-elevated border border-border rounded-lg p-4">
                    <h4 className="text-sm font-medium text-text-secondary mb-2">{t('journal.deepDive.prayer')}</h4>
                    <p className="text-text-primary text-sm">{deepDiveGuide.prayer_focus}</p>
                  </div>
                  <div className="bg-bg-elevated border border-border rounded-lg p-4">
                    <h4 className="text-sm font-medium text-text-secondary mb-2">{t('journal.deepDive.nextStep')}</h4>
                    <p className="text-text-primary text-sm">{deepDiveGuide.next_step}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
