/**
 * Auth hooks
 */
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import { getProfile, updateProfile, requestMagicLink, verifyMagicLink } from '../api/auth'

export function useProfile() {
  const { isAuthenticated } = useAuth()

  return useQuery({
    queryKey: ['profile'],
    queryFn: getProfile,
    enabled: isAuthenticated,
  })
}

export function useUpdateProfile() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateProfile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] })
    },
  })
}

export function useRequestMagicLink() {
  return useMutation({
    mutationFn: requestMagicLink,
  })
}

export function useVerifyMagicLink() {
  const { login } = useAuth()

  return useMutation({
    mutationFn: verifyMagicLink,
    onSuccess: (data) => {
      login(data.access_token, data.refresh_token)
    },
  })
}
