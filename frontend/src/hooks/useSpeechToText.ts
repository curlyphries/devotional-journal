import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * Voice entry using the browser's Web Speech API.
 *
 * Privacy: this app never records or uploads audio. Chrome, Edge and Safari
 * transcribe speech with the browser vendor's speech service (so audio leaves
 * the device, to that vendor, while dictating). Firefox has no implementation,
 * so `supported` is false there.
 */

// Minimal typings for the parts of the Web Speech API used here — the API is
// not in TypeScript's DOM lib.
interface SpeechAlternativeLike {
  transcript: string
}
interface SpeechResultLike {
  readonly isFinal: boolean
  readonly length: number
  [index: number]: SpeechAlternativeLike
}
interface SpeechResultListLike {
  readonly length: number
  [index: number]: SpeechResultLike
}
export interface SpeechRecognitionEventLike {
  readonly resultIndex: number
  readonly results: SpeechResultListLike
}
export interface SpeechRecognitionErrorEventLike {
  readonly error: string
  readonly message?: string
}
export interface SpeechRecognitionLike {
  continuous: boolean
  interimResults: boolean
  lang: string
  maxAlternatives: number
  onresult: ((event: SpeechRecognitionEventLike) => void) | null
  onerror: ((event: SpeechRecognitionErrorEventLike) => void) | null
  onend: (() => void) | null
  onstart: (() => void) | null
  start: () => void
  stop: () => void
  abort: () => void
}
export type SpeechRecognitionConstructor = new () => SpeechRecognitionLike

interface SpeechWindow {
  SpeechRecognition?: SpeechRecognitionConstructor
  webkitSpeechRecognition?: SpeechRecognitionConstructor
}

export function getSpeechRecognitionConstructor(): SpeechRecognitionConstructor | null {
  if (typeof window === 'undefined') return null
  const speechWindow = window as unknown as SpeechWindow
  return speechWindow.SpeechRecognition ?? speechWindow.webkitSpeechRecognition ?? null
}

export type SpeechErrorCode =
  | 'not-allowed'
  | 'no-speech'
  | 'network'
  | 'audio-capture'
  | 'unsupported'
  | 'unknown'

export interface SpeechError {
  code: SpeechErrorCode
  /** i18n key for the user-facing explanation. */
  messageKey: string
}

const ERROR_KEYS: Record<SpeechErrorCode, string> = {
  'not-allowed': 'voice.errors.notAllowed',
  'no-speech': 'voice.errors.noSpeech',
  network: 'voice.errors.network',
  'audio-capture': 'voice.errors.audioCapture',
  unsupported: 'voice.errors.unsupported',
  unknown: 'voice.errors.unknown',
}

/** Map a Web Speech API error name onto the handful of cases we explain. Null = not worth showing. */
export function mapSpeechError(error: string): SpeechError | null {
  // "aborted" is what the browser reports when we (or the user) stop it.
  if (error === 'aborted') return null
  let code: SpeechErrorCode = 'unknown'
  if (error === 'not-allowed' || error === 'service-not-allowed') code = 'not-allowed'
  else if (error === 'no-speech') code = 'no-speech'
  else if (error === 'network') code = 'network'
  else if (error === 'audio-capture') code = 'audio-capture'
  else if (error === 'language-not-supported') code = 'unsupported'
  return { code, messageKey: ERROR_KEYS[code] }
}

/**
 * Speech-recognition language for a UI language. Spanish follows the browser's
 * own regional variant when it has one (es-MX, es-AR…), otherwise es-MX for
 * the Americas, or es-ES when the browser says Spain.
 */
export function speechLanguageFor(uiLanguage: string | undefined): string {
  const browserLanguages: readonly string[] =
    typeof navigator !== 'undefined' ? navigator.languages ?? [navigator.language] : []
  if (uiLanguage?.startsWith('es')) {
    const regional = browserLanguages.find((lang) => /^es-[A-Za-z0-9]{2,3}$/.test(lang ?? ''))
    return regional ?? 'es-MX'
  }
  const regional = browserLanguages.find((lang) => /^en-[A-Za-z]{2}$/.test(lang ?? ''))
  return regional ?? 'en-US'
}

export interface UseSpeechToTextOptions {
  /** BCP-47 language, e.g. "en-US" or "es-MX". */
  lang: string
  /** Called once for each finished phrase. */
  onFinalText: (text: string) => void
}

export interface UseSpeechToText {
  /** False when the browser has no speech recognition (e.g. Firefox). */
  supported: boolean
  listening: boolean
  /** Words heard so far for the phrase in progress; not yet final. */
  interim: string
  error: SpeechError | null
  start: () => void
  stop: () => void
  toggle: () => void
}

export function useSpeechToText({ lang, onFinalText }: UseSpeechToTextOptions): UseSpeechToText {
  const [supported] = useState(() => getSpeechRecognitionConstructor() !== null)
  const [listening, setListening] = useState(false)
  const [interim, setInterim] = useState('')
  const [error, setError] = useState<SpeechError | null>(null)

  const recognitionRef = useRef<SpeechRecognitionLike | null>(null)
  // Latest callback without restarting recognition when the parent re-renders.
  const onFinalTextRef = useRef(onFinalText)
  useEffect(() => {
    onFinalTextRef.current = onFinalText
  }, [onFinalText])

  const detach = (recognition: SpeechRecognitionLike) => {
    recognition.onresult = null
    recognition.onerror = null
    recognition.onend = null
    recognition.onstart = null
  }

  const stop = useCallback(() => {
    // stop() (not abort()) lets the browser deliver the last phrase as final.
    recognitionRef.current?.stop()
  }, [])

  const start = useCallback(() => {
    const Recognition = getSpeechRecognitionConstructor()
    if (!Recognition) {
      setError({ code: 'unsupported', messageKey: ERROR_KEYS.unsupported })
      return
    }
    if (recognitionRef.current) return

    const recognition = new Recognition()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.maxAlternatives = 1
    recognition.lang = lang

    recognition.onstart = () => setListening(true)

    recognition.onresult = (event) => {
      let interimText = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        const transcript = result[0]?.transcript ?? ''
        if (result.isFinal) {
          const finalText = transcript.trim()
          if (finalText) onFinalTextRef.current(finalText)
        } else {
          interimText += transcript
        }
      }
      setInterim(interimText.trim())
    }

    recognition.onerror = (event) => {
      const mapped = mapSpeechError(event.error)
      if (mapped) setError(mapped)
    }

    recognition.onend = () => {
      detach(recognition)
      if (recognitionRef.current === recognition) recognitionRef.current = null
      setListening(false)
      setInterim('')
    }

    recognitionRef.current = recognition
    setError(null)
    setInterim('')
    try {
      recognition.start()
      // Some browsers never fire onstart; reflect the state right away.
      setListening(true)
    } catch {
      detach(recognition)
      recognitionRef.current = null
      setListening(false)
      setError({ code: 'unknown', messageKey: ERROR_KEYS.unknown })
    }
  }, [lang])

  const toggle = useCallback(() => {
    if (recognitionRef.current) stop()
    else start()
  }, [start, stop])

  // Never leave the microphone open after the component goes away.
  useEffect(() => {
    return () => {
      const recognition = recognitionRef.current
      if (recognition) {
        detach(recognition)
        recognitionRef.current = null
        recognition.abort()
      }
    }
  }, [])

  return { supported, listening, interim, error, start, stop, toggle }
}
