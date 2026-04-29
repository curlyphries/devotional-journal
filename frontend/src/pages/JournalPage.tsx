import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate, useParams, useSearchParams, Link } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ChevronLeft, Save, Trash2, Book, Lightbulb, Loader2, ExternalLink, Highlighter, Sparkles, MessageSquare, Target, X } from 'lucide-react'
import { createJournalEntry, updateJournalEntry, deleteJournalEntry, getJournalEntry, generateJournalDeepDive } from '../api/journal'
import { getHighlights, VerseHighlight } from '../api/highlights'
import { getPassage, Verse } from '../api/bible'
import { getActiveFocusIntentions } from '../api/devotional'
import client from '../api/client'
import ThreadPromptCard from '../components/ThreadPromptCard'
import type { StudyGuide } from '../api/devotional'

const MOODS = [
  { id: 'grateful', emoji: '🙏', label: 'Grateful' },
  { id: 'struggling', emoji: '😔', label: 'Struggling' },
  { id: 'convicted', emoji: '💭', label: 'Convicted' },
  { id: 'peaceful', emoji: '😌', label: 'Peaceful' },
  { id: 'fired_up', emoji: '🔥', label: 'Fired Up' },
]

const HIGHLIGHT_COLORS: Record<string, string> = {
  yellow: 'rgba(234, 179, 8, 0.3)',
  green: 'rgba(34, 197, 94, 0.3)',
  blue: 'rgba(59, 130, 246, 0.3)',
  pink: 'rgba(236, 72, 153, 0.3)',
  orange: 'rgba(249, 115, 22, 0.3)',
}

const PUBLIC_DOMAIN_TRANSLATIONS = ['KJV', 'ASV', 'WEB', 'YLT', 'DBY', 'WBT']

const isPublicDomainTranslation = (code: string): boolean => {
  return PUBLIC_DOMAIN_TRANSLATIONS.includes(code.toUpperCase())
}

// Unique delimiters that users won't accidentally type
const DJ_META_START = '<!-- DJ_META_START -->'
const DJ_META_END = '<!-- DJ_META_END -->'

function parseJournalContent(content: string): {
  planTitle?: string
  dayNumber?: string
  theme?: string
  passage?: string
  aiInsight?: string
  userContent: string
} {
  // First, try to parse new format with HTML comment delimiters
  const metaStartIdx = content.indexOf(DJ_META_START)
  const metaEndIdx = content.indexOf(DJ_META_END)
  
  if (metaStartIdx !== -1 && metaEndIdx !== -1 && metaEndIdx > metaStartIdx) {
    // New format: JSON metadata in HTML comments
    const metaJson = content.slice(metaStartIdx + DJ_META_START.length, metaEndIdx).trim()
    const userContent = content.slice(metaEndIdx + DJ_META_END.length).trim()
    
    try {
      const meta = JSON.parse(metaJson)
      return {
        planTitle: meta.planTitle,
        dayNumber: meta.dayNumber,
        theme: meta.theme,
        passage: meta.passage,
        aiInsight: meta.aiInsight,
        userContent,
      }
    } catch {
      // JSON parse failed, fall through to legacy parsing
    }
  }

  // Legacy format: Parse **Theme:** style markers (for backwards compatibility)
  const lines = content.split('\n')
  let planTitle: string | undefined
  let dayNumber: string | undefined
  let theme: string | undefined
  let passage: string | undefined
  let aiInsight: string | undefined
  let contentStartIndex = 0

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    // Only match at the very start of the content (first few lines)
    // This prevents matching user-typed **Theme:** in the body
    if (i > 10) break
    
    const planMatch = line.match(/^\*\*(.+?)\*\*\s*-\s*Day\s*(\d+)/)
    if (planMatch) {
      planTitle = planMatch[1]
      dayNumber = planMatch[2]
      contentStartIndex = i + 1
      continue
    }
    
    const themeMatch = line.match(/^\*\*Theme:\*\*\s*(.+)/)
    if (themeMatch) {
      theme = themeMatch[1]
      contentStartIndex = i + 1
      continue
    }
    
    const passageMatch = line.match(/^\*\*Passage:\*\*\s*(.+)/)
    if (passageMatch) {
      passage = passageMatch[1]
      contentStartIndex = i + 1
      continue
    }

    const insightMatch = line.match(/^\*\*AI Insight:\*\*/)
    if (insightMatch) {
      const insightLines = []
      for (let j = i + 1; j < lines.length; j++) {
        if (lines[j].trim() === '---') {
          contentStartIndex = j + 1
          break
        }
        insightLines.push(lines[j])
      }
      aiInsight = insightLines.join('\n').trim()
      continue
    }
    
    if (line === '---') {
      contentStartIndex = i + 1
      continue
    }
    
    if (line && !line.startsWith('**')) {
      break
    }
  }

  const userContent = lines.slice(contentStartIndex).join('\n').trim()
  return { planTitle, dayNumber, theme, passage, aiInsight, userContent }
}

