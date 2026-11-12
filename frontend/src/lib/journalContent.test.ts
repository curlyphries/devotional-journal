import { describe, it, expect } from 'vitest'
import {
  DJ_META_START,
  DJ_META_END,
  buildJournalContent,
  parseJournalContent,
  stripJournalMeta,
} from './journalContent'

describe('journalContent', () => {
  it('round-trips metadata containing quotes, newlines and delimiters-like text', () => {
    const meta = {
      focus_intention: 'Trust God "fully"\nand rest — even when it\'s hard \\ slow',
      focus_themes: ['peace', 'say "no"'],
      capture_type: 'quick',
      passage: 'John 3:16',
    }
    const body = 'Today was hard.\n\nHe said "wait", so I waited.'
    const stored = buildJournalContent(meta, body)

    const parsed = parseJournalContent(stored)
    expect(parsed.userContent).toBe(body)
    expect(parsed.meta).toEqual(meta)
    expect(parsed.passage).toBe('John 3:16')
    // Saving again must not change anything.
    expect(buildJournalContent(parsed.meta, parsed.userContent)).toBe(stored)
  })

  it('writes no block when there is no metadata', () => {
    expect(buildJournalContent({}, 'Just text')).toBe('Just text')
    expect(buildJournalContent({ theme: '', planTitle: null, highlights: [] }, 'Just text')).toBe('Just text')
  })

  it('strips the metadata block for previews', () => {
    const stored = buildJournalContent({ capture_type: 'quick' }, 'What I wrote')
    expect(stored).toContain(DJ_META_START)
    expect(stripJournalMeta(stored)).toBe('What I wrote')
  })

  it('never shows a broken or truncated block', () => {
    // Older builds interpolated strings, producing invalid JSON.
    const broken = `${DJ_META_START}\n{ "focus_intention": "say "hi"" }\n${DJ_META_END}\n\nReal text`
    expect(stripJournalMeta(broken)).toBe('Real text')

    const truncated = `${DJ_META_START}\n{ "focus_intention": "a very long inten`
    expect(stripJournalMeta(truncated)).toBe('')
  })

  it('reads the legacy marker format', () => {
    const legacy = '**Gospel of John** - Day 3\n**Theme:** New birth\n**Passage:** John 3\n---\nMy thoughts'
    const parsed = parseJournalContent(legacy)
    expect(parsed.planTitle).toBe('Gospel of John')
    expect(parsed.dayNumber).toBe('3')
    expect(parsed.theme).toBe('New birth')
    expect(parsed.passage).toBe('John 3')
    expect(parsed.userContent).toBe('My thoughts')
  })

  it('leaves plain text and empty input alone', () => {
    expect(stripJournalMeta('Plain entry')).toBe('Plain entry')
    expect(stripJournalMeta(undefined)).toBe('')
  })
})
