import { useQuery } from '@tanstack/react-query'
import client from '../api/client'
import { TrendingUp, TrendingDown, Minus, Loader2 } from 'lucide-react'

interface LifeAreaTrend {
  area: string
  current_score: number
  previous_score: number
  trend: 'improving' | 'declining' | 'stable'
  change: number
}

interface GrowthData {
  life_areas: LifeAreaTrend[]
  weekly_activity: {
    week: string
    journal_entries: number
    highlights: number
    reflections: number
  }[]
  focus_history: {
    intention: string
    period_type: string
    completed: boolean
    themes: string[]
  }[]
}

function TrendIcon({ trend, size = 'sm' }: { trend: string; size?: 'sm' | 'md' }) {
  const sizeClass = size === 'md' ? 'w-5 h-5' : 'w-4 h-4'
  if (trend === 'improving') return <TrendingUp className={`${sizeClass} text-green-500`} />
  if (trend === 'declining') return <TrendingDown className={`${sizeClass} text-red-500`} />
  return <Minus className={`${sizeClass} text-gray-500`} />
}

function ProgressBar({ value, previousValue }: { value: number; previousValue?: number }) {
  const change = previousValue !== undefined ? value - previousValue : 0
  
  return (
    <div className="relative">
      <div className="w-full bg-gray-700 rounded-full h-3">
        <div 
          className={`h-3 rounded-full transition-all duration-700 ${
            change > 0 ? 'bg-green-500' : change < 0 ? 'bg-red-400' : 'bg-amber-500'
          }`}
          style={{ width: `${Math.min(value, 100)}%` }}
        />
      </div>
      {previousValue !== undefined && previousValue !== value && (
        <div 
          className="absolute top-0 h-3 border-r-2 border-white/50"
          style={{ left: `${Math.min(previousValue, 100)}%` }}
          title={`Previous: ${previousValue}%`}
        />
      )}
    </div>
  )
}

export default function GrowthVisualization() {
  const { data, isLoading } = useQuery({
    queryKey: ['growth-data'],
    queryFn: async () => {
      const response = await client.get('/reflections/trends/growth/')
      return response.data as GrowthData
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
      {/* Life Area Scores */}
      <div className="card">
        <h3 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-green-500" />
          Life Area Growth
        </h3>
        <div className="space-y-4">
          {data.life_areas.map((area) => (
            <div key={area.area} className="space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-text-primary font-medium">{area.area}</span>
                <div className="flex items-center gap-2">
                  <span className="text-text-secondary text-sm">{area.current_score}%</span>
                  <TrendIcon trend={area.trend} />
                  {area.change !== 0 && (
                    <span className={`text-xs ${area.change > 0 ? 'text-green-500' : 'text-red-400'}`}>
                      {area.change > 0 ? '+' : ''}{area.change}%
                    </span>
                  )}
                </div>
              </div>
              <ProgressBar value={area.current_score} previousValue={area.previous_score} />
            </div>
          ))}
        </div>
      </div>

      {/* Weekly Activity Chart (Simple Bar Representation) */}
      {data.weekly_activity.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-text-primary mb-4">
            Weekly Activity
          </h3>
          <div className="flex items-end gap-2 h-32">
            {data.weekly_activity.map((week, i) => {
              const total = week.journal_entries + week.highlights + week.reflections
              const maxTotal = Math.max(...data.weekly_activity.map(w => w.journal_entries + w.highlights + w.reflections))
              const height = maxTotal > 0 ? (total / maxTotal) * 100 : 0
              
              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <div 
                    className="w-full bg-gradient-to-t from-amber-600 to-amber-400 rounded-t transition-all duration-500"
                    style={{ height: `${height}%`, minHeight: total > 0 ? '8px' : '0' }}
                    title={`Journal: ${week.journal_entries}, Highlights: ${week.highlights}, Reflections: ${week.reflections}`}
                  />
                  <span className="text-xs text-text-secondary">{week.week}</span>
                </div>
              )
            })}
          </div>
          <div className="flex items-center justify-center gap-4 mt-4 text-xs text-text-secondary">
            <span className="flex items-center gap-1">
              <div className="w-3 h-3 bg-amber-500 rounded" /> Activity
            </span>
          </div>
        </div>
      )}

      {/* Focus History */}
      {data.focus_history.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-text-primary mb-4">
            Focus Journey
          </h3>
          <div className="space-y-3">
            {data.focus_history.slice(0, 5).map((focus, i) => (
              <div 
                key={i} 
                className={`p-3 rounded-lg border ${
                  focus.completed 
                    ? 'bg-green-500/10 border-green-500/30' 
                    : 'bg-gray-800/50 border-gray-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-text-primary font-medium">{focus.intention}</span>
                  <span className={`text-xs px-2 py-0.5 rounded ${
                    focus.completed 
                      ? 'bg-green-500/20 text-green-400' 
                      : 'bg-amber-500/20 text-amber-400'
                  }`}>
                    {focus.completed ? 'Completed' : 'In Progress'}
                  </span>
                </div>
                <div className="flex flex-wrap gap-1 mt-2">
                  {focus.themes.map((theme, j) => (
                    <span key={j} className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded">
                      {theme}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
