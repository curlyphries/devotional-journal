/**
 * Unsaved lesson answers, kept on this device so an accidental reload does not
 * lose them. One draft per study + lesson; removed once the answers are saved.
 */
export interface LessonDraft {
  /** Answer text keyed by the question it answers. */
  answers: Record<string, string>
  stoodOut: string
  understanding: number | null
  resonance: number | null
}

const draftKey = (studyId: string, lesson: number) => `study-draft:${studyId}:${lesson}`

function toScale(value: unknown): number | null {
  return typeof value === 'number' && Number.isInteger(value) && value >= 1 && value <= 5 ? value : null
}

export function isDraftEmpty(draft: LessonDraft): boolean {
  return (
    !draft.stoodOut.trim() &&
    Object.values(draft.answers).every((answer) => !answer.trim()) &&
    draft.understanding === null &&
    draft.resonance === null
  )
}

export function loadDraft(studyId: string, lesson: number): LessonDraft | null {
  try {
    const raw = window.localStorage.getItem(draftKey(studyId, lesson))
    if (!raw) return null
    const parsed = JSON.parse(raw) as Partial<LessonDraft> | null
    if (!parsed || typeof parsed !== 'object') return null
    const answers: Record<string, string> = {}
    if (parsed.answers && typeof parsed.answers === 'object') {
      for (const [question, answer] of Object.entries(parsed.answers)) {
        if (typeof answer === 'string') answers[question] = answer
      }
    }
    const draft: LessonDraft = {
      answers,
      stoodOut: typeof parsed.stoodOut === 'string' ? parsed.stoodOut : '',
      understanding: toScale(parsed.understanding),
      resonance: toScale(parsed.resonance),
    }
    return isDraftEmpty(draft) ? null : draft
  } catch {
    // Storage unavailable or the draft is unreadable: start with an empty form.
    return null
  }
}

export function saveDraft(studyId: string, lesson: number, draft: LessonDraft): void {
  try {
    window.localStorage.setItem(draftKey(studyId, lesson), JSON.stringify(draft))
  } catch {
    // Storage full or unavailable (private mode): the form still works, just without a safety net.
  }
}

export function clearDraft(studyId: string, lesson: number): void {
  try {
    window.localStorage.removeItem(draftKey(studyId, lesson))
  } catch {
    // Nothing to clear.
  }
}
