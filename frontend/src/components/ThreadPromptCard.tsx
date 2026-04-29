import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import client from '../api/client'
import { MessageCircle, ThumbsUp, Minus, ThumbsDown, Check, ChevronDown, Loader2 } from 'lucide-react'

interface ThreadPrompt {
  id: string
  thread_id: string
  thread_type: string
  summary: string
  prompt_text: string
  life_area: string
  days_since: number
}

interface ThreadPromptCardProps {
  prompts: ThreadPrompt[]
  onAllResponded?: () => void
}

export default function ThreadPromptCard({ prompts, onAllResponded }: ThreadPromptCardProps) {
  const queryClient = useQueryClient()
  const [respondedIds, setRespondedIds] = useState<Set<string>>(new Set())
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [expandedText, setExpandedText] = useState('')

  const respondMutation = useMutation({
    mutationFn: async ({ threadId, response, expanded_text }: { 
      threadId: string
      response: 'better' | 'same' | 'worse' | 'resolved'
      expanded_text?: string 
    }) => {
      await client.post(`/thread-prompts/${threadId}/respond/`, {
        response,
        expanded_text,
      })
    },
    onSuccess: (_, variables) => {
      // Optimistically remove from list
      setRespondedIds(prev => new Set([...prev, variables.threadId]))
      setExpandedId(null)
      setExpandedText('')
      
      // Invalidate queries
      queryClient.invalidateQueries({ queryKey: ['pendingThreadPrompts'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      
      // Check if all responded
      const newRespondedCount = respondedIds.size + 1
      if (newRespondedCount >= prompts.length && onAllResponded) {
        onAllResponded()
      }
    },
  })

  // Filter out already responded prompts
  const visiblePrompts = prompts.filter(p => !respondedIds.has(p.id))

  if (visiblePrompts.length === 0) {
    return null
  }

  const handleResponse = (threadId: string, response: 'better' | 'same' | 'worse' | 'resolved') => {
    if (expandedId === threadId && expandedText.trim()) {
      respondMutation.mutate({ threadId, response, expanded_text: expandedText })
    } else {
      respondMutation.mutate({ threadId, response })
    }
  }

  return (
    <div className="bg-purple-900/20 border border-purple-500/30 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-4">
        <MessageCircle className="w-5 h-5 text-purple-400" />
        <h3 className="text-purple-400 font-semibold">Quick Check-In</h3>
        <span className="text-purple-400/60 text-sm">({visiblePrompts.length})</span>
      </div>

      <div className="space-y-4">
        {visiblePrompts.map((prompt) => (
          <div key={prompt.id} className="bg-gray-800/50 rounded-lg p-4">
            <p className="text-white text-sm mb-3">{prompt.prompt_text}</p>
            
            {prompt.summary && (
              <p className="text-gray-400 text-xs italic mb-3 border-l-2 border-purple-500/30 pl-2">
                "{prompt.summary}"
              </p>
            )}

            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => handleResponse(prompt.id, 'better')}
                disabled={respondMutation.isPending}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-green-600/20 hover:bg-green-600/30 border border-green-500/30 rounded-lg text-green-400 text-sm font-medium transition-colors disabled:opacity-50"
              >
                {respondMutation.isPending && respondMutation.variables?.threadId === prompt.id ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <ThumbsUp className="w-4 h-4" />
                )}
                Better
              </button>
              
              <button
                onClick={() => handleResponse(prompt.id, 'same')}
                disabled={respondMutation.isPending}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-600/20 hover:bg-gray-600/30 border border-gray-500/30 rounded-lg text-gray-400 text-sm font-medium transition-colors disabled:opacity-50"
              >
                <Minus className="w-4 h-4" />
                Same
              </button>
              
              <button
                onClick={() => handleResponse(prompt.id, 'worse')}
                disabled={respondMutation.isPending}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-red-600/20 hover:bg-red-600/30 border border-red-500/30 rounded-lg text-red-400 text-sm font-medium transition-colors disabled:opacity-50"
              >
                <ThumbsDown className="w-4 h-4" />
                Worse
              </button>

              <button
                onClick={() => handleResponse(prompt.id, 'resolved')}
                disabled={respondMutation.isPending}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-600/20 hover:bg-amber-600/30 border border-amber-500/30 rounded-lg text-amber-400 text-sm font-medium transition-colors disabled:opacity-50"
              >
                <Check className="w-4 h-4" />
                Resolved
              </button>

              <button
                onClick={() => setExpandedId(expandedId === prompt.id ? null : prompt.id)}
                className="flex items-center gap-1 px-2 py-1.5 text-purple-400/60 hover:text-purple-400 text-xs transition-colors ml-auto"
              >
                <ChevronDown className={`w-3 h-3 transition-transform ${expandedId === prompt.id ? 'rotate-180' : ''}`} />
                Add note
              </button>
            </div>

            {expandedId === prompt.id && (
              <div className="mt-3 pt-3 border-t border-gray-700">
                <textarea
                  value={expandedText}
                  onChange={(e) => setExpandedText(e.target.value)}
                  placeholder="Tell us more about how things are going..."
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2 text-white text-sm resize-none focus:border-purple-500 focus:outline-none"
                  rows={2}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