function parsePassageReference(ref: string): { book: string; chapter: number } | null {
  const match = ref.match(/^(\w+)\s*(\d+)/)
  if (match) {
    return { book: match[1].toUpperCase(), chapter: parseInt(match[2]) }
  }
  return null
}

export default function JournalPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { entryId } = useParams()
  const [searchParams] = useSearchParams()
  const isEditing = !!entryId

  const passageContext = {
    passage: searchParams.get('passage'),
    enrollmentId: searchParams.get('enrollmentId'),
    theme: searchParams.get('theme'),
    planTitle: searchParams.get('planTitle'),
    dayNumber: searchParams.get('dayNumber'),
    aiInsight: searchParams.get('aiInsight'),
    translation: searchParams.get('translation') || 'KJV',
  }

  const [date, setDate] = useState(new Date().toISOString().split('T')[0])
  const [content, setContent] = useState('')
  const [selectedMood, setSelectedMood] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [parsedMeta, setParsedMeta] = useState<ReturnType<typeof parseJournalContent> | null>(null)
  const [highlightInsight, setHighlightInsight] = useState('')
  const [loadingHighlightInsight, setLoadingHighlightInsight] = useState(false)
  const [showDeepDive, setShowDeepDive] = useState(false)
  const [deepDiveGuide, setDeepDiveGuide] = useState<StudyGuide | null>(null)
  const [deepDiveError, setDeepDiveError] = useState('')

  const parsedRef = passageContext.passage ? parsePassageReference(passageContext.passage) : null
  
  const { data: highlights = [] } = useQuery({
    queryKey: ['highlights', parsedRef?.book, parsedRef?.chapter],
    queryFn: () => getHighlights({ book: parsedRef!.book, chapter: parsedRef!.chapter }),
    enabled: !!parsedRef && !isEditing,
  })

  const { data: passageData } = useQuery({
    queryKey: ['passage', parsedRef?.book, parsedRef?.chapter],
    queryFn: () => getPassage(parsedRef!.book, parsedRef!.chapter, 'KJV'),
    enabled: !!parsedRef && !isEditing,
  })

  const { data: activeFocus = [] } = useQuery({
    queryKey: ['activeFocus'],
    queryFn: getActiveFocusIntentions,
    staleTime: 5 * 60 * 1000,
  })

  // Fetch pending thread prompts for quick check-in
  const { data: pendingPrompts = [] } = useQuery({
    queryKey: ['pendingThreadPrompts'],
    queryFn: async () => {
      const response = await client.get('/thread-prompts/pending/')
      return response.data
    },
    staleTime: 0,
    enabled: !isEditing,
  })

  const getVerseText = (verseNum: number): string => {
    if (!passageData?.verses) return ''
    const verse = passageData.verses.find((v: Verse) => v.verse === verseNum)
    return verse?.text || ''
  }

  const generateHighlightInsight = async () => {
    if (highlights.length === 0 || !passageData) return
    
    setLoadingHighlightInsight(true)
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

      const response = await client.post('/crew/ask-agent/', {
        agent: 'scripture',
        prompt,
        context: { 
          passage: passageContext.passage,
          theme: passageContext.theme,
          highlights: highlights.length,
          userFocus: activeFocus.length > 0 ? activeFocus[0].intention_text : null,
          focusThemes: activeFocus.length > 0 ? activeFocus[0].themes : [],
        },
      })
      setHighlightInsight(response.data.response)
    } catch (err) {
      console.error('Failed to generate highlight insight:', err)
    } finally {
      setLoadingHighlightInsight(false)
    }
  }

  useEffect(() => {
    if (entryId) {
      setIsLoading(true)
      getJournalEntry(entryId)
        .then((entry) => {
          setDate(entry.date)
          const fullContent = entry.decrypted_content || ''
          setContent(fullContent)
          setSelectedMood(entry.mood_tag || '')
          setParsedMeta(parseJournalContent(fullContent))
        })
        .catch((err) => console.error('Failed to load entry:', err))
        .finally(() => setIsLoading(false))
    }
  }, [entryId])

  useEffect(() => {
    if (passageContext.passage && !content && !entryId) {
      setContent('')
      setParsedMeta({
        planTitle: passageContext.planTitle || undefined,
        dayNumber: passageContext.dayNumber || undefined,
        theme: passageContext.theme || undefined,
        passage: passageContext.passage,
        aiInsight: passageContext.aiInsight || undefined,
        userContent: '',
      })
    }
  }, [passageContext.passage, entryId])

  const createMutation = useMutation({
    mutationFn: createJournalEntry,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
      navigate('/journal')
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof updateJournalEntry>[1] }) =>
      updateJournalEntry(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
      navigate('/journal')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: deleteJournalEntry,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
      navigate('/journal')
    },
  })

  const deepDiveMutation = useMutation<StudyGuide, Error, void>({
    mutationFn: () => {
      if (!entryId) {
        throw new Error('Journal entry must be saved before deep dive analysis')
      }
      return generateJournalDeepDive(entryId)
    },
    onSuccess: (guide: StudyGuide) => {
      setDeepDiveGuide(guide)
      setDeepDiveError('')
    },
    onError: () => {
      setDeepDiveGuide(null)
      setDeepDiveError('Failed to generate a deep-dive study guide. Please try again.')
    },
  })

  const handleSave = async () => {
    let fullContent = content
    
    // Build content with new robust metadata format (HTML comments + JSON)
    if (!isEditing && passageContext.passage) {
      const metadata = {
        planTitle: passageContext.planTitle || null,
        dayNumber: passageContext.dayNumber || null,
        theme: passageContext.theme || null,
        passage: passageContext.passage,
        aiInsight: passageContext.aiInsight || null,
        highlights: highlights.map((h: VerseHighlight) => ({
          verse: h.verse_start,
          note: h.note || null,
        })),
      }
      
      // New format: JSON metadata in HTML comments (won't be accidentally typed by users)
      const metaBlock = `${DJ_META_START}\n${JSON.stringify(metadata, null, 2)}\n${DJ_META_END}\n\n`
      fullContent = metaBlock + content
    }

    if (isEditing && entryId) {
      // When editing, preserve the metadata format
      let editContent = parsedMeta?.userContent || content
      
      if (parsedMeta?.passage) {
        const metadata = {
          planTitle: parsedMeta.planTitle || null,
          dayNumber: parsedMeta.dayNumber || null,
          theme: parsedMeta.theme || null,
          passage: parsedMeta.passage,
          aiInsight: parsedMeta.aiInsight || null,
        }
        editContent = `${DJ_META_START}\n${JSON.stringify(metadata, null, 2)}\n${DJ_META_END}\n\n${parsedMeta.userContent || content}`
      }
      
      updateMutation.mutate({
        id: entryId,
        data: {
          date,
          content: editContent,
          mood_tag: selectedMood || undefined,
        },
      })
    } else {
      createMutation.mutate({
        date,
        content: fullContent,
        mood_tag: selectedMood || undefined,
      })
    }
  }

  const handleDelete = () => {
    if (entryId && window.confirm('Are you sure you want to delete this entry?')) {
      deleteMutation.mutate(entryId)
    }
  }

  const handleGenerateDeepDive = async () => {
    if (!entryId) {
      return
    }

    setShowDeepDive(true)
    setDeepDiveGuide(null)
    setDeepDiveError('')

    await deepDiveMutation.mutateAsync()
  }

  const closeDeepDive = () => {
    setShowDeepDive(false)
    setDeepDiveGuide(null)
    setDeepDiveError('')
  }

  const isSaving = createMutation.isPending || updateMutation.isPending

  const displayMeta = parsedMeta || {
    planTitle: passageContext.planTitle,
    dayNumber: passageContext.dayNumber,
    theme: passageContext.theme,
    passage: passageContext.passage,
    aiInsight: passageContext.aiInsight,
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 text-amber-500 animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
        >
          <ChevronLeft className="w-5 h-5" />
          {t('common.back')}
        </button>

        {isEditing && (
          <button
            onClick={handleDelete}
            disabled={deleteMutation.isPending}
            className="flex items-center gap-2 text-danger hover:text-danger/80 transition-colors"
          >
            <Trash2 className="w-5 h-5" />
            {deleteMutation.isPending ? 'Deleting...' : t('common.delete')}
          </button>
        )}
      </div>

      {/* Active Focus Banner */}
      {!isEditing && activeFocus.length > 0 && (
        <div className="bg-gradient-to-r from-purple-900/20 to-purple-800/10 border border-purple-700/30 rounded-xl p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <Target className="w-5 h-5 text-purple-400" />
            </div>
            <div className="flex-1">
              <p className="text-purple-400 text-xs font-medium uppercase tracking-wider mb-1">Your Spiritual Focus</p>
              <p className="text-white font-medium">{activeFocus[0].intention_text}</p>
              {activeFocus[0].themes.length > 0 && (
                <div className="flex gap-1.5 mt-2">
                  {activeFocus[0].themes.slice(0, 4).map((theme: string) => (
                    <span key={theme} className="px-2 py-0.5 bg-purple-500/20 text-purple-300 text-xs rounded">
                      {theme}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Quick Check-In Thread Prompts */}
      {!isEditing && pendingPrompts.length > 0 && (
        <ThreadPromptCard prompts={pendingPrompts} />
      )}

      {/* Passage Context Banner */}
      {displayMeta.passage && (
        <div className="bg-gradient-to-r from-amber-900/30 to-amber-800/20 border border-amber-700/30 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 bg-amber-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <Book className="w-5 h-5 text-amber-500" />
            </div>
            <div className="flex-1">
              {displayMeta.planTitle && (
                <p className="text-amber-500/80 text-xs uppercase tracking-wider mb-1">
                  {displayMeta.planTitle} • Day {displayMeta.dayNumber}
                </p>
              )}
              <Link 
                to={`/bible?passage=${encodeURIComponent(displayMeta.passage!)}`}
                className="text-white font-semibold hover:text-amber-400 transition-colors flex items-center gap-2"
              >
                {displayMeta.passage}
                <ExternalLink className="w-4 h-4" />
              </Link>
              {displayMeta.theme && (
                <p className="text-gray-400 text-sm mt-1 flex items-center gap-1">
                  <Lightbulb className="w-3 h-3" />
                  {displayMeta.theme}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* AI Insight Section */}
      {(displayMeta.aiInsight || passageContext.aiInsight) && (
        <div className="bg-gradient-to-br from-purple-900/20 to-purple-800/10 border border-purple-700/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-4 h-4 text-purple-400" />
            <span className="text-purple-400 font-semibold text-sm">AI Insight</span>
          </div>
          <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
            {displayMeta.aiInsight || passageContext.aiInsight}
          </p>
        </div>
      )}

      {/* Highlights Section */}
      {highlights.length > 0 && !isEditing && (
        <div className="bg-gray-800/50 border border-amber-500/20 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Highlighter className="w-4 h-4 text-amber-400" />
              <span className="text-amber-400 font-semibold text-sm">Your Highlights</span>
            </div>
            {isPublicDomainTranslation(passageContext.translation) ? (
              <button
                onClick={generateHighlightInsight}
                disabled={loadingHighlightInsight || !passageData}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 rounded-lg text-purple-400 text-xs font-medium transition-colors disabled:opacity-50"
              >
                {loadingHighlightInsight ? (
                  <Loader2 className="w-3 h-3 animate-spin" />
                ) : (
                  <Sparkles className="w-3 h-3" />
                )}
                {loadingHighlightInsight ? 'Generating...' : 'Get AI Insight'}
              </button>
            ) : (
              <span className="text-xs text-gray-500" title="AI insights only available for public domain translations">
                AI requires KJV/ASV/WEB
              </span>
            )}
          </div>
          <div className="space-y-3">
            {highlights.map((h: VerseHighlight) => (
              <div 
                key={h.id} 
                className="p-3 rounded-lg"
                style={{ backgroundColor: HIGHLIGHT_COLORS[h.color] || HIGHLIGHT_COLORS.yellow }}
              >
                <div className="flex items-start gap-2 mb-2">
                  <span className="text-amber-500 font-bold text-sm flex-shrink-0">v{h.verse_start}</span>
                  <p className="text-gray-200 text-sm font-serif leading-relaxed">
                    {getVerseText(h.verse_start) || 'Loading...'}
                  </p>
                </div>
                {h.note && (
                  <div className="flex items-start gap-1 mt-2 pt-2 border-t border-white/10">
                    <MessageSquare className="w-3 h-3 text-amber-400 mt-0.5 flex-shrink-0" />
                    <p className="text-amber-200 text-sm italic">{h.note}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {highlightInsight && (
            <div className="mt-4 pt-4 border-t border-gray-600">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <span className="text-purple-400 font-semibold text-sm">AI Reflection on Your Highlights</span>
              </div>
              <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                {highlightInsight}
              </p>
            </div>
          )}
        </div>
      )}

      <div className="card">
        <h1 className="text-2xl font-bold text-text-primary mb-6">
          {isEditing ? t('common.edit') : displayMeta.passage ? 'Journal Your Reflection' : t('journal.newEntry')}
        </h1>

        <div className="mb-6">
          <label className="block text-sm font-medium text-text-primary mb-2">
            Date
          </label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="input"
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-text-primary mb-2">
            {displayMeta.passage ? 'Your Reflection' : t('reading.journalEntry')}
          </label>
          {displayMeta.theme && !isEditing && (
            <p className="text-gray-400 text-sm mb-3">
              Consider: How does this passage connect to "{displayMeta.theme}"? What is God speaking to you today?
            </p>
          )}
          <textarea
            value={isEditing ? (parsedMeta?.userContent || content) : content}
            onChange={(e) => {
              setContent(e.target.value)
              if (parsedMeta) {
                setParsedMeta({ ...parsedMeta, userContent: e.target.value })
              }
            }}
            placeholder={displayMeta.passage 
              ? `What stood out to you in ${displayMeta.passage}? How does it apply to your life?`
              : "Write your thoughts, prayers, and reflections..."
            }
            className="input w-full h-64 resize-none font-serif"
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-text-primary mb-3">
            How are you feeling?
          </label>
          <div className="flex flex-wrap gap-2">
            {MOODS.map((mood) => (
              <button
                key={mood.id}
                onClick={() => setSelectedMood(selectedMood === mood.id ? '' : mood.id)}
                className={`px-4 py-2 rounded-lg border transition-colors ${
                  selectedMood === mood.id
                    ? 'border-accent-primary bg-accent-primary/10 text-accent-primary'
                    : 'border-border text-text-secondary hover:border-text-secondary'
                }`}
              >
                <span className="mr-2">{mood.emoji}</span>
                {mood.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-3">
          {isEditing && (
            <button
              onClick={handleGenerateDeepDive}
              disabled={deepDiveMutation.isPending}
              className="px-4 py-2 bg-purple-500/20 text-purple-300 rounded-lg hover:bg-purple-500/30 transition-colors flex items-center gap-2 disabled:opacity-60"
            >
              {deepDiveMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              Deep Dive Study Guide
            </button>
          )}
          <button
            onClick={handleSave}
            disabled={isSaving || !(isEditing ? (parsedMeta?.userContent || content) : content).trim()}
            className="btn-primary flex items-center gap-2"
          >
            {isSaving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            {isSaving ? 'Saving...' : t('common.save')}
          </button>
          {displayMeta.passage && (
            <button
              onClick={() => {
                console.log('Back to Reading clicked, passage:', displayMeta.passage)
                const parsed = parsePassageReference(displayMeta.passage!)
                console.log('Parsed:', parsed)
                if (parsed) {
                  const url = `/bible?book=${parsed.book}&chapter=${parsed.chapter}`
                  console.log('Navigating to:', url)
                  navigate(url)
                } else {
                  console.log('Parse failed, going back')
                  navigate(-1)
                }
              }}
              className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              Back to Reading
            </button>
          )}
        </div>

        {(createMutation.isError || updateMutation.isError) && (
          <p className="text-red-400 mt-4">Failed to save entry. Please try again.</p>
        )}
      </div>

      {showDeepDive && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-xl p-6 max-w-3xl w-full border border-gray-800 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-xl font-semibold text-white">Journal Deep Dive</h2>
                <p className="text-purple-300 mt-1">Personalized study guide from this entry</p>
              </div>
              <button onClick={closeDeepDive} className="text-gray-400 hover:text-white">
                <X className="w-4 h-4" />
              </button>
            </div>

            {deepDiveMutation.isPending && (
              <div className="py-12 text-center">
                <Loader2 className="w-8 h-8 animate-spin text-purple-400 mx-auto" />
                <p className="text-gray-400 mt-3">Analyzing your entry and generating a study guide...</p>
              </div>
            )}

            {deepDiveError && !deepDiveMutation.isPending && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 text-red-300">
                {deepDiveError}
              </div>
            )}

            {deepDiveGuide && !deepDiveMutation.isPending && (
              <div className="space-y-6">
                {deepDiveGuide.study_session_id && (
                  <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4 flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="text-purple-300 text-sm font-medium">Study Tracking Enabled</p>
                      <p className="text-gray-400 text-xs mt-1">
                        Progress: {deepDiveGuide.study_progress?.progress_percentage ?? 0}% • Next Day: {deepDiveGuide.study_progress?.next_day ?? 'Complete'}
                      </p>
                    </div>
                    <button
                      onClick={() => navigate('/progress')}
                      className="px-3 py-1.5 bg-purple-500/20 text-purple-300 rounded-lg hover:bg-purple-500/30 text-sm"
                    >
                      Open Study Tracker
                    </button>
                  </div>
                )}

                <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                  <h3 className="text-purple-300 font-semibold mb-2">{deepDiveGuide.title}</h3>
                  <p className="text-gray-200 text-sm leading-relaxed">{deepDiveGuide.insight_summary}</p>
                </div>

                {deepDiveGuide.analytical_insights.length > 0 && (
                  <div>
                    <h4 className="text-sm text-gray-400 font-medium mb-2">Analytical Insights</h4>
                    <ul className="space-y-2">
                      {deepDiveGuide.analytical_insights.map((insight, index) => (
                        <li key={index} className="text-gray-300 text-sm flex items-start gap-2">
                          <span className="text-purple-400">•</span>
                          <span>{insight}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {deepDiveGuide.heart_check_questions.length > 0 && (
                  <div>
                    <h4 className="text-sm text-gray-400 font-medium mb-2">Heart-Check Questions</h4>
                    <ul className="space-y-2">
                      {deepDiveGuide.heart_check_questions.map((question, index) => (
                        <li key={index} className="text-gray-300 text-sm flex items-start gap-2">
                          <span className="text-amber-400">?</span>
                          <span>{question}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {deepDiveGuide.study_plan.length > 0 && (
                  <div>
                    <h4 className="text-sm text-gray-400 font-medium mb-3">Study Plan</h4>
                    <div className="space-y-3">
                      {deepDiveGuide.study_plan.map((day) => (
                        <div key={day.day} className="bg-gray-800/50 border border-gray-700 rounded-lg p-4">
                          <p className="text-purple-300 text-sm font-semibold">Day {day.day}: {day.focus}</p>
                          <p className="text-gray-400 text-xs mt-1">Scripture: {day.scripture}</p>
                          <p className="text-gray-300 text-sm mt-2"><span className="text-gray-400">Practice:</span> {day.practice}</p>
                          <p className="text-gray-300 text-sm mt-1"><span className="text-gray-400">Journal:</span> {day.journal_prompt}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-4">
                    <h4 className="text-sm font-medium text-gray-400 mb-2">Prayer Focus</h4>
                    <p className="text-gray-300 text-sm">{deepDiveGuide.prayer_focus}</p>
                  </div>
                  <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-4">
                    <h4 className="text-sm font-medium text-gray-400 mb-2">Next Step</h4>
                    <p className="text-gray-300 text-sm">{deepDiveGuide.next_step}</p>
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
