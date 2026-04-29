import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { format } from 'date-fns'
import { 
  BookOpen, 
  Heart, 
  AlertTriangle, 
  Sparkles, 
  ChevronRight,
  Loader2,
  CheckCircle,
  MessageCircle
} from 'lucide-react'
import { 
  useTodayContext, 
  useCreateReflection, 
  useLifeAreas,
  useGenerateInsight,
  useRespondToThread
} from '../hooks/useReflections'
import { ThreadPrompt } from '../api/reflections'

interface AreaScore {
  code: string
  name: string
  score: number
}

export default function ReflectionPage() {
  const navigate = useNavigate()
  const { data: todayContext, isLoading: contextLoading } = useTodayContext()
  const { data: lifeAreas } = useLifeAreas()
  const createReflection = useCreateReflection()
  const respondToThread = useRespondToThread()

  const [step, setStep] = useState<'scripture' | 'reflection' | 'areas' | 'threads' | 'complete'>('scripture')
  const [scriptureReference, setScriptureReference] = useState('')
  const [reflectionContent, setReflectionContent] = useState('')
  const [gratitudeNote, setGratitudeNote] = useState('')
  const [struggleNote, setStruggleNote] = useState('')
  const [tomorrowIntention, setTomorrowIntention] = useState('')
  const [areaScores, setAreaScores] = useState<AreaScore[]>([])
  const [threadResponses, setThreadResponses] = useState<Record<string, string>>({})
  const [createdReflectionId, setCreatedReflectionId] = useState<string | null>(null)

  // Initialize area scores when life areas load
  useEffect(() => {
    if (lifeAreas && areaScores.length === 0) {
      setAreaScores(
        lifeAreas.map((area) => ({
          code: area.code,
          name: area.name,
          score: 5,
        }))
      )
    }
  }, [lifeAreas, areaScores.length])

  // Initialize scripture from context
  useEffect(() => {
    if (todayContext?.scripture?.reference && !scriptureReference) {
      setScriptureReference(todayContext.scripture.reference)
    }
  }, [todayContext, scriptureReference])

  // If there's already a reflection for today, redirect to view it
  useEffect(() => {
    if (todayContext?.existing_reflection) {
      navigate(`/reflection/${todayContext.existing_reflection.id}`)
    }
  }, [todayContext, navigate])

  const handleAreaScoreChange = (code: string, score: number) => {
    setAreaScores((prev) =>
      prev.map((area) => (area.code === code ? { ...area, score } : area))
    )
  }

  const handleThreadResponse = (threadId: string, response: string) => {
    setThreadResponses((prev) => ({ ...prev, [threadId]: response }))
  }

  const handleSubmit = async () => {
    const scores: Record<string, number> = {}
    areaScores.forEach((area) => {
      scores[area.code] = area.score
    })

    try {
      const reflection = await createReflection.mutateAsync({
        date: format(new Date(), 'yyyy-MM-dd'),
        scripture_reference: scriptureReference,
        reflection_content: reflectionContent,
        area_scores: scores,
        gratitude_note: gratitudeNote,
        struggle_note: struggleNote,
        tomorrow_intention: tomorrowIntention,
      })

      setCreatedReflectionId(reflection.id)

      // Submit thread responses
      for (const [threadId, response] of Object.entries(threadResponses)) {
        if (response && response !== 'skip') {
          await respondToThread.mutateAsync({
            thread_id: threadId,
            response,
            reflection_id: reflection.id,
          })
        }
      }

      setStep('complete')
    } catch (error) {
      console.error('Failed to create reflection:', error)
    }
  }

  if (contextLoading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-accent-primary" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg-primary p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-text-primary">
            {format(new Date(), 'EEEE, MMMM d')}
          </h1>
          {todayContext?.journey && (
            <p className="text-text-secondary mt-1">
              Day {todayContext.journey.current_day} of {todayContext.journey.duration_days}
            </p>
          )}
        </div>

        {/* Progress Steps */}
        <div className="flex items-center gap-2 mb-8">
          {['scripture', 'reflection', 'areas', 'threads', 'complete'].map((s, i) => (
            <div key={s} className="flex items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  step === s
                    ? 'bg-accent-primary text-white'
                    : i < ['scripture', 'reflection', 'areas', 'threads', 'complete'].indexOf(step)
                    ? 'bg-green-500 text-white'
                    : 'bg-bg-secondary text-text-secondary'
                }`}
              >
                {i < ['scripture', 'reflection', 'areas', 'threads', 'complete'].indexOf(step) ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  i + 1
                )}
              </div>
              {i < 4 && <ChevronRight className="w-4 h-4 text-text-secondary mx-1" />}
            </div>
          ))}
        </div>

        {/* Step Content */}
        <div className="bg-bg-secondary rounded-xl p-6 shadow-lg">
          {step === 'scripture' && (
            <div className="space-y-6">
              <div className="flex items-center gap-3 text-accent-primary">
                <BookOpen className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Today's Scripture</h2>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">
                  Scripture Reference
                </label>
                <input
                  type="text"
                  value={scriptureReference}
                  onChange={(e) => setScriptureReference(e.target.value)}
                  placeholder="e.g., Proverbs 3:5-6"
                  className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary"
                />
              </div>

              {todayContext?.scripture?.theme && (
                <div className="p-4 bg-bg-primary rounded-lg border border-border-primary">
                  <p className="text-sm text-text-secondary">Today's Theme</p>
                  <p className="text-text-primary font-medium">{todayContext.scripture.theme}</p>
                </div>
              )}

              <button
                onClick={() => setStep('reflection')}
                disabled={!scriptureReference}
                className="w-full py-3 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Continue
              </button>
            </div>
          )}

          {step === 'reflection' && (
            <div className="space-y-6">
              <div className="flex items-center gap-3 text-accent-primary">
                <MessageCircle className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Your Reflection</h2>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">
                  How did this scripture speak to you today?
                </label>
                <textarea
                  value={reflectionContent}
                  onChange={(e) => setReflectionContent(e.target.value)}
                  rows={6}
                  placeholder="Share your thoughts, insights, and how this applies to your life..."
                  className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary resize-none"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">
                  <Heart className="w-4 h-4 inline mr-1" />
                  What are you grateful for?
                </label>
                <input
                  type="text"
                  value={gratitudeNote}
                  onChange={(e) => setGratitudeNote(e.target.value)}
                  placeholder="One thing you're thankful for today..."
                  className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">
                  <AlertTriangle className="w-4 h-4 inline mr-1" />
                  Any struggles today?
                </label>
                <input
                  type="text"
                  value={struggleNote}
                  onChange={(e) => setStruggleNote(e.target.value)}
                  placeholder="Something you're working through..."
                  className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">
                  Tomorrow's intention
                </label>
                <input
                  type="text"
                  value={tomorrowIntention}
                  onChange={(e) => setTomorrowIntention(e.target.value)}
                  placeholder="One thing you want to focus on tomorrow..."
                  className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary"
                />
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setStep('scripture')}
                  className="flex-1 py-3 bg-bg-primary text-text-primary rounded-lg font-medium hover:bg-bg-primary/80"
                >
                  Back
                </button>
                <button
                  onClick={() => setStep('areas')}
                  disabled={!reflectionContent}
                  className="flex-1 py-3 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Continue
                </button>
              </div>
            </div>
          )}

          {step === 'areas' && (
            <div className="space-y-6">
              <div className="flex items-center gap-3 text-accent-primary">
                <Sparkles className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Life Area Check-in</h2>
              </div>

              <p className="text-text-secondary text-sm">
                Rate how aligned you felt in each area today (1-10)
              </p>

              <div className="space-y-4">
                {areaScores.map((area) => (
                  <div key={area.code} className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-text-primary font-medium">{area.name}</span>
                      <span className="text-accent-primary font-bold">{area.score}</span>
                    </div>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={area.score}
                      onChange={(e) => handleAreaScoreChange(area.code, parseInt(e.target.value))}
                      className="w-full h-2 bg-bg-primary rounded-lg appearance-none cursor-pointer accent-accent-primary"
                    />
                  </div>
                ))}
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setStep('reflection')}
                  className="flex-1 py-3 bg-bg-primary text-text-primary rounded-lg font-medium hover:bg-bg-primary/80"
                >
                  Back
                </button>
                <button
                  onClick={() => {
                    if (todayContext?.thread_prompts && todayContext.thread_prompts.length > 0) {
                      setStep('threads')
                    } else {
                      handleSubmit()
                    }
                  }}
                  className="flex-1 py-3 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary/90"
                >
                  {todayContext?.thread_prompts && todayContext.thread_prompts.length > 0
                    ? 'Continue'
                    : 'Complete Reflection'}
                </button>
              </div>
            </div>
          )}

          {step === 'threads' && todayContext?.thread_prompts && (
            <div className="space-y-6">
              <div className="flex items-center gap-3 text-accent-primary">
                <MessageCircle className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Follow-up Check-in</h2>
              </div>

              <p className="text-text-secondary text-sm">
                Let's check in on some things you mentioned before
              </p>

              <div className="space-y-6">
                {todayContext.thread_prompts.map((prompt: ThreadPrompt) => (
                  <div key={prompt.thread_id} className="p-4 bg-bg-primary rounded-lg border border-border-primary">
                    <p className="text-text-primary font-medium mb-3">{prompt.prompt}</p>
                    <div className="flex flex-wrap gap-2">
                      {prompt.response_options.map((option) => (
                        <button
                          key={option}
                          onClick={() => handleThreadResponse(prompt.thread_id, option)}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                            threadResponses[prompt.thread_id] === option
                              ? 'bg-accent-primary text-white'
                              : 'bg-bg-secondary text-text-primary hover:bg-bg-secondary/80'
                          }`}
                        >
                          {option.charAt(0).toUpperCase() + option.slice(1)}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setStep('areas')}
                  className="flex-1 py-3 bg-bg-primary text-text-primary rounded-lg font-medium hover:bg-bg-primary/80"
                >
                  Back
                </button>
                <button
                  onClick={handleSubmit}
                  disabled={createReflection.isPending}
                  className="flex-1 py-3 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary/90 disabled:opacity-50"
                >
                  {createReflection.isPending ? (
                    <Loader2 className="w-5 h-5 animate-spin mx-auto" />
                  ) : (
                    'Complete Reflection'
                  )}
                </button>
              </div>
            </div>
          )}

          {step === 'complete' && (
            <CompleteStep reflectionId={createdReflectionId} />
          )}
        </div>
      </div>
    </div>
  )
}

