import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import '../i18n'
import DictationButton, { insertDictatedText } from './DictationButton'

describe('insertDictatedText', () => {
  it('appends with a space when there is no cursor', () => {
    expect(insertDictatedText('Hello', 'world')).toEqual({ value: 'Hello world', cursor: 11 })
    expect(insertDictatedText('', 'Hello')).toEqual({ value: 'Hello', cursor: 5 })
  })

  it('inserts at the cursor and replaces a selection', () => {
    expect(insertDictatedText('Hello world', 'big', 5, 5).value).toBe('Hello big world')
    expect(insertDictatedText('Hello old world', 'new', 6, 9).value).toBe('Hello new world')
  })
})

describe('DictationButton', () => {
  it('is shown disabled with an explanation when speech recognition is unsupported', () => {
    render(<DictationButton value="" onChange={() => undefined} />)
    const button = screen.getByRole('button', { name: /dictation unavailable/i })
    expect(button).toBeDisabled()
    expect(screen.getByText(/works in Chrome, Edge and Safari/i)).toBeInTheDocument()
  })
})
