import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes, useLocation } from 'react-router-dom'
import { renderWithApp } from '../test/renderWithApp'
import QuickCaptureModal from './QuickCaptureModal'
import * as journalApi from '../api/journal'
import { parseJournalContent } from '../lib/journalContent'

vi.mock('../api/journal', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/journal')>()
  return { ...actual, createJournalEntry: vi.fn() }
})

const api = vi.mocked(journalApi)

function Location() {
  const location = useLocation()
  return <p data-testid="location">{location.pathname + location.search}</p>
}

function renderModal(onClose = vi.fn(), activeFocus?: { intention: string; themes: string[] }) {
  renderWithApp(
    <>
      <Routes>
        <Route path="*" element={<Location />} />
      </Routes>
      <QuickCaptureModal isOpen onClose={onClose} activeFocus={activeFocus} />
    </>
  )
  return onClose
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe('QuickCaptureModal', () => {
  it('is a labelled modal dialog with named mood buttons', () => {
    renderModal()
    const dialog = screen.getByRole('dialog', { name: 'Quick capture' })
    expect(dialog).toHaveAttribute('aria-modal', 'true')
    expect(screen.getByLabelText("What's on your heart right now?")).toHaveFocus()
    expect(screen.getByRole('button', { name: 'Grateful' })).toHaveAttribute('aria-pressed', 'false')
  })

  it('shows the error and keeps the text when saving fails', async () => {
    api.createJournalEntry.mockRejectedValue({
      code: 'SERVER_ERROR',
      message: 'The database is unavailable.',
      suggestion: 'Try again in a minute.',
      requestId: 'req-42',
      status: 500,
    })
    const user = userEvent.setup()
    const onClose = renderModal()

    await user.type(screen.getByLabelText("What's on your heart right now?"), 'A hard day')
    await user.click(screen.getByRole('button', { name: 'Save' }))

    expect((await screen.findAllByText('The database is unavailable.')).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/SERVER_ERROR/).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/req-42/).length).toBeGreaterThan(0)
    expect(onClose).not.toHaveBeenCalled()
    expect(screen.getByLabelText("What's on your heart right now?")).toHaveValue('A hard day')
    expect(screen.getByTestId('location')).toHaveTextContent('/')
  })

  it('stores metadata as valid JSON and opens the entry for feedback on success', async () => {
    api.createJournalEntry.mockResolvedValue({ id: 'new-1', date: '2026-11-12', mood_tag: '', created_at: '' })
    const user = userEvent.setup()
    const onClose = renderModal(vi.fn(), { intention: 'Trust "fully"\nand rest', themes: ['peace'] })

    await user.type(screen.getByLabelText("What's on your heart right now?"), 'Grateful today')
    await user.click(screen.getByRole('button', { name: 'Peaceful' }))
    await user.click(screen.getByRole('button', { name: 'Save' }))

    await waitFor(() => expect(onClose).toHaveBeenCalled())
    const sent = api.createJournalEntry.mock.calls[0][0]
    expect(sent.mood_tag).toBe('peaceful')
    const parsed = parseJournalContent(sent.content)
    expect(parsed.userContent).toBe('Grateful today')
    expect(parsed.meta).toEqual({
      focus_intention: 'Trust "fully"\nand rest',
      focus_themes: ['peace'],
      capture_type: 'quick',
    })
    expect(screen.getByTestId('location')).toHaveTextContent('/journal/new-1?feedback=1')
  })

  it('closes on Escape', async () => {
    const user = userEvent.setup()
    const onClose = renderModal()
    await user.keyboard('{Escape}')
    expect(onClose).toHaveBeenCalled()
  })
})
