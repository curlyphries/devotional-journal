import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { Book, ChevronDown, Loader2, RefreshCw, Sparkles, Columns, AlignLeft, PenLine, Lightbulb, Highlighter, X, MessageSquare, Target } from 'lucide-react'
import { getPassage, getTranslations, parsePassageReference, PassageResponse, Verse } from '../api/bible'
import { getHighlights, createHighlight, updateHighlight, deleteHighlight, VerseHighlight } from '../api/highlights'
import { getActiveFocusIntentions } from '../api/devotional'
import client from '../api/client'

interface PlanContext {
  planId?: string
  planTitle?: string
  dayNumber?: number
  theme?: string
  enrollmentId?: string
}

interface ScriptureReaderProps {
  reference: string
  defaultTranslation?: string
  showComparison?: boolean
  planContext?: PlanContext
  onClose?: () => void
}

const HIGHLIGHT_COLORS = [
  { id: 'yellow', bg: 'rgba(234, 179, 8, 0.3)', border: '#eab308', text: '#eab308' },
  { id: 'green', bg: 'rgba(34, 197, 94, 0.3)', border: '#22c55e', text: '#22c55e' },
  { id: 'blue', bg: 'rgba(59, 130, 246, 0.3)', border: '#3b82f6', text: '#3b82f6' },
  { id: 'pink', bg: 'rgba(236, 72, 153, 0.3)', border: '#ec4899', text: '#ec4899' },
  { id: 'orange', bg: 'rgba(249, 115, 22, 0.3)', border: '#f97316', text: '#f97316' },
] as const

// Public domain translations - safe for AI processing without copyright concerns
const PUBLIC_DOMAIN_TRANSLATIONS = ['KJV', 'ASV', 'WEB', 'YLT', 'DBY', 'WBT']

const isPublicDomainTranslation = (code: string): boolean => {
  return PUBLIC_DOMAIN_TRANSLATIONS.includes(code.toUpperCase())
}

function groupIntoParagraphs(verses: Verse[]): Verse[][] {
  const paragraphs: Verse[][] = []
  let currentParagraph: Verse[] = []
  
  verses.forEach((verse, idx) => {
    const text = verse.text
    const prevText = idx > 0 ? verses[idx - 1].text : ''
    
    const startsNewParagraph = 
      idx === 0 ||
      prevText.endsWith('"') ||
      prevText.endsWith('."') ||
      prevText.endsWith('?"') ||
      prevText.endsWith('!"') ||
      (text.startsWith('And ') && prevText.includes('"')) ||
      (text.startsWith('Then ') && currentParagraph.length >= 2) ||
      (text.startsWith('Now ') && currentParagraph.length >= 2) ||
      (text.startsWith('But ') && currentParagraph.length >= 3) ||
      (currentParagraph.length >= 4 && (text.startsWith('And ') || text.startsWith('Then ') || text.startsWith('So ')))
    
    if (startsNewParagraph && currentParagraph.length > 0) {
      paragraphs.push(currentParagraph)
      currentParagraph = []
    }
    
    currentParagraph.push(verse)
  })
  
  if (currentParagraph.length > 0) {
    paragraphs.push(currentParagraph)
  }
  
  return paragraphs
}

function getHighlightForVerse(highlights: VerseHighlight[] | undefined, verseNum: number): VerseHighlight | undefined {
  if (!highlights || !Array.isArray(highlights)) return undefined;
  return highlights.find(h => 
    verseNum >= h.verse_start && verseNum <= (h.verse_end || h.verse_start)
  )
}

function getColorClasses(color: string) {
  return HIGHLIGHT_COLORS.find(c => c.id === color) || HIGHLIGHT_COLORS[0]
}

interface VerseSpanProps {
  verse: Verse
  highlight?: VerseHighlight
  onHighlightClick: (verse: Verse, highlight?: VerseHighlight) => void
  isLast: boolean
}

