import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Target, 
  Calendar, 
  CheckCircle2, 
  Pause, 
  Play, 
  Flag,
  Loader2,
  ChevronRight,
  Plus
} from 'lucide-react'
import { 
  useActiveJourney, 
  useJourneys, 
  useCreateJourney, 
  useJourneyActions,
  useLifeAreas
} from '../hooks/useReflections'
import { UserJourney, CreateJourneyData } from '../api/reflections'

export default function JourneyPage() {
  const navigate = useNavigate()
  const { data: activeJourney, isLoading: activeLoading } = useActiveJourney()
  const { data: journeys, isLoading: journeysLoading } = useJourneys()
  const [showCreateForm, setShowCreateForm] = useState(false)

  if (activeLoading || journeysLoading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-accent-primary" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg-primary p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold text-text-primary">Your Journey</h1>
          {!activeJourney && !showCreateForm && (
            <button
              onClick={() => setShowCreateForm(true)}
              className="flex items-center gap-2 px-4 py-2 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary/90"
            >
              <Plus className="w-5 h-5" />
              Start New Journey
            </button>
          )}
        </div>

        {showCreateForm && (
          <CreateJourneyForm 
            onCancel={() => setShowCreateForm(false)}
            onSuccess={() => setShowCreateForm(false)}
          />
        )}

        {activeJourney && !showCreateForm && (
          <ActiveJourneyCard journey={activeJourney} />
        )}

        {!activeJourney && !showCreateForm && journeys && journeys.length > 0 && (
          <div className="mt-8">
            <h2 className="text-lg font-semibold text-text-primary mb-4">Past Journeys</h2>
            <div className="space-y-4">
              {journeys.filter(j => j.status !== 'active').map((journey) => (
                <JourneyCard key={journey.id} journey={journey} />
              ))}
            </div>
          </div>
        )}

        {!activeJourney && !showCreateForm && (!journeys || journeys.length === 0) && (
          <div className="text-center py-16">
            <Target className="w-16 h-16 text-text-secondary mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-text-primary mb-2">
              No Active Journey
            </h2>
            <p className="text-text-secondary mb-6">
              Start a new journey to track your spiritual growth
            </p>
            <button
              onClick={() => setShowCreateForm(true)}
              className="px-6 py-3 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary/90"
            >
              Start Your Journey
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function ActiveJourneyCard({ journey }: { journey: UserJourney }) {
  const { pause, resume, complete } = useJourneyActions(journey.id)

  return (
    <div className="bg-bg-secondary rounded-xl p-6 shadow-lg">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-text-primary">{journey.title}</h2>
          <p className="text-text-secondary mt-1">
            Day {journey.current_day} of {journey.duration_days}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {journey.status === 'active' ? (
            <button
              onClick={() => pause.mutate()}
              disabled={pause.isPending}
              className="p-2 text-text-secondary hover:text-text-primary rounded-lg hover:bg-bg-primary"
              title="Pause Journey"
            >
              <Pause className="w-5 h-5" />
            </button>
          ) : journey.status === 'paused' ? (
            <button
              onClick={() => resume.mutate()}
              disabled={resume.isPending}
              className="p-2 text-text-secondary hover:text-text-primary rounded-lg hover:bg-bg-primary"
              title="Resume Journey"
            >
              <Play className="w-5 h-5" />
            </button>
          ) : null}
          <button
            onClick={() => complete.mutate()}
            disabled={complete.isPending}
            className="p-2 text-green-500 hover:text-green-400 rounded-lg hover:bg-bg-primary"
            title="Complete Journey"
          >
            <Flag className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm text-text-secondary mb-2">
          <span>Progress</span>
          <span>{journey.progress_percentage}%</span>
        </div>
        <div className="h-3 bg-bg-primary rounded-full overflow-hidden">
          <div
            className="h-full bg-accent-primary rounded-full transition-all duration-500"
            style={{ width: `${journey.progress_percentage}%` }}
          />
        </div>
      </div>

      {/* Goal */}
      <div className="p-4 bg-bg-primary rounded-lg mb-4">
        <div className="flex items-center gap-2 text-accent-primary mb-2">
          <Target className="w-5 h-5" />
          <span className="font-medium">Your Goal</span>
        </div>
        <p className="text-text-primary">{journey.goal_statement}</p>
      </div>

      {/* Success Definition */}
      <div className="p-4 bg-bg-primary rounded-lg mb-4">
        <div className="flex items-center gap-2 text-green-500 mb-2">
          <CheckCircle2 className="w-5 h-5" />
          <span className="font-medium">Success Looks Like</span>
        </div>
        <p className="text-text-primary">{journey.success_definition}</p>
      </div>

      {/* Focus Areas */}
      {journey.focus_areas && journey.focus_areas.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {journey.focus_areas.map((area) => (
            <span
              key={area}
              className="px-3 py-1 bg-accent-primary/10 text-accent-primary rounded-full text-sm font-medium"
            >
              {area}
            </span>
          ))}
        </div>
      )}

      {/* Days Remaining */}
      <div className="mt-6 pt-4 border-t border-border-primary flex items-center justify-between">
        <div className="flex items-center gap-2 text-text-secondary">
          <Calendar className="w-5 h-5" />
          <span>{journey.days_remaining} days remaining</span>
        </div>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
          journey.status === 'active' 
            ? 'bg-green-500/10 text-green-500'
            : journey.status === 'paused'
            ? 'bg-yellow-500/10 text-yellow-500'
            : 'bg-gray-500/10 text-gray-500'
        }`}>
          {journey.status.charAt(0).toUpperCase() + journey.status.slice(1)}
        </span>
      </div>
    </div>
  )
}

function JourneyCard({ journey }: { journey: UserJourney }) {
  return (
    <div className="bg-bg-secondary rounded-lg p-4 flex items-center justify-between">
      <div>
        <h3 className="font-medium text-text-primary">{journey.title}</h3>
        <p className="text-sm text-text-secondary">
          {journey.current_day} / {journey.duration_days} days • {journey.status}
        </p>
      </div>
      <ChevronRight className="w-5 h-5 text-text-secondary" />
    </div>
  )
}

function CreateJourneyForm({ 
  onCancel, 
  onSuccess 
}: { 
  onCancel: () => void
  onSuccess: () => void 
}) {
  const { data: lifeAreas } = useLifeAreas()
  const createJourney = useCreateJourney()

  const [title, setTitle] = useState('')
  const [goalStatement, setGoalStatement] = useState('')
  const [successDefinition, setSuccessDefinition] = useState('')
  const [focusAreas, setFocusAreas] = useState<string[]>([])
  const [durationDays, setDurationDays] = useState(30)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      await createJourney.mutateAsync({
        title,
        goal_statement: goalStatement,
        success_definition: successDefinition,
        focus_areas: focusAreas,
        duration_days: durationDays,
      })
      onSuccess()
    } catch (error) {
      console.error('Failed to create journey:', error)
    }
  }

  const toggleFocusArea = (code: string) => {
    setFocusAreas((prev) =>
      prev.includes(code) ? prev.filter((a) => a !== code) : [...prev, code]
    )
  }

  return (
    <form onSubmit={handleSubmit} className="bg-bg-secondary rounded-xl p-6 shadow-lg">
      <h2 className="text-xl font-bold text-text-primary mb-6">Start a New Journey</h2>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-2">
            Journey Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g., 30 Days of Patience"
            className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-text-secondary mb-2">
            What's your goal?
          </label>
          <textarea
            value={goalStatement}
            onChange={(e) => setGoalStatement(e.target.value)}
            placeholder="Describe what you want to achieve..."
            rows={3}
            className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary resize-none"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-text-secondary mb-2">
            What does success look like?
          </label>
          <textarea
            value={successDefinition}
            onChange={(e) => setSuccessDefinition(e.target.value)}
            placeholder="How will you know you've succeeded?"
            rows={3}
            className="w-full px-4 py-3 bg-bg-primary border border-border-primary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary resize-none"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-text-secondary mb-2">
            Duration
          </label>
          <div className="flex gap-3">
            {[7, 14, 21, 30, 90].map((days) => (
              <button
                key={days}
                type="button"
                onClick={() => setDurationDays(days)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  durationDays === days
                    ? 'bg-accent-primary text-white'
                    : 'bg-bg-primary text-text-primary hover:bg-bg-primary/80'
                }`}
              >
                {days} days
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-text-secondary mb-2">
            Focus Areas (select up to 3)
          </label>
          <div className="flex flex-wrap gap-2">
            {lifeAreas?.map((area) => (
              <button
                key={area.code}
                type="button"
                onClick={() => toggleFocusArea(area.code)}
                disabled={focusAreas.length >= 3 && !focusAreas.includes(area.code)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  focusAreas.includes(area.code)
                    ? 'bg-accent-primary text-white'
                    : 'bg-bg-primary text-text-primary hover:bg-bg-primary/80 disabled:opacity-50'
                }`}
              >
                {area.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="flex gap-3 mt-8">
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 py-3 bg-bg-primary text-text-primary rounded-lg font-medium hover:bg-bg-primary/80"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={createJourney.isPending || !title || !goalStatement || !successDefinition}
          className="flex-1 py-3 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {createJourney.isPending ? (
            <Loader2 className="w-5 h-5 animate-spin mx-auto" />
          ) : (
            'Start Journey'
          )}
        </button>
      </div>
    </form>
  )
}
