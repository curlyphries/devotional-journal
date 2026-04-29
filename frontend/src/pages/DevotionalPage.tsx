import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Book, Calendar, Sun, CalendarDays, CalendarRange, 
  Plus, Check, ChevronRight, Sparkles, BookOpen,
  Quote, Lightbulb, PenLine, Loader2, X, ExternalLink
} from 'lucide-react'
import {
  useTodayDevotional,
  useCreateFocusIntention,
  useMarkPassageRead,
  useSavePassageReflection,
  useActiveFocusIntentions,
  usePassageDeepDive,
} from '../hooks/useDevotional'
import type { DevotionalPassage, FocusIntention, StudyGuide } from '../api/devotional'

// Scripture references organized by theme - curated passages for self-study
const THEME_SCRIPTURES: Record<string, { title: string; passages: { ref: string; summary: string }[] }> = {
  discipline: {
    title: 'Discipline & Self-Control',
    passages: [
      { ref: 'Proverbs 25:28', summary: 'A person without self-control is like a city broken into' },
      { ref: 'Galatians 5:22-23', summary: 'The fruit of the Spirit includes self-control' },
      { ref: '1 Corinthians 9:24-27', summary: 'Paul disciplines his body like an athlete' },
      { ref: '2 Timothy 1:7', summary: 'God gave us a spirit of power, love, and self-discipline' },
      { ref: 'Proverbs 12:1', summary: 'Whoever loves discipline loves knowledge' },
      { ref: 'Hebrews 12:11', summary: 'Discipline yields the peaceful fruit of righteousness' },
      { ref: 'Titus 2:11-12', summary: 'Grace teaches us to live self-controlled lives' },
    ]
  },
  habits: {
    title: 'Building Good Habits',
    passages: [
      { ref: 'Daniel 6:10', summary: 'Daniel prayed three times daily as his habit' },
      { ref: 'Luke 4:16', summary: 'Jesus went to synagogue on Sabbath as was his custom' },
      { ref: 'Acts 17:11', summary: 'The Bereans examined Scripture daily' },
      { ref: 'Psalm 1:1-3', summary: 'Blessed is one who meditates on God\'s law day and night' },
      { ref: 'Colossians 3:16', summary: 'Let the word of Christ dwell in you richly' },
      { ref: 'Joshua 1:8', summary: 'Meditate on the law day and night' },
      { ref: 'Mark 1:35', summary: 'Jesus rose early to pray in a solitary place' },
    ]
  },
  perseverance: {
    title: 'Perseverance & Endurance',
    passages: [
      { ref: 'James 1:2-4', summary: 'Testing produces perseverance, leading to maturity' },
      { ref: 'Romans 5:3-5', summary: 'Suffering produces perseverance, character, and hope' },
      { ref: 'Hebrews 12:1-2', summary: 'Run with perseverance, fixing eyes on Jesus' },
      { ref: 'Galatians 6:9', summary: 'Do not grow weary in doing good' },
      { ref: '2 Corinthians 4:16-18', summary: 'We do not lose heart; troubles are achieving glory' },
      { ref: 'Philippians 3:13-14', summary: 'Press on toward the goal' },
      { ref: 'Romans 12:12', summary: 'Be joyful in hope, patient in affliction' },
    ]
  },
  intentionality: {
    title: 'Living with Purpose',
    passages: [
      { ref: 'Ephesians 5:15-17', summary: 'Be careful how you live, making the most of time' },
      { ref: 'Proverbs 4:25-27', summary: 'Let your eyes look straight ahead' },
      { ref: 'Colossians 3:23-24', summary: 'Whatever you do, work at it with all your heart' },
      { ref: 'Jeremiah 29:11', summary: 'God has plans to prosper you and give you hope' },
      { ref: 'Proverbs 16:3', summary: 'Commit your works to the Lord' },
      { ref: 'Matthew 6:33', summary: 'Seek first the kingdom of God' },
      { ref: 'Romans 12:2', summary: 'Be transformed by renewing your mind' },
    ]
  },
  consistency: {
    title: 'Consistency & Faithfulness',
    passages: [
      { ref: 'Lamentations 3:22-23', summary: 'God\'s mercies are new every morning' },
      { ref: '1 Corinthians 15:58', summary: 'Be steadfast, immovable, always abounding' },
      { ref: 'Proverbs 3:5-6', summary: 'Trust in the Lord with all your heart' },
      { ref: 'Matthew 25:21', summary: 'Well done, good and faithful servant' },
      { ref: 'Luke 16:10', summary: 'Faithful in little, faithful in much' },
      { ref: 'Psalm 119:105', summary: 'Your word is a lamp to my feet' },
      { ref: 'Philippians 4:6-7', summary: 'Do not be anxious; the peace of God will guard you' },
    ]
  },
  patience: {
    title: 'Patience & Waiting',
    passages: [
      { ref: 'Psalm 27:14', summary: 'Wait for the Lord; be strong and take heart' },
      { ref: 'Isaiah 40:31', summary: 'Those who wait on the Lord will renew their strength' },
      { ref: 'James 5:7-8', summary: 'Be patient like a farmer waiting for harvest' },
      { ref: 'Ecclesiastes 3:1', summary: 'There is a time for everything' },
      { ref: 'Romans 8:25', summary: 'We wait for what we do not see with patience' },
      { ref: 'Psalm 37:7', summary: 'Be still before the Lord and wait patiently' },
      { ref: 'Hebrews 6:12', summary: 'Imitate those who through faith and patience inherit promises' },
    ]
  },
  faith: {
    title: 'Faith & Trust',
    passages: [
      { ref: 'Hebrews 11:1', summary: 'Faith is the substance of things hoped for' },
      { ref: 'Romans 10:17', summary: 'Faith comes by hearing the word of God' },
      { ref: 'Mark 11:22-24', summary: 'Have faith in God; believe and it will be done' },
      { ref: 'Matthew 17:20', summary: 'Faith as small as a mustard seed can move mountains' },
      { ref: '2 Corinthians 5:7', summary: 'We walk by faith, not by sight' },
      { ref: 'Hebrews 11:6', summary: 'Without faith it is impossible to please God' },
      { ref: 'James 2:17', summary: 'Faith without works is dead' },
    ]
  },
  prayer: {
    title: 'Prayer & Communication with God',
    passages: [
      { ref: '1 Thessalonians 5:16-18', summary: 'Pray without ceasing; give thanks in all things' },
      { ref: 'Matthew 6:5-13', summary: 'The Lord\'s Prayer - how to pray' },
      { ref: 'Philippians 4:6-7', summary: 'Present your requests to God with thanksgiving' },
      { ref: 'James 5:16', summary: 'The prayer of a righteous person is powerful' },
      { ref: 'Jeremiah 33:3', summary: 'Call to me and I will answer you' },
      { ref: 'Mark 1:35', summary: 'Jesus rose early to pray in a solitary place' },
      { ref: 'Luke 18:1', summary: 'Always pray and do not give up' },
    ]
  },
  gratitude: {
    title: 'Gratitude & Thanksgiving',
    passages: [
      { ref: 'Psalm 100:4', summary: 'Enter his gates with thanksgiving' },
      { ref: '1 Thessalonians 5:18', summary: 'Give thanks in all circumstances' },
      { ref: 'Colossians 3:15-17', summary: 'Let the peace of Christ rule; be thankful' },
      { ref: 'Psalm 107:1', summary: 'Give thanks to the Lord for he is good' },
      { ref: 'Philippians 4:6', summary: 'With thanksgiving present your requests to God' },
      { ref: 'Ephesians 5:20', summary: 'Always giving thanks for everything' },
      { ref: 'Psalm 136:1', summary: 'His love endures forever' },
    ]
  },
  peace: {
    title: 'Peace & Rest',
    passages: [
      { ref: 'John 14:27', summary: 'My peace I give you; do not be troubled' },
      { ref: 'Philippians 4:6-7', summary: 'The peace of God will guard your hearts' },
      { ref: 'Isaiah 26:3', summary: 'Perfect peace for those whose minds are steadfast' },
      { ref: 'Matthew 11:28-30', summary: 'Come to me and I will give you rest' },
      { ref: 'Psalm 23:1-3', summary: 'He leads me beside still waters' },
      { ref: 'Colossians 3:15', summary: 'Let the peace of Christ rule in your hearts' },
      { ref: 'Romans 15:13', summary: 'May the God of hope fill you with peace' },
    ]
  },
}

