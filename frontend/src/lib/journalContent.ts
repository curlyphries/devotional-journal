/**
 * Journal entry content format.
 *
 * An entry's stored text may begin with a machine-readable metadata block:
 *
 *   <!-- DJ_META_START -->
 *   { "passage": "John 3", "capture_type": "quick", ... }
 *   <!-- DJ_META_END -->
 *
 *   The words the user actually wrote…
 *
 * This module is the single place that reads and writes that format. The
 * block is always written with JSON.stringify so quotes and newlines in
 * values cannot corrupt it. Older entries used `**Theme:** …` marker lines;
 * those are still read (and are rewritten in the new format on next save).
 */

export const DJ_META_START = '<!-- DJ_META_START -->'
export const DJ_META_END = '<!-- DJ_META_END -->'

export type JournalMeta = Record<string, unknown>

export interface ParsedJournalContent {
  /** Every metadata field found, unknown keys included, so nothing is lost on re-save. */
  meta: JournalMeta
  planTitle?: string
  dayNumber?: string
  theme?: string
  passage?: string
  aiInsight?: string
  /** The text the user wrote, without any metadata. */
  userContent: string
}

function asText(value: unknown): string | undefined {
  if (typeof value === 'string') return value.trim() ? value : undefined
  if (typeof value === 'number') return String(value)
  return undefined
}

function fromMeta(meta: JournalMeta, userContent: string): ParsedJournalContent {
  return {
    meta,
    planTitle: asText(meta.planTitle),
    dayNumber: asText(meta.dayNumber),
    theme: asText(meta.theme),
    passage: asText(meta.passage),
    aiInsight: asText(meta.aiInsight),
    userContent,
  }
}

function parseLegacy(content: string): ParsedJournalContent {
  const lines = content.split('\n')
  const meta: JournalMeta = {}
  let contentStartIndex = 0

  // Markers are only honoured in the first few lines, so a user typing
  // "**Theme:**" in the body of an entry is left alone.
  for (let i = 0; i < lines.length && i <= 10; i++) {
    const line = lines[i].trim()

    const planMatch = line.match(/^\*\*(.+?)\*\*\s*-\s*Day\s*(\d+)/)
    if (planMatch) {
      meta.planTitle = planMatch[1]
      meta.dayNumber = planMatch[2]
      contentStartIndex = i + 1
      continue
    }

    const themeMatch = line.match(/^\*\*Theme:\*\*\s*(.+)/)
    if (themeMatch) {
      meta.theme = themeMatch[1]
      contentStartIndex = i + 1
      continue
    }

    const passageMatch = line.match(/^\*\*Passage:\*\*\s*(.+)/)
    if (passageMatch) {
      meta.passage = passageMatch[1]
      contentStartIndex = i + 1
      continue
    }

    if (/^\*\*AI Insight:\*\*/.test(line)) {
      const insightLines: string[] = []
      let end = lines.length
      for (let j = i + 1; j < lines.length; j++) {
        if (lines[j].trim() === '---') {
          end = j + 1
          break
        }
        insightLines.push(lines[j])
      }
      meta.aiInsight = insightLines.join('\n').trim()
      contentStartIndex = end
      i = end - 1
      continue
    }

    if (line === '---') {
      contentStartIndex = i + 1
      continue
    }

    if (line && !line.startsWith('**')) break
  }

  return fromMeta(meta, lines.slice(contentStartIndex).join('\n').trim())
}

/** Split stored entry text into metadata and the user's own words. */
export function parseJournalContent(content: string | null | undefined): ParsedJournalContent {
  const text = content ?? ''
  const start = text.indexOf(DJ_META_START)

  if (start !== -1) {
    const end = text.indexOf(DJ_META_END, start)
    if (end === -1) {
      // A truncated preview: the block never closes, so none of what follows
      // is the user's text.
      return fromMeta({}, text.slice(0, start).trim())
    }
    const before = text.slice(0, start).trim()
    const after = text.slice(end + DJ_META_END.length).trim()
    const userContent = [before, after].filter(Boolean).join('\n\n')
    try {
      const parsed: unknown = JSON.parse(text.slice(start + DJ_META_START.length, end))
      const meta =
        typeof parsed === 'object' && parsed !== null && !Array.isArray(parsed)
          ? (parsed as JournalMeta)
          : {}
      return fromMeta(meta, userContent)
    } catch {
      // Unreadable block (older builds wrote it by string interpolation).
      // Still never show it to the user.
      return fromMeta({}, userContent)
    }
  }

  return parseLegacy(text)
}

/** Drop empty values so the stored block stays small and stable. */
function cleanMeta(meta: JournalMeta | null | undefined): JournalMeta {
  const out: JournalMeta = {}
  if (!meta) return out
  for (const [key, value] of Object.entries(meta)) {
    if (value === null || value === undefined || value === '') continue
    if (Array.isArray(value) && value.length === 0) continue
    out[key] = value
  }
  return out
}

/** Build the text to store: metadata block (if any) followed by the user's words. */
export function buildJournalContent(meta: JournalMeta | null | undefined, userContent: string): string {
  const cleaned = cleanMeta(meta)
  if (Object.keys(cleaned).length === 0) return userContent
  return `${DJ_META_START}\n${JSON.stringify(cleaned, null, 2)}\n${DJ_META_END}\n\n${userContent}`
}

/** The user's own words only — safe to show in lists and previews. */
export function stripJournalMeta(content: string | null | undefined): string {
  return parseJournalContent(content).userContent
}
