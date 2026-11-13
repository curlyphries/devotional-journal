import { useCallback } from 'react'
import { useTranslation } from 'react-i18next'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { getGrowthPlan, listGrowthPlans, type GrowthPlan } from '../../api/growthPlans'
import { growthKeys } from '../../api/profile'
import { useToast } from '../Toast'

/** The person's growth plans, active first. */
export function useGrowthPlans() {
  const { i18n } = useTranslation()
  return useQuery<GrowthPlan[]>({
    queryKey: growthKeys.plans(i18n.language),
    queryFn: listGrowthPlans,
  })
}

export function useGrowthPlan(planId: string | undefined) {
  const { i18n } = useTranslation()
  return useQuery<GrowthPlan>({
    queryKey: growthKeys.plan(planId ?? '', i18n.language),
    queryFn: () => getGrowthPlan(planId as string),
    enabled: !!planId,
    retry: false,
  })
}

/** Put a plan the server just returned into the cache and mark the list stale. */
export function useApplyPlan() {
  const { i18n } = useTranslation()
  const queryClient = useQueryClient()
  return useCallback(
    (plan: GrowthPlan) => {
      queryClient.setQueryData(growthKeys.plan(plan.id, i18n.language), plan)
      queryClient.invalidateQueries({ queryKey: growthKeys.plans(i18n.language) })
    },
    [i18n.language, queryClient],
  )
}

/**
 * A change to a plan whose endpoint answers with the whole updated plan
 * (goals, check-ins, status). The result replaces the cached plan; a failure
 * is always shown, as a toast headed by `errorTitle`.
 */
export function usePlanMutation<TVariables = void>(
  action: (variables: TVariables) => Promise<GrowthPlan>,
  options: { errorTitle: string; onSuccess?: (plan: GrowthPlan, variables: TVariables) => void },
) {
  const toast = useToast()
  const applyPlan = useApplyPlan()
  return useMutation({
    mutationFn: action,
    onSuccess: (plan, variables) => {
      applyPlan(plan)
      options.onSuccess?.(plan, variables)
    },
    onError: (err) => toast.fromError(err, options.errorTitle),
  })
}
