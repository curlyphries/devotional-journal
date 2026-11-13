import { useId, useLayoutEffect, useRef } from 'react'
import DictationButton from '../DictationButton'

interface ReflectFieldProps {
  /** The question, shown as the field's label. */
  label: string
  value: string
  onChange: (value: string) => void
  placeholder?: string
  /** Show the microphone button under the field. */
  dictation?: boolean
  disabled?: boolean
}

/** A question with a textarea that grows with what is written, and optional dictation. */
export default function ReflectField({
  label,
  value,
  onChange,
  placeholder,
  dictation = true,
  disabled = false,
}: ReflectFieldProps) {
  const id = useId()
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-grow: fit the content so nobody writes inside a tiny scrolling box.
  useLayoutEffect(() => {
    const textarea = textareaRef.current
    if (!textarea) return
    textarea.style.height = 'auto'
    if (textarea.scrollHeight > 0) textarea.style.height = `${textarea.scrollHeight + 2}px`
  }, [value])

  return (
    <div>
      <label htmlFor={id} className="mb-2 block font-medium leading-snug text-text-primary">
        {label}
      </label>
      <textarea
        id={id}
        ref={textareaRef}
        value={value}
        rows={3}
        disabled={disabled}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
        className="input block min-h-[6rem] w-full resize-none overflow-hidden font-serif text-base leading-relaxed"
      />
      {dictation && (
        <DictationButton
          className="mt-2"
          value={value}
          onChange={onChange}
          textareaRef={textareaRef}
          hidePrivacyNote
        />
      )}
    </div>
  )
}
