import { useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { Link, Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import {
  Flame, Lock, Languages, Sparkles, BookOpen, Calendar, Target,
  Heart, Github, Download, ChevronRight, Check, ArrowRight, Compass,
  Server, Zap,
} from 'lucide-react'

export default function LandingPage() {
  const { t, i18n } = useTranslation()
  const { isAuthenticated, isLoading } = useAuth()

  useEffect(() => {
    document.title = t('landing.docTitle', 'Devotional Journal — Bilingual Bible study, focus, and encrypted journaling')
  }, [t])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="text-text-primary">{t('common.loading')}</div>
      </div>
    )
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  const toggleLanguage = () => {
    const next = i18n.language === 'es' ? 'en' : 'es'
    i18n.changeLanguage(next)
  }

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary">
      {/* Top bar */}
      <header className="border-b border-border bg-bg-surface/60 backdrop-blur-sm sticky top-0 z-30">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link to="/welcome" className="flex items-center gap-2 focus:outline-none focus:ring-2 focus:ring-accent-primary rounded-lg" aria-label="Devotional Journal home">
            <Flame className="w-7 h-7 text-accent-primary" aria-hidden="true" />
            <span className="text-lg font-bold">Devotional Journal</span>
          </Link>
          <nav className="flex items-center gap-2 sm:gap-4 text-sm">
            <a href="#features" className="hidden sm:inline text-text-secondary hover:text-text-primary transition-colors">
              {t('landing.nav.features', 'Features')}
            </a>
            <a href="#privacy" className="hidden sm:inline text-text-secondary hover:text-text-primary transition-colors">
              {t('landing.nav.privacy', 'Privacy')}
            </a>
            <a href="#faq" className="hidden md:inline text-text-secondary hover:text-text-primary transition-colors">
              {t('landing.nav.faq', 'FAQ')}
            </a>
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1.5 px-3 py-1.5 text-text-secondary hover:text-text-primary border border-border rounded-lg transition-colors"
              aria-label={t('nav.changeLanguage', 'Change language')}
            >
              <Languages className="w-4 h-4" aria-hidden="true" />
              <span>{i18n.language === 'es' ? 'EN' : 'ES'}</span>
            </button>
            <Link
              to="/login"
              className="bg-accent-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-opacity-90 transition-colors"
            >
              {t('landing.nav.signIn', 'Sign in')}
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="px-4 pt-16 pb-20 sm:pt-24 sm:pb-28">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 mb-6 rounded-full border border-accent-primary/30 bg-accent-primary/10 text-accent-primary text-xs font-medium">
            <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
            {t('landing.hero.eyebrow', 'Open-source · Encrypted · Bilingual')}
          </div>
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold leading-tight mb-6">
            {t('landing.hero.headline.part1', 'Build a daily Bible rhythm')}
            <br />
            <span className="text-accent-primary">{t('landing.hero.headline.part2', 'that actually sticks.')}</span>
          </h1>
          <p className="text-lg sm:text-xl text-text-secondary max-w-2xl mx-auto mb-10">
            {t(
              'landing.hero.sub',
              'A bilingual (EN/ES) Bible study companion for men who want consistency. Set a focus, follow AI-curated reading plans, and journal privately — encrypted end-to-end.'
            )}
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 mb-12">
            <Link
              to="/login"
              className="w-full sm:w-auto bg-accent-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-opacity-90 transition-colors flex items-center justify-center gap-2"
            >
              {t('landing.hero.ctaPrimary', 'Get started — free')}
              <ArrowRight className="w-4 h-4" aria-hidden="true" />
            </Link>
            <a
              href="https://github.com/curlyphries/devotional-journal"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto bg-bg-elevated text-text-primary px-6 py-3 rounded-lg font-semibold border border-border hover:bg-bg-surface transition-colors flex items-center justify-center gap-2"
            >
              <Github className="w-4 h-4" aria-hidden="true" />
              {t('landing.hero.ctaSecondary', 'Self-host on GitHub')}
            </a>
          </div>

          {/* Trust badges */}
          <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-3 text-sm text-text-secondary">
            <span className="inline-flex items-center gap-1.5"><Lock className="w-4 h-4 text-accent-primary" aria-hidden="true" /> {t('landing.trust.encrypted', 'End-to-end encrypted')}</span>
            <span className="inline-flex items-center gap-1.5"><Languages className="w-4 h-4 text-accent-primary" aria-hidden="true" /> {t('landing.trust.bilingual', 'EN / ES bilingual')}</span>
            <span className="inline-flex items-center gap-1.5"><Server className="w-4 h-4 text-accent-primary" aria-hidden="true" /> {t('landing.trust.selfHost', 'Self-host friendly')}</span>
            <span className="inline-flex items-center gap-1.5"><Zap className="w-4 h-4 text-accent-primary" aria-hidden="true" /> {t('landing.trust.byoai', 'Bring your own AI')}</span>
          </div>

          {/* Hero screenshot */}
          <div className="mt-14 max-w-5xl mx-auto">
            <div className="rounded-2xl overflow-hidden border border-border shadow-2xl">
              <img
                src="/devotional-journal/docs/screenshots/dashboard.png"
                onError={(e) => { (e.currentTarget as HTMLImageElement).src = 'https://raw.githubusercontent.com/curlyphries/devotional-journal/master/docs/screenshots/dashboard.png' }}
                alt={t('landing.hero.screenshotAlt', 'Devotional Journal dashboard preview')}
                className="w-full h-auto"
                loading="eager"
              />
            </div>
          </div>
        </div>
      </section>

      {/* The problem */}
      <section className="px-4 py-16 sm:py-20 bg-bg-surface/40 border-y border-border">
        <div className="max-w-3xl mx-auto text-center">
          <p className="text-2xl sm:text-3xl font-serif italic text-text-primary mb-6 leading-relaxed">
            "{t('landing.problem.quote', 'I want to be consistent in my faith — but I keep falling off.')}"
          </p>
          <p className="text-text-secondary text-lg">
            {t(
              'landing.problem.body',
              'Most Bible apps are content libraries or social feeds. They don\'t help you build a daily rhythm. Devotional Journal is built around the habit loop — focus, read, journal, reflect, track.'
            )}
          </p>
        </div>
      </section>

      {/* How it works */}
      <section className="px-4 py-16 sm:py-20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold mb-3">{t('landing.how.heading', 'How it works')}</h2>
            <p className="text-text-secondary text-lg">
              {t('landing.how.sub', 'Five small steps that compound into a real habit.')}
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              { icon: Compass, title: t('landing.how.step1.title', 'Set a focus'), body: t('landing.how.step1.body', 'Pick what you\'re working through — anxiety, leadership, prayer life, anger.') },
              { icon: BookOpen, title: t('landing.how.step2.title', 'Read'), body: t('landing.how.step2.body', 'AI curates daily passages tied to your focus, in your translation.') },
              { icon: Heart, title: t('landing.how.step3.title', 'Journal'), body: t('landing.how.step3.body', 'Encrypted at rest. Mood-tagged. Only you can read it.') },
              { icon: Sparkles, title: t('landing.how.step4.title', 'Reflect'), body: t('landing.how.step4.body', 'Life-area scoring. AI threads follow up on what you wrestled with last week.') },
              { icon: Target, title: t('landing.how.step5.title', 'Track'), body: t('landing.how.step5.body', 'Streaks, milestones, and a 30/60/90-day growth report you can export.') },
            ].map((step, i) => (
              <div key={i} className="card relative">
                <div className="absolute -top-3 -left-3 w-8 h-8 rounded-full bg-accent-primary text-white text-sm font-bold flex items-center justify-center">
                  {i + 1}
                </div>
                <step.icon className="w-7 h-7 text-accent-primary mb-3" aria-hidden="true" />
                <h3 className="font-semibold mb-1">{step.title}</h3>
                <p className="text-sm text-text-secondary leading-relaxed">{step.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features grid */}
      <section id="features" className="px-4 py-16 sm:py-20 bg-bg-surface/40 border-y border-border">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold mb-3">{t('landing.features.heading', 'Everything you need to build the habit')}</h2>
            <p className="text-text-secondary text-lg max-w-2xl mx-auto">
              {t('landing.features.sub', 'No upsells. No social feed. No paywalled study guides. Just the tools to show up daily.')}
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { icon: Sparkles, title: t('landing.features.f1.title', 'AI-curated devotionals'), body: t('landing.features.f1.body', 'Set a focus, get daily scripture, prompts, and study guides personalized to it.') },
              { icon: Calendar, title: t('landing.features.f2.title', 'Reading plans'), body: t('landing.features.f2.body', 'Browse pre-built plans or generate your own with AI from a single topic.') },
              { icon: Lock, title: t('landing.features.f3.title', 'Encrypted journal'), body: t('landing.features.f3.body', 'Per-user AES encryption. Even with database access, no one can read your entries.') },
              { icon: BookOpen, title: t('landing.features.f4.title', 'Built-in Bible reader'), body: t('landing.features.f4.body', 'KJV included. ASV, YLT, WEB, RVR1960 (Spanish) and more via the Bolls API.') },
              { icon: Heart, title: t('landing.features.f5.title', 'Open threads'), body: t('landing.features.f5.body', '"Last week you mentioned anxiety about work. How\'s that going?" The AI remembers what you wrestled with.') },
              { icon: Target, title: t('landing.features.f6.title', 'Streaks & milestones'), body: t('landing.features.f6.body', 'Confetti at milestones. Share cards for 3, 7, 30, 90, and 365 days.') },
              { icon: Languages, title: t('landing.features.f7.title', 'Bilingual to the bone'), body: t('landing.features.f7.body', 'Plans, themes, and prompts stored in EN and ES. Bilingual mode shows both side by side.') },
              { icon: Download, title: t('landing.features.f8.title', 'Export everything'), body: t('landing.features.f8.body', 'Full ZIP backup or Markdown exports for journal, highlights, and growth reports.') },
              { icon: Server, title: t('landing.features.f9.title', 'Self-host friendly'), body: t('landing.features.f9.body', 'Docker Compose stack. Runs on a Pi or any cloud VM. AGPL-3.0 licensed.') },
            ].map((f, i) => (
              <div key={i} className="card">
                <div className="w-10 h-10 rounded-lg bg-accent-primary/15 flex items-center justify-center mb-3">
                  <f.icon className="w-5 h-5 text-accent-primary" aria-hidden="true" />
                </div>
                <h3 className="font-semibold mb-1">{f.title}</h3>
                <p className="text-sm text-text-secondary leading-relaxed">{f.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Privacy */}
      <section id="privacy" className="px-4 py-16 sm:py-20">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-10">
            <Lock className="w-10 h-10 text-accent-primary mx-auto mb-3" aria-hidden="true" />
            <h2 className="text-3xl sm:text-4xl font-bold mb-3">{t('landing.privacy.heading', 'Your reflections are yours')}</h2>
            <p className="text-text-secondary text-lg max-w-2xl mx-auto">
              {t(
                'landing.privacy.sub',
                'Privacy isn\'t a marketing line here. The encryption code is open and the threat model is documented.'
              )}
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              t('landing.privacy.p1', 'Per-user AES encryption on every journal entry'),
              t('landing.privacy.p2', 'No third-party analytics by default'),
              t('landing.privacy.p3', 'Bring your own AI — Ollama keeps everything local'),
              t('landing.privacy.p4', 'GDPR-style export and delete from your account'),
              t('landing.privacy.p5', 'Source code under AGPL-3.0 — audit it yourself'),
              t('landing.privacy.p6', 'Share cards never include journal text'),
            ].map((line, i) => (
              <div key={i} className="flex items-start gap-3 p-4 rounded-lg border border-border bg-bg-surface/40">
                <Check className="w-5 h-5 text-accent-primary shrink-0 mt-0.5" aria-hidden="true" />
                <span className="text-text-primary">{line}</span>
              </div>
            ))}
          </div>
          <div className="text-center mt-8">
            <a
              href="https://github.com/curlyphries/devotional-journal/blob/master/PRIVACY.md"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-accent-primary hover:underline font-medium"
            >
              {t('landing.privacy.readMore', 'Read the full privacy policy')}
              <ChevronRight className="w-4 h-4" aria-hidden="true" />
            </a>
          </div>
        </div>
      </section>

      {/* Screenshots */}
      <section className="px-4 py-16 sm:py-20 bg-bg-surface/40 border-y border-border">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl sm:text-4xl font-bold mb-3">{t('landing.shots.heading', 'A look inside')}</h2>
            <p className="text-text-secondary text-lg">
              {t('landing.shots.sub', 'Designed to be calm, focused, and out of the way.')}
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { src: '/devotional-journal/docs/screenshots/focus.png', remote: 'https://raw.githubusercontent.com/curlyphries/devotional-journal/master/docs/screenshots/focus.png', label: t('landing.shots.focus', 'Daily focus') },
              { src: '/devotional-journal/docs/screenshots/plans.png', remote: 'https://raw.githubusercontent.com/curlyphries/devotional-journal/master/docs/screenshots/plans.png', label: t('landing.shots.plans', 'Reading plans') },
              { src: '/devotional-journal/docs/screenshots/progress.png', remote: 'https://raw.githubusercontent.com/curlyphries/devotional-journal/master/docs/screenshots/progress.png', label: t('landing.shots.progress', 'Progress & streaks') },
              { src: '/devotional-journal/docs/screenshots/journal.png', remote: 'https://raw.githubusercontent.com/curlyphries/devotional-journal/master/docs/screenshots/journal.png', label: t('landing.shots.journal', 'Encrypted journal') },
            ].map((s, i) => (
              <figure key={i} className="rounded-xl overflow-hidden border border-border bg-bg-surface">
                <img
                  src={s.src}
                  onError={(e) => { (e.currentTarget as HTMLImageElement).src = s.remote }}
                  alt={s.label}
                  loading="lazy"
                  className="w-full h-auto"
                />
                <figcaption className="px-4 py-2 text-sm text-text-secondary border-t border-border">
                  {s.label}
                </figcaption>
              </figure>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="px-4 py-16 sm:py-20">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl sm:text-4xl font-bold mb-3">{t('landing.faq.heading', 'Frequently asked questions')}</h2>
          </div>
          <div className="space-y-3">
            {[
              { q: t('landing.faq.q1', 'Is this only for men?'), a: t('landing.faq.a1', 'The tone, prompts, and focus suggestions are written with men in mind — fathers, leaders, men in recovery, men building faith discipline. The features themselves work for anyone.') },
              { q: t('landing.faq.q2', 'Do I need an OpenAI or Anthropic account?'), a: t('landing.faq.a2', 'No. You can run everything locally with Ollama. Your reflections never leave your network in that setup.') },
              { q: t('landing.faq.q3', 'What happens if I lose my encryption key?'), a: t('landing.faq.a3', 'Every journal entry becomes unreadable forever. There is no recovery. Treat the key like a master password and back it up before anything else.') },
              { q: t('landing.faq.q4', 'Can I export my data?'), a: t('landing.faq.a4', 'Yes. Settings → Export gives you a full ZIP and Markdown exports for journal, highlights, and a growth report.') },
              { q: t('landing.faq.q5', 'Is there a hosted version?'), a: t('landing.faq.a5', 'A maintainer-run instance exists for personal use. There is no public hosted offering yet — self-host is the supported path.') },
              { q: t('landing.faq.q6', 'How much does it cost?'), a: t('landing.faq.a6', 'Free. AGPL-3.0 licensed. If you self-host for others, your modifications must be open-sourced under the same license.') },
            ].map((item, i) => (
              <details key={i} className="group rounded-xl border border-border bg-bg-surface/40 overflow-hidden">
                <summary className="flex items-center justify-between px-5 py-4 cursor-pointer list-none hover:bg-bg-surface/70 transition-colors">
                  <span className="font-semibold text-text-primary">{item.q}</span>
                  <ChevronRight className="w-4 h-4 text-text-secondary transition-transform group-open:rotate-90" aria-hidden="true" />
                </summary>
                <div className="px-5 pb-4 text-text-secondary leading-relaxed">
                  {item.a}
                </div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="px-4 py-20">
        <div className="max-w-3xl mx-auto text-center">
          <Flame className="w-12 h-12 text-accent-primary mx-auto mb-4" aria-hidden="true" />
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">{t('landing.cta.heading', 'Start the rhythm today')}</h2>
          <p className="text-text-secondary text-lg mb-8 max-w-xl mx-auto">
            {t(
              'landing.cta.sub',
              'Sign in with Google or your email. Set a focus in 30 seconds. Read your first passage today.'
            )}
          </p>
          <Link
            to="/login"
            className="inline-flex items-center gap-2 bg-accent-primary text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-opacity-90 transition-colors"
          >
            {t('landing.cta.button', 'Sign in to get started')}
            <ArrowRight className="w-5 h-5" aria-hidden="true" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-bg-surface/60 px-4 py-10">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-text-secondary">
          <div className="flex items-center gap-2">
            <Flame className="w-5 h-5 text-accent-primary" aria-hidden="true" />
            <span>Devotional Journal · {t('landing.footer.tagline', 'Built for consistency.')}</span>
          </div>
          <nav className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
            <a href="https://github.com/curlyphries/devotional-journal" target="_blank" rel="noopener noreferrer" className="hover:text-text-primary transition-colors">
              GitHub
            </a>
            <a href="https://github.com/curlyphries/devotional-journal/blob/master/PRIVACY.md" target="_blank" rel="noopener noreferrer" className="hover:text-text-primary transition-colors">
              {t('landing.footer.privacy', 'Privacy')}
            </a>
            <a href="https://github.com/curlyphries/devotional-journal/blob/master/SECURITY.md" target="_blank" rel="noopener noreferrer" className="hover:text-text-primary transition-colors">
              {t('landing.footer.security', 'Security')}
            </a>
            <a href="https://github.com/curlyphries/devotional-journal/blob/master/ROADMAP.md" target="_blank" rel="noopener noreferrer" className="hover:text-text-primary transition-colors">
              {t('landing.footer.roadmap', 'Roadmap')}
            </a>
            <a href="https://github.com/curlyphries/devotional-journal/blob/master/CHANGELOG.md" target="_blank" rel="noopener noreferrer" className="hover:text-text-primary transition-colors">
              {t('landing.footer.changelog', 'Changelog')}
            </a>
            <a href="https://github.com/curlyphries/devotional-journal/blob/master/LICENSE" target="_blank" rel="noopener noreferrer" className="hover:text-text-primary transition-colors">
              AGPL-3.0
            </a>
          </nav>
        </div>
      </footer>
    </div>
  )
}
