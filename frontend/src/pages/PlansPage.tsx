import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Book, Calendar, CheckCircle, Play, BookOpen, ArrowLeft } from 'lucide-react'
import {
  getPlans,
  getPlanDetail,
  enrollInPlan,
  getEnrolledPlans,
  getTodayReading,
  advanceDay,
  ReadingPlanDetail,
  UserPlanEnrollment,
  ReadingPlanDay,
} from '../api/plans'
import ScriptureReader from '../components/ScriptureReader'

const CATEGORIES = [
  { value: '', label: 'All Plans' },
  { value: 'general', label: 'General' },
  { value: 'faith', label: 'Faith Foundations' },
  { value: 'fatherhood', label: 'Fatherhood' },
  { value: 'leadership', label: 'Leadership' },
  { value: 'marriage', label: 'Marriage' },
  { value: 'recovery', label: 'Recovery' },
]

function formatPassage(passage: string | { book: string; chapter: number; verses?: string }): string {
  if (typeof passage === 'string') {
    return passage
  }
  const bookName = passage.book || 'Unknown'
  const chapter = passage.chapter || ''
  const verses = passage.verses ? `:${passage.verses}` : ''
  return `${bookName} ${chapter}${verses}`
}

interface ReadingContext {
  passage: string
  planId: string
  planTitle: string
  dayNumber: number
  theme: string
  enrollmentId?: string
}

