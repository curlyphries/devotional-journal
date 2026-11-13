import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { ScanFace } from 'lucide-react'
import InlineError from '../components/InlineError'
import ProfileSetup from '../components/growth/ProfileSetup'
import ProfileView from '../components/growth/ProfileView'
import { useGrowthProfile, useGuidesCatalog } from '../components/growth/useGrowthProfile'

function Skeleton() {
  const { t } = useTranslation()
  return (
    <div role="status" className="space-y-4">
      <span className="sr-only">{t('common.loading')}</span>
      {[0, 1, 2].map((row) => (
        <div key={row} className="card animate-pulse space-y-3" aria-hidden="true">
          <div className="h-5 w-1/3 rounded bg-bg-elevated" />
          <div className="h-3 w-full rounded bg-bg-elevated" />
          <div className="h-3 w-5/6 rounded bg-bg-elevated" />
          <div className="h-3 w-2/3 rounded bg-bg-elevated" />
        </div>
      ))}
    </div>
  )
}

/**
 * "My growth profile": what the app understands about the person's faith and
 * inner life, shown back to them plainly, with the means to correct or erase it.
 */
export default function ProfilePage() {
  const { t } = useTranslation()
  const profile = useGrowthProfile()
  const catalog = useGuidesCatalog()

  // 'auto' follows the server (`exists`); 'setup' keeps the first-run steps open
  // even after the first save makes the profile exist; 'view' is after finishing.
  const [mode, setMode] = useState<'auto' | 'setup' | 'view'>('auto')
  const exists = profile.data?.exists
  useEffect(() => {
    if (exists === false) setMode((current) => (current === 'auto' ? 'setup' : current))
  }, [exists])

  const showSetup = mode === 'setup' || (mode === 'auto' && exists === false)

  let body: React.ReactNode
  if (profile.isLoading || catalog.isLoading) {
    body = <Skeleton />
  } else if (profile.isError || !profile.data) {
    body = <InlineError error={profile.error} title={t('profile.loadFailed')} onRetry={() => profile.refetch()} />
  } else if (catalog.isError || !catalog.data) {
    body = <InlineError error={catalog.error} title={t('profile.catalogFailed')} onRetry={() => catalog.refetch()} />
  } else if (showSetup) {
    body = <ProfileSetup catalog={catalog.data} profile={profile.data} onDone={() => setMode('view')} />
  } else {
    body = (
      <ProfileView
        profile={profile.data}
        catalog={catalog.data}
        onRestartSetup={() => setMode('setup')}
        onErased={() => setMode('auto')}
      />
    )
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <header>
        <div className="flex items-center gap-2">
          <ScanFace className="h-6 w-6 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          <h1 className="text-2xl font-bold text-text-primary">{t('profile.title')}</h1>
        </div>
        <p className="mt-2 leading-relaxed text-text-secondary">
          {showSetup ? t('profile.setup.pageIntro') : t('profile.intro')}
        </p>
      </header>
      {body}
    </div>
  )
}
