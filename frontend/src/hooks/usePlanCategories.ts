import { useQuery } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import { getPlanCategories, type PlanCategory, type PlanCategoryGroup } from '../api/plans'

/**
 * The reading-plan categories. The server owns the list (backend
 * apps/plans/categories.py), so the plan builder, the plans filter and plan
 * validation can never disagree about what exists.
 *
 * If the list cannot be loaded, `groups` falls back to "General" alone so a
 * plan can still be built; `isError` lets the caller say that the full list
 * is unavailable.
 */
export function usePlanCategories(options: { enabled?: boolean } = {}) {
  const { t, i18n } = useTranslation()
  const lang = i18n.language?.startsWith('es') ? 'es' : 'en'

  const query = useQuery({
    queryKey: ['plan-categories', lang],
    queryFn: () => getPlanCategories(lang),
    staleTime: 5 * 60 * 1000,
    enabled: options.enabled ?? true,
  })

  const fallback: PlanCategoryGroup[] = [
    {
      key: 'faith',
      title: t('plans.categories.fallbackGroup'),
      categories: [{ value: 'general', label: t('plans.categories.general'), plan_count: 0 }],
    },
  ]
  const groups = query.data && query.data.length > 0 ? query.data : fallback
  const all: PlanCategory[] = groups.flatMap((group) => group.categories)

  /** Display name for a category key; an unknown key is shown as written. */
  const labelOf = (value: string): string =>
    all.find((category) => category.value === value)?.label ?? value.replace(/_/g, ' ')

  return { ...query, groups, all, labelOf }
}