export default function PlansPage() {
  const queryClient = useQueryClient()
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedPlan, setSelectedPlan] = useState<ReadingPlanDetail | null>(null)
  const [activeEnrollment, setActiveEnrollment] = useState<UserPlanEnrollment | null>(null)
  const [readingContext, setReadingContext] = useState<ReadingContext | null>(null)

  const { data: plans = [], isLoading: plansLoading } = useQuery({
    queryKey: ['plans', selectedCategory],
    queryFn: () => getPlans(selectedCategory || undefined),
  })

  const { data: enrollments = [] } = useQuery({
    queryKey: ['enrollments'],
    queryFn: () => getEnrolledPlans(),
  })

  const enrollMutation = useMutation({
    mutationFn: enrollInPlan,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['enrollments'] })
      setSelectedPlan(null)
    },
  })

  const advanceMutation = useMutation({
    mutationFn: advanceDay,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['enrollments'] })
      queryClient.invalidateQueries({ queryKey: ['todayReading'] })
    },
  })

  const handleViewPlan = async (planId: string) => {
    const detail = await getPlanDetail(planId)
    setSelectedPlan(detail)
  }

  const handleEnroll = (planId: string) => {
    enrollMutation.mutate(planId)
  }

  const isEnrolled = (planId: string) => {
    return enrollments.some((e) => e.plan.id === planId && e.is_active && !e.completed_at)
  }

  const handleReadPassage = (
    passage: string,
    plan: { id: string; title: string },
    day: { day_number: number; theme: string },
    enrollmentId?: string
  ) => {
    setReadingContext({
      passage,
      planId: plan.id,
      planTitle: plan.title,
      dayNumber: day.day_number,
      theme: day.theme,
      enrollmentId,
    })
    setSelectedPlan(null)
    setActiveEnrollment(null)
  }

  const activeEnrollments = enrollments.filter((e) => e.is_active && !e.completed_at)

  // If reading a passage, show the scripture reader with context
  if (readingContext) {
    return (
      <div className="space-y-4">
        <button
          onClick={() => setReadingContext(null)}
          className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Plans
        </button>
        <ScriptureReader
          reference={readingContext.passage}
          showComparison={true}
          planContext={{
            planId: readingContext.planId,
            planTitle: readingContext.planTitle,
            dayNumber: readingContext.dayNumber,
            theme: readingContext.theme,
            enrollmentId: readingContext.enrollmentId,
          }}
          onClose={() => setReadingContext(null)}
        />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <Book className="w-8 h-8 text-amber-500" />
          Reading Plans
        </h1>
        <p className="text-gray-400 mt-2">
          Structured Bible reading plans to guide your spiritual journey
        </p>
      </div>

      {/* Active Enrollments */}
      {activeEnrollments.length > 0 && (
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <Play className="w-5 h-5 text-green-500" />
            Your Active Plans
          </h2>
          <div className="grid gap-4 md:grid-cols-2">
            {activeEnrollments.map((enrollment) => (
              <div
                key={enrollment.id}
                className="bg-gray-700 rounded-lg p-4 cursor-pointer hover:bg-gray-600 transition-colors"
                onClick={() => setActiveEnrollment(enrollment)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-medium text-white">{enrollment.plan.title}</h3>
                    <p className="text-sm text-gray-400 mt-1">
                      Day {enrollment.current_day} of {enrollment.plan.duration_days}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-amber-500">
                      {Math.round(enrollment.progress_percentage)}%
                    </div>
                  </div>
                </div>
                <div className="mt-3 bg-gray-600 rounded-full h-2">
                  <div
                    className="bg-amber-500 h-2 rounded-full transition-all"
                    style={{ width: `${enrollment.progress_percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Category Filter */}
      <div className="flex gap-2 flex-wrap">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.value}
            onClick={() => setSelectedCategory(cat.value)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              selectedCategory === cat.value
                ? 'bg-amber-500 text-black'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Plans Grid */}
      {plansLoading ? (
        <div className="text-center py-12 text-gray-400">Loading plans...</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className="bg-gray-800 rounded-xl p-5 hover:bg-gray-750 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-white text-lg">{plan.title}</h3>
                  <p className="text-gray-400 text-sm mt-2 line-clamp-2">{plan.description}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-4 mt-4 text-sm text-gray-400">
                <span className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  {plan.duration_days} days
                </span>
                <span className="capitalize px-2 py-0.5 bg-gray-700 rounded text-xs">
                  {plan.category}
                </span>
              </div>

              <div className="flex gap-2 mt-4">
                <button
                  onClick={() => handleViewPlan(plan.id)}
                  className="flex-1 py-2 px-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors text-sm flex items-center justify-center gap-1"
                >
                  <BookOpen className="w-4 h-4" />
                  View Plan
                </button>
                {isEnrolled(plan.id) ? (
                  <button
                    className="py-2 px-3 bg-green-600 text-white rounded-lg text-sm flex items-center gap-1 cursor-default"
                    disabled
                  >
                    <CheckCircle className="w-4 h-4" />
                    Enrolled
                  </button>
                ) : (
                  <button
                    onClick={() => handleEnroll(plan.id)}
                    disabled={enrollMutation.isPending}
                    className="py-2 px-3 bg-amber-500 text-black rounded-lg hover:bg-amber-400 transition-colors text-sm font-medium"
                  >
                    Start Plan
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Plan Detail Modal */}
      {selectedPlan && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-hidden">
            <div className="p-6 border-b border-gray-700">
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-2xl font-bold text-white">{selectedPlan.title}</h2>
                  <p className="text-gray-400 mt-1">{selectedPlan.description}</p>
                  <div className="flex items-center gap-4 mt-3 text-sm text-gray-400">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {selectedPlan.duration_days} days
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedPlan(null)}
                  className="text-gray-400 hover:text-white text-2xl"
                >
                  ×
                </button>
              </div>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[50vh]">
              <h3 className="text-lg font-semibold text-white mb-4">Reading Schedule</h3>
              <div className="space-y-2">
                {selectedPlan.days.map((day) => {
                  const passageStr = Array.isArray(day.passages) 
                    ? day.passages.map(formatPassage).join(', ')
                    : String(day.passages)
                  const firstPassage = Array.isArray(day.passages) 
                    ? formatPassage(day.passages[0])
                    : String(day.passages)
                  return (
                    <div
                      key={day.day_number}
                      className="flex items-center gap-4 p-3 bg-gray-700 rounded-lg hover:bg-gray-600 cursor-pointer transition-colors"
                      onClick={() => handleReadPassage(
                        firstPassage,
                        { id: selectedPlan.id, title: selectedPlan.title },
                        { day_number: day.day_number, theme: day.theme || 'Daily Reading' }
                      )}
                    >
                      <div className="w-10 h-10 bg-amber-500/20 text-amber-500 rounded-full flex items-center justify-center font-bold text-sm">
                        {day.day_number}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-white">{day.theme || 'Daily Reading'}</div>
                        <div className="text-sm text-gray-400">{passageStr}</div>
                      </div>
                      <BookOpen className="w-5 h-5 text-gray-400" />
                    </div>
                  )
                })}
              </div>
            </div>

            <div className="p-6 border-t border-gray-700 flex gap-3">
              <button
                onClick={() => setSelectedPlan(null)}
                className="flex-1 py-2 px-4 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                Close
              </button>
              {!isEnrolled(selectedPlan.id) && (
                <button
                  onClick={() => handleEnroll(selectedPlan.id)}
                  disabled={enrollMutation.isPending}
                  className="flex-1 py-2 px-4 bg-amber-500 text-black font-medium rounded-lg hover:bg-amber-400 transition-colors"
                >
                  {enrollMutation.isPending ? 'Enrolling...' : 'Start This Plan'}
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Today's Reading Modal */}
      {activeEnrollment && (
        <TodayReadingModal
          enrollment={activeEnrollment}
          onClose={() => setActiveEnrollment(null)}
          onAdvance={() => {
            advanceMutation.mutate(activeEnrollment.id)
            setActiveEnrollment(null)
          }}
          onReadPassage={(passage, day) => handleReadPassage(
            passage,
            { id: activeEnrollment.plan.id, title: activeEnrollment.plan.title },
            day,
            activeEnrollment.id
          )}
        />
      )}
    </div>
  )
}

function TodayReadingModal({
  enrollment,
  onClose,
  onAdvance,
  onReadPassage,
}: {
  enrollment: UserPlanEnrollment
  onClose: () => void
  onAdvance: () => void
  onReadPassage: (passage: string, day: { day_number: number; theme: string }) => void
}) {
  const { data: todayReading, isLoading } = useQuery({
    queryKey: ['todayReading', enrollment.id],
    queryFn: () => getTodayReading(enrollment.id),
  })

  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div className="bg-gray-800 rounded-xl p-8 text-center">
          <div className="text-gray-400">Loading today's reading...</div>
        </div>
      </div>
    )
  }

  if (!todayReading) return null

  const { day } = todayReading
  const isLastDay = enrollment.current_day >= enrollment.plan.duration_days

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
      <div className="bg-gray-800 rounded-xl max-w-lg w-full">
        <div className="p-6 border-b border-gray-700">
          <div className="flex justify-between items-start">
            <div>
              <div className="text-amber-500 text-sm font-medium">
                Day {day.day_number} of {enrollment.plan.duration_days}
              </div>
              <h2 className="text-2xl font-bold text-white mt-1">{enrollment.plan.title}</h2>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white text-2xl"
            >
              ×
            </button>
          </div>
        </div>

        <div className="p-6">
          {day.theme && (
            <div className="mb-4">
              <div className="text-sm text-gray-400">Today's Theme</div>
              <div className="text-xl font-semibold text-white">{day.theme}</div>
            </div>
          )}

          <div>
            <div className="text-sm text-gray-400 mb-2">Passages to Read</div>
            <div className="space-y-2">
              {Array.isArray(day.passages) && day.passages.map((passage, idx) => {
                const passageStr = formatPassage(passage)
                return (
                  <button
                    key={idx}
                    onClick={() => onReadPassage(passageStr, { day_number: day.day_number, theme: day.theme || 'Daily Reading' })}
                    className="w-full flex items-center gap-3 p-3 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors text-left"
                  >
                    <div className="w-8 h-8 bg-amber-500/20 text-amber-500 rounded flex items-center justify-center">
                      <Book className="w-4 h-4" />
                    </div>
                    <span className="text-white font-medium flex-1">{passageStr}</span>
                    <span className="text-amber-500 text-sm">Read →</span>
                  </button>
                )
              })}
            </div>
          </div>
        </div>

        <div className="p-6 border-t border-gray-700 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 py-2 px-4 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
          >
            Close
          </button>
          <button
            onClick={onAdvance}
            className="flex-1 py-2 px-4 bg-amber-500 text-black font-medium rounded-lg hover:bg-amber-400 transition-colors flex items-center justify-center gap-2"
          >
            <CheckCircle className="w-5 h-5" />
            {isLastDay ? 'Complete Plan' : 'Mark Complete'}
          </button>
        </div>
      </div>
    </div>
  )
}
