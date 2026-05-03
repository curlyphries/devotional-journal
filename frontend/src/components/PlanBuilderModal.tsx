import { useState } from 'react'
import { X, Sparkles, Plus, Trash2, Loader2 } from 'lucide-react'
import apiClient from '../api/client'

interface GeneratedDay {
  day_number: number
  passages: string[]
  theme: string
  reflection_prompts_seed: string
}

interface GeneratedPlan {
  id: string
  title: string
  description: string
  duration_days: number
  category: string
  is_public: boolean
  is_owned: boolean
  days: GeneratedDay[]
}

interface PlanBuilderModalProps {
  isOpen: boolean
  onClose: () => void
  onCreated: (plan: GeneratedPlan) => void
}

const CATEGORIES = [
  { value: 'general', label: 'General' },
  { value: 'faith', label: 'Faith Foundations' },
  { value: 'fatherhood', label: 'Fatherhood' },
  { value: 'leadership', label: 'Leadership' },
  { value: 'marriage', label: 'Marriage' },
  { value: 'recovery', label: 'Recovery' },
]

const DURATIONS = [7, 14, 21, 28, 30, 40]

export default function PlanBuilderModal({ isOpen, onClose, onCreated }: PlanBuilderModalProps) {
  const [topic, setTopic] = useState('')
  const [category, setCategory] = useState('general')
  const [durationDays, setDurationDays] = useState(7)
  const [anchorInput, setAnchorInput] = useState('')
  const [anchors, setAnchors] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (!isOpen) return null

  const addAnchor = () => {
    const trimmed = anchorInput.trim()
    if (trimmed && !anchors.includes(trimmed)) {
      setAnchors([...anchors, trimmed])
      setAnchorInput('')
    }
  }

  const removeAnchor = (i: number) => setAnchors(anchors.filter((_, idx) => idx !== i))

  const handleGenerate = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic or description.')
      return
    }
    setError('')
    setLoading(true)
    try {
      const res = await apiClient.post('/plans/generate/', {
        topic: topic.trim(),
        duration_days: durationDays,
        category,
        anchor_passages: anchors,
      })
      onCreated(res.data)
      onClose()
      resetForm()
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { error?: string } } })?.response?.data?.error ||
        'Generation failed. Please try again.'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setTopic('')
    setCategory('general')
    setDurationDays(7)
    setAnchors([])
    setAnchorInput('')
    setError('')
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60">
      <div className="relative w-full max-w-lg bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-amber-500/20">
              <Sparkles className="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Build a Reading Plan</h2>
              <p className="text-sm text-gray-400">AI-generated from your topic</p>
            </div>
          </div>
          <button
            onClick={() => { onClose(); resetForm() }}
            className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-5">
          {/* Topic */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Topic or Description <span className="text-red-400">*</span>
            </label>
            <textarea
              value={topic}
              onChange={e => setTopic(e.target.value)}
              placeholder="e.g. Covenant faithfulness — a 4-week deep dive based on Deuteronomy 29"
              rows={3}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-amber-500 resize-none text-sm"
            />
          </div>

          {/* Category + Duration */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Category</label>
              <select
                value={category}
                onChange={e => setCategory(e.target.value)}
                className="w-full px-3 py-2.5 bg-gray-800 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-amber-500 text-sm"
              >
                {CATEGORIES.map(c => (
                  <option key={c.value} value={c.value}>{c.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Duration</label>
              <select
                value={durationDays}
                onChange={e => setDurationDays(Number(e.target.value))}
                className="w-full px-3 py-2.5 bg-gray-800 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-amber-500 text-sm"
              >
                {DURATIONS.map(d => (
                  <option key={d} value={d}>{d} days</option>
                ))}
              </select>
            </div>
          </div>

          {/* Anchor Passages */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Anchor Passages <span className="text-gray-500 font-normal">(optional)</span>
            </label>
            <div className="flex gap-2">
              <input
                value={anchorInput}
                onChange={e => setAnchorInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), addAnchor())}
                placeholder="e.g. Deuteronomy 29:1-9"
                className="flex-1 px-3 py-2.5 bg-gray-800 border border-gray-600 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-amber-500 text-sm"
              />
              <button
                onClick={addAnchor}
                className="px-3 py-2.5 bg-gray-700 hover:bg-gray-600 text-white rounded-xl transition-colors"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
            {anchors.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {anchors.map((a, i) => (
                  <span
                    key={i}
                    className="flex items-center gap-1.5 px-3 py-1 bg-amber-500/15 border border-amber-500/30 text-amber-300 rounded-full text-xs"
                  >
                    {a}
                    <button onClick={() => removeAnchor(i)} className="hover:text-red-400 transition-colors">
                      <Trash2 className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {error && (
            <p className="text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3">
              {error}
            </p>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 pb-6 flex gap-3">
          <button
            onClick={() => { onClose(); resetForm() }}
            className="flex-1 px-4 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-xl font-medium transition-colors text-sm"
          >
            Cancel
          </button>
          <button
            onClick={handleGenerate}
            disabled={loading || !topic.trim()}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-amber-500 hover:bg-amber-400 disabled:opacity-50 disabled:cursor-not-allowed text-gray-900 rounded-xl font-semibold transition-colors text-sm"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Generating…
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Generate Plan
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