function CompleteStep({ reflectionId }: { reflectionId: string | null }) {
  const navigate = useNavigate()
  const generateInsight = useGenerateInsight(reflectionId || '')
  const [insight, setInsight] = useState<string | null>(null)

  const handleGenerateInsight = async () => {
    if (!reflectionId) return
    try {
      const result = await generateInsight.mutateAsync()
      setInsight(result.insight)
    } catch (error) {
      console.error('Failed to generate insight:', error)
    }
  }

  return (
    <div className="space-y-6 text-center">
      <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto">
        <CheckCircle className="w-10 h-10 text-white" />
      </div>

      <div>
        <h2 className="text-2xl font-bold text-text-primary">Reflection Complete!</h2>
        <p className="text-text-secondary mt-2">
          Great job taking time to reflect today.
        </p>
      </div>

      {!insight && (
        <button
          onClick={handleGenerateInsight}
          disabled={generateInsight.isPending}
          className="w-full py-3 bg-accent-secondary text-white rounded-lg font-medium hover:bg-accent-secondary/90 disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {generateInsight.isPending ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating insight...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Get AI Insight
            </>
          )}
        </button>
      )}

      {insight && (
        <div className="p-4 bg-accent-primary/10 rounded-lg border border-accent-primary/20 text-left">
          <div className="flex items-center gap-2 text-accent-primary mb-2">
            <Sparkles className="w-5 h-5" />
            <span className="font-medium">AI Insight</span>
          </div>
          <p className="text-text-primary">{insight}</p>
        </div>
      )}

      <button
        onClick={() => navigate('/')}
        className="w-full py-3 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary/90"
      >
        Return to Dashboard
      </button>
    </div>
  )
}
