import { describe, it, expect, vi, afterEach } from 'vitest'
import { act, renderHook } from '@testing-library/react'
import {
  mapSpeechError,
  useSpeechToText,
  type SpeechRecognitionErrorEventLike,
  type SpeechRecognitionEventLike,
  type SpeechRecognitionLike,
} from './useSpeechToText'

class MockRecognition implements SpeechRecognitionLike {
  static last: MockRecognition | null = null
  continuous = false
  interimResults = false
  lang = ''
  maxAlternatives = 1
  onresult: ((event: SpeechRecognitionEventLike) => void) | null = null
  onerror: ((event: SpeechRecognitionErrorEventLike) => void) | null = null
  onend: (() => void) | null = null
  onstart: (() => void) | null = null
  start = vi.fn(() => this.onstart?.())
  stop = vi.fn(() => this.onend?.())
  abort = vi.fn()

  constructor() {
    MockRecognition.last = this
  }

  emit(results: { transcript: string; isFinal: boolean }[]) {
    const list = results.map((r) => ({ isFinal: r.isFinal, length: 1, 0: { transcript: r.transcript } }))
    this.onresult?.({ resultIndex: 0, results: Object.assign(list, { length: list.length }) })
  }
}

type SpeechWindow = { SpeechRecognition?: unknown; webkitSpeechRecognition?: unknown }
const speechWindow = window as unknown as SpeechWindow

afterEach(() => {
  delete speechWindow.SpeechRecognition
  delete speechWindow.webkitSpeechRecognition
  MockRecognition.last = null
})

describe('useSpeechToText', () => {
  it('reports supported=false when the browser has no speech recognition', () => {
    const { result } = renderHook(() => useSpeechToText({ lang: 'en-US', onFinalText: vi.fn() }))
    expect(result.current.supported).toBe(false)

    act(() => result.current.start())
    expect(result.current.listening).toBe(false)
    expect(result.current.error?.code).toBe('unsupported')
  })

  it('delivers final transcripts and exposes interim text', () => {
    speechWindow.webkitSpeechRecognition = MockRecognition
    const onFinalText = vi.fn()
    const { result } = renderHook(() => useSpeechToText({ lang: 'es-MX', onFinalText }))
    expect(result.current.supported).toBe(true)

    act(() => result.current.start())
    const recognition = MockRecognition.last!
    expect(recognition.start).toHaveBeenCalledTimes(1)
    expect(recognition.continuous).toBe(true)
    expect(recognition.interimResults).toBe(true)
    expect(recognition.lang).toBe('es-MX')
    expect(result.current.listening).toBe(true)

    act(() => recognition.emit([{ transcript: 'today I felt', isFinal: false }]))
    expect(result.current.interim).toBe('today I felt')
    expect(onFinalText).not.toHaveBeenCalled()

    act(() => recognition.emit([{ transcript: ' today I felt anxious ', isFinal: true }]))
    expect(onFinalText).toHaveBeenCalledWith('today I felt anxious')
    expect(result.current.interim).toBe('')

    act(() => result.current.stop())
    expect(recognition.stop).toHaveBeenCalled()
    expect(result.current.listening).toBe(false)
  })

  it('maps a blocked microphone to an explained error', () => {
    speechWindow.SpeechRecognition = MockRecognition
    const { result } = renderHook(() => useSpeechToText({ lang: 'en-US', onFinalText: vi.fn() }))

    act(() => result.current.start())
    const recognition = MockRecognition.last!
    act(() => {
      recognition.onerror?.({ error: 'not-allowed' })
      recognition.onend?.()
    })

    expect(result.current.error).toEqual({ code: 'not-allowed', messageKey: 'voice.errors.notAllowed' })
    expect(result.current.listening).toBe(false)
  })

  it('maps the other error names', () => {
    expect(mapSpeechError('no-speech')?.code).toBe('no-speech')
    expect(mapSpeechError('network')?.code).toBe('network')
    expect(mapSpeechError('audio-capture')?.code).toBe('audio-capture')
    expect(mapSpeechError('service-not-allowed')?.code).toBe('not-allowed')
    expect(mapSpeechError('something-new')?.code).toBe('unknown')
    expect(mapSpeechError('aborted')).toBeNull()
  })

  it('releases the microphone on unmount', () => {
    speechWindow.SpeechRecognition = MockRecognition
    const { result, unmount } = renderHook(() => useSpeechToText({ lang: 'en-US', onFinalText: vi.fn() }))
    act(() => result.current.start())
    const recognition = MockRecognition.last!
    unmount()
    expect(recognition.abort).toHaveBeenCalled()
  })
})
