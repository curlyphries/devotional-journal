import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import client from '../api/client'
import { 
  MessageCircle, X, Check, Clock, ChevronRight, 
  Loader2, AlertCircle, Heart, Lightbulb
} from 'lucide-react'

interface ThreadPrompt {
  id: string
  thread_id: string
  thread_type: string
  summary: string
  prompt_text: string
  life_area: string
  days_since: number
  followup_count: number
}

interface ThreadPromptsProps {
  maxPrompts?: number
  onClose?: () => void
}

const THREAD_TYPE_ICONS: Record<string, typeof MessageCircle> = {
  struggle: AlertCircle,
  commitment: Check,
  question: Lightbulb,
  relationship: Heart,
  decision: Clock,
  confession: MessageCircle,
}

const THREAD_TYPE_COLORS: Record<string, string> = {
  struggle: 'text-red-400 bg-red-500/20',
  commitment: 'text-green-400 bg-green-500/20',
  question: 'text-blue-400 bg-blue-500/20',
  relationship: 'text-pink-400 bg-pink-500/20',
  decision: 'text-amber-400 bg-amber-500/20',
  confession: 'text-purple-400 bg-purple-500/20',
}

export default function ThreadPrompts({ maxPrompts = 2, onClose }: ThreadPromptsProps) {
  const queryClient = useQueryClient()
  const [expandedThread, setExpandedThread] = useState<string | null>(null)
  const [responseText, setResponseText] = useState('')

  const { data: prompts, isLoading } = useQuery({
    queryKey: ['thread-prompts'],
    queryFn: async () => {
      const response = await client.get('/reflections/thread-prompts/pending/')
      return response.data as ThreadPrompt[]
    },
    staleTime: 300000, // 5 minutes
  })

  const respondMutation = useMutation({
    mutationFn: async ({ promptId, response, action }: { promptId: string; response?: string; action: 'respond' | 'skip' | 'resolved' }) => {
      await client.post(`/reflections/thread-prompts/${promptId}/respond/`, {
        response,
        action,
      })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['thread-prompts'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      setExpandedThread(null)
      setResponseText('')
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-4">
        <Loader2 className="w-5 h-5 text-amber-500 animate-spin" />
      </div>
    )
  }

  const visiblePrompts = prompts?.slice(0, maxPrompts) || []

  if (visiblePrompts.length === 0) {
    return null
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-text-secondary flex items-center gap-2">
          <MessageCircle className="w-4 h-4" />
          Follow-up Prompts
        </h3>
        {onClose && (
          <button onClick={onClose} className="text-text-secondary hover:text-text-primary">
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {visiblePrompts.map((prompt) => {
        const Icon = THREAD_TYPE_ICONS[prompt.thread_type] || MessageCircle
        const colorClass = THREAD_TYPE_COLORS[prompt.thread_type] || 'text-gray-400 bg-gray-500/20'
        const isExpanded = expandedThread === prompt.id

        return (
          <div 
            key={prompt.id}
            className="bg-gray-800/50 rounded-lg border border-gray-700 overflow-hidden"
          >
            <div 
              className="p-4 cursor-pointer hover:bg-gray-800/70 transition-colors"
              onClick={() => setExpandedThread(isExpanded ? null : prompt.id)}
            >
              <div className="flex items-start gap-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${colorClass.split(' ')[1]}`}>
                  <Icon className={`w-4 h-4 ${colorClass.split(' ')[0]}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-text-primary text-sm">{prompt.prompt_text}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs text-text-secondary">
                      {prompt.days_since} days ago
                    </span>
                    {prompt.life_area && (
                      <span className="text-xs px-2 py-0.5 bg-gray-700 rounded text-text-secondary">
                        {prompt.life_area}
                      </span>
                    )}
                  </div>
                </div>
                <ChevronRight className={`w-4 h-4 text-text-secondary transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
              </div>
            </div>

            {isExpanded && (
              <div className="px-4 pb-4 border-t border-gray-700 pt-3">
                <p className="text-sm text-text-secondary mb-3 italic">
                  "{prompt.summary}"
                </p>
                
                <textarea
                  value={responseText}
                  onChange={(e) => setResponseText(e.target.value)}
                  placeholder="Share an update or reflection..."
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-text-primary text-sm resize-none focus:border-amber-500 focus:outline-none"
                  rows={3}
                />

                <div className="flex items-center gap-2 mt-3">
                  <button
                    onClick={() => respondMutation.mutate({ 
                      promptId: prompt.id, 
                      response: responseText, 
                      action: 'respond' 
                    })}
                    disabled={!responseText.trim() || respondMutation.isPending}
                    className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-amber-600 hover:bg-amber-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg text-sm transition-colors"
                  >
                    {respondMutation.isPending ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <>
                        <MessageCircle className="w-4 h-4" />
                        Share Update
                      </>
                    )}
                  </button>
                  
                  <button
                    onClick={() => respondMutation.mutate({ 
                      promptId: prompt.id, 
                      action: 'resolved' 
                    })}
                    disabled={respondMutation.isPending}
                    className="px-3 py-2 bg-green-600 hover:bg-green-500 text-white rounded-lg text-sm transition-colors"
                    title="Mark as resolved"
                  >
                    <Check className="w-4 h-4" />
                  </button>
                  
                  <button
                    onClick={() => respondMutation.mutate({ 
                      promptId: prompt.id, 
                      action: 'skip' 
                    })}
                    disabled={respondMutation.isPending}
                    className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-text-secondary rounded-lg text-sm transition-colors"
                    title="Skip for now"
                  >
                    <Clock className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}
          </div>
        )
      })}

      {prompts && prompts.length > maxPrompts && (
        <p className="text-xs text-text-secondary text-center">
          +{prompts.length - maxPrompts} more follow-ups
        </p>
      )}
    </div>
  )
}
