import client from './client'

export interface Translation {
  code: string
  name: string
  language: string
  public_domain?: boolean
  attribution?: string
}

export interface LocalPassageResponse {
  translation: {
    code: string
    name: string
    language: string
  }
  verses: Array<{
    book: string
    book_name: string
    chapter: number
    verse: number
    text: string
    translation_code: string
  }>
  full_text: string
}

export interface BibleSearchResult {
  book: string
  book_name: string
  chapter: number
  verse: number
  text: string
  translation_code: string
}

export interface BibleSearchResponse {
  query: string
  translation: {
    code: string
    name: string
    language: string
  }
  results: BibleSearchResult[]
  count: number
}

export interface Verse {
  verse: number
  text: string
  translation: string
  book: string
  chapter: number
}

export interface PassageResponse {
  source: string
  translation: {
    code: string
    name: string
    language: string
  }
  book: string
  chapter: number
  verses: Verse[]
  full_text: string
  attribution?: string
}

// Strip Strong's numbers and other markup from text
// Removes: <S>1697</S> (Strong's numbers), <sup>...</sup> (footnotes/annotations), and other HTML tags
export function cleanVerseText(text: string): string {
  return text
    .replace(/<S>\d+<\/S>/g, '')           // Remove Strong's numbers
    .replace(/<sup>[^<]*<\/sup>/gi, '')    // Remove superscript annotations
    .replace(/<[^>]+>/g, '')               // Remove any remaining HTML tags
    .replace(/\s+/g, ' ')                  // Normalize whitespace
    .trim()
}

export const getTranslations = async (): Promise<Translation[]> => {
  // Use Bolls API translations
  const response = await client.get('/bible/bolls/translations/')
  return response.data.translations
}

export const readPassage = async (params: {
  translation: string
  book: string
  chapter: number
  verse_start?: number
  verse_end?: number
}): Promise<LocalPassageResponse> => {
  const response = await client.get('/bible/read/', { params })
  return response.data
}

export const searchBible = async (params: { translation: string; q: string }): Promise<BibleSearchResponse> => {
  const response = await client.get('/bible/search/', {
    params: {
      translation: params.translation,
      query: params.q,
    },
  })
  return response.data
}

export const getPassage = async (
  book: string,
  chapter: number,
  translation: string = 'KJV',
  verseStart?: number,
  verseEnd?: number
): Promise<PassageResponse> => {
  const params: Record<string, string | number> = {
    book,
    chapter,
    translation,
  }
  if (verseStart) params.verse_start = verseStart
  if (verseEnd) params.verse_end = verseEnd
  
  // Use Bolls API for passage reading
  const response = await client.get('/bible/bolls/read/', { params })
  
  // Clean Strong's numbers from verse text
  const data = response.data
  data.verses = data.verses.map((v: Verse) => ({
    ...v,
    text: cleanVerseText(v.text)
  }))
  data.full_text = cleanVerseText(data.full_text)
  
  return data
}

// Parse passage reference like "Genesis 3:1-19" or "NEH 1"
export function parsePassageReference(ref: string): {
  book: string
  chapter: number
  verseStart?: number
  verseEnd?: number
} | null {
  // Handle formats: "Genesis 3:1-19", "NEH 1", "Psalm 23", "1 Samuel 15:17-23"
  const match = ref.match(/^(\d?\s*[A-Za-z]+)\s*(\d+)(?::(\d+)(?:-(\d+))?)?$/)
  if (!match) return null
  
  return {
    book: match[1].trim(),
    chapter: parseInt(match[2]),
    verseStart: match[3] ? parseInt(match[3]) : undefined,
    verseEnd: match[4] ? parseInt(match[4]) : undefined,
  }
}
