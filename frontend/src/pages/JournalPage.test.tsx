import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes, useLocation } from 'react-router-dom'
import { renderWithApp } from '../test/renderWithApp'
import JournalPage from './JournalPage'
import * as journalApi from '../api/journal'
import { buildJournalContent, parseJournalContent } from '../lib/journalContent'

vi.mock('../api/journal', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/journal')>()
  return {
    ...actual,
    getJournalEntry: vi.fn(),
    createJournalEntry: vi.fn(),
    updateJournalEntry: vi.fn(),
    deleteJournalEntry: vi.fn(),
  }
})
vi.mock('../api/devotional', () => ({ getActiveFocusIntentions: vi.fn().mockResolvedValue([]) }))
vi.mock('../api/highlights', () => ({ getHighlights: vi.fn().mockResolvedValue([]) }))
vi.mock('../api/bible', () => ({ getPassage: vi.fn().mockResolvedValue({ verses: [] }) }))
vi.mock('../api/client', () => ({
  default: { get: vi.fn().mockResolvedValue({ data: [] }), post: vi.fn() },
}))
vi.mock('../components/JournalFeedbackPanel', () => ({
  default: ({ entryId, autoGenerate }: { entryId: string; autoGenerate?: boolean }) => (
    <div data-testid="feedback-panel" data-entry={entryId} data-auto={String(!!autoGenerate)} />
  ),
}))

const api = vi.mocked(journalApi)

function Location() {
  const location = useLocation()
  return <p data-testid="location">{location.pathname + location.search}</p>
}

function renderAt(route: string) {
  return renderWithApp(
    <>
      <Location />
      <Routes>
        <Route path="/journal/new" element={<JournalPage />} />
        <Route path="/journal/:entryId" element={<JournalPage />} />
        <Route path="/journal" element={<p>History</p>} />
      </Routes>
    </>,
    { route }
  )
}

const failure = { code: 'SERVER_ERROR', message: 'Decryption failed.', requestId: 'req-9', status: 500 }

beforeEach(() => {
  vi.clearAllMocks()
})

describe('JournalPage', () => {
  it('shows an error — not an empty editor — when the entry fails to load', async () => {
    api.getJournalEntry.mockRejectedValue(failure)
    renderAt('/journal/e1')

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('This entry could not be loaded')
    expect(alert).toHaveTextContent('Decryption failed.')
    expect(alert).toHaveTextContent('req-9')
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /save/i })).not.toBeInTheDocument()
  })

  it('after saving a new entry, stays with it and asks for feedback', async () => {
    api.createJournalEntry.mockResolvedValue({ id: 'e2', date: '2026-11-12', mood_tag: '', created_at: '' })
    api.getJournalEntry.mockResolvedValue({
      id: 'e2',
      date: '2026-11-12',
      mood_tag: 'grateful',
      decrypted_content: 'A good day',
      created_at: '',
    })
    const user = userEvent.setup()
    renderAt('/journal/new')

    await user.type(screen.getByLabelText('Your entry'), 'A good day')
    await user.click(screen.getByRole('button', { name: /Grateful/ }))
    await user.click(screen.getByRole('button', { name: 'Save and get feedback' }))

    await waitFor(() => expect(screen.getByTestId('location')).toHaveTextContent('/journal/e2?feedback=1'))
    expect(api.createJournalEntry).toHaveBeenCalledWith(
      expect.objectContaining({ content: 'A good day', mood_tag: 'grateful' })
    )
    const panel = await screen.findByTestId('feedback-panel')
    expect(panel).toHaveAttribute('data-entry', 'e2')
    expect(panel).toHaveAttribute('data-auto', 'true')
    expect(await screen.findByText('Entry saved.')).toBeInTheDocument()
    await waitFor(() => expect(screen.getByLabelText('Your entry')).toHaveValue('A good day'))
  })

  it('keeps a quick-capture entry\'s metadata when it is edited', async () => {
    const meta = { focus_intention: 'Trust "fully"', focus_themes: ['peace'], capture_type: 'quick' }
    api.getJournalEntry.mockResolvedValue({
      id: 'e3',
      date: '2026-11-10',
      mood_tag: '',
      decrypted_content: buildJournalContent(meta, 'First thought'),
      created_at: '',
    })
    api.updateJournalEntry.mockResolvedValue({ id: 'e3', date: '2026-11-10', mood_tag: '', created_at: '' })
    const user = userEvent.setup()
    renderAt('/journal/e3')

    const textbox = await screen.findByLabelText('Your entry')
    await waitFor(() => expect(textbox).toHaveValue('First thought'))
    // The raw block is never shown.
    expect(screen.queryByText(/DJ_META/)).not.toBeInTheDocument()
    expect(screen.getByTestId('feedback-panel')).toHaveAttribute('data-auto', 'false')

    await user.type(textbox, ' — and more')
    await user.click(screen.getByRole('button', { name: 'Save changes' }))

    await waitFor(() => expect(api.updateJournalEntry).toHaveBeenCalled())
    const [id, data] = api.updateJournalEntry.mock.calls[0]
    expect(id).toBe('e3')
    const parsed = parseJournalContent(data.content)
    expect(parsed.meta).toEqual(meta)
    expect(parsed.userContent).toBe('First thought — and more')
    // Stays on the entry.
    expect(screen.getByTestId('location')).toHaveTextContent('/journal/e3')
  })

  it('confirms before deleting and reports a failed delete', async () => {
    api.getJournalEntry.mockResolvedValue({
      id: 'e4',
      date: '2026-11-10',
      mood_tag: '',
      decrypted_content: 'Keep me',
      created_at: '',
    })
    api.deleteJournalEntry.mockRejectedValue(failure)
    const user = userEvent.setup()
    renderAt('/journal/e4')

    await user.click(await screen.findByRole('button', { name: 'Delete' }))
    expect(api.deleteJournalEntry).not.toHaveBeenCalled()
    const dialog = screen.getByRole('dialog', { name: 'Delete this entry?' })
    expect(dialog).toBeInTheDocument()

    await user.click(screen.getAllByRole('button', { name: 'Delete' }).find((b) => dialog.contains(b))!)
    expect(api.deleteJournalEntry).toHaveBeenCalledWith('e4')
    expect(await screen.findByText(/The entry could not be deleted/)).toBeInTheDocument()
    expect(screen.getByTestId('location')).toHaveTextContent('/journal/e4')
  })
})
