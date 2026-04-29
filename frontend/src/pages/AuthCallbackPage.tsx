import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Flame, Loader2 } from 'lucide-react'

export default function AuthCallbackPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { login } = useAuth()

  useEffect(() => {
    const accessToken = searchParams.get('access_token')
    const refreshToken = searchParams.get('refresh_token')
    const newUser = searchParams.get('new_user') === 'true'

    if (accessToken && refreshToken) {
      // Store tokens and redirect
      login(accessToken, refreshToken)
      
      // Redirect new users to onboarding, existing users to dashboard
      if (newUser) {
        navigate('/settings', { replace: true })
      } else {
        navigate('/', { replace: true })
      }
    } else {
      // No tokens, redirect to login with error
      navigate('/login?error=no_tokens', { replace: true })
    }
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
