import { useCallback, useEffect, useId, useLayoutEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { useTranslation } from 'react-i18next'
import { X, ChevronLeft, ChevronRight } from 'lucide-react'
import { useDialogFocus } from '../hooks/useDialogFocus'

/**
 * First-run walkthrough of the app.
 *
 * Mounting: DashboardPage renders `<OnboardingTour open onClose />` and
 * records completion in localStorage under `onboarding_tour_completed`.
 *
 * Restarting from anywhere else:
 *   - `requestTourRestart()` (exported below) — call it, then navigate to "/"
 *     if the dashboard is not the current page. It dispatches the window event
 *     `devotional-journal:start-tour` (handled immediately if the tour is
 *     mounted) and also leaves a one-shot sessionStorage flag
 *     (`onboarding_tour_restart`) that the tour consumes the next time it
 *     mounts, i.e. when the dashboard appears.
 *   - or dispatch the event yourself:
 *     `window.dispatchEvent(new Event('devotional-journal:start-tour'))`.
 *
 * Anchors: each step lists CSS selectors, tried in order; the first one that
 * matches a visible element is spotlighted. `data-tour-id` attributes are
 * preferred; nav links are also found by their href so the tour keeps working
 * when the navigation is restyled. A step whose anchor is missing or hidden
 * (e.g. collapsed into a mobile menu) is shown as a centred card instead.
 */

export const TOUR_START_EVENT = 'devotional-journal:start-tour'
export const TOUR_COMPLETED_KEY = 'onboarding_tour_completed'
const TOUR_RESTART_FLAG = 'onboarding_tour_restart'

/** Ask the tour to (re)start. Safe to call from any page; see the comment above. */
export function requestTourRestart(): void {
  try {
    window.sessionStorage.setItem(TOUR_RESTART_FLAG, '1')
  } catch {
    // Storage unavailable (private mode): the event below still works when mounted.
  }
  window.dispatchEvent(new Event(TOUR_START_EVENT))
}

function consumeRestartFlag(): boolean {
  try {
    if (window.sessionStorage.getItem(TOUR_RESTART_FLAG) !== '1') return false
    window.sessionStorage.removeItem(TOUR_RESTART_FLAG)
    return true
  } catch {
    return false
  }
}

export interface TourStep {
  /** i18n key prefix: `${key}.title` and `${key}.body`. */
  key: string
  /** Selectors for the element to spotlight, in order of preference. Empty = centred card. */
  targets: string[]
}

const tourId = (id: string) => `[data-tour-id="${id}"]`
const navLink = (path: string) => `nav a[href$="${path}"]`

export const TOUR_STEPS: TourStep[] = [
  { key: 'tour.welcome', targets: [] },
  { key: 'tour.write', targets: [tourId('new-entry'), tourId('fab')] },
  { key: 'tour.feedback', targets: [] },
  // Desktop: the Study link in the bar. Phone (link is inside the closed menu): the dashboard's study card.
  { key: 'tour.study', targets: [tourId('nav-study'), navLink('/study'), tourId('study-card')] },
  { key: 'tour.speakYourMind', targets: [tourId('speak-your-mind')] },
  { key: 'tour.history', targets: [tourId('nav-journal'), navLink('/journal')] },
  { key: 'tour.devotional', targets: [tourId('nav-devotional'), navLink('/devotional'), tourId('snapshot')] },
  { key: 'tour.progress', targets: [tourId('nav-progress'), navLink('/progress')] },
  { key: 'tour.settings', targets: [tourId('nav-settings'), navLink('/settings')] },
  { key: 'tour.help', targets: [tourId('help'), navLink('/help')] },
]

const PAD = 12
const MAX_TIP_WIDTH = 360

function findTarget(selectors: string[]): HTMLElement | null {
  for (const selector of selectors) {
    let matches: HTMLElement[] = []
    try {
      matches = Array.from(document.querySelectorAll<HTMLElement>(selector))
    } catch {
      continue
    }
    const visible = matches.find((el) => {
      const rect = el.getBoundingClientRect()
      return rect.width > 0 && rect.height > 0
    })
    if (visible) return visible
  }
  return null
}

interface Placement {
  /** Viewport rectangle of the spotlighted element. */
  ring: { top: number; left: number; width: number; height: number }
  tip: { top: number; left: number; width: number }
}

interface Props {
  open: boolean
  onClose: () => void
  /** Override the steps (used by tests). */
  steps?: TourStep[]
}

export default function OnboardingTour({ open, onClose, steps = TOUR_STEPS }: Props) {
  const { t } = useTranslation()
  const titleId = useId()
  const bodyId = useId()
  const [restarted, setRestarted] = useState(false)
  const [step, setStep] = useState(0)
  const [placement, setPlacement] = useState<Placement | null>(null)
  const [tick, setTick] = useState(0)
  const tooltipRef = useRef<HTMLDivElement>(null)
  const scrolledForStep = useRef(-1)

  const isOpen = open || restarted
  const total = steps.length
  const current = steps[Math.min(step, total - 1)]

  // Restart requests: a pending flag from another page, or a live event.
  useEffect(() => {
    if (consumeRestartFlag()) setRestarted(true)
    const onStart = () => {
      consumeRestartFlag()
      setStep(0)
      setRestarted(true)
    }
    window.addEventListener(TOUR_START_EVENT, onStart)
    return () => window.removeEventListener(TOUR_START_EVENT, onStart)
  }, [])

  // Always begin at the first step.
  useEffect(() => {
    if (isOpen) {
      setStep(0)
      scrolledForStep.current = -1
    }
  }, [isOpen])

  const close = useCallback(() => {
    setRestarted(false)
    onClose()
  }, [onClose])

  const next = useCallback(() => {
    if (step < total - 1) setStep(step + 1)
    else close()
  }, [step, total, close])

  const back = useCallback(() => {
    setStep((s) => Math.max(0, s - 1))
  }, [])

  // Tab stays inside the card, Esc closes, focus returns to the opener.
  useDialogFocus(tooltipRef, isOpen, close)

  // Arrow keys move between steps.
  useEffect(() => {
    if (!isOpen) return
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'ArrowRight') {
        event.preventDefault()
        next()
      } else if (event.key === 'ArrowLeft') {
        event.preventDefault()
        back()
      }
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [isOpen, next, back])

  // Move focus into the card on every step so screen readers announce it.
  useEffect(() => {
    if (isOpen) tooltipRef.current?.focus()
  }, [isOpen, step])

  // Re-measure when the page scrolls, resizes, or content loads in late.
  useEffect(() => {
    if (!isOpen) return
    let frame = 0
    const bump = () => {
      cancelAnimationFrame(frame)
      frame = requestAnimationFrame(() => setTick((n) => n + 1))
    }
    window.addEventListener('resize', bump)
    window.addEventListener('scroll', bump, true)
    const interval = window.setInterval(bump, 600)
    return () => {
      cancelAnimationFrame(frame)
      window.removeEventListener('resize', bump)
      window.removeEventListener('scroll', bump, true)
      window.clearInterval(interval)
    }
  }, [isOpen])

  // Find the anchor, bring it into view, and place the card next to it —
  // measured, and always inside the viewport.
  useLayoutEffect(() => {
    if (!isOpen) return
    const target = findTarget(current.targets)
    if (!target) {
      setPlacement(null)
      return
    }

    if (scrolledForStep.current !== step) {
      scrolledForStep.current = step
      if (typeof target.scrollIntoView === 'function') {
        target.scrollIntoView({ block: 'center', inline: 'nearest' })
      }
    }

    const rect = target.getBoundingClientRect()
    const vw = window.innerWidth
    const vh = window.innerHeight
    const width = Math.min(MAX_TIP_WIDTH, vw - PAD * 2)
    const height = tooltipRef.current?.offsetHeight ?? 220

    const below = rect.bottom + PAD
    const above = rect.top - PAD - height
    let top: number
    if (below + height <= vh - PAD) top = below
    else if (above >= PAD) top = above
    // Neither side has room (tall anchor or short screen): sit over the lower edge.
    else top = vh - height - PAD
    top = Math.max(PAD, Math.min(top, vh - height - PAD))

    const centred = rect.left + rect.width / 2 - width / 2
    const left = Math.max(PAD, Math.min(centred, vw - width - PAD))

    setPlacement((previous) => {
      const nextPlacement: Placement = {
        ring: { top: rect.top - 4, left: rect.left - 4, width: rect.width + 8, height: rect.height + 8 },
        tip: { top, left, width },
      }
      // Avoid re-rendering when nothing moved.
      return previous && JSON.stringify(previous) === JSON.stringify(nextPlacement) ? previous : nextPlacement
    })
  }, [isOpen, step, tick, current])

  if (!isOpen) return null

  const isLast = step >= total - 1

  const tipStyle: React.CSSProperties = placement
    ? { position: 'fixed', top: placement.tip.top, left: placement.tip.left, width: placement.tip.width }
    : {
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: `min(${MAX_TIP_WIDTH}px, calc(100vw - ${PAD * 2}px))`,
      }

  return createPortal(
    <>
      {/* Keeps clicks from reaching the page while the tour is open. */}
      <div className="fixed inset-0" style={{ zIndex: 58 }} aria-hidden="true" />
      {placement ? (
        // Spotlight: a ring around the anchor; its huge shadow dims everything else.
        <div
          aria-hidden="true"
          data-testid="tour-spotlight"
          style={{
            position: 'fixed',
            top: placement.ring.top,
            left: placement.ring.left,
            width: placement.ring.width,
            height: placement.ring.height,
            borderRadius: 10,
            boxShadow: '0 0 0 9999px rgba(0, 0, 0, 0.6)',
            border: '2px solid #C87533',
            pointerEvents: 'none',
            zIndex: 59,
          }}
        />
      ) : (
        <div className="fixed inset-0 bg-black/60" style={{ zIndex: 59 }} aria-hidden="true" />
      )}

      <div
        ref={tooltipRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={bodyId}
        tabIndex={-1}
        data-anchored={placement ? 'true' : 'false'}
        style={{ ...tipStyle, zIndex: 60, maxHeight: `calc(100vh - ${PAD * 2}px)` }}
        className="overflow-y-auto rounded-xl border border-border bg-bg-elevated p-5 shadow-2xl focus:outline-none"
      >
        <div className="mb-2 flex items-start justify-between gap-3">
          <h2 id={titleId} className="text-base font-bold leading-snug text-text-primary">
            {t(`${current.key}.title`)}
          </h2>
          <button
            type="button"
            onClick={close}
            className="-mr-1 -mt-1 shrink-0 rounded-lg p-1.5 text-text-secondary transition-colors hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary"
            aria-label={t('tour.close')}
          >
            <X className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>

        <p id={bodyId} className="mb-4 text-sm leading-relaxed text-text-secondary">
          {t(`${current.key}.body`)}
        </p>

        <div className="mb-4 flex items-center justify-center gap-1.5" aria-hidden="true">
          {steps.map((s, i) => (
            <span
              key={s.key}
              className={`block rounded-full transition-all ${
                i === step ? 'h-1.5 w-4 bg-accent-primary' : 'h-1.5 w-1.5 bg-border'
              }`}
            />
          ))}
        </div>

        <div className="flex items-center justify-between gap-3">
          <button
            type="button"
            onClick={back}
            disabled={step === 0}
            className="flex items-center gap-1 rounded-lg px-2 py-1.5 text-sm text-text-secondary transition-colors hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary disabled:cursor-not-allowed disabled:opacity-30"
          >
            <ChevronLeft className="h-4 w-4" aria-hidden="true" />
            {t('tour.back')}
          </button>

          <span className="text-xs text-text-secondary" aria-live="polite">
            {t('tour.stepLabel', { current: step + 1, total })}
          </span>

          <button
            type="button"
            onClick={next}
            className="btn-primary flex items-center gap-1 px-3 py-1.5 text-sm"
          >
            {isLast ? t('tour.finish') : t('tour.next')}
            {!isLast && <ChevronRight className="h-4 w-4" aria-hidden="true" />}
          </button>
        </div>

        {!isLast && (
          <button
            type="button"
            onClick={close}
            className="mt-3 block w-full text-center text-xs text-text-secondary underline-offset-2 hover:text-text-primary hover:underline"
          >
            {t('tour.skip')}
          </button>
        )}
      </div>
    </>,
    document.body
  )
}
