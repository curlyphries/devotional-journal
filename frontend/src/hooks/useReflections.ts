import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  lifeAreasApi,
  journeysApi,
  reflectionsApi,
  trendsApi,
  threadsApi,
  crewApi,
  CreateJourneyData,
  CreateReflectionData,
} from '../api/reflections'

// Life Areas
export function useLifeAreas() {
  return useQuery({
    queryKey: ['lifeAreas'],
    queryFn: () => lifeAreasApi.list().then((res) => res.data),
    staleTime: 1000 * 60 * 60, // 1 hour - reference data rarely changes
  })
}

// Journeys
export function useJourneys() {
  return useQuery({
    queryKey: ['journeys'],
    queryFn: () => journeysApi.list().then((res) => res.data),
  })
}

export function useActiveJourney() {
  return useQuery({
    queryKey: ['journeys', 'active'],
    queryFn: () => journeysApi.getActive().then((res) => res.data),
    retry: false, // Don't retry on 404
  })
}

export function useJourney(id: string) {
  return useQuery({
    queryKey: ['journeys', id],
    queryFn: () => journeysApi.get(id).then((res) => res.data),
    enabled: !!id,
  })
}

export function useCreateJourney() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CreateJourneyData) => journeysApi.create(data).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journeys'] })
    },
  })
}

export function useJourneyActions(id: string) {
  const queryClient = useQueryClient()
  
  const advanceDay = useMutation({
    mutationFn: () => journeysApi.advanceDay(id).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journeys'] })
    },
  })

  const complete = useMutation({
    mutationFn: () => journeysApi.complete(id).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journeys'] })
    },
  })

  const pause = useMutation({
    mutationFn: () => journeysApi.pause(id).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journeys'] })
    },
  })

  const resume = useMutation({
    mutationFn: () => journeysApi.resume(id).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journeys'] })
    },
  })

  return { advanceDay, complete, pause, resume }
}

// Reflections
export function useReflections() {
  return useQuery({
    queryKey: ['reflections'],
    queryFn: () => reflectionsApi.list().then((res) => res.data),
  })
}

export function useReflection(id: string) {
  return useQuery({
    queryKey: ['reflections', id],
    queryFn: () => reflectionsApi.get(id).then((res) => res.data),
    enabled: !!id,
  })
}

export function useTodayContext() {
  return useQuery({
    queryKey: ['reflections', 'today'],
    queryFn: () => reflectionsApi.getToday().then((res) => res.data),
  })
}

export function useReflectionByDate(date: string) {
  return useQuery({
    queryKey: ['reflections', 'date', date],
    queryFn: () => reflectionsApi.getByDate(date).then((res) => res.data),
    enabled: !!date,
    retry: false,
  })
}

export function useCreateReflection() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CreateReflectionData) => reflectionsApi.create(data).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reflections'] })
      queryClient.invalidateQueries({ queryKey: ['threads'] })
    },
  })
}

export function useUpdateReflection(id: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: Partial<CreateReflectionData>) => 
      reflectionsApi.update(id, data).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reflections'] })
    },
  })
}

export function useGenerateInsight(id: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => reflectionsApi.generateInsight(id).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reflections', id] })
    },
  })
}

// Trends
export function useWeeklyTrends() {
  return useQuery({
    queryKey: ['trends', 'weekly'],
    queryFn: () => trendsApi.getWeekly().then((res) => res.data),
  })
}

export function useMonthlyTrends() {
  return useQuery({
    queryKey: ['trends', 'monthly'],
    queryFn: () => trendsApi.getMonthly().then((res) => res.data),
  })
}

export function useTrendsByArea(areaCode: string) {
  return useQuery({
    queryKey: ['trends', 'area', areaCode],
    queryFn: () => trendsApi.getByArea(areaCode).then((res) => res.data),
    enabled: !!areaCode,
  })
}

// Threads
export function useThreads() {
  return useQuery({
    queryKey: ['threads'],
    queryFn: () => threadsApi.list().then((res) => res.data),
  })
}

export function useActiveThreads() {
  return useQuery({
    queryKey: ['threads', 'active'],
    queryFn: () => threadsApi.getActive().then((res) => res.data),
  })
}

export function useThreadsNeedingFollowup() {
  return useQuery({
    queryKey: ['threads', 'followup'],
    queryFn: () => threadsApi.getNeedingFollowup().then((res) => res.data.prompts),
  })
}

export function useThreadStats() {
  return useQuery({
    queryKey: ['threads', 'stats'],
    queryFn: () => threadsApi.getStats().then((res) => res.data),
  })
}

export function useThreadActions(id: string) {
  const queryClient = useQueryClient()

  const resolve = useMutation({
    mutationFn: (resolution_note?: string) => 
      threadsApi.resolve(id, resolution_note).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threads'] })
    },
  })

  const defer = useMutation({
    mutationFn: (days?: number) => threadsApi.defer(id, days).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threads'] })
    },
  })

  const drop = useMutation({
    mutationFn: () => threadsApi.drop(id).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threads'] })
    },
  })

  return { resolve, defer, drop }
}

export function useRespondToThread() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { thread_id: string; response: string; expanded_text?: string; reflection_id?: string }) =>
      threadsApi.respond(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threads'] })
    },
  })
}

// AI Crew
export function useCrewHealth() {
  return useQuery({
    queryKey: ['crew', 'health'],
    queryFn: () => crewApi.health().then((res) => res.data),
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}

export function useWeeklyReview() {
  return useMutation({
    mutationFn: () => crewApi.weeklyReview().then((res) => res.data),
  })
}

export function useMonthlyRecap() {
  return useMutation({
    mutationFn: () => crewApi.monthlyRecap().then((res) => res.data),
  })
}

export function useAskAgent() {
  return useMutation({
    mutationFn: ({ agent, prompt, context }: { agent: string; prompt: string; context?: Record<string, unknown> }) =>
      crewApi.askAgent(agent, prompt, context).then((res) => res.data),
  })
}
