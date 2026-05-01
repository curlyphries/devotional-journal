import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../context/AuthContext'
import { updateProfile, testAIConnection } from '../api/auth'
import { Save, User, Bot, Key, CheckCircle, XCircle, Loader2, Eye, EyeOff } from 'lucide-react'

const AI_PROVIDERS = [
  { value: 'none', label: 'None (Use System Default)', needsKey: false, needsUrl: false },
  { value: 'openai', label: 'OpenAI', needsKey: true, needsUrl: false, defaultModel: 'gpt-4o-mini' },
  { value: 'anthropic', label: 'Anthropic (Claude)', needsKey: true, needsUrl: false, defaultModel: 'claude-3-haiku-20240307' },
  { value: 'openrouter', label: 'OpenRouter', needsKey: true, needsUrl: false, defaultModel: 'openai/gpt-4o-mini' },
  { value: 'ollama', label: 'Ollama (Local)', needsKey: false, needsUrl: true, defaultModel: 'llama3.1:8b' },
  { value: 'custom', label: 'Custom OpenAI-Compatible', needsKey: true, needsUrl: true, defaultModel: '' },
]

export default function SettingsPage() {
  const { t, i18n } = useTranslation()
  const { user, refreshUser } = useAuth()

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
  const [message, setMessage] = useState('')
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

  const handleSave = async () => {
    setIsSaving(true)
    setMessage('')

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
      i18n.changeLanguage(language === 'bilingual' ? 'en' : language)
      await refreshUser()
      setMessage('Settings saved successfully!')
      setAiApiKey('') // Clear the key field after save
    } catch {
      setMessage('Failed to save settings.')
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
      const apiErr = err as { response?: { data?: { error?: string } } }
      setTestResult({
        success: false,
        message: apiErr.response?.data?.error || 'Connection test failed'
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
            />
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
          </div>
        </div>
      </div>

      {/* AI Provider Settings */}
      <div className="card">
        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-border">
          <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
            <Bot className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-text-primary">AI Provider</h2>
            <p className="text-sm text-text-secondary">Connect your own AI for insights and summaries</p>
          </div>
        </div>

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
              />
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
        {message && (
          <p
            className={`text-sm mb-4 ${
              message.includes('success') ? 'text-success' : 'text-danger'
            }`}
          >
            {message}
          </p>
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
    </div>
  )
}
