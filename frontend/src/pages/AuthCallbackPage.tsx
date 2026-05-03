import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Flame, Loader2 } from 'lucide-react'
import apiClient from '../api/client'

export default function AuthCallbackPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { login } = useAuth()

  useEffect(() => {
    const code = searchParams.get('code')

    if (!code) {
      navigate('/login?error=no_tokens', { replace: true })
      return
    }

    apiClient.post('/auth/google/exchange/', { code })
      .then((res) => {
        const { access_token, refresh_token, new_user } = res.data
        login(access_token, refresh_token)
        if (new_user) {
          navigate('/settings', { replace: true })
        } else {
          navigate('/', { replace: true })
        }
      })
      .catch(() => {
        navigate('/login?error=no_tokens', { replace: true })
      })
  }, [searchParams, login, navigate])

  return (
    <div className="min-h-screen bg-bg-primary flex items-center justify-center">
      <div className="text-center">
        <Flame className="w-16 h-16 text-accent-primary mx-auto mb-4 animate-pulse" />
        <Loader2 className="w-8 h-8 text-accent-primary mx-auto animate-spin" />
        <p className="text-text-secondary mt-4">Completing sign in...</p>
      </div>
    </div>
  )
}
