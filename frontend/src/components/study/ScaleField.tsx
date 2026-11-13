import { useId } from 'react'

const STEPS = [1, 2, 3, 4, 5]

interface ScaleFieldProps {
  /** The question being rated; becomes the group's name. */
  legend: string
  /** What 1 means, e.g. "lost". */
  lowLabel: string
  /** What 5 means, e.g. "clear". */
  highLabel: string
  value: number | null
  onChange: (value: number) => void
  disabled?: boolean
}

/** A 1-5 rating as a native radio group, with both ends of the scale spelled out. */
export default function ScaleField({ legend, lowLabel, highLabel, value, onChange, disabled = false }: ScaleFieldProps) {
  const name = useId()

  return (
    <fieldset className="min-w-0" disabled={disabled}>
      <legend className="mb-3 font-medium leading-snug text-text-primary">{legend}</legend>
      <div className="flex max-w-sm items-center justify-between gap-2">
        {STEPS.map((step) => {
          const endLabel = step === 1 ? lowLabel : step === 5 ? highLabel : null
          return (
            <label key={step} className="relative cursor-pointer">
              <input
                type="radio"
                name={name}
                value={step}
                checked={value === step}
                onChange={() => onChange(step)}
                className="peer sr-only"
              />
              <span
                className="flex h-11 w-11 items-center justify-center rounded-full border border-border bg-bg-elevated text-base font-semibold text-text-primary transition-colors hover:border-accent-primary peer-checked:border-accent-primary peer-checked:bg-accent-primary peer-checked:text-white peer-focus-visible:ring-2 peer-focus-visible:ring-accent-primary peer-focus-visible:ring-offset-2 peer-focus-visible:ring-offset-bg-surface peer-disabled:cursor-not-allowed peer-disabled:opacity-60"
              >
                {step}
              </span>
              {endLabel && <span className="sr-only"> — {endLabel}</span>}
            </label>
          )
        })}
      </div>
      <div className="mt-2 flex max-w-sm justify-between gap-4 text-xs text-text-secondary" aria-hidden="true">
        <span>1 = {lowLabel}</span>
        <span className="text-right">5 = {highLabel}</span>
      </div>
    </fieldset>
  )
}
