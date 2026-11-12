import i18next from 'i18next'

/**
 * Language persistence. Kept free of react-i18next so non-UI code (and tests
 * that mock react-i18next) can import it.
 */
export type AppLanguage = 'en' | 'es'

const STORAGE_KEY = 'dj_language'

function isAppLanguage(value: unknown): value is AppLanguage {
  return value === 'en' || value === 'es'
}

/** The language the user explicitly picked on this device, if any. */
export function getStoredLanguage(): AppLanguage | null {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY)
    return isAppLanguage(stored) ? stored : null
  } catch {
    return null
  }
}

/** Switch language and remember it as this device's explicit choice. */
export function setLanguage(language: AppLanguage): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, language)
  } catch {
    // Storage unavailable (private mode): the choice still applies for this visit.
  }
  void i18next.changeLanguage(language)
}

/**
 * Apply the profile's language after sign-in, unless the user already chose
 * one on this device. "bilingual" has no single UI language, so it is left alone.
 */
export function applyProfileLanguage(preference: string | null | undefined): void {
  if (getStoredLanguage()) return
  if (isAppLanguage(preference) && i18next.isInitialized && i18next.language !== preference) {
    void i18next.changeLanguage(preference)
  }
}
