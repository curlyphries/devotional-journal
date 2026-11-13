import { useCallback } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { getCatalog, guidesKeys, type Catalog } from '../../api/guides'
import { getGrowthProfile, growthKeys, type GrowthProfile } from '../../api/profile'

/** The catalog of life stages, topics, characteristics and assessment items (shared cache with the study pages). */
export function useGuidesCatalog() {
  const { i18n } = useTranslation()
  return useQuery<Catalog>({
    queryKey: guidesKeys.catalog(i18n.language),
    queryFn: getCatalog,
    staleTime: 5 * 60_000,
  })
}

export function useGrowthProfile(options: { enabled?: boolean } = {}) {
  const { i18n } = useTranslation()
  return useQuery<GrowthProfile>({
    queryKey: growthKeys.profile(i18n.language),
    queryFn: getGrowthProfile,
    enabled: options.enabled ?? true,
  })
}

/**
 * Put a profile the server just returned into the cache, and refresh what
 * depends on it elsewhere (study suggestions, the study hub's own profile read).
 */
export function useApplyProfile() {
  const { i18n } = useTranslation()
  const queryClient = useQueryClient()
  return useCallback(
    (profile: GrowthProfile, options: { lifeStageChanged?: boolean } = {}) => {
      queryClient.setQueryData(growthKeys.profile(i18n.language), profile)
      queryClient.invalidateQueries({ queryKey: guidesKeys.profileBasics() })
      queryClient.invalidateQueries({ queryKey: guidesKeys.recommendations(i18n.language) })
      // Each topic's "how this meets your life stage" note comes with the catalog.
      if (options.lifeStageChanged) queryClient.invalidateQueries({ queryKey: guidesKeys.catalog(i18n.language) })
    },
    [i18n.language, queryClient],
  )
}
