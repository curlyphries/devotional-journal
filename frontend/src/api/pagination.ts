/** DRF page envelope returned by every router viewset list endpoint. */
export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

/**
 * Return the items of a list response whether the server sent a bare array
 * or a paginated envelope. Anything else yields an empty list.
 */
export function unwrapList<T>(data: unknown): T[] {
  if (Array.isArray(data)) return data as T[]
  if (data && typeof data === 'object' && Array.isArray((data as Paginated<T>).results)) {
    return (data as Paginated<T>).results
  }
  return []
}