function VerseSpan({ verse, highlight, onHighlightClick, isLast }: VerseSpanProps) {
  const colorConfig = highlight ? getColorClasses(highlight.color) : null
  
  // Make highlight more visible with stronger background
  const bgStyle = colorConfig ? { 
    backgroundColor: colorConfig.bg,
    borderBottom: `2px solid ${colorConfig.border}`,
    paddingBottom: '2px'
  } : undefined
  
  return (
    <span 
      className="cursor-pointer hover:bg-gray-700/50 rounded transition-colors px-0.5 relative group"
      style={bgStyle}
      onClick={() => onHighlightClick(verse, highlight)}
    >
      <sup className="text-amber-500 text-[10px] font-bold mr-0.5 select-none align-super">
        {verse.verse}
      </sup>
      {verse.text}
      {highlight?.note && (
        <>
          <MessageSquare className="w-3 h-3 inline ml-0.5 text-amber-400" />
          {/* Hover tooltip for note */}
          <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 border border-amber-500/30 rounded-lg text-sm text-gray-200 whitespace-normal max-w-xs opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 shadow-xl">
            <span className="text-amber-400 text-xs font-medium block mb-1">Note:</span>
            {highlight.note}
            <span className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900"></span>
          </span>
        </>
      )}
      {!isLast ? ' ' : ''}
    </span>
  )
}

