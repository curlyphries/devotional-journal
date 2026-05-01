import { useQuery } from '@tanstack/react-query'
import client from '../api/client'
import { Trophy, Loader2, Check } from 'lucide-react'

interface NextMilestone {
  id: string
  title: string
  description: string
  progress: number
  target: number
  percentage: number
  remaining: number
  type: string
}

interface Achievement {
  id: string
  title: string
  description: string
  achieved: boolean
}

interface MilestonesData {
  next_milestone: NextMilestone | null
  recent_achievements: Achievement[]
  stats: {
    total_achieved: number
    current_streak: number
    longest_streak: number
    total_journal_entries: number
    total_highlights: number
    focus_completed: number
  }
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

export default function Milestones() {
  const { data, isLoading } = useQuery({
    queryKey: ['milestones'],
    queryFn: async () => {
      const response = await client.get('/reflections/milestones/')
      return response.data as MilestonesData
    },
    staleTime: 300000,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-6 h-6 text-amber-500 animate-spin" />
      </div>
    )
  }

  if (!data) return null

  return (
    <div className="space-y-6">
      {/* Hero: Next Milestone */}
      {data.next_milestone && (
        <div className="bg-gradient-to-r from-amber-900/30 to-purple-900/20 border border-amber-500/30 rounded-xl p-6">
          <div className="flex items-center justify-between mb-3">
            <span className="text-amber-400 text-sm font-medium uppercase tracking-wider">
              Next Milestone
            </span>
            <Trophy className="w-5 h-5 text-amber-400" />
          </div>
          <h3 className="text-xl font-bold text-text-primary mb-1">
            {data.next_milestone.title}
          </h3>
          <p className="text-text-secondary mb-4">
            {data.next_milestone.remaining} more to unlock
          </p>
          <ProgressBar 
            value={data.next_milestone.progress} 
            max={data.next_milestone.target} 
            color="amber" 
          />
          <div className="flex justify-between mt-2 text-sm text-text-secondary">
            <span>{data.next_milestone.progress} / {data.next_milestone.target}</span>
            <span>{data.next_milestone.percentage}%</span>
          </div>
        </div>
      )}

      {/* All Complete State */}
      {!data.next_milestone && data.recent_achievements.length > 0 && (
        <div className="text-center py-8">
          <Trophy className="w-16 h-16 text-amber-500 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-text-primary mb-2">
            All Milestones Achieved!
          </h3>
          <p className="text-text-secondary mb-4">
            You've completed all available milestones. New ones coming soon!
          </p>
        </div>
      )}

      {/* Recent Achievements */}
      {data.recent_achievements.length > 0 && (
        <div className="space-y-3">
          <h4 className="text-sm font-medium text-text-secondary uppercase tracking-wider">
            Achieved
          </h4>
          {data.recent_achievements.map((achievement) => (
            <div key={achievement.id} className="flex items-center gap-3 p-3 bg-gray-800/50 rounded-lg">
              <div className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center">
                <Check className="w-5 h-5 text-green-400" />
              </div>
              <div>
                <p className="text-text-primary font-medium">{achievement.title}</p>
                <p className="text-text-secondary text-sm">{achievement.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
