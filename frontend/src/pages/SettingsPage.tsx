import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useQueryClient } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../context/AuthContext'
import { updateProfile, testAIConnection } from '../api/auth'
import { Save, User, Bot, Key, CheckCircle, XCircle, Loader2, Eye, EyeOff, Download, FileText, ShieldCheck } from 'lucide-react'
import client from '../api/client'
import { setLanguage as applyLanguage } from '../i18n/language'
import { ApiError, toApiError } from '../api/errors'
import { AI_STATUS_QUERY_KEY, useAiStatus } from '../hooks/useAiStatus'
import InlineError from '../components/InlineError'
import { useToast } from '../components/Toast'

const AI_PROVIDERS = [
  { value: 'none', label: 'None (Use System Default)', needsKey: false, needsUrl: false },
  { value: 'openai', label: 'OpenAI', needsKey: true, needsUrl: false, defaultModel: 'gpt-4o-mini' },
  { value: 'anthropic', label: 'Anthropic (Claude)', needsKey: true, needsUrl: false, defaultModel: 'claude-3-haiku-20240307' },
  { value: 'openrouter', label: 'OpenRouter', needsKey: true, needsUrl: false, defaultModel: 'openai/gpt-4o-mini' },
  { value: 'ollama', label: 'Ollama (Local)', needsKey: false, needsUrl: true, defaultModel: 'llama3.1:8b' },
  { value: 'custom', label: 'Custom OpenAI-Compatible', needsKey: true, needsUrl: true, defaultModel: '' },
]

/** First validation message the server sent for a field, if any. */
function fieldMessage(details: ApiError['details'], field: string): string | null {
  const value = details?.[field]
  if (Array.isArray(value)) return value.map(String).join(' ') || null
  if (typeof value === 'string') return value || null
  return null
}

function FieldError({ id, message }: { id: string; message: string | null }) {
  if (!message) return null
  return (
    <p id={id} role="alert" className="text-sm text-red-400 mt-1">
      {message}
    </p>
  )
}

