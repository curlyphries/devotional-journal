import { useEffect, useRef, type RefObject } from 'react'

const FOCUSABLE =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'

/**
 * Keyboard behaviour for a modal dialog: while `active`, Tab stays inside the
 * container, Esc calls `onEscape`, and when the dialog closes focus goes back
 * to whatever had it before. Moving focus *into* the dialog is left to the
 * caller (autoFocus or an explicit .focus()), since the right first target
 * differs per dialog.
 */
export function useDialogFocus(
  containerRef: RefObject<HTMLElement>,
  active: boolean,
  onEscape?: () => void
): void {
  const onEscapeRef = useRef(onEscape)
  useEffect(() => {
    onEscapeRef.current = onEscape
  }, [onEscape])

  useEffect(() => {
    if (!active) return
    const opener = document.activeElement instanceof HTMLElement ? document.activeElement : null

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onEscapeRef.current?.()
        return
      }
      const container = containerRef.current
      if (event.key !== 'Tab' || !container) return
      const focusable = Array.from(container.querySelectorAll<HTMLElement>(FOCUSABLE))
      if (focusable.length === 0) {
        event.preventDefault()
        container.focus()
        return
      }
      const first = focusable[0]
      const last = focusable[focusable.length - 1]
      const current = document.activeElement
      const outside = !container.contains(current)
      if (event.shiftKey && (current === first || current === container || outside)) {
        event.preventDefault()
        last.focus()
      } else if (!event.shiftKey && (current === last || outside)) {
        event.preventDefault()
        first.focus()
      }
    }

    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      // Only restore if the opener is still on the page.
      if (opener && document.contains(opener)) opener.focus()
    }
  }, [active, containerRef])
}
