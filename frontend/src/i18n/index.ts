import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './en.json'
import es from './es.json'
import { getStoredLanguage } from './language'

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    es: { translation: es },
  },
  // An explicit choice on this device wins; the profile preference is applied
  // after sign-in (see applyProfileLanguage).
  lng: getStoredLanguage() ?? 'en',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
})

i18n.on('languageChanged', (language) => {
  if (typeof document !== 'undefined') document.documentElement.lang = language
})
if (typeof document !== 'undefined') document.documentElement.lang = i18n.language

export default i18n
