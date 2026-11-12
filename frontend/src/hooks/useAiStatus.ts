import { useQuery } from '@tanstack/react-query'
import { getAiStatus, AiStatus } from '../api/prompts'

export const AI_STATUS_QUERY_KEY = ['aiStatus'] as const

/** True when AI features can be used as things stand. */
export function isAiUsable(status: AiStatus | undefined): boolean {
  return !!status && status.configured && status.reachable && !status.consent_required
}

/** Current AI availability (GET /prompts/ai-status/). Cached for a minute. */
export function useAiStatus(options: { enabled?: boolean } = {}) {
  return useQuery<AiStatus>({
    queryKey: AI_STATUS_QUERY_KEY,
    queryFn: getAiStatus,
    staleTime: 60_000,
    retry: false,
    enabled: options.enabled ?? true,
  })
}
