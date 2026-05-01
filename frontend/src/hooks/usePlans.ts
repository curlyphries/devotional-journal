/**
 * Reading Plans hooks
 */
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  getPlans,
  getPlanDetail,
  enrollInPlan,
  getEnrolledPlans,
  getTodayReading,
  advanceDay,
} from '../api/plans'

export function usePlans(params?: { category?: string; language?: string }) {
  return useQuery({
    queryKey: ['plans', params],
    queryFn: () => getPlans(params?.category),
  })
}

export function usePlanDetail(planId: string) {
  return useQuery({
    queryKey: ['plan', planId],
    queryFn: () => getPlanDetail(planId),
    enabled: !!planId,
  })
}

export function useEnrolledPlans() {
  return useQuery({
    queryKey: ['enrolledPlans'],
    queryFn: () => getEnrolledPlans(),
  })
}

export function useTodayReading(enrollmentId: string) {
  return useQuery({
    queryKey: ['todayReading', enrollmentId],
    queryFn: () => getTodayReading(enrollmentId),
    enabled: !!enrollmentId,
  })
}

export function useEnrollInPlan() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: enrollInPlan,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['enrolledPlans'] })
    },
  })
}

export function useAdvanceDay() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: advanceDay,
    onSuccess: (_result: { message: string; enrollment: unknown }, enrollmentId: string) => {
      queryClient.invalidateQueries({ queryKey: ['enrolledPlans'] })
      queryClient.invalidateQueries({ queryKey: ['todayReading', enrollmentId] })
    },
  })
}
