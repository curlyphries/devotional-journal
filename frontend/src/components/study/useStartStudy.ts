import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { guidesKeys, startStudy } from '../../api/guides'
import { useToast } from '../Toast'

/**
 * Start a study of a topic and open it. `mutate(topicKey)`; while it runs,
 * `variables` is the topic being started (for a per-card busy state).
 */
export function useStartStudy() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const toast = useToast()

  return useMutation({
    mutationFn: (topicKey: string) => startStudy(topicKey),
    onSuccess: (study) => {
      // Enrolment shows up on catalog cards, suggestions and the "Continue" list.
      queryClient.invalidateQueries({ queryKey: guidesKeys.all })
      navigate(`/study/${study.id}`)
    },
    onError: (err) => toast.fromError(err, t('study.startFailed')),
  })
}
