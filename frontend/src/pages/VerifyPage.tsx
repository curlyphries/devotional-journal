import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../context/AuthContext'
import { verifyMagicLink } from '../api/auth'
import { Loader2 } from 'lucide-react'

export default function VerifyPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { login } = useAuth()
  const [error, setError] = useState('')

  useEffect(() => {
    const token = searchParams.get('token')

    if (!token) {
      setError('Invalid verification link')
      return
    }

    const verify = async () => {
      try {
        const tokens = await verifyMagicLink(token)
        login(tokens.access_token, tokens.refresh_token)
        navigate('/')
      } catch {
        setError('Verification failed. The link may have expired.')
      }
    }

    verify()
  }, [searchParams, login, navigate])

  return (
    <div className="min-h-screen bg-bg-primary flex items-center justify-center">
      <div className="text-center">
        {error ? (
          <div className="card">
            <p className="text-danger mb-4">{error}</p>
            <a href="/login" className="btn-primary">
              Back to Login
            </a>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="w-12 h-12 text-accent-primary animate-spin" />
            <p className="text-text-primary">{t('auth.verifying')}</p>
          </div>
        )}
      </div>
    </div>
  )
}
