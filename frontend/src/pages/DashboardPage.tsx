import { useEffect, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import client from '../api/client'
import confetti from 'canvas-confetti'
import { 
  Flame, BookOpen, ChevronRight, Target, Calendar, 
  Highlighter, PenLine, TrendingUp, TrendingDown, Minus,
  Sparkles, MessageCircle, Loader2, BookMarked, Clock, Trophy,
  Heart, Compass, CheckCircle2
} from 'lucide-react'
import DailyPulseCard from '../components/DailyPulseCard'
import StreakSaverModal from '../components/StreakSaverModal'
import HeartPromptExplorer from '../components/HeartPromptExplorer'

interface DashboardStats {
  date: string
  greeting_name: string
  focus: {
    intention: string
    themes: string[]
    period_type: string
    day_number: number
    total_days: number
    passages_count: number
    passages_read: number
  } | null
  reading_plan: {
    plan_title: string
    current_day: number
    total_days: number
    completed_days: number
  } | null
  stats: {
    journal_streak: number
    journal_today: number
    journal_week: number
    journal_month: number
    highlights_today: number
    highlights_week: number
    reflections_week: number
    open_threads: number
  }
  recent_highlights: Array<{
    book: string
    chapter: number
    verse: number
    note: string
    color: string
  }>
  life_area_scores: Array<{
    area: string
    score: number
    trend: string
  }>
  weekly_insight: string | null
}

const fetchDashboardStats = async (): Promise<DashboardStats> => {
  const response = await client.get('/dashboard/stats/')
  return response.data
}

function TrendIcon({ trend }: { trend: string }) {
  if (trend === 'improving') return <TrendingUp className="w-4 h-4 text-green-500" />
  if (trend === 'declining') return <TrendingDown className="w-4 h-4 text-red-500" />
  return <Minus className="w-4 h-4 text-gray-500" />
}

function ProgressBar({ value, max, color = 'amber' }: { value: number; max: number; color?: string }) {
  const percentage = Math.min((value / max) * 100, 100)
  const colorClasses = {
    amber: 'bg-amber-500',
    green: 'bg-green-500',
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
  }
  return (
    <div className="w-full bg-gray-700 rounded-full h-2">
      <div 
        className={`h-2 rounded-full transition-all duration-500 ${colorClasses[color as keyof typeof colorClasses] || colorClasses.amber}`}
        style={{ width: `${percentage}%` }}
      />
    </div>
  )
}

interface Milestone {
  id: string
  title: string
  description: string
  progress: number
  target: number
  completed: boolean
}

const fetchMilestones = async () => {
  const response = await client.get('/milestones/')
  return response.data
}

const fetchFocusToday = async () => {
  const response = await client.get('/focus/today/')
  return response.data
}

const fireCelebration = () => {
  // Brand colors: Amber, Purple, Green
  const colors = ['#f59e0b', '#8b5cf6', '#10b981']
  
  confetti({
    particleCount: 120,
    spread: 70,
    origin: { y: 0.6 },
    colors,
  })
  
  // Second burst for extra effect
  setTimeout(() => {
    confetti({
      particleCount: 80,
      spread: 100,
      origin: { y: 0.7, x: 0.3 },
      colors,
    })
    confetti({
      particleCount: 80,
      spread: 100,
      origin: { y: 0.7, x: 0.7 },
      colors,
    })
  }, 200)
}

// Pre-defined focus suggestions for onboarding
const FOCUS_SUGGESTIONS = [
  { text: 'Finding peace in anxiety', themes: ['Peace', 'Trust', 'Surrender'] },
  { text: 'Building consistency in faith', themes: ['Discipline', 'Growth', 'Faithfulness'] },
  { text: 'Deepening my relationship with God', themes: ['Prayer', 'Intimacy', 'Presence'] },
  { text: 'Overcoming fear and doubt', themes: ['Courage', 'Faith', 'Trust'] },
]

export default function DashboardPage() {
  const { t } = useTranslation()
  const { user } = useAuth()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const hasCelebrated = useRef(false)
  const [wizardStep, setWizardStep] = useState<'idle' | 'focus' | 'plan' | 'complete'>('idle')
  const [wizardDismissed, setWizardDismissed] = useState(false)
  const [showStreakSaver, setShowStreakSaver] = useState(false)

  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: fetchDashboardStats,
    staleTime: 60000, // 1 minute
    refetchOnWindowFocus: true,
  })

  const { data: milestonesData } = useQuery({
    queryKey: ['milestones'],
    queryFn: fetchMilestones,
    staleTime: 60000,
  })

  const { data: focusToday } = useQuery({
    queryKey: ['focus-today'],
    queryFn: fetchFocusToday,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })

  // Check for newly completed milestones and celebrate
  useEffect(() => {
    if (!milestonesData?.achievements || hasCelebrated.current) return

    const achievements = milestonesData.achievements as Milestone[]
    const storedMilestones = localStorage.getItem('celebratedMilestones')
    const celebrated: Record<string, boolean> = storedMilestones ? JSON.parse(storedMilestones) : {}

    // Find newly completed milestones
    const newlyCompleted = achievements.filter(
      (m: Milestone) => m.completed && !celebrated[m.id]
    )

    if (newlyCompleted.length > 0) {
      // Fire confetti!
      fireCelebration()
      hasCelebrated.current = true

      // Mark as celebrated
      newlyCompleted.forEach((m: Milestone) => {
        celebrated[m.id] = true
      })
      localStorage.setItem('celebratedMilestones', JSON.stringify(celebrated))
    }
  }, [milestonesData])

  // Create focus mutation for onboarding wizard
  const createFocusMutation = useMutation({
    mutationFn: async (focus: { text: string; themes: string[] }) => {
      const response = await client.post('/focus/', {
        intention_text: focus.text,
        themes: focus.themes,
        period_type: 'weekly',
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      queryClient.invalidateQueries({ queryKey: ['activeFocus'] })
      setWizardStep('plan')
    },
  })

  // Detect if user is new (no focus, no plan, no streak)
  const isNewUser = !stats?.focus && !stats?.reading_plan && 
    (stats?.stats.journal_streak === 0 || stats?.stats.journal_streak === undefined)

  // Show wizard for new users
  const showWizard = isNewUser && !wizardDismissed && wizardStep !== 'complete'

  // Initialize wizard step
  useEffect(() => {
    if (isNewUser && wizardStep === 'idle') {
      setWizardStep('focus')
    }
  }, [isNewUser, wizardStep])

  const handleFocusSelect = (focus: { text: string; themes: string[] }) => {
    createFocusMutation.mutate(focus)
  }

  const handleSkipWizard = () => {
    setWizardDismissed(true)
  }

  // Streak Saver Modal logic
  useEffect(() => {
    const dismissed = localStorage.getItem('streakSaverDismissed')
    const dismissedDate = localStorage.getItem('streakSaverDismissedDate')
    const today = new Date().toISOString().split('T')[0]
    
    const streak = stats?.stats.journal_streak || 0
    const journaledToday = stats?.stats.journal_today > 0
    const currentHour = new Date().getHours()
    
    if (
      streak >= 3 && 
      !journaledToday && 
      currentHour >= 18 &&
      (dismissed !== 'true' || dismissedDate !== today)
    ) {
      setShowStreakSaver(true)
    }
  }, [stats])

  const greeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) return t('dashboard.greeting')
    if (hour < 18) return 'Good afternoon'
    return 'Good evening'
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 text-amber-500 animate-spin" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400">Failed to load dashboard</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Onboarding Wizard for New Users */}
      {showWizard && (
        <div className="card bg-gradient-to-br from-amber-900/30 to-purple-900/20 border-2 border-amber-500/50 p-6">
          {wizardStep === 'focus' && (
            <>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-amber-500/20 rounded-full flex items-center justify-center">
                  <Compass className="w-6 h-6 text-amber-400" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-text-primary">Let's start your journey</h2>
                  <p className="text-text-secondary">What's on your heart right now?</p>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                {FOCUS_SUGGESTIONS.map((focus, i) => (
                  <button
                    key={i}
                    onClick={() => handleFocusSelect(focus)}
                    disabled={createFocusMutation.isPending}
                    className="p-4 bg-gray-800/50 hover:bg-gray-800 border border-gray-700 hover:border-amber-500/50 rounded-xl text-left transition-all group"
                  >
                    <p className="text-text-primary font-medium group-hover:text-amber-400 transition-colors">
                      {focus.text}
                    </p>
                    <div className="flex gap-1.5 mt-2">
                      {focus.themes.map((theme, j) => (
                        <span key={j} className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded">
                          {theme}
                        </span>
                      ))}
                    </div>
                  </button>
                ))}
              </div>

              <div className="flex items-center justify-between">
                <button
                  onClick={handleSkipWizard}
                  className="text-sm text-text-secondary hover:text-text-primary transition-colors"
                >
                  Skip for now
                </button>
                <button
                  onClick={() => navigate('/devotional')}
                  className="text-sm text-amber-400 hover:text-amber-300 transition-colors"
                >
                  Write my own focus →
                </button>
              </div>
            </>
          )}

          {wizardStep === 'plan' && (
            <>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center">
                  <CheckCircle2 className="w-6 h-6 text-green-400" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-text-primary">Great choice!</h2>
                  <p className="text-text-secondary">Now let's pick a reading path</p>
                </div>
              </div>

              <div className="p-4 bg-gray-800/50 border border-blue-500/30 rounded-xl mb-4">
                <div className="flex items-center gap-3">
                  <BookMarked className="w-8 h-8 text-blue-400" />
                  <div className="flex-1">
                    <p className="text-text-primary font-medium">Gospel of John - 7 Days</p>
                    <p className="text-text-secondary text-sm">A perfect introduction to Jesus' life and teachings</p>
                  </div>
                  <button
                    onClick={() => {
                      setWizardStep('complete')
                      navigate('/plans')
                    }}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-colors"
                  >
                    Start Plan
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <button
                  onClick={() => setWizardStep('complete')}
                  className="text-sm text-text-secondary hover:text-text-primary transition-colors"
                >
                  Skip for now
                </button>
                <button
                  onClick={() => {
                    setWizardStep('complete')
                    navigate('/plans')
                  }}
                  className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
                >
                  Browse all plans →
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">
            {greeting()}, {stats?.greeting_name || user?.display_name || 'Brother'}
          </h1>
          <p className="text-text-secondary mt-1">
            {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
          </p>
        </div>

        {/* Streak Badge */}
        <div className="card flex items-center gap-3 bg-gradient-to-r from-orange-500/20 to-amber-500/20 border-amber-500/30">
          <Flame className="w-8 h-8 text-amber-500" />
          <div>
            <div className="text-2xl font-bold text-text-primary">{stats?.stats.journal_streak || 0}</div>
            <div className="text-sm text-text-secondary">day streak</div>
          </div>
        </div>
      </div>

      {/* Daily Pulse Card */}
      {focusToday?.active_intentions?.length > 0 && focusToday?.todays_passages?.length > 0 && (
        <DailyPulseCard
          focus={{
            intention: focusToday.active_intentions[0].intention_text,
            themes: focusToday.active_intentions[0].themes,
            day_number: stats?.focus?.day_number || 1,
            total_days: stats?.focus?.total_days || 7,
          }}
          todaysVerse={{
            reference: focusToday.todays_passages[0].scripture_reference,
            text: focusToday.todays_passages[0].scripture_text,
            passage_id: focusToday.todays_passages[0].id,
            is_read: focusToday.todays_passages[0].is_read,
          }}
        />
      )}

      {/* Speak Your Mind — Freeform Prompt */}
      <HeartPromptExplorer />

      {/* Today's Spiritual Snapshot */}
      <div className="card bg-gradient-to-br from-gray-800 to-gray-900 border-amber-500/20">
        <div className="flex items-center gap-2 mb-4">
          <Calendar className="w-5 h-5 text-amber-500" />
          <h2 className="text-lg font-semibold text-text-primary">Today's Spiritual Snapshot</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Focus Card */}
          {stats?.focus ? (
            <Link to="/devotional" className="p-4 bg-gray-800/50 rounded-lg border border-purple-500/30 hover:border-purple-400 transition-colors cursor-pointer group">
              <div className="flex items-center gap-2 mb-2">
                <Target className="w-4 h-4 text-purple-400" />
                <span className="text-sm font-medium text-purple-400">Focus</span>
                <ChevronRight className="w-4 h-4 text-purple-400 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              <p className="text-text-primary font-medium mb-1 line-clamp-1">{stats.focus.intention}</p>
              <div className="flex items-center gap-2 text-sm text-text-secondary">
                <span>Day {stats.focus.day_number} of {stats.focus.total_days}</span>
              </div>
              <ProgressBar value={stats.focus.day_number} max={stats.focus.total_days} color="purple" />
              <div className="flex flex-wrap gap-1 mt-2">
                {stats.focus.themes.slice(0, 3).map((theme, i) => (
                  <span key={i} className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded">
                    {theme}
                  </span>
                ))}
              </div>
            </Link>
          ) : (
            <Link 
              to="/devotional" 
              className="p-6 bg-purple-900/10 border border-purple-500/20 rounded-lg hover:border-purple-500/40 transition-colors group"
            >
              <div className="text-center">
                <Target className="w-10 h-10 text-purple-400 mx-auto mb-3 group-hover:scale-110 transition-transform" />
                <h3 className="text-lg font-semibold text-text-primary mb-2">
                  What focus is on your heart?
                </h3>
                <p className="text-text-secondary mb-4 max-w-sm mx-auto">
                  Set a focus to personalize your daily devotions and scripture recommendations.
                </p>
                <span className="inline-block px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg font-medium transition-colors">
                  Set Your Focus →
                </span>
              </div>
            </Link>
          )}

          {/* Reading Plan Card */}
          {stats?.reading_plan ? (
            <Link to="/plans" className="p-4 bg-gray-800/50 rounded-lg border border-blue-500/30 hover:border-blue-400 transition-colors cursor-pointer group">
              <div className="flex items-center gap-2 mb-2">
                <BookMarked className="w-4 h-4 text-blue-400" />
                <span className="text-sm font-medium text-blue-400">Reading Plan</span>
                <ChevronRight className="w-4 h-4 text-blue-400 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              <p className="text-text-primary font-medium mb-1 line-clamp-1">{stats.reading_plan.plan_title}</p>
              <div className="flex items-center gap-2 text-sm text-text-secondary">
                <span>Day {stats.reading_plan.current_day} of {stats.reading_plan.total_days}</span>
              </div>
              <ProgressBar value={stats.reading_plan.completed_days} max={stats.reading_plan.total_days} color="blue" />
            </Link>
          ) : (
            <Link 
              to="/plans" 
              className="p-6 bg-blue-900/10 border border-blue-500/20 rounded-lg hover:border-blue-500/40 transition-colors group"
            >
              <div className="text-center">
                <BookMarked className="w-10 h-10 text-blue-400 mx-auto mb-3 group-hover:scale-110 transition-transform" />
                <h3 className="text-lg font-semibold text-text-primary mb-2">
                  Ready for a Guided Journey?
                </h3>
                <p className="text-text-secondary mb-4 max-w-sm mx-auto">
                  Start with "Gospel of John - 7 Days" or browse all plans.
                </p>
                <span className="inline-block px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-colors">
                  Browse Plans →
                </span>
              </div>
            </Link>
          )}

          {/* Today's Activity Card */}
          <div className="p-4 bg-gray-800/50 rounded-lg border border-amber-500/30">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span className="text-sm font-medium text-amber-400">Today's Activity</span>
            </div>
            <div className="space-y-2">
              <Link to="/bible" className="flex items-center justify-between hover:bg-gray-700/30 p-2 rounded transition-colors group">
                <span className="text-text-secondary text-sm flex items-center gap-1">
                  <Highlighter className="w-3 h-3" /> Highlights
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-text-primary font-medium">{stats?.stats.highlights_today || 0}</span>
                  <ChevronRight className="w-3 h-3 text-amber-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </Link>
              <Link to="/journal" className="flex items-center justify-between hover:bg-gray-700/30 p-2 rounded transition-colors group">
                <span className="text-text-secondary text-sm flex items-center gap-1">
                  <PenLine className="w-3 h-3" /> Journal entries
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-text-primary font-medium">{stats?.stats.journal_today || 0}</span>
                  <ChevronRight className="w-3 h-3 text-amber-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Weekly Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <Highlighter className="w-6 h-6 text-amber-500 mx-auto mb-2" />
          <div className="text-2xl font-bold text-text-primary">{stats?.stats.highlights_week || 0}</div>
          <div className="text-sm text-text-secondary">Highlights this week</div>
        </div>
        <div className="card text-center">
          <PenLine className="w-6 h-6 text-green-500 mx-auto mb-2" />
          <div className="text-2xl font-bold text-text-primary">{stats?.stats.journal_week || 0}</div>
          <div className="text-sm text-text-secondary">Journal entries</div>
        </div>
        <div className="card text-center">
          <BookOpen className="w-6 h-6 text-blue-500 mx-auto mb-2" />
          <div className="text-2xl font-bold text-text-primary">{stats?.stats.reflections_week || 0}</div>
          <div className="text-sm text-text-secondary">Reflections</div>
        </div>
        <div className="card text-center">
          <MessageCircle className="w-6 h-6 text-purple-500 mx-auto mb-2" />
          <div className="text-2xl font-bold text-text-primary">{stats?.stats.open_threads || 0}</div>
          <div className="text-sm text-text-secondary">Open threads</div>
        </div>
      </div>

      {/* Life Area Scores */}
      {stats?.life_area_scores && stats.life_area_scores.length > 0 && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-green-500" />
              Life Area Growth
            </h2>
            <Link to="/reflections" className="text-sm text-amber-500 hover:text-amber-400">
              View Details →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {stats.life_area_scores.map((area, i) => (
              <div key={i} className="flex items-center gap-3 p-3 bg-gray-800/50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-text-primary font-medium">{area.area}</span>
                    <div className="flex items-center gap-1">
                      <span className="text-text-secondary text-sm">{area.score}%</span>
                      <TrendIcon trend={area.trend} />
                    </div>
                  </div>
                  <ProgressBar value={area.score} max={100} color="green" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Highlights with Notes */}
      {stats?.recent_highlights && stats.recent_highlights.length > 0 && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
              <Highlighter className="w-5 h-5 text-amber-500" />
              Recent Notes
            </h2>
            <Link to="/journal" className="text-sm text-amber-500 hover:text-amber-400">
              View All →
            </Link>
          </div>
          <div className="space-y-3">
            {stats.recent_highlights.map((highlight, i) => (
              <div key={i} className="p-3 bg-gray-800/50 rounded-lg border-l-4 border-amber-500">
                <div className="text-sm text-amber-500 mb-1">
                  {highlight.book} {highlight.chapter}:{highlight.verse}
                </div>
                <p className="text-text-primary text-sm">{highlight.note}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link to="/devotional" className="card hover:border-purple-500/50 transition-colors group">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center group-hover:bg-purple-500/30 transition-colors">
              <Target className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h3 className="font-medium text-text-primary">Daily Devotional</h3>
              <p className="text-sm text-text-secondary">Continue your focus journey</p>
            </div>
            <ChevronRight className="w-5 h-5 text-text-secondary ml-auto" />
          </div>
        </Link>

        <Link to="/plans" className="card hover:border-blue-500/50 transition-colors group">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center group-hover:bg-blue-500/30 transition-colors">
              <BookOpen className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h3 className="font-medium text-text-primary">Reading Plans</h3>
              <p className="text-sm text-text-secondary">Structured Bible study</p>
            </div>
            <ChevronRight className="w-5 h-5 text-text-secondary ml-auto" />
          </div>
        </Link>

        <Link to="/journal/new" className="card hover:border-green-500/50 transition-colors group">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center group-hover:bg-green-500/30 transition-colors">
              <PenLine className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <h3 className="font-medium text-text-primary">New Journal Entry</h3>
              <p className="text-sm text-text-secondary">Capture your thoughts</p>
            </div>
            <ChevronRight className="w-5 h-5 text-text-secondary ml-auto" />
          </div>
        </Link>
      </div>

      {/* Streak Saver Modal */}
      <StreakSaverModal
        isOpen={showStreakSaver}
        streakCount={stats?.stats.journal_streak || 0}
        onDismiss={() => {
          localStorage.setItem('streakSaverDismissed', 'true')
          localStorage.setItem('streakSaverDismissedDate', new Date().toISOString().split('T')[0])
          setShowStreakSaver(false)
        }}
        onJournalNow={() => navigate('/journal/new')}
      />
    </div>
  )
}
