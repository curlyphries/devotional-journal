import { useId, type ReactNode } from 'react'
import { useTranslation } from 'react-i18next'

const SCALE = [1, 2, 3, 4, 5] as const

interface ScaleInputProps {
  /** The statement or question being rated; names the radio group. */
  label: ReactNode
  /** Optional smaller line under the label. */
  hint?: ReactNode
  value: number | null | undefined
  /** `null` clears the answer: every item can be left unanswered. */
  onChange: (value: number | null) => void
  disabled?: boolean
  className?: string
}

/**
 * A 1-5 rating as a labelled radio group. Native radios, so arrow keys move
 * between the options. Deliberately colour-neutral: a number on this scale is
 * a description, not a grade.
 */
export function ScaleInput({ label, hint, value, onChange, disabled = false, className = '' }: ScaleInputProps) {
  const { t } = useTranslation()
  const id = useId()
  const labelId = `${id}-label`
  const hintId = `${id}-hint`

  return (
    <div
      role="radiogroup"
      aria-labelledby={labelId}
      aria-describedby={hint ? hintId : undefined}
      className={className}
    >
      <p id={labelId} className="text-text-primary">
        {label}
      </p>
      {hint && (
        <p id={hintId} className="mt-0.5 text-sm text-text-secondary">
          {hint}
        </p>
      )}
      <div className="mt-2 flex flex-wrap items-center gap-2">
        {SCALE.map((option) => (
          <label key={option} className="relative cursor-pointer">
            <input
              type="radio"
              name={id}
              value={option}
              checked={value === option}
              disabled={disabled}
              onChange={() => onChange(option)}
              aria-label={t('growth.scale.option', { value: option })}
              className="peer sr-only"
            />
            <span
              aria-hidden="true"
              className="flex h-11 w-11 items-center justify-center rounded-full border border-border bg-bg-elevated text-base font-semibold text-text-primary transition-colors hover:border-accent-primary peer-checked:border-accent-primary peer-checked:bg-accent-primary peer-checked:text-white peer-focus-visible:ring-2 peer-focus-visible:ring-accent-primary peer-focus-visible:ring-offset-2 peer-focus-visible:ring-offset-bg-surface peer-disabled:cursor-not-allowed peer-disabled:opacity-60"
            >
              {option}
            </span>
          </label>
        ))}
        {value != null && !disabled && (
          <button
            type="button"
            onClick={() => onChange(null)}
            className="rounded px-2 py-1 text-sm text-text-secondary underline-offset-2 hover:text-text-primary hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary"
          >
            {t('growth.scale.clear')}
          </button>
        )}
      </div>
    </div>
  )
}

interface MeterBarProps {
  label: string
  /** Null renders an empty track and the words "Not answered". */
  value: number | null
  max?: number
  /** Text shown at the right; defaults to "3 of 5". */
  valueText?: string
  /** `neutral` for anything that describes a person; `accent` for progress on a task. */
  tone?: 'neutral' | 'accent'
  className?: string
}

/** A labelled horizontal bar. Never red or green: it describes, it does not grade. */
export function MeterBar({ label, value, max = 5, valueText, tone = 'neutral', className = '' }: MeterBarProps) {
  const { t } = useTranslation()
  const answered = value != null
  const clamped = answered ? Math.max(0, Math.min(max, value)) : 0
  const text = answered ? (valueText ?? t('growth.scale.value', { value, max })) : t('growth.scale.notAnswered')

  return (
    <div className={className}>
      <div className="flex items-baseline justify-between gap-3 text-sm">
        <span className="min-w-0 break-words text-text-primary">{label}</span>
        <span className="flex-shrink-0 text-text-secondary">{text}</span>
      </div>
      {answered ? (
        <div
          role="meter"
          aria-label={label}
          aria-valuemin={0}
          aria-valuemax={max}
          aria-valuenow={clamped}
          aria-valuetext={text}
          className="mt-1.5 h-2 overflow-hidden rounded-full bg-bg-elevated"
        >
          <div
            className={`h-full rounded-full ${tone === 'accent' ? 'bg-accent-primary' : 'bg-text-secondary'}`}
            style={{ width: `${max > 0 ? (clamped / max) * 100 : 0}%` }}
          />
        </div>
      ) : (
        <div aria-hidden="true" className="mt-1.5 h-2 rounded-full border border-dashed border-border" />
      )}
    </div>
  )
}

interface ChipProps {
  selected: boolean
  onToggle: () => void
  disabled?: boolean
  onFocus?: () => void
  onMouseEnter?: () => void
  children: ReactNode
}

/** A toggle chip (`aria-pressed`) for single- and multi-select lists. */
export function Chip({ selected, onToggle, disabled = false, onFocus, onMouseEnter, children }: ChipProps) {
  return (
    <button
      type="button"
      aria-pressed={selected}
      disabled={disabled}
      onClick={onToggle}
      onFocus={onFocus}
      onMouseEnter={onMouseEnter}
      className={`rounded-full border px-3 py-1.5 text-left text-sm transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary focus-visible:ring-offset-2 focus-visible:ring-offset-bg-surface disabled:cursor-not-allowed disabled:opacity-50 ${
        selected
          ? 'border-accent-primary bg-accent-primary/20 text-text-primary'
          : 'border-border bg-bg-elevated text-text-primary hover:border-accent-primary'
      }`}
    >
      {children}
    </button>
  )
}

/** A 1-5 rating as five neutral dots, with the number for screen readers. */
export function RatingDots({ rating, max = 5 }: { rating: number; max?: number }) {
  const { t } = useTranslation()
  return (
    <span className="inline-flex items-center gap-1" role="img" aria-label={t('growth.scale.value', { value: rating, max })}>
      {Array.from({ length: max }, (_, index) => (
        <span
          key={index}
          aria-hidden="true"
          className={`h-2.5 w-2.5 rounded-full border ${
            index < rating ? 'border-text-secondary bg-text-secondary' : 'border-border bg-transparent'
          }`}
        />
      ))}
    </span>
  )
}

/** A count next to a theme, as used on the audit page. */
export function ThemeChips({ themes, label }: { themes: { theme: string; count: number }[]; label: string }) {
  const { t } = useTranslation()
  return (
    <ul className="flex flex-wrap gap-2" aria-label={label}>
      {themes.map((item) => (
        <li
          key={item.theme}
          className="inline-flex items-center gap-2 rounded-full border border-border bg-bg-elevated px-3 py-1 text-sm text-text-primary"
        >
          {item.theme}
          <span className="rounded-full bg-bg-surface px-1.5 text-xs font-medium text-text-secondary">
            <span className="sr-only">{t('audit.themes.times')} </span>
            {item.count}
          </span>
        </li>
      ))}
    </ul>
  )
}

/** A calm notice: information, not an alarm. */
export function Notice({
  icon,
  title,
  children,
  className = '',
  role = 'note',
}: {
  icon?: ReactNode
  title?: ReactNode
  children: ReactNode
  className?: string
  role?: 'note' | 'status'
}) {
  return (
    <div role={role} className={`flex items-start gap-3 rounded-xl border border-border bg-bg-elevated p-4 text-sm ${className}`}>
      {icon && <span className="mt-0.5 flex-shrink-0 text-accent-primary">{icon}</span>}
      <div className="min-w-0 flex-1 space-y-1 break-words">
        {title && <p className="font-semibold text-text-primary">{title}</p>}
        {children}
      </div>
    </div>
  )
}