export default function SettingsPage() {
  const { t } = useTranslation()
  const { user, refreshUser } = useAuth()
  const toast = useToast()
  const queryClient = useQueryClient()
  const location = useLocation()
  const aiStatusQuery = useAiStatus()
  const aiStatus = aiStatusQuery.data

  // Profile settings
  const [displayName, setDisplayName] = useState(user?.display_name || '')
  const [language, setLanguage] = useState<'en' | 'es' | 'bilingual'>(user?.language_preference as 'en' | 'es' | 'bilingual' || 'en')
  const [timezone, setTimezone] = useState(user?.timezone || 'UTC')
  
  // AI settings
  const [aiProvider, setAiProvider] = useState(user?.ai_provider || 'none')
  const [aiApiKey, setAiApiKey] = useState('')
  const [aiModel, setAiModel] = useState(user?.ai_model || '')
  const [aiBaseUrl, setAiBaseUrl] = useState(user?.ai_base_url || '')
  const [showApiKey, setShowApiKey] = useState(false)
  
  // Status
  const [isSaving, setIsSaving] = useState(false)
  const [isTesting, setIsTesting] = useState(false)
  const [saveError, setSaveError] = useState<ApiError | null>(null)
  const [isSavingConsent, setIsSavingConsent] = useState(false)
  const details = saveError?.details
  const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null)

  const selectedProvider = AI_PROVIDERS.find(p => p.value === aiProvider)

  useEffect(() => {
    if (user) {
      setDisplayName(user.display_name || '')
      setLanguage(user.language_preference || 'en')
      setTimezone(user.timezone || 'UTC')
      setAiProvider(user.ai_provider || 'none')
      setAiModel(user.ai_model || '')
      setAiBaseUrl(user.ai_base_url || '')
    }
  }, [user])

  // Set default model when provider changes
  useEffect(() => {
    if (selectedProvider?.defaultModel && !aiModel) {
      setAiModel(selectedProvider.defaultModel)
    }
  }, [aiProvider, selectedProvider, aiModel])

  // Links such as /settings#ai-provider land on that section.
  useEffect(() => {
    if (!location.hash) return
    document.getElementById(location.hash.slice(1))?.scrollIntoView?.({ block: 'start' })
  }, [location.hash])

  const handleConsentChange = async (allowed: boolean) => {
    setIsSavingConsent(true)
    try {
      await updateProfile({ allow_server_cloud_ai: allowed })
      await refreshUser()
      await queryClient.invalidateQueries({ queryKey: AI_STATUS_QUERY_KEY })
      toast.success(allowed ? t('settings.ai.consentOn') : t('settings.ai.consentOff'))
    } catch (err) {
      toast.fromError(err)
    } finally {
      setIsSavingConsent(false)
    }
  }

  const handleSave = async () => {
    setIsSaving(true)
    setSaveError(null)

    try {
      await updateProfile({
        display_name: displayName,
        language_preference: language as 'en' | 'es' | 'bilingual',
        timezone,
        ai_provider: aiProvider,
        ai_api_key: aiApiKey || undefined, // Only send if changed
        ai_model: aiModel,
        ai_base_url: aiBaseUrl,
      })
      // A single-language choice becomes this device's UI language; "bilingual" keeps the current one.
      if (language !== 'bilingual') applyLanguage(language)
      await refreshUser()
      void queryClient.invalidateQueries({ queryKey: AI_STATUS_QUERY_KEY })
      toast.success(t('settings.saved'))
      setAiApiKey('') // Clear the key field after save
    } catch (err) {
      // Rendered next to the Save button, with per-field messages under the fields.
      setSaveError(toApiError(err))
    } finally {
      setIsSaving(false)
    }
  }

  const handleTestConnection = async () => {
    setIsTesting(true)
    setTestResult(null)

    try {
      const result = await testAIConnection({
        provider: aiProvider,
        api_key: aiApiKey || undefined,
        model: aiModel,
        base_url: aiBaseUrl,
      })
      setTestResult({
        success: result.success,
        message: result.success ? (result.message ?? '') : (result.error ?? '')
      })
    } catch (err: unknown) {
      const apiError = toApiError(err)
      setTestResult({
        success: false,
        message: [apiError.message, apiError.suggestion].filter(Boolean).join(' ')
      })
    } finally {
      setIsTesting(false)
    }
  }

  return (
    <div className="max-w-2xl space-y-8">
      <h1 className="text-2xl font-bold text-text-primary mb-8">
        {t('settings.title')}
      </h1>

      {/* Profile Settings */}
      <div className="card">
        <div className="flex items-center gap-4 mb-8 pb-6 border-b border-border">
          <div className="w-16 h-16 rounded-full bg-bg-elevated flex items-center justify-center">
            <User className="w-8 h-8 text-text-secondary" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-text-primary">
              {user?.display_name || 'User'}
            </h2>
            <p className="text-text-secondary">{user?.email}</p>
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              {t('settings.displayName')}
            </label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="input w-full"
              placeholder="Your name"
              aria-invalid={!!fieldMessage(details, 'display_name')}
              aria-describedby="display-name-error"
            />
            <FieldError id="display-name-error" message={fieldMessage(details, 'display_name')} />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              {t('settings.language')}
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as 'en' | 'es' | 'bilingual')}
              className="input w-full"
            >
              <option value="en">{t('settings.languages.en')}</option>
              <option value="es">{t('settings.languages.es')}</option>
              <option value="bilingual">{t('settings.languages.bilingual')}</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              {t('settings.timezone')}
            </label>
            <select
              value={timezone}
              onChange={(e) => setTimezone(e.target.value)}
              className="input w-full"
            >
              <option value="America/Chicago">Central Time (US)</option>
              <option value="America/New_York">Eastern Time (US)</option>
              <option value="America/Denver">Mountain Time (US)</option>
              <option value="America/Los_Angeles">Pacific Time (US)</option>
              <option value="America/Mexico_City">Mexico City</option>
              <option value="UTC">UTC</option>
            </select>
            <FieldError id="timezone-error" message={fieldMessage(details, 'timezone')} />
          </div>
        </div>
      </div>

      {/* AI Provider Settings */}
      <div className="card scroll-mt-4" id="ai-provider">
        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-border">
          <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
            <Bot className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-text-primary">AI Provider</h2>
            <p className="text-sm text-text-secondary">Connect your own AI for insights and summaries</p>
          </div>
        </div>

        {/* AI & privacy: where the AI runs right now, and the one switch that sends text to a cloud. */}
        <section aria-labelledby="ai-privacy-heading" className="mb-6 rounded-xl border border-border bg-bg-elevated p-4">
          <h3 id="ai-privacy-heading" className="flex items-center gap-2 font-semibold text-text-primary">
            <ShieldCheck className="w-5 h-5 text-accent-primary" aria-hidden="true" />
            {t('settings.ai.heading')}
          </h3>

          <div className="mt-3 text-sm text-text-primary" aria-live="polite">
            {aiStatusQuery.isLoading ? (
              <p className="flex items-center gap-2 text-text-secondary">
                <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                {t('settings.ai.checking')}
              </p>
            ) : aiStatusQuery.isError || !aiStatus ? (
              <InlineError
                error={aiStatusQuery.error}
                title={t('settings.ai.statusFailed')}
                onRetry={() => aiStatusQuery.refetch()}
              />
            ) : (
              <>
                <p>
                  {aiStatus.local
                    ? t('settings.ai.runsLocal', { backend: aiStatus.backend })
                    : aiStatus.source === 'user'
                      ? t('settings.ai.runsCloudUser', { backend: aiStatus.backend })
                      : t('settings.ai.runsCloudServer', { backend: aiStatus.backend })}
                  {aiStatus.model ? ` ${t('settings.ai.model', { model: aiStatus.model })}` : ''}
                </p>
                <p className="mt-1 text-text-secondary">
                  {aiStatus.source === 'user' ? t('settings.ai.sourceUser') : t('settings.ai.sourceServer')}
                </p>
                {(!aiStatus.configured || !aiStatus.reachable || aiStatus.consent_required) && (
                  <p className="mt-2 text-text-primary" role="status">
                    {aiStatus.consent_required
                      ? t('errors.ai.consentRequired')
                      : !aiStatus.configured
                        ? t('errors.ai.notConfigured')
                        : t('errors.ai.unreachable', { backend: aiStatus.backend })}
                    {aiStatus.suggestion ? ` ${aiStatus.suggestion}` : ''}
                  </p>
                )}
              </>
            )}
          </div>

          <label className="mt-4 flex items-start gap-3 cursor-pointer">
            <input
              type="checkbox"
              className="mt-1 h-4 w-4 shrink-0 accent-accent-primary"
              checked={!!user?.allow_server_cloud_ai}
              disabled={isSavingConsent}
              onChange={(e) => handleConsentChange(e.target.checked)}
              aria-describedby="cloud-ai-consent-help"
            />
            <span className="text-sm">
              <span className="font-medium text-text-primary">{t('settings.ai.consentLabel')}</span>
              <span id="cloud-ai-consent-help" className="block text-text-secondary mt-1">
                {t('settings.ai.consentHelp', {
                  provider:
                    aiStatus && aiStatus.source === 'server' && !aiStatus.local
                      ? aiStatus.backend
                      : t('settings.ai.genericCloudProvider'),
                })}
              </span>
            </span>
          </label>

          <p className="mt-4 text-sm text-text-secondary">
            {t('settings.ai.auditIntro')}{' '}
            <Link to="/audit" className="text-accent-primary hover:underline">
              {t('settings.ai.auditLink')}
            </Link>
            {' · '}
            <Link to="/help" className="text-accent-primary hover:underline">
              {t('settings.ai.helpLink')}
            </Link>
          </p>
        </section>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Provider
            </label>
            <select
              value={aiProvider}
              onChange={(e) => {
                setAiProvider(e.target.value)
                setAiModel('')
                setTestResult(null)
              }}
              className="input w-full"
            >
              {AI_PROVIDERS.map(provider => (
                <option key={provider.value} value={provider.value}>
                  {provider.label}
                </option>
              ))}
            </select>
          </div>

          {selectedProvider?.needsKey && (
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                <Key className="w-4 h-4 inline mr-1" />
                API Key
                {user?.ai_api_key_set && (
                  <span className="ml-2 text-xs text-green-500">(Key saved)</span>
                )}
              </label>
              <div className="relative">
                <input
                  type={showApiKey ? 'text' : 'password'}
                  value={aiApiKey}
                  onChange={(e) => setAiApiKey(e.target.value)}
                  className="input w-full pr-10"
                  placeholder={user?.ai_api_key_set ? '••••••••••••••••' : 'Enter your API key'}
                />
                <button
                  type="button"
                  onClick={() => setShowApiKey(!showApiKey)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary"
                >
                  {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              <FieldError id="ai-api-key-error" message={fieldMessage(details, 'ai_api_key')} />
              <p className="text-xs text-text-secondary mt-1">
                Your API key is stored securely and never shared.
              </p>
            </div>
          )}

          {selectedProvider?.needsUrl && (
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Base URL
              </label>
              <input
                type="text"
                value={aiBaseUrl}
                onChange={(e) => setAiBaseUrl(e.target.value)}
                className="input w-full"
                placeholder={aiProvider === 'ollama' ? 'http://localhost:11434' : 'https://api.example.com/v1'}
                aria-invalid={!!fieldMessage(details, 'ai_base_url')}
                aria-describedby="ai-base-url-error"
              />
              <FieldError id="ai-base-url-error" message={fieldMessage(details, 'ai_base_url')} />
            </div>
          )}

          {aiProvider !== 'none' && (
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Model
              </label>
              <input
                type="text"
                value={aiModel}
                onChange={(e) => setAiModel(e.target.value)}
                className="input w-full"
                placeholder={selectedProvider?.defaultModel || 'Model name'}
              />
              <FieldError id="ai-model-error" message={fieldMessage(details, 'ai_model')} />
              <p className="text-xs text-text-secondary mt-1">
                {aiProvider === 'openai' && 'e.g., gpt-4o, gpt-4o-mini, gpt-3.5-turbo'}
                {aiProvider === 'anthropic' && 'e.g., claude-3-opus-20240229, claude-3-sonnet-20240229'}
                {aiProvider === 'openrouter' && 'e.g., openai/gpt-4o, anthropic/claude-3-opus'}
                {aiProvider === 'ollama' && 'e.g., llama3.1:8b, mistral, codellama'}
              </p>
            </div>
          )}

          {/* Test Connection Button */}
          {aiProvider !== 'none' && (
            <div className="pt-4 border-t border-border">
              <button
                onClick={handleTestConnection}
                disabled={isTesting || (selectedProvider?.needsKey && !aiApiKey && !user?.ai_api_key_set)}
                className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
              >
                {isTesting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Testing...
                  </>
                ) : (
                  <>
                    <Bot className="w-4 h-4" />
                    Test Connection
                  </>
                )}
              </button>

              {testResult && (
                <div className={`mt-3 p-3 rounded-lg flex items-start gap-2 ${
                  testResult.success 
                    ? 'bg-green-500/20 border border-green-500/30' 
                    : 'bg-red-500/20 border border-red-500/30'
                }`}>
                  {testResult.success ? (
                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                  )}
                  <span className={testResult.success ? 'text-green-400' : 'text-red-400'}>
                    {testResult.message}
                  </span>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Save Button */}
      <div className="card">
        {saveError && (
          <InlineError error={saveError} title={t('settings.saveFailed')} className="mb-4" />
        )}

        <button
          onClick={handleSave}
          disabled={isSaving}
          className="btn-primary flex items-center gap-2"
        >
          <Save className="w-4 h-4" />
          {isSaving ? t('common.loading') : t('settings.saveChanges')}
        </button>
      </div>

      {/* Export Your Data */}
      <div className="card">
        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-border">
          <Download className="w-6 h-6 text-amber-500" />
          <div>
            <h2 className="text-lg font-semibold text-text-primary">Export Your Data</h2>
            <p className="text-sm text-text-secondary">Download your data — it's yours</p>
          </div>
        </div>

        <div className="space-y-3">
          <ExportButton
            label="Full Data Export"
            description="Everything as JSON in a ZIP file (GDPR-compliant)"
            endpoint="/me/export/"
            filename="devotional-journal-export.zip"
            icon={<Download className="w-4 h-4" />}
          />
          <ExportButton
            label="Journal (Markdown)"
            description="All journal entries formatted for reading or printing"
            endpoint="/me/export/journal/"
            filename="journal-entries.md"
            icon={<FileText className="w-4 h-4" />}
          />
          <ExportButton
            label="Highlights (Markdown)"
            description="Verse highlights and notes grouped by book"
            endpoint="/me/export/highlights/"
            filename="highlights.md"
            icon={<FileText className="w-4 h-4" />}
          />
          <ExportButton
            label="Growth Report (Markdown)"
            description="Summary of your spiritual growth journey with stats"
            endpoint="/me/export/growth/"
            filename="growth-report.md"
            icon={<FileText className="w-4 h-4" />}
          />
        </div>
      </div>
    </div>
  )
}

function ExportButton({
  label,
  description,
  endpoint,
  filename,
  icon,
}: {
  label: string
  description: string
  endpoint: string
  filename: string
  icon: React.ReactNode
}) {
  const [isDownloading, setIsDownloading] = useState(false)
  const toast = useToast()
  const { t } = useTranslation()

  const handleDownload = async () => {
    setIsDownloading(true)
    try {
      const response = await client.get(endpoint, { responseType: 'blob', timeout: 120_000 })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      toast.fromError(err, t('settings.exportFailed'))
    } finally {
      setIsDownloading(false)
    }
  }

  return (
    <button
      onClick={handleDownload}
      disabled={isDownloading}
      className="w-full flex items-center gap-4 p-4 bg-gray-800/50 hover:bg-gray-800 border border-gray-700 hover:border-amber-500/30 rounded-xl text-left transition-all group disabled:opacity-50"
    >
      <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-400 group-hover:bg-amber-500/20 transition-colors">
        {isDownloading ? <Loader2 className="w-4 h-4 animate-spin" /> : icon}
      </div>
      <div className="flex-1">
        <p className="text-text-primary font-medium">{label}</p>
        <p className="text-text-secondary text-sm">{description}</p>
      </div>
      <Download className="w-4 h-4 text-text-secondary opacity-0 group-hover:opacity-100 transition-opacity" />
    </button>
  )
}
