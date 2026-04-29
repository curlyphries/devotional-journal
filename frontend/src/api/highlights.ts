import client from './client'

export interface VerseHighlight {
  id: string
  book: string
  chapter: number
  verse_start: number
  verse_end?: number
  translation: string
  color: 'yellow' | 'green' | 'blue' | 'pink' | 'orange'
  note: string
  reference: string
  created_at: string
  updated_at: string
}

export interface CreateHighlight {
  book: string
  chapter: number
  verse_start: number
  verse_end?: number
  translation?: string
  color?: VerseHighlight['color']
  note?: string
}

export const getHighlights = async (filters?: {
  book?: string
  chapter?: number
  translation?: string
}): Promise<VerseHighlight[]> => {
  const response = await client.get('/bible/highlights/', { params: filters })
  return response.data
}

export const createHighlight = async (data: CreateHighlight): Promise<VerseHighlight> => {
  const response = await client.post('/bible/highlights/', data)
  return response.data
}

export const updateHighlight = async (id: string, data: Partial<CreateHighlight>): Promise<VerseHighlight> => {
  const response = await client.patch(`/bible/highlights/${id}/`, data)
  return response.data
}

export const deleteHighlight = async (id: string): Promise<void> => {
  await client.delete(`/bible/highlights/${id}/`)
}
