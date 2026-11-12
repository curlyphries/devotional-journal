import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Compass } from 'lucide-react'

export default function NotFoundPage() {
  const { t } = useTranslation()
  return (
    <div className="max-w-xl mx-auto py-8">
      <div className="card text-center">
        <Compass className="w-10 h-10 text-accent-primary mx-auto mb-3" aria-hidden="true" />
        <h1 className="text-xl font-semibold text-text-primary">{t('errors.notFoundTitle')}</h1>
        <p className="text-text-secondary mt-2">{t('errors.notFoundBody')}</p>
        <Link to="/" className="btn-primary inline-block mt-5">
          {t('errors.goHome')}
        </Link>
      </div>
    </div>
  )
}
