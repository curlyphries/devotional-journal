import { useMutation, useQueryClient } from '@tanstack/react-query'
import client from '../api/client'
import { Target, Check, Loader2 } from 'lucide-react'

interface DailyPulseCardProps {
  focus: {
    intention: string
    themes: string[]
    day_number: number
    total_days: number
  }
  todaysVerse?: {
    reference: string
    text: string
    passage_id: string
    is_read: boolean
  }
  onComplete?: () => void
}

export default function DailyPulseCard({ focus, todaysVerse, onComplete }: DailyPulseCardProps) {
  const queryClient = useQueryClient()

  const markCompleteMutation = useMutation({
    mutationFn: async (passageId: string) => {
      const response = await client.post(`/passages/${passageId}/mark_read/`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      queryClient.invalidateQueries({ queryKey: ['focus-today'] })
      if (onComplete) onComplete()
    },
    onError: (error) => {
      console.error('Failed to mark passage as read:', error)
    },
  })

  if (!todaysVerse) return null

  return (
    <div className="bg-gradient-to-r from-purple-800 to-purple-900 rounded-xl p-6 border border-purple-500/30 mb-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-3">
            <Target className="w-5 h-5 text-purple-300" />
            <span className="text-purple-300 text-xs font-medium uppercase tracking-wider">
              Today's Focus: Day {focus.day_number} of {focus.total_days}
            </span>
          </div>
          
          <p className="text-2xl font-serif text-white mb-3">
            "{todaysVerse.text}"
          </p>
          
          <p className="text-purple-200 text-sm italic mb-4">
            — {todaysVerse.reference}
          </p>

          <div className="flex flex-wrap gap-2 mb-4">
            {focus.themes.slice(0, 3).map((theme: string, i: number) => (
              <span 
                key={i} 
                className="px-2 py-1 bg-purple-700/50 text-purple-200 text-xs rounded"
              >
                {theme}
              </span>
            ))}
          </div>
        </div>

        <div className="ml-4">
          {todaysVerse.is_read ? (
            <div className="flex items-center gap-2 px-4 py-2 bg-green-600/20 border border-green-500/30 rounded-lg text-green-400">
              <Check className="w-5 h-5" />
              <span className="font-medium">Completed</span>
            </div>
          ) : (
            <button
              onClick={() => markCompleteMutation.mutate(todaysVerse.passage_id)}
              disabled={markCompleteMutation.isPending}
              className="flex items-center gap-2 px-4 py-2 bg-amber-500 hover:bg-amber-400 text-purple-900 rounded-lg font-semibold transition-colors disabled:opacity-50"
            >
              {markCompleteMutation.isPending ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Check className="w-5 h-5" />
              )}
              I did this today
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
