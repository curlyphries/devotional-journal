/**
 * Bible hooks
 */
import { useQuery } from '@tanstack/react-query'
import { getTranslations, readPassage, searchBible } from '../api/bible'

export function useTranslations() {
  return useQuery({
    queryKey: ['bibleTranslations'],
    queryFn: getTranslations,
    staleTime: Infinity, // Translations don't change
  })
}

export function usePassage(params: {
  translation: string
  book: string
  chapter: number
  verse_start?: number
  verse_end?: number
}) {
  return useQuery({
    queryKey: ['passage', params],
    queryFn: () => readPassage(params),
    enabled: !!params.translation && !!params.book && !!params.chapter,
    staleTime: Infinity, // Bible text doesn't change
  })
}

export function useBibleSearch(params: { translation: string; q: string }) {
  return useQuery({
    queryKey: ['bibleSearch', params],
    queryFn: () => searchBible(params),
    enabled: !!params.translation && params.q.length >= 3,
  })
}
