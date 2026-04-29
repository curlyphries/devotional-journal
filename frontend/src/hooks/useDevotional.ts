import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  getFocusIntentions,
  getActiveFocusIntentions,
  getTodayDevotional,
  createFocusIntention,
  completeFocusIntention,
  getFocusIntentionPassages,
  getDevotionalPassages,
  getTodayPassages,
  getUpcomingPassages,
  markPassageRead,
  savePassageReflection,
  generatePassageDeepDive,
  FocusIntention,
  DevotionalPassage,
  TodayDevotional,
  StudyGuide,
  CreateFocusIntentionInput,
} from '../api/devotional'

// Focus Intention Hooks
export function useFocusIntentions() {
  return useQuery<FocusIntention[]>({
    queryKey: ['focusIntentions'],
    queryFn: getFocusIntentions,
  })
}

export function useActiveFocusIntentions() {
  return useQuery<FocusIntention[]>({
    queryKey: ['focusIntentions', 'active'],
    queryFn: getActiveFocusIntentions,
  })
}

export function useTodayDevotional() {
  return useQuery<TodayDevotional>({
    queryKey: ['devotional', 'today'],
    queryFn: getTodayDevotional,
  })
}

export function useFocusIntentionPassages(intentionId: string) {
  return useQuery<DevotionalPassage[]>({
    queryKey: ['focusIntentions', intentionId, 'passages'],
    queryFn: () => getFocusIntentionPassages(intentionId),
    enabled: !!intentionId,
  })
}

export function useCreateFocusIntention() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: CreateFocusIntentionInput) => createFocusIntention(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['focusIntentions'] })
      queryClient.invalidateQueries({ queryKey: ['devotional'] })
    },
  })
}

export function usePassageDeepDive() {
  return useMutation<StudyGuide, Error, { id: string; context?: string }>({
    mutationFn: ({ id, context }) => generatePassageDeepDive(id, context),
  })
}

export function useCompleteFocusIntention() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => completeFocusIntention(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['focusIntentions'] })
      queryClient.invalidateQueries({ queryKey: ['devotional'] })
    },
  })
}

// Devotional Passage Hooks
export function useDevotionalPassages() {
  return useQuery<DevotionalPassage[]>({
    queryKey: ['passages'],
    queryFn: getDevotionalPassages,
  })
}

export function useTodayPassages() {
  return useQuery<DevotionalPassage[]>({
    queryKey: ['passages', 'today'],
    queryFn: getTodayPassages,
  })
}

export function useUpcomingPassages() {
  return useQuery<DevotionalPassage[]>({
    queryKey: ['passages', 'upcoming'],
    queryFn: getUpcomingPassages,
  })
}

export function useMarkPassageRead() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => markPassageRead(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['passages'] })
      queryClient.invalidateQueries({ queryKey: ['devotional'] })
    },
  })
}

export function useSavePassageReflection() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, reflection }: { id: string; reflection: string }) => 
      savePassageReflection(id, reflection),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['passages'] })
      queryClient.invalidateQueries({ queryKey: ['devotional'] })
    },
  })
}
