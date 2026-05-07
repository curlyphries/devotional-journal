import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { useTranslation } from 'react-i18next'
import { X, ChevronLeft, ChevronRight } from 'lucide-react'

interface TourStep {
  targetId: string
  titleKey: string
  bodyKey: string
  position: 'top' | 'bottom' | 'left' | 'right'
}

const STEPS: TourStep[] = [
  { targetId: 'streak',         titleKey: 'tour.streak.title',       bodyKey: 'tour.streak.body',       position: 'bottom' },
  { targetId: 'speak-your-mind',titleKey: 'tour.speakYourMind.title', bodyKey: 'tour.speakYourMind.body', position: 'bottom' },
  { targetId: 'snapshot',       titleKey: 'tour.snapshot.title',     bodyKey: 'tour.snapshot.body',     position: 'bottom' },
  { targetId: 'fab',            titleKey: 'tour.fab.title',          bodyKey: 'tour.fab.body',          position: 'top'    },
  { targetId: 'language',       titleKey: 'tour.language.title',     bodyKey: 'tour.language.body',     position: 'bottom' },
  { targetId: 'help',           titleKey: 'tour.help.title',         bodyKey: 'tour.help.body',         position: 'bottom' },
]

interface Rect { top: number; left: number; width: number; height: number }

function getRect(id: string): Rect | null {
  const el = document.querySelector(`[data-tour-id="${id}"]`)
  if (!el) return null
  const r = el.getBoundingClientRect()
  return { top: r.top + window.scrollY, left: r.left + window.scrollX, width: r.width, height: r.height }
}

const PAD = 12
const TIP_W = 320

interface Props {
  open: boolean
  onClose: () => void
}

export default function OnboardingTour({ open, onClose }: Props) {
  const { t } = useTranslation()
  const [step, setStep] = useState(0)
  const [rect, setRect] = useState<Rect | null>(null)
  const tooltipRef = useRef<HTMLDivElement>(null)

  const current = STEPS[step]

  const measureAndScroll = (s: TourStep) => {
    const r = getRect(s.targetId)
    if (!r) { setRect(null); return }
    setRect(r)
    const mid = r.top + r.height / 2
    const vh = window.innerHeight
    window.scrollTo({ top: mid - vh / 2, behavior: 'smooth' })
  }

  useLayoutEffect(() => {
    if (!open) return
    measureAndScroll(current)
  }, [open, step]) // eslint-disable-line react-hooks/exhaustive-deps

  // Re-measure on resize
  useEffect(() => {
    if (!open) return
    const onResize = () => measureAndScroll(current)
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [open, step]) // eslint-disable-line react-hooks/exhaustive-deps

  // Close on Escape
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open, onClose])

  if (!open) return null

  const handleNext = () => {
    if (step < STEPS.length - 1) { setStep(s => s + 1) }
    else { onClose() }
  }
  const handleBack = () => { if (step > 0) setStep(s => s - 1) }

  // Tooltip positioning
  const getTooltipStyle = (): React.CSSProperties => {
    if (!rect) return { top: '50%', left: '50%', transform: 'translate(-50%,-50%)', position: 'fixed' }

    const vw = window.innerWidth
    const pos = current.position

    if (pos === 'bottom') {
      return {
        position: 'absolute',
        top: rect.top + rect.height + PAD,
        left: Math.max(PAD, Math.min(rect.left + rect.width / 2 - TIP_W / 2, vw - TIP_W - PAD)),
        width: TIP_W,
      }
    }
    if (pos === 'top') {
      return {
        position: 'absolute',
        top: rect.top - PAD - 180, // approximate tooltip height
        left: Math.max(PAD, Math.min(rect.left + rect.width / 2 - TIP_W / 2, vw - TIP_W - PAD)),
        width: TIP_W,
      }
    }
    if (pos === 'left') {
      return {
        position: 'absolute',
        top: rect.top + rect.height / 2 - 80,
        left: Math.max(PAD, rect.left - TIP_W - PAD),
        width: TIP_W,
      }
    }
    // right
    return {
      position: 'absolute',
      top: rect.top + rect.height / 2 - 80,
      left: Math.min(rect.left + rect.width + PAD, vw - TIP_W - PAD),
      width: TIP_W,
    }
  }

  const getArrowClass = () => {
    const pos = current.position
    if (pos === 'bottom') return 'before:absolute before:-top-2 before:left-1/2 before:-translate-x-1/2 before:border-4 before:border-transparent before:border-b-bg-elevated'
    if (pos === 'top')    return 'before:absolute before:-bottom-2 before:left-1/2 before:-translate-x-1/2 before:border-4 before:border-transparent before:border-t-bg-elevated'
    return ''
  }

  const highlightStyle: React.CSSProperties | undefined = rect ? {
    position: 'absolute',
    top: rect.top - 4,
    left: rect.left - 4,
    width: rect.width + 8,
    height: rect.height + 8,
    borderRadius: 8,
    boxShadow: '0 0 0 9999px rgba(0,0,0,0.55)',
    border: '2px solid var(--color-accent-primary, #f59e0b)',
    pointerEvents: 'none',
    zIndex: 49,
  } : undefined

  return createPortal(
    <>
      {/* Backdrop when no target found */}
      {!rect && (
        <div
          className="fixed inset-0 bg-black/60 z-40"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Spotlight highlight ring */}
      {highlightStyle && <div style={highlightStyle} aria-hidden="true" />}

      {/* Tooltip */}
      <div
        ref={tooltipRef}
        role="dialog"
        aria-modal="true"
        aria-label={t(current.titleKey)}
        style={{ ...getTooltipStyle(), zIndex: 50 }}
        className={`bg-bg-elevated border border-border rounded-xl shadow-2xl p-5 relative ${getArrowClass()}`}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-2">
          <h2 className="font-bold text-text-primary text-base leading-snug">{t(current.titleKey)}</h2>
          <button
            onClick={onClose}
            className="shrink-0 text-text-secondary hover:text-text-primary transition-colors mt-0.5"
            aria-label={t('tour.skip')}
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <p className="text-text-secondary text-sm leading-relaxed mb-4">{t(current.bodyKey)}</p>

        {/* Progress dots */}
        <div className="flex items-center justify-center gap-1.5 mb-4">
          {STEPS.map((_, i) => (
            <span
              key={i}
              className={`block rounded-full transition-all ${
                i === step
                  ? 'w-4 h-1.5 bg-accent-primary'
                  : 'w-1.5 h-1.5 bg-border'
              }`}
            />
          ))}
        </div>

        {/* Controls */}
        <div className="flex items-center justify-between gap-3">
          <button
            onClick={handleBack}
            disabled={step === 0}
            className="flex items-center gap-1 text-sm text-text-secondary hover:text-text-primary disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          >
            <ChevronLeft className="w-4 h-4" aria-hidden="true" />
            {t('tour.back')}
          </button>

          <span className="text-xs text-text-secondary">
            {t('tour.stepLabel', { current: step + 1, total: STEPS.length })}
          </span>

          <button
            onClick={handleNext}
            className="flex items-center gap-1 text-sm font-medium text-accent-primary hover:text-amber-400 transition-colors"
          >
            {step < STEPS.length - 1 ? t('tour.next') : t('tour.finish')}
            {step < STEPS.length - 1 && <ChevronRight className="w-4 h-4" aria-hidden="true" />}
          </button>
        </div>
      </div>
    </>,
    document.body
  )
}