type PeriodType = 'day' | 'week' | 'month'

const periodConfig: Record<PeriodType, { icon: typeof Sun; label: string; description: string }> = {
  day: { 
    icon: Sun, 
    label: 'Daily Focus', 
    description: 'Set your intention for today' 
  },
  week: { 
    icon: CalendarDays, 
    label: 'Weekly Focus', 
    description: 'Guide your week with purpose' 
  },
  month: { 
    icon: CalendarRange, 
    label: 'Monthly Focus', 
    description: 'A month-long spiritual journey' 
  },
}

export default function DevotionalPage() {
  const navigate = useNavigate()
  const [showNewFocus, setShowNewFocus] = useState(false)
  const [selectedPeriod, setSelectedPeriod] = useState<PeriodType>('day')
  const [intentionText, setIntentionText] = useState('')
  const [selectedPassage, setSelectedPassage] = useState<DevotionalPassage | null>(null)
  const [reflectionText, setReflectionText] = useState('')
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null)
  const [deepDivePassage, setDeepDivePassage] = useState<DevotionalPassage | null>(null)
  const [deepDiveGuide, setDeepDiveGuide] = useState<StudyGuide | null>(null)
  const [deepDiveError, setDeepDiveError] = useState('')

  const { data: todayData, isLoading } = useTodayDevotional()
  const { data: activeIntentions } = useActiveFocusIntentions()
  const createFocus = useCreateFocusIntention()
  const markRead = useMarkPassageRead()
  const saveReflection = useSavePassageReflection()
  const passageDeepDive = usePassageDeepDive()

  const handleCreateFocus = async () => {
    if (!intentionText.trim()) return
    
    await createFocus.mutateAsync({
      period_type: selectedPeriod,
      intention: intentionText.trim(),
    })
    
    setIntentionText('')
    setShowNewFocus(false)
  }

  const handleSaveReflection = async () => {
    if (!selectedPassage || !reflectionText.trim()) return
    
    await saveReflection.mutateAsync({
      id: selectedPassage.id,
      reflection: reflectionText.trim(),
    })
    
    setReflectionText('')
    setSelectedPassage(null)
  }

  const handleGenerateDeepDive = async (passage: DevotionalPassage) => {
    setDeepDivePassage(passage)
    setDeepDiveGuide(null)
    setDeepDiveError('')

    try {
      const guide = await passageDeepDive.mutateAsync({ id: passage.id })
      setDeepDiveGuide(guide)
    } catch {
      setDeepDiveError('Failed to generate a study guide. Please try again.')
    }
  }

  const closeDeepDive = () => {
    setDeepDivePassage(null)
    setDeepDiveGuide(null)
    setDeepDiveError('')
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-amber-500" />
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Book className="w-7 h-7 text-amber-500" />
            Devotional Focus
          </h1>
          <p className="text-gray-400 mt-1">
            Set your spiritual intentions and receive curated scripture passages
          </p>
        </div>
        <button
          onClick={() => setShowNewFocus(true)}
          className="flex items-center gap-2 px-4 py-2 bg-amber-500/20 text-amber-500 rounded-lg hover:bg-amber-500/30 transition-colors"
        >
          <Plus className="w-4 h-4" />
          New Focus
        </button>
      </div>

      {/* New Focus Modal */}
      {showNewFocus && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-xl p-6 max-w-lg w-full border border-gray-800">
            <h2 className="text-xl font-semibold text-white mb-4">
              Set Your Focus Intention
            </h2>
            
            {/* Period Selection */}
            <div className="grid grid-cols-3 gap-3 mb-6">
              {(Object.keys(periodConfig) as PeriodType[]).map((period) => {
                const config = periodConfig[period]
                const Icon = config.icon
                const isSelected = selectedPeriod === period
                const hasActive = period === 'day' ? todayData?.has_daily_focus :
                                  period === 'week' ? todayData?.has_weekly_focus :
                                  todayData?.has_monthly_focus
                
                return (
                  <button
                    key={period}
                    onClick={() => setSelectedPeriod(period)}
                    disabled={hasActive}
                    className={`p-4 rounded-lg border transition-all ${
                      isSelected 
                        ? 'border-amber-500 bg-amber-500/10' 
                        : hasActive
                          ? 'border-gray-700 bg-gray-800/50 opacity-50 cursor-not-allowed'
                          : 'border-gray-700 hover:border-gray-600'
                    }`}
                  >
                    <Icon className={`w-6 h-6 mx-auto mb-2 ${isSelected ? 'text-amber-500' : 'text-gray-400'}`} />
                    <div className={`text-sm font-medium ${isSelected ? 'text-amber-500' : 'text-gray-300'}`}>
                      {config.label}
                    </div>
                    {hasActive && (
                      <div className="text-xs text-green-500 mt-1">Active</div>
                    )}
                  </button>
                )
              })}
            </div>

            {/* Intention Input */}
            <div className="mb-6">
              <label className="block text-sm text-gray-400 mb-2">
                What would you like to focus on?
              </label>
              <textarea
                value={intentionText}
                onChange={(e) => setIntentionText(e.target.value)}
                placeholder="e.g., I want to grow in patience with my family, especially during stressful moments..."
                className="w-full h-32 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-amber-500 resize-none"
              />
              <p className="text-xs text-gray-500 mt-2">
                Be specific about your intention. The AI will curate scripture passages that speak directly to your focus.
              </p>
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={() => setShowNewFocus(false)}
                className="flex-1 py-2 px-4 border border-gray-700 text-gray-300 rounded-lg hover:bg-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateFocus}
                disabled={!intentionText.trim() || createFocus.isPending}
                className="flex-1 py-2 px-4 bg-amber-500 text-black font-medium rounded-lg hover:bg-amber-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                {createFocus.isPending ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Creating...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    Create Focus
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Active Intentions */}
      {activeIntentions && activeIntentions.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <Calendar className="w-5 h-5 text-amber-500" />
            Active Focus Intentions
          </h2>
          <div className="grid gap-4">
            {activeIntentions.map((intention) => (
              <IntentionCard 
                key={intention.id} 
                intention={intention} 
                onThemeClick={(theme) => setSelectedTheme(theme)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Today's Passages */}
      {todayData?.todays_passages && todayData.todays_passages.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-amber-500" />
            Today's Devotional
          </h2>
          <div className="space-y-6">
            {todayData.todays_passages.map((passage) => (
              <PassageCard 
                key={passage.id} 
                passage={passage}
                onReflect={() => {
                  setSelectedPassage(passage)
                  setReflectionText(passage.user_reflection || '')
                }}
                onMarkRead={() => markRead.mutate(passage.id)}
                onDeepDive={() => handleGenerateDeepDive(passage)}
                isDeepDiveLoading={passageDeepDive.isPending && deepDivePassage?.id === passage.id}
              />
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {(!activeIntentions || activeIntentions.length === 0) && (
        <div className="text-center py-16 bg-gray-900/50 rounded-xl border border-gray-800">
          <Book className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">
            Start Your Devotional Journey
          </h3>
          <p className="text-gray-400 max-w-md mx-auto mb-6">
            Set a focus intention and receive AI-curated scripture passages 
            tailored to your spiritual needs.
          </p>
          <button
            onClick={() => setShowNewFocus(true)}
            className="inline-flex items-center gap-2 px-6 py-3 bg-amber-500 text-black font-medium rounded-lg hover:bg-amber-400 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Set Your First Focus
          </button>
        </div>
      )}

      {/* Reflection Modal */}
      {selectedPassage && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-xl p-6 max-w-2xl w-full border border-gray-800 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-xl font-semibold text-white">
                  Reflect on This Passage
                </h2>
                <p className="text-amber-500 mt-1">
                  {selectedPassage.scripture_reference}
                </p>
              </div>
              <button
                onClick={() => setSelectedPassage(null)}
                className="text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            {/* Passage Quote */}
            <div className="bg-gray-800/50 rounded-lg p-4 mb-4 border-l-4 border-amber-500">
              <p className="text-gray-200 italic whitespace-pre-line">
                {selectedPassage.stylized_quote || selectedPassage.scripture_text}
              </p>
              <p className="text-gray-500 text-sm mt-2">
                — {selectedPassage.scripture_reference} ({selectedPassage.translation})
              </p>
            </div>

            {/* Reflection Prompts */}
            {selectedPassage.reflection_prompts.length > 0 && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4" />
                  Reflection Prompts
                </h3>
                <ul className="space-y-2">
                  {selectedPassage.reflection_prompts.map((prompt, i) => (
                    <li key={i} className="text-gray-300 text-sm pl-4 border-l-2 border-gray-700">
                      {prompt}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Reflection Input */}
            <div className="mb-4">
              <label className="block text-sm text-gray-400 mb-2 flex items-center gap-2">
                <PenLine className="w-4 h-4" />
                Your Reflection
              </label>
              <textarea
                value={reflectionText}
                onChange={(e) => setReflectionText(e.target.value)}
                placeholder="Write your thoughts, prayers, or insights..."
                className="w-full h-40 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-amber-500 resize-none"
              />
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={() => setSelectedPassage(null)}
                className="flex-1 py-2 px-4 border border-gray-700 text-gray-300 rounded-lg hover:bg-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveReflection}
                disabled={!reflectionText.trim() || saveReflection.isPending}
                className="flex-1 py-2 px-4 bg-amber-500 text-black font-medium rounded-lg hover:bg-amber-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                {saveReflection.isPending ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Saving...
                  </>
                ) : (
                  <>
                    <Check className="w-4 h-4" />
                    Save Reflection
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Theme Scriptures Modal */}
      {selectedTheme && THEME_SCRIPTURES[selectedTheme] && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-xl p-6 max-w-2xl w-full border border-gray-800 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-xl font-semibold text-white">
                  {THEME_SCRIPTURES[selectedTheme].title}
                </h2>
                <p className="text-gray-400 text-sm mt-1">
                  Explore these passages to deepen your understanding
                </p>
              </div>
              <button
                onClick={() => setSelectedTheme(null)}
                className="text-gray-400 hover:text-white p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              {THEME_SCRIPTURES[selectedTheme].passages.map((passage, i) => (
                <button
                  key={i}
                  onClick={() => {
                    navigate(`/bible?passage=${encodeURIComponent(passage.ref)}`)
                    setSelectedTheme(null)
                  }}
                  className="w-full text-left p-4 bg-gray-800/50 hover:bg-gray-800 border border-gray-700 hover:border-amber-500/50 rounded-lg transition-all group"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-amber-500 font-semibold group-hover:text-amber-400">
                        {passage.ref}
                      </h3>
                      <p className="text-gray-400 text-sm mt-1">
                        {passage.summary}
                      </p>
                    </div>
                    <ExternalLink className="w-4 h-4 text-gray-500 group-hover:text-amber-500 flex-shrink-0 mt-1" />
                  </div>
                </button>
              ))}
            </div>

            <div className="mt-6 pt-4 border-t border-gray-800">
              <p className="text-gray-500 text-xs text-center">
                Click any passage to read it in the Bible reader
              </p>
            </div>
          </div>
        </div>
      )}

      {deepDivePassage && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-xl p-6 max-w-3xl w-full border border-gray-800 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-xl font-semibold text-white">Personalized Study Guide</h2>
                <p className="text-amber-500 mt-1">{deepDivePassage.scripture_reference}</p>
              </div>
              <button
                onClick={closeDeepDive}
                className="text-gray-400 hover:text-white p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {passageDeepDive.isPending && (
              <div className="py-12 text-center">
                <Loader2 className="w-8 h-8 text-amber-500 animate-spin mx-auto" />
                <p className="text-gray-400 mt-4">Generating your deep dive study guide...</p>
              </div>
            )}

            {deepDiveError && !passageDeepDive.isPending && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 text-red-300">
                {deepDiveError}
              </div>
            )}

            {deepDiveGuide && !passageDeepDive.isPending && (
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

                <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-4">
                  <h3 className="text-amber-400 font-semibold mb-2">{deepDiveGuide.title}</h3>
                  <p className="text-gray-200 text-sm leading-relaxed">{deepDiveGuide.insight_summary}</p>
                </div>

                {deepDiveGuide.analytical_insights.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-400 mb-2">Analytical Insights</h4>
                    <ul className="space-y-2">
                      {deepDiveGuide.analytical_insights.map((insight, index) => (
                        <li key={index} className="text-gray-300 text-sm flex items-start gap-2">
                          <span className="text-amber-500">•</span>
                          <span>{insight}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {deepDiveGuide.heart_check_questions.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-400 mb-2">Heart-Check Questions</h4>
                    <ul className="space-y-2">
                      {deepDiveGuide.heart_check_questions.map((question, index) => (
                        <li key={index} className="text-gray-300 text-sm flex items-start gap-2">
                          <span className="text-purple-400">?</span>
                          <span>{question}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {deepDiveGuide.study_plan.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-400 mb-3">3-Day Action Plan</h4>
                    <div className="space-y-3">
                      {deepDiveGuide.study_plan.map((day) => (
                        <div key={day.day} className="bg-gray-800/50 border border-gray-700 rounded-lg p-4">
                          <p className="text-amber-500 text-sm font-semibold">Day {day.day}: {day.focus}</p>
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

function IntentionCard({ intention, onThemeClick }: { intention: FocusIntention; onThemeClick: (theme: string) => void }) {
  const config = periodConfig[intention.period_type]
  const Icon = config.icon

  return (
    <div className="bg-gray-900/50 rounded-xl p-5 border border-gray-800">
      <div className="flex items-start gap-4">
        <div className="p-3 bg-amber-500/10 rounded-lg">
          <Icon className="w-6 h-6 text-amber-500" />
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-sm font-medium text-amber-500">{config.label}</span>
            <span className="text-xs text-gray-500">
              {intention.period_start} - {intention.period_end}
            </span>
          </div>
          <p className="text-gray-200 mb-3">{intention.intention_text}</p>
          
          {/* Themes - clickable to show related scriptures */}
          {intention.themes.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-3">
              {intention.themes.map((theme, i) => {
                const themeKey = theme.toLowerCase()
                const hasScriptures = THEME_SCRIPTURES[themeKey]
                return (
                  <button
                    key={i}
                    onClick={() => {
                      if (hasScriptures) onThemeClick(themeKey)
                    }}
                    className={`px-2 py-1 text-xs rounded-full transition-colors ${
                      hasScriptures 
                        ? 'bg-amber-500/20 text-amber-400 hover:bg-amber-500/30 cursor-pointer' 
                        : 'bg-gray-800 text-gray-400'
                    }`}
                    title={hasScriptures ? `View scriptures about ${theme}` : theme}
                  >
                    {theme}
                    {hasScriptures && <span className="ml-1">→</span>}
                  </button>
                )
              })}
            </div>
          )}

          {/* Progress */}
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <BookOpen className="w-4 h-4" />
            <span>{intention.passages_count} passages</span>
            {intention.passages_generated && (
              <span className="text-green-500 flex items-center gap-1">
                <Check className="w-3 h-3" />
                Ready
              </span>
            )}
          </div>
        </div>
        <ChevronRight className="w-5 h-5 text-gray-600" />
      </div>
    </div>
  )
}

function PassageCard({ 
  passage, 
  onReflect,
  onMarkRead,
  onDeepDive,
  isDeepDiveLoading,
}: { 
  passage: DevotionalPassage
  onReflect: () => void
  onMarkRead: () => void
  onDeepDive: () => void
  isDeepDiveLoading: boolean
}) {
  return (
    <div className={`bg-gray-900/50 rounded-xl border ${passage.is_read ? 'border-green-500/30' : 'border-gray-800'}`}>
      {/* Header */}
      <div className="p-5 border-b border-gray-800">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-semibold text-amber-500">
              {passage.scripture_reference}
            </h3>
            <p className="text-sm text-gray-500">{passage.translation}</p>
          </div>
          {passage.is_read && (
            <span className="flex items-center gap-1 text-green-500 text-sm">
              <Check className="w-4 h-4" />
              Read
            </span>
          )}
        </div>
      </div>

      {/* Quote */}
      <div className="p-5 bg-gradient-to-br from-amber-500/5 to-transparent">
        <Quote className="w-8 h-8 text-amber-500/30 mb-2" />
        <p className="text-gray-200 text-lg leading-relaxed whitespace-pre-line">
          {passage.stylized_quote || passage.scripture_text}
        </p>
      </div>

      {/* Context & Connection */}
      <div className="p-5 space-y-4 border-t border-gray-800">
        {passage.context_note && (
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-1">Historical Context</h4>
            <p className="text-gray-300 text-sm">{passage.context_note}</p>
          </div>
        )}
        
        <div>
          <h4 className="text-sm font-medium text-gray-400 mb-1">Connection to Your Focus</h4>
          <p className="text-gray-300 text-sm">{passage.connection_to_focus}</p>
        </div>

        {/* Application Suggestions */}
        {passage.application_suggestions.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-2">Practical Applications</h4>
            <ul className="space-y-1">
              {passage.application_suggestions.map((suggestion, i) => (
                <li key={i} className="text-gray-300 text-sm flex items-start gap-2">
                  <span className="text-amber-500">•</span>
                  {suggestion}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="p-5 border-t border-gray-800 flex flex-wrap gap-3">
        {!passage.is_read && (
          <button
            onClick={onMarkRead}
            className="flex-1 min-w-[180px] py-2 px-4 border border-gray-700 text-gray-300 rounded-lg hover:bg-gray-800 transition-colors flex items-center justify-center gap-2"
          >
            <Check className="w-4 h-4" />
            Mark as Read
          </button>
        )}
        <button
          onClick={onReflect}
          className="flex-1 min-w-[180px] py-2 px-4 bg-amber-500/20 text-amber-500 rounded-lg hover:bg-amber-500/30 transition-colors flex items-center justify-center gap-2"
        >
          <PenLine className="w-4 h-4" />
          {passage.user_reflection ? 'Edit Reflection' : 'Write Reflection'}
        </button>
        <button
          onClick={onDeepDive}
          disabled={isDeepDiveLoading}
          className="flex-1 min-w-[180px] py-2 px-4 bg-purple-500/20 text-purple-400 rounded-lg hover:bg-purple-500/30 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {isDeepDiveLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
          Deep Dive
        </button>
      </div>

      {/* Existing Reflection */}
      {passage.user_reflection && (
        <div className="px-5 pb-5">
          <div className="bg-gray-800/50 rounded-lg p-4 border-l-4 border-green-500">
            <h4 className="text-sm font-medium text-green-500 mb-2">Your Reflection</h4>
            <p className="text-gray-300 text-sm whitespace-pre-line">{passage.user_reflection}</p>
          </div>
        </div>
      )}
    </div>
  )
}
