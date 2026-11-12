/** BCP-47 locale for the active UI language. */
export function localeFor(language: string | undefined): string {
  return language?.startsWith('es') ? 'es' : 'en-US'
}

/**
 * Parse a date. Date-only strings ("2026-11-12") are read as local calendar
 * days — `new Date('2026-11-12')` would be UTC midnight, which displays as the
 * previous day in the Americas.
 */
export function parseDate(value: string): Date {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value)
  if (match) return new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]))
  return new Date(value)
}

export function formatDate(
  value: string | null | undefined,
  language: string | undefined,
  options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' }
): string {
  if (!value) return ''
  const date = parseDate(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString(localeFor(language), options)
}

export function formatDateTime(value: string | null | undefined, language: string | undefined): string {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString(localeFor(language), { dateStyle: 'medium', timeStyle: 'short' })
}

/** Today's date as YYYY-MM-DD in the user's own timezone. */
export function todayLocalISO(): string {
  const now = new Date()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${now.getFullYear()}-${month}-${day}`
}
