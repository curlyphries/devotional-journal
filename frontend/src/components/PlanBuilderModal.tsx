import { useState, useEffect } from 'react'
import {
  X, Sparkles, Plus, Trash2, Loader2, PenLine, ChevronDown, ChevronUp,
  AlertTriangle, CheckCircle2, BookOpen, ArrowLeft
} from 'lucide-react'
import apiClient from '../api/client'

interface DraftDay {
  day_number: number
  passages: string[]
  theme_en: string
  theme_es: string
  reflection_prompt: string
}

interface PlanDraft {
  title_en: string
  title_es: string
  description_en: string
  description_es: string
  duration_days: number
  category: string
  days: DraftDay[]
}

interface PlanBuilderModalProps {
  isOpen: boolean
  onClose: () => void
  onCreated: () => void
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

const GENERATE_STEPS = [
  'Analysing your topic…',
  'Selecting passages…',
  'Building themes…',
  'Writing reflection prompts…',
  'Finalising plan…',
]

type AIStatus = { configured: boolean; reachable: boolean; backend: string; model: string | null }

export default function PlanBuilderModal({ isOpen, onClose, onCreated }: PlanBuilderModalProps) {
  const [mode, setMode] = useState<'ai' | 'manual'>('ai')
  const [aiStatus, setAiStatus] = useState<AIStatus | null>(null)
  const [aiStatusLoading, setAiStatusLoading] = useState(false)

  // Form state
  const [topic, setTopic] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('general')
  const [durationDays, setDurationDays] = useState(7)
  const [anchorInput, setAnchorInput] = useState('')
  const [anchors, setAnchors] = useState<string[]>([])

  // Multi-step state
  const [step, setStep] = useState<'form' | 'generating' | 'preview'>('form')
  const [generateStepIdx, setGenerateStepIdx] = useState(0)
  const [draft, setDraft] = useState<PlanDraft | null>(null)
  const [expandedDay, setExpandedDay] = useState<number | null>(null)

  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  // Fetch AI status whenever modal opens
  useEffect(() => {
    if (!isOpen) return
    setAiStatusLoading(true)
    apiClient.get('/prompts/ai-status/')
      .then(r => setAiStatus(r.data))
      .catch(() => setAiStatus({ configured: false, reachable: false, backend: 'unknown', model: null }))
      .finally(() => setAiStatusLoading(false))
  }, [isOpen])

  if (!isOpen) return null

  const addAnchor = () => {
    const t = anchorInput.trim()
    if (t && !anchors.includes(t)) { setAnchors([...anchors, t]); setAnchorInput('') }
  }
  const removeAnchor = (i: number) => setAnchors(anchors.filter((_, idx) => idx !== i))

  const handleGenerate = async () => {
    if (!topic.trim()) { setError('Please enter a topic or description.'); return }
    setError('')
    setStep('generating')
    setGenerateStepIdx(0)

    const interval = setInterval(() => {
      setGenerateStepIdx(i => Math.min(i + 1, GENERATE_STEPS.length - 1))
    }, 18000)

    try {
      const res = await apiClient.post('/plans/generate/', {
        topic: topic.trim(),
        duration_days: durationDays,
        category,
        anchor_passages: anchors,
      })
      clearInterval(interval)
      setDraft(res.data)
      setStep('preview')
    } catch (err: unknown) {
      clearInterval(interval)
      const data = (err as { response?: { data?: { error?: string; days_returned?: number; partial_plan?: PlanDraft } } })?.response?.data
      if (data?.partial_plan) {
        setDraft(data.partial_plan)
        setDurationDays(data.partial_plan.duration_days)
        setError(`AI generated ${data.days_returned} of ${durationDays} days. You can review and save what was generated.`)
        setStep('preview')
      } else {
        const msg = data?.error || 'Generation failed. Please try again.'
        setError(msg)
        setStep('form')
      }
    }
  }

  const handleSave = async () => {
    if (!draft) return
    setSaving(true)
    setError('')
    try {
      const res = await apiClient.post('/plans/save/', draft)
      const planId = res.data?.id
      if (planId) {
        try { await apiClient.post(`/plans/${planId}/enroll/`) } catch { /* non-blocking */ }
      }
      onCreated()
      handleClose()
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { error?: string } } })?.response?.data?.error ||
        'Save failed. Please try again.'
      setError(msg)
    } finally {
      setSaving(false)
    }
  }

  const handleClose = () => {
    setTopic(''); setDescription(''); setCategory('general'); setDurationDays(7)
    setAnchors([]); setAnchorInput(''); setError('')
    setStep('form'); setDraft(null); setExpandedDay(null)
    onClose()
  }

  const aiUnavailable = mode === 'ai' && !aiStatusLoading && aiStatus && !aiStatus.reachable

  // ── GENERATING SCREEN ──────────────────────────────────────────────
  if (step === 'generating') {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70">
        <div className="w-full max-w-sm bg-gray-900 border border-gray-700 rounded-2xl p-8 text-center">
          <div className="flex justify-center mb-6">
            <div className="relative">
              <div className="w-16 h-16 rounded-full border-4 border-amber-500/20 border-t-amber-500 animate-spin" />
              <Sparkles className="absolute inset-0 m-auto w-6 h-6 text-amber-400" />
            </div>
          </div>
          <h3 className="text-white font-semibold text-lg mb-2">Building your plan…</h3>
          <p className="text-amber-400 text-sm font-medium mb-6 h-5 transition-all">
            {GENERATE_STEPS[generateStepIdx]}
          </p>
          <div className="space-y-2">
            {GENERATE_STEPS.map((s, i) => (
              <div key={i} className="flex items-center gap-3 text-sm">
                <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 transition-colors ${
                  i < generateStepIdx ? 'bg-green-500' :
                  i === generateStepIdx ? 'bg-amber-500 animate-pulse' :
                  'bg-gray-700'
                }`}>
                  {i < generateStepIdx && <CheckCircle2 className="w-3 h-3 text-white" />}
                </div>
                <span className={i <= generateStepIdx ? 'text-gray-200' : 'text-gray-500'}>{s}</span>
              </div>
            ))}
          </div>
          <p className="text-gray-500 text-xs mt-6">This can take 1–2 minutes depending on plan length</p>
        </div>
      </div>
    )
  }

  // ── PREVIEW SCREEN ─────────────────────────────────────────────────
  if (step === 'preview' && draft) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70">
        <div className="relative w-full max-w-2xl bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl flex flex-col max-h-[90vh]">
          {/* Header */}
          <div className="flex items-center justify-between p-5 border-b border-gray-700 shrink-0">
            <div className="flex items-center gap-3">
              <button onClick={() => setStep('form')} className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-colors">
                <ArrowLeft className="w-4 h-4" />
              </button>
              <div>
                <h2 className="text-base font-semibold text-white">
                  {mode === 'manual' ? 'Build Your Plan' : 'Review Your Plan'}
                </h2>
                <p className="text-xs text-gray-400">
                  {mode === 'manual' ? 'Fill in passages for each day' : 'Edit anything before saving'}
                </p>
              </div>
            </div>
            <button onClick={handleClose} className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-colors">
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Scrollable body */}
          <div className="overflow-y-auto flex-1 p-5 space-y-5">
            {/* Title / Description */}
            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-gray-400 mb-1">Plan Title (English)</label>
                <input
                  value={draft.title_en}
                  onChange={e => setDraft({ ...draft, title_en: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-400 mb-1">Description</label>
                <textarea
                  value={draft.description_en}
                  onChange={e => setDraft({ ...draft, description_en: e.target.value })}
                  rows={2}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 resize-none"
                />
              </div>
            </div>

            {/* Day list */}
            <div>
              <h3 className="text-sm font-semibold text-gray-300 mb-3 flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-amber-400" />
                {draft.days.length} Days
              </h3>
              <div className="space-y-2">
                {draft.days.map((day, idx) => (
                  <div key={idx} className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden">
                    <button
                      onClick={() => setExpandedDay(expandedDay === idx ? null : idx)}
                      className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-gray-750 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-7 h-7 rounded-full bg-amber-500/20 text-amber-400 text-xs font-bold flex items-center justify-center shrink-0">
                          {day.day_number}
                        </span>
                        <div>
                          <p className="text-sm font-medium text-white leading-tight">{day.theme_en || `Day ${day.day_number}`}</p>
                          {(day.passages || []).length > 0
                            ? <p className="text-xs text-gray-400">{day.passages.join(', ')}</p>
                            : <p className="text-xs text-gray-500 italic">No passages yet — tap to add</p>
                          }
                        </div>
                      </div>
                      {expandedDay === idx
                        ? <ChevronUp className="w-4 h-4 text-gray-400 shrink-0" />
                        : <ChevronDown className="w-4 h-4 text-gray-400 shrink-0" />
                      }
                    </button>

                    {expandedDay === idx && (
                      <div className="px-4 pb-4 space-y-3 border-t border-gray-700 pt-3">
                        <div>
                          <label className="block text-xs text-gray-400 mb-1">
                            Passages
                            <span className="text-gray-500 font-normal ml-1">(comma-separated, e.g. Romans 8:1-17, Psalm 23)</span>
                          </label>
                          <input
                            value={(day.passages || []).join(', ')}
                            onChange={e => {
                              const updated = [...draft.days]
                              updated[idx] = {
                                ...updated[idx],
                                passages: e.target.value.split(',').map(p => p.trim()).filter(Boolean),
                              }
                              setDraft({ ...draft, days: updated })
                            }}
                            placeholder="e.g. John 1:1-18"
                            className="w-full px-3 py-1.5 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-500 text-sm focus:outline-none focus:ring-1 focus:ring-amber-500"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-gray-400 mb-1">Theme <span className="text-gray-500 font-normal">(optional)</span></label>
                          <input
                            value={day.theme_en}
                            onChange={e => {
                              const updated = [...draft.days]
                              updated[idx] = { ...updated[idx], theme_en: e.target.value }
                              setDraft({ ...draft, days: updated })
                            }}
                            placeholder="e.g. The Word became flesh"
                            className="w-full px-3 py-1.5 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-500 text-sm focus:outline-none focus:ring-1 focus:ring-amber-500"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-gray-400 mb-1">Reflection Prompt <span className="text-gray-500 font-normal">(optional)</span></label>
                          <textarea
                            value={day.reflection_prompt}
                            onChange={e => {
                              const updated = [...draft.days]
                              updated[idx] = { ...updated[idx], reflection_prompt: e.target.value }
                              setDraft({ ...draft, days: updated })
                            }}
                            rows={2}
                            placeholder="e.g. Where have you seen God's grace made tangible this week?"
                            className="w-full px-3 py-1.5 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-500 text-sm focus:outline-none focus:ring-1 focus:ring-amber-500 resize-none"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {error && (
              <p className="text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3">{error}</p>
            )}
          </div>

          {/* Footer */}
          <div className="px-5 pb-5 pt-3 border-t border-gray-700 flex gap-3 shrink-0">
            <button
              onClick={() => { setStep('form'); setError('') }}
              className="px-4 py-2.5 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-xl text-sm font-medium transition-colors"
            >
              {mode === 'manual' ? '← Back' : '← Regenerate'}
            </button>
            <button
              onClick={handleSave}
              disabled={saving || !draft.title_en.trim()}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-amber-500 hover:bg-amber-400 disabled:opacity-50 disabled:cursor-not-allowed text-gray-900 rounded-xl font-semibold text-sm transition-colors"
            >
              {saving ? <><Loader2 className="w-4 h-4 animate-spin" /> Saving…</> : 'Save Plan'}
            </button>
          </div>
        </div>
      </div>
    )
  }

  // ── FORM SCREEN ────────────────────────────────────────────────────
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60">
      <div className="relative w-full max-w-lg bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-amber-500/20">
              {mode === 'ai' ? <Sparkles className="w-5 h-5 text-amber-400" /> : <PenLine className="w-5 h-5 text-amber-400" />}
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Build a Reading Plan</h2>
              <p className="text-sm text-gray-400">{mode === 'ai' ? 'AI-generated from your topic' : 'Manual entry'}</p>
            </div>
          </div>
          <button onClick={handleClose} className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-5">
          {/* AI / Manual toggle */}
          <div className="flex gap-2 p-1 bg-gray-800 rounded-xl">
            <button
              onClick={() => setMode('ai')}
              className={`flex-1 flex items-center justify-center gap-2 py-2 rounded-lg text-sm font-medium transition-colors ${
                mode === 'ai' ? 'bg-amber-500 text-gray-900' : 'text-gray-400 hover:text-white'
              }`}
            >
              <Sparkles className="w-4 h-4" /> AI-Generated
            </button>
            <button
              onClick={() => setMode('manual')}
              className={`flex-1 flex items-center justify-center gap-2 py-2 rounded-lg text-sm font-medium transition-colors ${
                mode === 'manual' ? 'bg-amber-500 text-gray-900' : 'text-gray-400 hover:text-white'
              }`}
            >
              <PenLine className="w-4 h-4" /> Manual
            </button>
          </div>

          {/* AI status banner */}
          {mode === 'ai' && (
            <div>
              {aiStatusLoading && (
                <div className="flex items-center gap-2 text-xs text-gray-400 px-1">
                  <Loader2 className="w-3 h-3 animate-spin" /> Checking AI availability…
                </div>
              )}
              {!aiStatusLoading && aiStatus && !aiStatus.reachable && (
                <div className="flex items-start gap-3 px-4 py-3 bg-yellow-500/10 border border-yellow-500/30 rounded-xl">
                  <AlertTriangle className="w-4 h-4 text-yellow-400 shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-yellow-300">AI not reachable</p>
                    <p className="text-xs text-yellow-400/80 mt-0.5">
                      Backend: <span className="font-mono">{aiStatus.backend}</span>
                      {aiStatus.model ? ` · Model: ${aiStatus.model}` : ''}.
                      {' '}Switch to Manual to create a plan without AI.
                    </p>
                  </div>
                </div>
              )}
              {!aiStatusLoading && aiStatus && aiStatus.reachable && (
                <div className="flex items-center gap-2 px-3 py-2 bg-green-500/10 border border-green-500/20 rounded-xl">
                  <CheckCircle2 className="w-4 h-4 text-green-400 shrink-0" />
                  <p className="text-xs text-green-300">
                    AI ready · <span className="font-mono">{aiStatus.backend}</span>
                    {aiStatus.model ? ` · ${aiStatus.model}` : ''}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Manual note */}
          {mode === 'manual' && (
            <div className="flex items-start gap-3 px-4 py-3 bg-blue-500/10 border border-blue-500/20 rounded-xl">
              <PenLine className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
              <p className="text-xs text-blue-300">
                You'll define the title, description and category here — then add days and passages on the next screen.
              </p>
            </div>
          )}

          {/* Topic (AI) or Title (Manual) */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              {mode === 'ai' ? 'Topic or Description' : 'Plan Title'}{' '}
              <span className="text-red-400">*</span>
            </label>
            <textarea
              value={topic}
              onChange={e => setTopic(e.target.value)}
              placeholder={
                mode === 'ai'
                  ? 'e.g. Covenant faithfulness — a 4-week deep dive anchored in Deuteronomy 29'
                  : 'e.g. 7 Days Through the Sermon on the Mount'
              }
              rows={3}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-amber-500 resize-none text-sm"
            />
          </div>

          {/* Description (manual mode only — AI generates this) */}
          {mode === 'manual' && (
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Description <span className="text-gray-500 font-normal">(optional)</span>
              </label>
              <textarea
                value={description}
                onChange={e => setDescription(e.target.value)}
                placeholder="A brief description of what this plan covers"
                rows={2}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-amber-500 resize-none text-sm"
              />
            </div>
          )}

          {/* Category + Duration */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Category</label>
              <select
                value={category}
                onChange={e => setCategory(e.target.value)}
                className="w-full px-3 py-2.5 bg-gray-800 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-amber-500 text-sm"
              >
                {CATEGORIES.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Duration</label>
              <select
                value={durationDays}
                onChange={e => setDurationDays(Number(e.target.value))}
                className="w-full px-3 py-2.5 bg-gray-800 border border-gray-600 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-amber-500 text-sm"
              >
                {DURATIONS.map(d => <option key={d} value={d}>{d} days</option>)}
              </select>
            </div>
          </div>

          {/* Anchor Passages (AI only) */}
          {mode === 'ai' && (
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
                <button onClick={addAnchor} className="px-3 py-2.5 bg-gray-700 hover:bg-gray-600 text-white rounded-xl transition-colors">
                  <Plus className="w-4 h-4" />
                </button>
              </div>
              {anchors.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {anchors.map((a, i) => (
                    <span key={i} className="flex items-center gap-1.5 px-3 py-1 bg-amber-500/15 border border-amber-500/30 text-amber-300 rounded-full text-xs">
                      {a}
                      <button onClick={() => removeAnchor(i)} className="hover:text-red-400 transition-colors">
                        <Trash2 className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}

          {error && (
            <p className="text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3">{error}</p>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 pb-6 flex gap-3">
          <button
            onClick={handleClose}
            className="flex-1 px-4 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-xl font-medium transition-colors text-sm"
          >
            Cancel
          </button>

          {mode === 'ai' ? (
            <button
              onClick={handleGenerate}
              disabled={aiUnavailable || !topic.trim()}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-amber-500 hover:bg-amber-400 disabled:opacity-50 disabled:cursor-not-allowed text-gray-900 rounded-xl font-semibold transition-colors text-sm"
            >
              <Sparkles className="w-4 h-4" />
              Generate Plan
            </button>
          ) : (
            <button
              onClick={() => {
                if (!topic.trim()) { setError('Please enter a plan title.'); return }
                setDraft({
                  title_en: topic.trim(),
                  title_es: '',
                  description_en: description.trim(),
                  description_es: '',
                  duration_days: durationDays,
                  category,
                  days: Array.from({ length: durationDays }, (_, i) => ({
                    day_number: i + 1,
                    passages: [],
                    theme_en: '',
                    theme_es: '',
                    reflection_prompt: '',
                  })),
                })
                setExpandedDay(0)
                setStep('preview')
              }}
              disabled={!topic.trim()}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-amber-500 hover:bg-amber-400 disabled:opacity-50 disabled:cursor-not-allowed text-gray-900 rounded-xl font-semibold transition-colors text-sm"
            >
              <PenLine className="w-4 h-4" />
              Set Up Days →
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
