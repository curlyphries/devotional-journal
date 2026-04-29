import { useState, useEffect } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import client from '../api/client'
import { X, Save, Loader2, Sparkles } from 'lucide-react'

interface QuickCaptureModalProps {
  isOpen: boolean
  onClose: () => void
  activeFocus?: {
    intention: string
    themes: string[]
  }
}

const MOODS = [
  { id: 'grateful', emoji: '🙏' },
  { id: 'struggling', emoji: '😔' },
  { id: 'peaceful', emoji: '😌' },
  { id: 'fired_up', emoji: '🔥' },
  { id: 'convicted', emoji: '💭' },
]

export default function QuickCaptureModal({ isOpen, onClose, activeFocus }: QuickCaptureModalProps) {
  const queryClient = useQueryClient()
  const [content, setContent] = useState('')
  const [selectedMood, setSelectedMood] = useState('')

  // ESC key handler
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }
    
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose])

  const createMutation = useMutation({
    mutationFn: async (data: { date: string; content: string; mood_tag?: string }) => {
      const response = await client.post('/journal/', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      setContent('')
      setSelectedMood('')
      onClose()
    },
  })

  const handleSave = () => {
    if (!content.trim()) return
    
    let fullContent = content
    
    // Tag with active focus if available
    if (activeFocus) {
      fullContent = `<!-- DJ_META_START -->
{
  "focus_intention": "${activeFocus.intention}",
  "focus_themes": ${JSON.stringify(activeFocus.themes)},
  "capture_type": "quick"
}
<!-- DJ_META_END -->

${content}`
    }
    
    createMutation.mutate({
      date: new Date().toISOString().split('T')[0],
      content: fullContent,
      mood_tag: selectedMood || undefined,
    })
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-2xl border border-gray-700 w-full max-w-lg shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-amber-400" />
            <h3 className="text-lg font-semibold text-text-primary">Quick Capture</h3>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5 text-text-secondary" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 space-y-4">
          {activeFocus && (
            <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-3">
              <p className="text-purple-400 text-xs font-medium uppercase tracking-wider mb-1">
                Tagged with Focus
              </p>
              <p className="text-white text-sm">{activeFocus.intention}</p>
            </div>
          )}

          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="What's on your heart right now?"
            className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-text-primary resize-none focus:border-amber-500 focus:outline-none"
            rows={4}
            autoFocus
          />

          <div>
            <p className="text-sm text-text-secondary mb-2">How are you feeling?</p>
            <div className="flex flex-wrap gap-2">
              {MOODS.map((mood) => (
                <button
                  key={mood.id}
                  onClick={() => setSelectedMood(selectedMood === mood.id ? '' : mood.id)}
                  className={`px-3 py-2 rounded-lg border transition-colors ${
                    selectedMood === mood.id
                      ? 'border-amber-500 bg-amber-500/20 text-amber-400'
                      : 'border-gray-700 hover:border-gray-600 text-text-secondary'
                  }`}
                >
                  {mood.emoji}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex gap-3 p-4 border-t border-gray-700">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
          >
            Later
          </button>
          <button
            onClick={handleSave}
            disabled={createMutation.isPending || !content.trim()}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-amber-500 hover:bg-amber-400 text-purple-900 rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            {createMutation.isPending ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            Save
          </button>
        </div>
      </div>
    </div>
  )
}