export default function ScriptureReader({
  reference,
  defaultTranslation = 'KJV',
  showComparison = true,
  planContext,
  onClose,
}: ScriptureReaderProps) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [selectedTranslation, setSelectedTranslation] = useState(defaultTranslation)
  const [showTranslationPicker, setShowTranslationPicker] = useState(false)
  const [comparisonMode, setComparisonMode] = useState(false)
  const [twoColumnMode, setTwoColumnMode] = useState(false)
  const [aiInsights, setAiInsights] = useState<string | null>(null)
  const [loadingInsights, setLoadingInsights] = useState(false)
  const [themeInsights, setThemeInsights] = useState<string | null>(null)
  const [loadingThemeInsights, setLoadingThemeInsights] = useState(false)
  
  // Highlight state
  const [selectedVerse, setSelectedVerse] = useState<Verse | null>(null)
  const [selectedHighlight, setSelectedHighlight] = useState<VerseHighlight | null>(null)
  const [highlightNote, setHighlightNote] = useState('')
  const [highlightColor, setHighlightColor] = useState<typeof HIGHLIGHT_COLORS[number]['id']>('yellow')
  const [showHighlightPanel, setShowHighlightPanel] = useState(false)

  const parsed = parsePassageReference(reference)

  const { data: translations = [] } = useQuery({
    queryKey: ['translations'],
    queryFn: getTranslations,
    staleTime: Infinity,
  })

  const { data: passage, isLoading, error, refetch } = useQuery({
    queryKey: ['passage', reference, selectedTranslation],
    queryFn: () => {
      if (!parsed) throw new Error('Invalid reference')
      return getPassage(parsed.book, parsed.chapter, selectedTranslation, parsed.verseStart, parsed.verseEnd)
    },
    enabled: !!parsed,
  })

  // Fetch highlights for this chapter
  const { data: highlights = [], refetch: refetchHighlights } = useQuery({
    queryKey: ['highlights', parsed?.book, parsed?.chapter, selectedTranslation],
    queryFn: () => getHighlights({ 
      book: parsed!.book, 
      chapter: parsed!.chapter, 
      translation: selectedTranslation 
    }),
    enabled: !!parsed,
    staleTime: 0, // Always refetch
  })

  // Fetch active focus intentions to personalize insights
  const { data: activeFocus = [] } = useQuery({
    queryKey: ['activeFocus'],
    queryFn: getActiveFocusIntentions,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  })

  const { data: comparisonData } = useQuery({
    queryKey: ['comparison', reference],
    queryFn: async () => {
      if (!parsed) return null
      const otherTranslations = ['KJV', 'ASV', 'WEB'].filter(t => t !== selectedTranslation)
      const results = await Promise.all(
        otherTranslations.slice(0, 2).map(async (trans) => {
          try {
            return await getPassage(parsed.book, parsed.chapter, trans, parsed.verseStart, parsed.verseEnd)
          } catch { return null }
        })
      )
      return results.filter(Boolean) as PassageResponse[]
    },
    enabled: comparisonMode && !!parsed,
  })

  const createHighlightMutation = useMutation({
    mutationFn: createHighlight,
    onSuccess: () => {
      // Force refetch highlights
      refetchHighlights()
      closeHighlightPanel()
    },
  })

  const updateHighlightMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof updateHighlight>[1] }) => 
      updateHighlight(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ predicate: (query) => query.queryKey[0] === 'highlights' })
      closeHighlightPanel()
    },
  })

  const deleteHighlightMutation = useMutation({
    mutationFn: deleteHighlight,
    onSuccess: () => {
      queryClient.invalidateQueries({ predicate: (query) => query.queryKey[0] === 'highlights' })
      closeHighlightPanel()
    },
  })

  const handleVerseClick = (verse: Verse, existingHighlight?: VerseHighlight) => {
    setSelectedVerse(verse)
    if (existingHighlight) {
      setSelectedHighlight(existingHighlight)
      setHighlightNote(existingHighlight.note)
      setHighlightColor(existingHighlight.color)
    } else {
      setSelectedHighlight(null)
      setHighlightNote('')
      setHighlightColor('yellow')
    }
    setShowHighlightPanel(true)
  }

  const closeHighlightPanel = () => {
    setShowHighlightPanel(false)
    setSelectedVerse(null)
    setSelectedHighlight(null)
    setHighlightNote('')
  }

  const saveHighlight = () => {
    if (!selectedVerse || !parsed) return

    if (selectedHighlight) {
      updateHighlightMutation.mutate({
        id: selectedHighlight.id,
        data: { color: highlightColor, note: highlightNote },
      })
    } else {
      createHighlightMutation.mutate({
        book: parsed.book,
        chapter: parsed.chapter,
        verse_start: selectedVerse.verse,
        translation: selectedTranslation,
        color: highlightColor,
        note: highlightNote,
      })
    }
  }

  const removeHighlight = () => {
    if (selectedHighlight) {
      deleteHighlightMutation.mutate(selectedHighlight.id)
    }
  }

  const generateThemeInsights = async () => {
    if (!passage || !planContext?.theme) return
    setLoadingThemeInsights(true)
    try {
      // Check cache first
      const cacheParams = new URLSearchParams({
        reference,
        translation: selectedTranslation,
        theme: planContext.theme || '',
        focus_intention: activeFocus.length > 0 ? activeFocus[0].intention_text : '',
      })
      
      const cacheCheck = await client.get(`/insights/scripture/?${cacheParams}`)
      
      if (cacheCheck.data.cached) {
        setThemeInsights(cacheCheck.data.insight)
        setLoadingThemeInsights(false)
        return
      }

      // Build focus context if user has active focus intentions
      const focusContext = activeFocus.length > 0 
        ? `\n\nIMPORTANT - The reader has set a personal spiritual focus: "${activeFocus[0].intention_text}". Their focus themes include: ${activeFocus[0].themes.join(', ')}. Please connect this passage not only to the plan's theme but also to their personal focus, showing how the scripture speaks to what they're working on spiritually.`
        : ''

      const response = await client.post('/crew/ask-agent/', {
        agent: 'scripture',
        prompt: `You are a biblical scholar and spiritual director guiding someone through "${planContext.planTitle || 'Bible Study'}". Day ${planContext.dayNumber || 1}, theme: "${planContext.theme}". 

Reading ${reference}:
"${passage.full_text.substring(0, 1500)}"${focusContext}

Provide a rich, theologically substantive devotional insight (3-4 paragraphs) that:

1. **EXEGETICAL DEPTH**: Explain the original Hebrew/Greek context, cultural background, and what this meant to the original audience. What theological truth is being revealed?

2. **THEOLOGICAL CONNECTIONS**: Connect this passage to the broader biblical narrative - how does it relate to God's character, the gospel, or major biblical themes? Reference other relevant scriptures.

3. **PRACTICAL WISDOM**: Bridge the ancient text to modern life with specific, concrete applications. How does this truth challenge or comfort us today? What does obedience to this passage actually look like in daily decisions?

4. **PERSONAL ENGAGEMENT**: End with 2-3 penetrating reflection questions that require honest self-examination, not surface-level answers.${activeFocus.length > 0 ? '\n\n5. **CONNECTION TO YOUR FOCUS**: Create a dedicated section showing how this passage specifically speaks to their personal spiritual intention: "' + activeFocus[0].intention_text + '". Make this connection explicit and practical.' : ''}

Write with depth, nuance, and intellectual rigor while remaining accessible. Avoid clichés and shallow platitudes. Challenge the reader to think deeply.`,
        context: { 
          reference, 
          theme: planContext.theme,
          userFocus: activeFocus.length > 0 ? activeFocus[0].intention_text : null,
          focusThemes: activeFocus.length > 0 ? activeFocus[0].themes : [],
        },
      })
      const generatedInsight = response.data.response
      setThemeInsights(generatedInsight)
      
      // Cache the generated insight
      await client.post('/insights/scripture/', {
        reference,
        translation: selectedTranslation,
        theme: planContext.theme || '',
        focus_intention: activeFocus.length > 0 ? activeFocus[0].intention_text : '',
        focus_themes: activeFocus.length > 0 ? activeFocus[0].themes : [],
        insight: generatedInsight,
      }).catch(err => console.error('Failed to cache insight:', err))
    } catch (err) {
      console.error('Failed to generate theme insights:', err)
    } finally {
      setLoadingThemeInsights(false)
    }
  }

  const generateComparisonInsights = async () => {
    if (!passage || !comparisonData?.length) return
    setLoadingInsights(true)
    try {
      const response = await client.post('/crew/ask-agent/', {
        agent: 'scripture',
        prompt: `Compare these translations of ${reference}:\n\n${selectedTranslation}: "${passage.full_text}"\n\n${comparisonData.map(c => `${c.translation.code}: "${c.full_text}"`).join('\n\n')}\n\nProvide insights on key differences and original meaning.`,
        context: { reference },
      })
      setAiInsights(response.data.response)
    } catch (err) {
      console.error('Failed to generate insights:', err)
    } finally {
      setLoadingInsights(false)
    }
  }

  const handleJournalEntry = () => {
    const params = new URLSearchParams({
      passage: reference,
      translation: selectedTranslation,
      ...(planContext?.enrollmentId && { enrollmentId: planContext.enrollmentId }),
      ...(planContext?.theme && { theme: planContext.theme }),
      ...(planContext?.planTitle && { planTitle: planContext.planTitle }),
      ...(planContext?.dayNumber && { dayNumber: String(planContext.dayNumber) }),
      ...(themeInsights && { aiInsight: themeInsights }),
    })
    navigate(`/journal/new?${params.toString()}`)
  }

  if (!parsed) {
    return (
      <div className="bg-gray-800 rounded-xl p-6 text-center">
        <p className="text-red-400">Invalid passage reference: {reference}</p>
      </div>
    )
  }

  const paragraphs = passage ? groupIntoParagraphs(passage.verses) : []

  return (
    <div className="bg-gray-800 rounded-xl overflow-hidden shadow-2xl relative">
      {/* Plan Context Header */}
      {planContext?.theme && (
        <div className="px-6 py-4 bg-gradient-to-r from-amber-900/30 to-amber-800/20 border-b border-amber-700/30">
          <div className="flex items-center justify-between">
            <div>
              {planContext.planTitle && (
                <p className="text-amber-500/80 text-xs uppercase tracking-wider mb-1">
                  {planContext.planTitle} • Day {planContext.dayNumber}
                </p>
              )}
              <h2 className="text-xl font-serif text-amber-100 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-amber-500" />
                {planContext.theme}
              </h2>
            </div>
            <button
              onClick={handleJournalEntry}
              className="flex items-center gap-2 px-4 py-2 bg-amber-600 hover:bg-amber-500 text-black font-medium rounded-lg transition-colors"
            >
              <PenLine className="w-4 h-4" />
              Journal
            </button>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="px-6 py-3 border-b border-gray-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Book className="w-5 h-5 text-amber-500" />
          <h3 className="text-base font-serif text-gray-200 tracking-wide uppercase">{reference}</h3>
          <span className="text-xs text-gray-500">Click any verse to highlight</span>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={() => setTwoColumnMode(!twoColumnMode)}
            className={`p-1.5 rounded transition-colors ${twoColumnMode ? 'bg-amber-500 text-black' : 'text-gray-400 hover:text-white'}`}
            title={twoColumnMode ? 'Single column' : 'Two columns'}
          >
            {twoColumnMode ? <AlignLeft className="w-4 h-4" /> : <Columns className="w-4 h-4" />}
          </button>

          <div className="relative">
            <button
              onClick={() => setShowTranslationPicker(!showTranslationPicker)}
              className="flex items-center gap-1 px-2 py-1 bg-gray-700 rounded text-xs text-gray-300 hover:bg-gray-600 transition-colors"
            >
              {selectedTranslation}
              <ChevronDown className="w-3 h-3" />
            </button>
            
            {showTranslationPicker && (
              <div className="absolute right-0 top-full mt-1 bg-gray-700 rounded-lg shadow-xl z-10 min-w-[180px] border border-gray-600">
                {translations.map((trans) => (
                  <button
                    key={trans.code}
                    onClick={() => { setSelectedTranslation(trans.code); setShowTranslationPicker(false) }}
                    className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-600 first:rounded-t-lg last:rounded-b-lg ${
                      trans.code === selectedTranslation ? 'bg-amber-500/20 text-amber-500' : 'text-gray-300'
                    }`}
                  >
                    <div className="font-medium">{trans.code}</div>
                    <div className="text-xs text-gray-500">{trans.name}</div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {showComparison && (
            <button
              onClick={() => setComparisonMode(!comparisonMode)}
              className={`px-2 py-1 rounded text-xs transition-colors ${
                comparisonMode ? 'bg-amber-500 text-black' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              Compare
            </button>
          )}

          {!planContext?.theme && (
            <button
              onClick={handleJournalEntry}
              className="flex items-center gap-1 px-2 py-1 bg-amber-600 hover:bg-amber-500 text-black rounded text-xs font-medium transition-colors"
            >
              <PenLine className="w-3 h-3" />
              Journal
            </button>
          )}

          {onClose && (
            <button onClick={onClose} className="text-gray-500 hover:text-white text-lg px-1">×</button>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-8 max-h-[75vh] overflow-y-auto bg-gray-900">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 text-amber-500 animate-spin" />
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-red-400 mb-4">Failed to load passage</p>
            <button onClick={() => refetch()} className="flex items-center gap-2 mx-auto px-4 py-2 bg-gray-700 rounded text-white hover:bg-gray-600">
              <RefreshCw className="w-4 h-4" /> Retry
            </button>
          </div>
        ) : passage ? (
          <div className="space-y-8">
            {/* Active Focus Banner */}
            {activeFocus.length > 0 && (
              <div className="bg-gradient-to-r from-purple-900/20 to-purple-800/10 border border-purple-700/30 rounded-lg p-3 max-w-2xl mx-auto">
                <div className="flex items-center gap-2">
                  <Target className="w-4 h-4 text-purple-400" />
                  <span className="text-purple-400 text-xs font-medium">Your Focus:</span>
                  <span className="text-purple-300 text-xs">{activeFocus[0].intention_text}</span>
                </div>
                {activeFocus[0].themes.length > 0 && (
                  <div className="flex gap-1.5 mt-2 ml-6">
                    {activeFocus[0].themes.slice(0, 4).map((theme: string) => (
                      <span key={theme} className="px-2 py-0.5 bg-purple-500/20 text-purple-300 text-xs rounded">
                        {theme}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Theme Insights */}
            {planContext?.theme && (
              <div className="bg-gradient-to-br from-amber-900/20 to-amber-800/10 border border-amber-700/30 rounded-lg p-5 max-w-2xl mx-auto">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-amber-500" />
                    <span className="text-amber-400 font-semibold text-sm">
                      {activeFocus.length > 0 ? 'Personalized Insight' : "Today's Insight"}
                    </span>
                  </div>
                  {!themeInsights && !loadingThemeInsights && isPublicDomainTranslation(selectedTranslation) && (
                    <button onClick={generateThemeInsights} className="text-xs text-amber-500 hover:text-amber-400">
                      Generate Insight
                    </button>
                  )}
                  {!isPublicDomainTranslation(selectedTranslation) && !themeInsights && (
                    <span className="text-xs text-gray-500" title="AI insights only available for public domain translations (KJV, ASV, WEB)">
                      Switch to KJV/ASV/WEB for AI
                    </span>
                  )}
                </div>
                {loadingThemeInsights ? (
                  <div className="flex items-center gap-2 text-gray-400">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">
                      {activeFocus.length > 0 
                        ? 'Connecting this passage to your focus...' 
                        : 'Preparing your insight...'}
                    </span>
                  </div>
                ) : themeInsights ? (
                  <div 
                    className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap"
                    dangerouslySetInnerHTML={{
                      __html: themeInsights
                        .replace(/\*\*(.+?)\*\*/g, '<strong class="text-amber-300 font-semibold">$1</strong>')
                        .replace(/\n/g, '<br />')
                    }}
                  />
                ) : (
                  <p className="text-gray-400 text-sm italic">
                    {activeFocus.length > 0 
                      ? `Click "Generate Insight" to see how this passage connects to your focus on "${activeFocus[0].intention_text}"`
                      : `Click "Generate Insight" for a reflection on "${planContext.theme}"`}
                  </p>
                )}
              </div>
            )}

            {/* Main passage with clickable verses */}
            <div className={`font-serif ${twoColumnMode ? 'columns-2 gap-8' : 'max-w-2xl mx-auto'}`}>
              <div className="space-y-4 text-[15px] text-gray-200">
                {paragraphs.map((para, pIdx) => (
                  <p key={pIdx} className="text-justify leading-7 first-letter:ml-4">
                    {para.map((verse, vIdx) => (
                      <VerseSpan
                        key={verse.verse}
                        verse={verse}
                        highlight={getHighlightForVerse(highlights, verse.verse)}
                        onHighlightClick={handleVerseClick}
                        isLast={vIdx === para.length - 1}
                      />
                    ))}
                  </p>
                ))}
              </div>
            </div>

            {/* Quick Journal Prompt */}
            <div className="max-w-2xl mx-auto bg-gray-800 rounded-lg p-5 border border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-white font-medium flex items-center gap-2">
                    <PenLine className="w-4 h-4 text-amber-500" />
                    Reflect & Journal
                  </h4>
                  <p className="text-gray-400 text-sm mt-1">
                    What stood out to you? How does it apply to your life?
                  </p>
                </div>
                <button
                  onClick={handleJournalEntry}
                  className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-black font-medium rounded-lg transition-colors whitespace-nowrap"
                >
                  Start Entry
                </button>
              </div>
            </div>

            {/* Comparison Mode */}
            {comparisonMode && comparisonData && comparisonData.length > 0 && (
              <div className="border-t border-gray-700 pt-6 space-y-6">
                <h4 className="text-xs font-bold text-gray-500 uppercase tracking-widest text-center">Compare Translations</h4>
                {comparisonData.map((comp) => {
                  const compParagraphs = groupIntoParagraphs(comp.verses)
                  return (
                    <div key={comp.translation.code} className="bg-gray-800 rounded-lg p-5 max-w-2xl mx-auto">
                      <div className="flex items-center gap-2 mb-3 pb-2 border-b border-gray-700">
                        <span className="text-amber-500 font-bold text-sm">{comp.translation.code}</span>
                        <span className="text-gray-500 text-xs">{comp.translation.name}</span>
                      </div>
                      <div className="space-y-3 font-serif text-sm text-gray-300">
                        {compParagraphs.map((para, idx) => (
                          <p key={idx} className="text-justify leading-7 first-letter:ml-4">
                            {para.map((verse, vIdx) => (
                              <span key={verse.verse}>
                                <sup className="text-amber-500 text-[10px] font-bold mr-0.5">{verse.verse}</sup>
                                {verse.text}{vIdx < para.length - 1 ? ' ' : ''}
                              </span>
                            ))}
                          </p>
                        ))}
                      </div>
                    </div>
                  )
                })}
                <div className="flex justify-center">
                  <button
                    onClick={generateComparisonInsights}
                    disabled={loadingInsights}
                    className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-500 disabled:opacity-50 text-sm"
                  >
                    {loadingInsights ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                    {loadingInsights ? 'Analyzing...' : 'Get AI Insights'}
                  </button>
                </div>
                {aiInsights && (
                  <div className="bg-purple-900/30 border border-purple-700/50 rounded-lg p-4 max-w-2xl mx-auto">
                    <div className="flex items-center gap-2 mb-3">
                      <Sparkles className="w-4 h-4 text-purple-400" />
                      <span className="text-purple-400 font-semibold text-sm">Translation Insights</span>
                    </div>
                    <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">{aiInsights}</div>
                  </div>
                )}
              </div>
            )}
          </div>
        ) : null}
      </div>

      {/* Highlight Panel */}
      {showHighlightPanel && selectedVerse && (
        <div className="absolute bottom-0 left-0 right-0 bg-gray-800 border-t border-gray-700 p-4 shadow-2xl">
          <div className="max-w-2xl mx-auto">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Highlighter className="w-4 h-4 text-amber-500" />
                <span className="text-white font-medium">
                  {selectedHighlight ? 'Edit Highlight' : 'Add Highlight'} - Verse {selectedVerse.verse}
                </span>
              </div>
              <button onClick={closeHighlightPanel} className="text-gray-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <p className="text-gray-400 text-sm mb-3 line-clamp-2 italic">"{selectedVerse.text}"</p>
            
            <div className="flex items-center gap-2 mb-3">
              <span className="text-gray-400 text-sm">Color:</span>
              {HIGHLIGHT_COLORS.map((color) => (
                <button
                  key={color.id}
                  onClick={() => setHighlightColor(color.id)}
                  className={`w-6 h-6 rounded-full border-2 ${
                    highlightColor === color.id ? 'ring-2 ring-white ring-offset-2 ring-offset-gray-800' : ''
                  }`}
                  style={{ backgroundColor: color.bg, borderColor: color.border }}
                />
              ))}
            </div>
            
            <textarea
              value={highlightNote}
              onChange={(e) => setHighlightNote(e.target.value)}
              placeholder="Add a note (optional)..."
              className="w-full bg-gray-700 text-white rounded-lg p-3 text-sm resize-none h-20 mb-3"
            />
            
            <div className="flex gap-2">
              <button
                onClick={saveHighlight}
                disabled={createHighlightMutation.isPending || updateHighlightMutation.isPending}
                className="flex-1 py-2 bg-amber-600 hover:bg-amber-500 text-black font-medium rounded-lg transition-colors"
              >
                {createHighlightMutation.isPending || updateHighlightMutation.isPending ? 'Saving...' : 'Save Highlight'}
              </button>
              {selectedHighlight && (
                <button
                  onClick={removeHighlight}
                  disabled={deleteHighlightMutation.isPending}
                  className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg transition-colors"
                >
                  {deleteHighlightMutation.isPending ? '...' : 'Remove'}
                </button>
              )}
              <button
                onClick={closeHighlightPanel}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
