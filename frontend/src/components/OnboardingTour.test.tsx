import { describe, it, expect, vi, afterEach } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '../i18n'
import en from '../i18n/en.json'
import es from '../i18n/es.json'
import OnboardingTour, { TOUR_STEPS, requestTourRestart, type TourStep } from './OnboardingTour'

const STEPS: TourStep[] = [
  { key: 'tour.welcome', targets: [] },
  { key: 'tour.write', targets: ['[data-tour-id="fab"]'] },
  { key: 'tour.help', targets: ['[data-tour-id="help"]'] },
]

/** jsdom has no layout; give an element a real-looking box. */
function addAnchor(id: string) {
  const el = document.createElement('button')
  el.setAttribute('data-tour-id', id)
  el.getBoundingClientRect = () =>
    ({ top: 100, left: 40, right: 140, bottom: 140, width: 100, height: 40, x: 40, y: 100, toJSON: () => ({}) }) as DOMRect
  document.body.appendChild(el)
  return el
}

function lookup(source: unknown, key: string): unknown {
  return key.split('.').reduce<unknown>(
    (node, part) => (node && typeof node === 'object' ? (node as Record<string, unknown>)[part] : undefined),
    source
  )
}

afterEach(() => {
  document.querySelectorAll('[data-tour-id]').forEach((el) => el.remove())
  window.sessionStorage.clear()
})

describe('OnboardingTour', () => {
  it('renders nothing when closed', () => {
    render(<OnboardingTour open={false} onClose={vi.fn()} steps={STEPS} />)
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('advances and goes back through the steps, then finishes', async () => {
    addAnchor('fab')
    addAnchor('help')
    const onClose = vi.fn()
    const user = userEvent.setup()
    render(<OnboardingTour open onClose={onClose} steps={STEPS} />)

    const dialog = screen.getByRole('dialog', { name: 'Welcome to your Devotional Journal' })
    expect(dialog).toHaveFocus()
    expect(screen.getByText('Step 1 of 3')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Back' })).toBeDisabled()

    await user.click(screen.getByRole('button', { name: 'Next' }))
    expect(screen.getByRole('dialog', { name: 'Start with an entry' })).toHaveAttribute('data-anchored', 'true')
    expect(screen.getByTestId('tour-spotlight')).toBeInTheDocument()
    expect(screen.getByText('Step 2 of 3')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Back' }))
    expect(screen.getByText('Step 1 of 3')).toBeInTheDocument()

    // Arrow keys work too.
    await user.keyboard('{ArrowRight}{ArrowRight}')
    expect(screen.getByText('Step 3 of 3')).toBeInTheDocument()
    await user.keyboard('{ArrowLeft}')
    expect(screen.getByText('Step 2 of 3')).toBeInTheDocument()
    await user.keyboard('{ArrowRight}')

    expect(onClose).not.toHaveBeenCalled()
    await user.click(screen.getByRole('button', { name: 'Got it' }))
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('falls back to a centred card when the anchor is missing or hidden', async () => {
    // "fab" exists but has no size (hidden); "help" does not exist at all.
    const hidden = document.createElement('button')
    hidden.setAttribute('data-tour-id', 'fab')
    document.body.appendChild(hidden)
    const user = userEvent.setup()
    render(<OnboardingTour open onClose={vi.fn()} steps={STEPS} />)

    await user.click(screen.getByRole('button', { name: 'Next' }))
    expect(screen.getByRole('dialog', { name: 'Start with an entry' })).toHaveAttribute('data-anchored', 'false')
    expect(screen.queryByTestId('tour-spotlight')).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Next' }))
    expect(screen.getByRole('dialog', { name: 'Questions, or something went wrong?' })).toHaveAttribute(
      'data-anchored',
      'false'
    )
  })

  it('closes on Escape and returns focus to the opener', async () => {
    const opener = document.createElement('button')
    opener.textContent = 'Replay'
    document.body.appendChild(opener)
    opener.focus()

    const onClose = vi.fn()
    const user = userEvent.setup()
    const { rerender } = render(<OnboardingTour open onClose={onClose} steps={STEPS} />)
    expect(screen.getByRole('dialog')).toHaveFocus()

    await user.keyboard('{Escape}')
    expect(onClose).toHaveBeenCalledTimes(1)

    rerender(<OnboardingTour open={false} onClose={onClose} steps={STEPS} />)
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(opener).toHaveFocus()
    opener.remove()
  })

  it('can be skipped from any step', async () => {
    const onClose = vi.fn()
    const user = userEvent.setup()
    render(<OnboardingTour open onClose={onClose} steps={STEPS} />)
    await user.click(screen.getByRole('button', { name: 'Skip tour' }))
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('restarts on request, whether already mounted or mounted later', () => {
    const onClose = vi.fn()
    const { unmount } = render(<OnboardingTour open={false} onClose={onClose} steps={STEPS} />)
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    act(() => requestTourRestart())
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    unmount()

    // Requested from another page: the tour picks it up when it next mounts.
    requestTourRestart()
    render(<OnboardingTour open={false} onClose={onClose} steps={STEPS} />)
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })

  it('has between 7 and 9 steps, each translated in English and Spanish', () => {
    expect(TOUR_STEPS.length).toBeGreaterThanOrEqual(7)
    expect(TOUR_STEPS.length).toBeLessThanOrEqual(9)
    for (const step of TOUR_STEPS) {
      for (const source of [en, es]) {
        expect(typeof lookup(source, `${step.key}.title`)).toBe('string')
        expect(typeof lookup(source, `${step.key}.body`)).toBe('string')
      }
    }
  })
})
