/**
 * Journal hooks
 */
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  getJournalEntries,
  getJournalEntry,
  createJournalEntry,
  updateJournalEntry,
  deleteJournalEntry,
  CreateJournalEntry,
} from '../api/journal'

export function useJournalEntries(params?: {
  date_from?: string
  date_to?: string
  mood_tag?: string
}) {
  return useQuery({
    queryKey: ['journalEntries', params],
    queryFn: () => getJournalEntries(params),
  })
}

export function useJournalEntry(entryId: string) {
  return useQuery({
    queryKey: ['journalEntry', entryId],
    queryFn: () => getJournalEntry(entryId),
    enabled: !!entryId,
  })
}

export function useCreateJournalEntry() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateJournalEntry) => createJournalEntry(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
      queryClient.invalidateQueries({ queryKey: ['profile'] }) // Update streak
    },
  })
}

export function useUpdateJournalEntry() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ entryId, data }: { entryId: string; data: Partial<CreateJournalEntry> }) =>
      updateJournalEntry(entryId, data),
    onSuccess: (_, { entryId }) => {
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
      queryClient.invalidateQueries({ queryKey: ['journalEntry', entryId] })
    },
  })
}

export function useDeleteJournalEntry() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteJournalEntry,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
    },
  })
}
