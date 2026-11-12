/** The mood tags an entry can carry. Labels come from i18n: `journal.moods.<id>`. */
export interface Mood {
  id: string
  emoji: string
  /** Tailwind classes for a small badge. */
  badgeClass: string
}

export const MOODS: Mood[] = [
  { id: 'grateful', emoji: '🙏', badgeClass: 'bg-success/20 text-success' },
  { id: 'struggling', emoji: '😔', badgeClass: 'bg-text-secondary/20 text-text-secondary' },
  { id: 'convicted', emoji: '💭', badgeClass: 'bg-accent-primary/20 text-accent-primary' },
  { id: 'peaceful', emoji: '😌', badgeClass: 'bg-accent-secondary/20 text-text-primary' },
  { id: 'fired_up', emoji: '🔥', badgeClass: 'bg-danger/20 text-text-primary' },
]

export function getMood(id: string | null | undefined): Mood | undefined {
  return MOODS.find((mood) => mood.id === id)
}

export function moodLabelKey(id: string): string {
  return `journal.moods.${id}`
}
