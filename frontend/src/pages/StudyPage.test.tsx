import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AxiosError, type AxiosResponse } from 'axios'
import { Route, Routes } from 'react-router-dom'
import { renderWithApp } from '../test/renderWithApp'
import StudyPage from './StudyPage'
import * as guidesApi from '../api/guides'
import type { Lesson, LessonReply, LessonResult, StudyDetail, TopicCard } from '../api/guides'

vi.mock('../api/guides', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/guides')>()
  return {
    ...actual,
    getStudy: vi.fn(),
    getLesson: vi.fn(),
    respondToLesson: vi.fn(),
    simplifyLesson: vi.fn(),
    personalizeLesson: vi.fn(),
    leaveStudy: vi.fn(),
    startStudy: vi.fn(),
  }
})

const api = vi.mocked(guidesApi)
// src/test/setup.ts replaces localStorage with vi.fn() stubs.
const storage = {
  getItem: vi.mocked(window.localStorage.getItem),
  setItem: vi.mocked(window.localStorage.setItem),
  removeItem: vi.mocked(window.localStorage.removeItem),
}

const DRAFT_KEY = 'study-draft:s-1:2'
const Q1 = 'What worry are you carrying today?'
const Q2 = 'What would it look like to hand it over?'

const study: StudyDetail = {
  id: 's-1',
  topic: { key: 'anxiety', title: 'When worry will not stop', category: 'peace', sensitive: false },
  life_stage: 'adult',
  status: 'active',
  current_lesson: 2,
  lesson_count: 4,
  completed_lessons: [1],
  progress_percent: 25,
  started_at: '2026-11-10T09:00:00Z',
  completed_at: null,
  stage_note: 'For full lives: when the list never ends.',
  summary: 'Handing your fears to God, one at a time.',
  lessons: [
    { number: 1, title: 'Naming the worry', reference: 'Matthew 6:25-27', completed: true },
    { number: 2, title: 'Casting your cares', reference: '1 Peter 5:6-7', completed: false },
    { number: 3, title: 'Peace that guards', reference: 'Philippians 4:6-7', completed: false },
    { number: 4, title: 'Tomorrow', reference: 'Matthew 6:33-34', completed: false },
  ],
}

const lesson: Lesson = {
  study_id: 's-1',
  number: 2,
  lesson_count: 4,
  title: 'Casting your cares',
  topic: { key: 'anxiety', title: 'When worry will not stop' },
  passage: {
    reference: '1 Peter 5:6-7',
    text: 'Humble yourselves therefore under the mighty hand of God… casting all your worries on him, because he cares for you.',
    translation: 'WEB',
    translation_name: 'World English Bible',
    verified: true,
    source: 'bolls',
  },
  passage_error: null,
  reference: '1 Peter 5:6-7',
  explanation: 'Peter pictures worry as a weight you were never built to carry by yourself.',
  explanation_level: 'standard',
  questions: [Q1, Q2],
  practice: 'Write one worry on paper and pray over it by name.',
  prayer: 'Father, I give you what I cannot carry.',
  with_grown_up: false,
  support_note: null,
  personal: null,
  response: null,
  previous: { number: 1 },
  next: { number: 3 },
}

const aiReply: LessonReply = {
  text: 'Naming it is already a way of handing it over.',
  follow_up: 'Who could carry this with you this week?',
  source: 'ai',
  fallback_reason: null,
}

function resultFor(overrides: Partial<LessonResult> = {}, base: Lesson = lesson): LessonResult {
  return {
    lesson: {
      ...base,
      response: {
        answers: [{ question: Q1, answer: 'The deadline at work.' }],
        stood_out: 'He cares for you.',
        understanding: 4,
        resonance: 5,
        reply: overrides.reply ?? aiReply,
        completed_at: '2026-11-13T10:00:00Z',
      },
    },
    reply: aiReply,
    study: { ...study, current_lesson: 3, completed_lessons: [1, 2], progress_percent: 50 },
    next_step: { kind: 'next_lesson', number: 3 },
    ...overrides,
  }
}

function notFound(): AxiosError {
  const response = {
    status: 404,
    statusText: 'Not Found',
    headers: {},
    config: {},
    data: { error: 'No such study.', code: 'NOT_FOUND', request_id: 'abc12345' },
  } as unknown as AxiosResponse
  return new AxiosError('Request failed with status code 404', 'ERR_BAD_REQUEST', undefined, undefined, response)
}

function renderStudy(route = '/study/s-1') {
  return renderWithApp(
    <Routes>
      <Route path="/study/:studyId" element={<StudyPage />} />
      <Route path="/study" element={<p>Study hub</p>} />
    </Routes>,
    { route }
  )
}

function scale(name: string) {
  return screen.getByRole('group', { name })
}

async function fillAndSave(user: ReturnType<typeof userEvent.setup>) {
  await user.type(await screen.findByLabelText(Q1), 'The deadline at work.')
  await user.type(screen.getByLabelText('What stood out to you?'), 'He cares for you.')
  await user.click(within(scale('How well did you understand this passage?')).getByRole('radio', { name: /^4/ }))
  await user.click(
    within(scale('How much does this speak to where you are right now?')).getByRole('radio', { name: /^5/ })
  )
  await user.click(screen.getByRole('button', { name: 'Save my reflection' }))
}

beforeEach(() => {
  vi.clearAllMocks()
  storage.getItem.mockReset()
  api.getStudy.mockResolvedValue(study)
  api.getLesson.mockResolvedValue(lesson)
})

describe('StudyPage', () => {
  it('opens where the person left off, with the verified passage and the questions', async () => {
    renderStudy()

    expect(await screen.findByRole('heading', { level: 1, name: study.topic.title })).toBeInTheDocument()
    expect(await screen.findByRole('heading', { level: 2, name: 'Lesson 2: Casting your cares' })).toBeInTheDocument()
    expect(api.getLesson).toHaveBeenCalledWith('s-1', 2)
    expect(screen.getByText('Lesson 2 of 4')).toBeInTheDocument()

    // Stepper: every lesson can be opened; done and current are marked.
    const stepper = screen.getByRole('navigation', { name: 'Lessons in this study' })
    expect(within(stepper).getByRole('link', { name: 'Lesson 1: Naming the worry (completed)' })).toHaveAttribute(
      'href',
      '/study/s-1?lesson=1'
    )
    expect(within(stepper).getByRole('link', { name: 'Lesson 2: Casting your cares' })).toHaveAttribute(
      'aria-current',
      'step'
    )
    expect(within(stepper).getAllByRole('link')).toHaveLength(4)

    // Read: the Bible text, its translation, and the verified badge.
    expect(screen.getByRole('heading', { name: '1 Peter 5:6-7' })).toBeInTheDocument()
    expect(screen.getByText(/casting all your worries on him/)).toBeInTheDocument()
    expect(screen.getByText('Verified against World English Bible')).toBeInTheDocument()
    expect(screen.getByText('World English Bible (WEB)')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Open in Bible/ })).toHaveAttribute(
      'href',
      '/bible?passage=1%20Peter%205%3A6-7'
    )

    // Understand, reflect, practice, pray.
    expect(screen.getByText(lesson.explanation)).toBeInTheDocument()
    expect(screen.getByLabelText(Q1)).toHaveValue('')
    expect(screen.getByLabelText(Q2)).toBeInTheDocument()
    expect(screen.getByLabelText('What stood out to you?')).toBeInTheDocument()
    expect(within(scale('How well did you understand this passage?')).getAllByRole('radio')).toHaveLength(5)
    expect(
      within(scale('How well did you understand this passage?')).getByRole('radio', { name: /^1 — lost/ })
    ).toBeInTheDocument()
    expect(
      within(scale('How much does this speak to where you are right now?')).getByRole('radio', { name: /^5 — deeply/ })
    ).toBeInTheDocument()
    expect(screen.getByText(lesson.practice)).toBeInTheDocument()
    expect(screen.getByText(lesson.prayer)).toBeInTheDocument()

    expect(screen.queryByText('Read this one together with a grown-up.')).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'All studies' })).toHaveAttribute('href', '/study')
  })

  it('opens the lesson named in ?lesson=', async () => {
    api.getLesson.mockResolvedValue({ ...lesson, number: 1, title: 'Naming the worry', previous: null, next: { number: 2 } })
    renderStudy('/study/s-1?lesson=1')
    expect(await screen.findByRole('heading', { level: 2, name: 'Lesson 1: Naming the worry' })).toBeInTheDocument()
    expect(api.getLesson).toHaveBeenCalledWith('s-1', 1)
    expect(screen.getByText('Lesson 1 of 4')).toBeInTheDocument()
  })

  it('shows the grown-up banner and the care note when the lesson has them', async () => {
    api.getLesson.mockResolvedValue({
      ...lesson,
      with_grown_up: true,
      support_note: 'You do not have to carry this alone. Talk to someone you trust.',
    })
    renderStudy()
    expect(await screen.findByText('Read this one together with a grown-up.')).toBeInTheDocument()
    expect(screen.getByText('You do not have to carry this alone. Talk to someone you trust.')).toBeInTheDocument()
  })

  it('still shows the reference, the reason and a retry when the Bible text is missing', async () => {
    api.getLesson
      .mockResolvedValueOnce({
        ...lesson,
        passage: null,
        passage_error: {
          code: 'SCRIPTURE_UNAVAILABLE',
          message: 'The Bible source did not answer.',
          suggestion: 'Check your connection and try again.',
        },
      })
      .mockResolvedValue(lesson)
    const user = userEvent.setup()
    renderStudy()

    expect(await screen.findByRole('heading', { name: '1 Peter 5:6-7' })).toBeInTheDocument()
    const alert = screen.getByRole('alert')
    expect(within(alert).getByText('The Bible source did not answer.')).toBeInTheDocument()
    expect(within(alert).getByText('Check your connection and try again.')).toBeInTheDocument()
    expect(screen.queryByText(/Verified against/)).not.toBeInTheDocument()
    // The rest of the lesson is still there.
    expect(screen.getByText(lesson.explanation)).toBeInTheDocument()

    await user.click(within(alert).getByRole('button', { name: 'Try again' }))
    expect(await screen.findByText(/casting all your worries on him/)).toBeInTheDocument()
  })

  it('"Explain it more simply" swaps in the simpler explanation', async () => {
    api.simplifyLesson.mockResolvedValue({
      ...lesson,
      explanation: 'Worry is heavy. God wants to carry it for you.',
      explanation_level: 'simple',
    })
    const user = userEvent.setup()
    renderStudy()

    await user.click(await screen.findByRole('button', { name: 'Explain it more simply' }))
    expect(api.simplifyLesson).toHaveBeenCalledWith('s-1', 2)
    expect(await screen.findByText('Worry is heavy. God wants to carry it for you.')).toBeInTheDocument()
    expect(screen.queryByText(lesson.explanation)).not.toBeInTheDocument()
    expect(screen.getByText('Showing the simpler explanation.')).toBeInTheDocument()
    // Already simple: nothing further to offer.
    expect(screen.queryByRole('button', { name: 'Explain it more simply' })).not.toBeInTheDocument()
  })

  it('"Make it personal" shows the connection, swaps the questions and says where the AI ran', async () => {
    let finish: (value: Lesson) => void = () => undefined
    api.personalizeLesson.mockReturnValue(
      new Promise<Lesson>((resolve) => {
        finish = resolve
      })
    )
    const user = userEvent.setup()
    renderStudy()

    await user.click(await screen.findByRole('button', { name: 'Make it personal' }))
    expect(api.personalizeLesson).toHaveBeenCalledWith('s-1', 2)
    // Calm progress state while the model works.
    expect(await screen.findByText('Connecting this lesson to your life…')).toBeInTheDocument()

    finish({
      ...lesson,
      personal: {
        connection: 'You have written about deadlines three times this week.',
        explanation: 'For you, casting your cares may start with the Thursday meeting.',
        questions: ['What would you tell God about Thursday?'],
        provider: 'ollama',
        model: 'llama3.1:8b',
        local: true,
        created_at: '2026-11-13T10:00:00Z',
      },
    })

    expect(await screen.findByText('You have written about deadlines three times this week.')).toBeInTheDocument()
    expect(screen.getByText('For you, casting your cares may start with the Thursday meeting.')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Written by AI (ollama · llama3.1:8b) on your network, from your profile and recent journal themes.'
      )
    ).toBeInTheDocument()
    // The personal questions replace the standard ones; the standard explanation stays.
    expect(screen.getByLabelText('What would you tell God about Thursday?')).toBeInTheDocument()
    expect(screen.queryByLabelText(Q1)).not.toBeInTheDocument()
    expect(screen.getByText(lesson.explanation)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Make it personal' })).not.toBeInTheDocument()
  })

  it('keeps an answer already written when personal questions arrive', async () => {
    api.personalizeLesson.mockResolvedValue({
      ...lesson,
      personal: {
        connection: 'c',
        explanation: 'e',
        questions: ['What would you tell God about Thursday?'],
        provider: 'anthropic',
        model: 'claude',
        local: false,
        created_at: '2026-11-13T10:00:00Z',
      },
    })
    const user = userEvent.setup()
    renderStudy()

    await user.type(await screen.findByLabelText(Q1), 'The deadline.')
    await user.click(screen.getByRole('button', { name: 'Make it personal' }))
    expect(await screen.findByLabelText('What would you tell God about Thursday?')).toBeInTheDocument()
    expect(screen.getByLabelText(Q1)).toHaveValue('The deadline.')
    expect(screen.queryByLabelText(Q2)).not.toBeInTheDocument()
    expect(screen.getByText(/Written by AI \(anthropic · claude\) in the cloud/)).toBeInTheDocument()
  })

  it('shows why personalising failed, with the suggestion, and leaves the standard lesson usable', async () => {
    api.personalizeLesson.mockRejectedValue({
      code: 'AI_UNAVAILABLE',
      message: 'Could not reach Ollama at http://localhost:11434.',
      suggestion: 'Make sure Ollama is running.',
      requestId: 'req-42',
      status: 503,
    })
    const user = userEvent.setup()
    renderStudy()

    await user.click(await screen.findByRole('button', { name: 'Make it personal' }))
    const alert = await screen.findByRole('alert')
    expect(within(alert).getByText("This lesson couldn't be made personal")).toBeInTheDocument()
    expect(within(alert).getByText('Could not reach Ollama at http://localhost:11434.')).toBeInTheDocument()
    expect(within(alert).getByText('Make sure Ollama is running.')).toBeInTheDocument()
    expect(within(alert).getByText(/AI_UNAVAILABLE/)).toBeInTheDocument()

    // The standard lesson is untouched and can still be answered.
    expect(screen.getByText(lesson.explanation)).toBeInTheDocument()
    expect(screen.getByLabelText(Q1)).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Save my reflection' })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Make it personal' })).toBeEnabled()
  })

  it('asks for an answer and both ratings before saving', async () => {
    const user = userEvent.setup()
    renderStudy()

    await user.click(await screen.findByRole('button', { name: 'Save my reflection' }))
    expect(screen.getByRole('alert')).toHaveTextContent('Write at least one answer')
    await user.type(screen.getByLabelText(Q1), 'Something.')
    await user.click(screen.getByRole('button', { name: 'Save my reflection' }))
    expect(screen.getByRole('alert')).toHaveTextContent('Choose a number from 1 to 5')
    expect(api.respondToLesson).not.toHaveBeenCalled()
  })

  it('saves the reflection, then shows the reply and the next lesson', async () => {
    api.respondToLesson.mockResolvedValue(resultFor())
    const user = userEvent.setup()
    renderStudy()

    await fillAndSave(user)

    expect(api.respondToLesson).toHaveBeenCalledWith('s-1', 2, {
      answers: [{ question: Q1, answer: 'The deadline at work.' }],
      stood_out: 'He cares for you.',
      understanding: 4,
      resonance: 5,
    })

    expect(await screen.findByRole('heading', { name: 'A reply to your reflection' })).toBeInTheDocument()
    expect(screen.getByText(aiReply.text)).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Something to think about' })).toBeInTheDocument()
    expect(screen.getByText(aiReply.follow_up!)).toBeInTheDocument()
    expect(screen.queryByText(/prepared reply/)).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Next lesson' })).toHaveAttribute('href', '/study/s-1?lesson=3')

    // The answers are now shown read-only, and the draft is gone from this device.
    expect(screen.queryByLabelText(Q1)).not.toBeInTheDocument()
    expect(screen.getByText('The deadline at work.')).toBeInTheDocument()
    expect(screen.getByText('Understood: 4 of 5')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Edit my answers' })).toBeInTheDocument()
    expect(storage.removeItem).toHaveBeenCalledWith(DRAFT_KEY)
    // Understood well: no need to push the simpler explanation.
    expect(screen.queryByText('Was this one hard to follow?')).not.toBeInTheDocument()
  })

  it('says so when the reply is a built-in one because the AI was unavailable', async () => {
    const builtIn: LessonReply = {
      text: 'Thank you for taking time with this passage.',
      follow_up: null,
      source: 'built_in',
      fallback_reason: {
        code: 'AI_UNAVAILABLE',
        message: 'Could not reach Ollama at http://localhost:11434.',
        suggestion: 'Make sure Ollama is running.',
      },
    }
    api.respondToLesson.mockResolvedValue(resultFor({ reply: builtIn }))
    const user = userEvent.setup()
    renderStudy()

    await fillAndSave(user)

    expect(await screen.findByText(builtIn.text)).toBeInTheDocument()
    const note = screen.getByText(/this is a prepared reply/).closest('[role="note"]') as HTMLElement
    expect(within(note).getByText(/Could not reach Ollama/)).toBeInTheDocument()
    expect(within(note).getByText('Make sure Ollama is running.')).toBeInTheDocument()
    expect(within(note).getByRole('link', { name: 'Check AI settings' })).toHaveAttribute(
      'href',
      '/settings#ai-provider'
    )
    expect(screen.queryByRole('heading', { name: 'Something to think about' })).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Next lesson' })).toBeInTheDocument()
  })

  it('keeps what was typed and shows the error when saving fails', async () => {
    api.respondToLesson.mockRejectedValue({
      code: 'SERVER_ERROR',
      message: 'The server had a problem.',
      suggestion: 'Try again.',
      status: 500,
    })
    const user = userEvent.setup()
    renderStudy()

    await fillAndSave(user)
    const alert = await screen.findByRole('alert')
    expect(within(alert).getByText("Your reflection couldn't be saved")).toBeInTheDocument()
    expect(within(alert).getByText('The server had a problem.')).toBeInTheDocument()
    expect(screen.getByLabelText(Q1)).toHaveValue('The deadline at work.')
    expect(storage.removeItem).not.toHaveBeenCalledWith(DRAFT_KEY)
  })

  it('keeps a draft on this device and restores it after a reload', async () => {
    storage.getItem.mockImplementation((key: string) =>
      key === DRAFT_KEY
        ? JSON.stringify({
            answers: { [Q1]: 'Half a thought about the dead' },
            stoodOut: 'because he cares',
            understanding: 3,
            resonance: null,
          })
        : null
    )
    const user = userEvent.setup()
    renderStudy()

    expect(await screen.findByLabelText(Q1)).toHaveValue('Half a thought about the dead')
    expect(screen.getByLabelText('What stood out to you?')).toHaveValue('because he cares')
    expect(
      within(scale('How well did you understand this passage?')).getByRole('radio', { name: /^3/ })
    ).toBeChecked()
    expect(screen.getByText('We brought back what you had written here before.')).toBeInTheDocument()

    // Typing keeps the draft up to date.
    await user.type(screen.getByLabelText(Q1), 'line')
    await waitFor(() => {
      const calls = storage.setItem.mock.calls.filter(([key]) => key === DRAFT_KEY)
      expect(calls.length).toBeGreaterThan(0)
      const latest = JSON.parse(calls[calls.length - 1][1] as string)
      expect(latest.answers[Q1]).toBe('Half a thought about the deadline')
      expect(latest.stoodOut).toBe('because he cares')
      expect(latest.understanding).toBe(3)
    })
  })

  it('celebrates the end of a study and suggests what to do next', async () => {
    const last: Lesson = { ...lesson, number: 4, title: 'Tomorrow', previous: { number: 3 }, next: null }
    const suggestion: TopicCard = {
      key: 'rest',
      category: 'peace',
      title: 'Rest for the weary',
      summary: 'Sabbath, sleep and the God who never slumbers.',
      lesson_count: 3,
      stages: ['adult'],
      traits: [],
      sensitive: false,
      stage_note: null,
      enrollment: null,
    }
    api.getStudy.mockResolvedValue({ ...study, current_lesson: 4, completed_lessons: [1, 2, 3] })
    api.getLesson.mockResolvedValue(last)
    api.respondToLesson.mockResolvedValue(
      resultFor(
        {
          study: { ...study, status: 'completed', completed_lessons: [1, 2, 3, 4], progress_percent: 100 },
          next_step: { kind: 'study_complete', suggestions: [suggestion] },
        },
        last
      )
    )
    api.startStudy.mockResolvedValue({ ...study, id: 's-7' })
    const user = userEvent.setup()
    renderStudy()

    await fillAndSave(user)
    expect(api.respondToLesson).toHaveBeenCalledWith('s-1', 4, expect.objectContaining({ understanding: 4 }))

    const done = (await screen.findByRole('heading', { name: 'You finished “When worry will not stop”' })).closest(
      'section'
    )!
    expect(within(done).getByRole('heading', { name: 'Rest for the weary' })).toBeInTheDocument()
    expect(within(done).getByRole('link', { name: 'Turn this into a growth plan' })).toHaveAttribute('href', '/growth')
    expect(within(done).getByRole('link', { name: 'Write about it in your journal' })).toHaveAttribute(
      'href',
      '/journal/new'
    )
    expect(screen.queryByRole('link', { name: 'Next lesson' })).not.toBeInTheDocument()

    await user.click(within(done).getByRole('button', { name: 'Start: Rest for the weary' }))
    expect(api.startStudy).toHaveBeenCalledWith('rest')
  })

  it('shows saved answers read-only with the saved reply, and lets them be edited', async () => {
    api.getLesson.mockResolvedValue({
      ...lesson,
      response: {
        answers: [{ question: Q1, answer: 'Money.' }],
        stood_out: 'Humble yourselves.',
        understanding: 2,
        resonance: 4,
        reply: aiReply,
        completed_at: '2026-11-12T10:00:00Z',
      },
    })
    api.simplifyLesson.mockResolvedValue({ ...lesson, explanation: 'Simpler words.', explanation_level: 'simple' })
    const user = userEvent.setup()
    renderStudy()

    expect(await screen.findByText('Money.')).toBeInTheDocument()
    expect(screen.getByText('Humble yourselves.')).toBeInTheDocument()
    expect(screen.getByText('Understood: 2 of 5')).toBeInTheDocument()
    expect(screen.getByText('Speaks to me: 4 of 5')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Save my reflection' })).not.toBeInTheDocument()
    expect(screen.getByText(aiReply.text)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Next lesson' })).toHaveAttribute('href', '/study/s-1?lesson=3')

    // They found it hard: the simpler explanation is offered prominently, next to the reply.
    const reply = screen.getByRole('heading', { name: 'A reply to your reflection' }).closest('section')!
    expect(within(reply).getByText('Was this one hard to follow?')).toBeInTheDocument()
    expect(within(reply).getByRole('button', { name: 'Explain it more simply' })).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Edit my answers' }))
    expect(screen.getByLabelText(Q1)).toHaveValue('Money.')
    expect(screen.getByLabelText('What stood out to you?')).toHaveValue('Humble yourselves.')
    expect(
      within(scale('How well did you understand this passage?')).getByRole('radio', { name: /^2/ })
    ).toBeChecked()
    expect(screen.getByRole('button', { name: 'Save my reflection' })).toBeInTheDocument()
    // While editing, the old reply steps aside.
    expect(screen.queryByText(aiReply.text)).not.toBeInTheDocument()
  })

  it('shows a not-found state for an id that does not exist', async () => {
    api.getStudy.mockRejectedValue(notFound())
    api.getLesson.mockRejectedValue(notFound())
    renderStudy('/study/nope')

    expect(await screen.findByRole('heading', { name: "We couldn't find that study" })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'See all studies' })).toHaveAttribute('href', '/study')
    expect(screen.queryByRole('button', { name: 'Leave this study' })).not.toBeInTheDocument()
  })

  it('shows the error with a retry when the study cannot be loaded', async () => {
    api.getStudy
      .mockRejectedValueOnce({ code: 'SERVER_ERROR', message: 'Boom.', suggestion: 'Try again.', status: 500 })
      .mockResolvedValue(study)
    const user = userEvent.setup()
    renderStudy()

    const alert = await screen.findByRole('alert')
    expect(within(alert).getByText("This study couldn't be loaded")).toBeInTheDocument()
    await user.click(within(alert).getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('heading', { level: 1, name: study.topic.title })).toBeInTheDocument()
  })

  it('leaves the study after confirming, and goes back to the hub', async () => {
    api.leaveStudy.mockResolvedValue(undefined)
    const user = userEvent.setup()
    renderStudy()

    await user.click(await screen.findByRole('button', { name: 'Leave this study' }))
    const dialog = screen.getByRole('dialog', { name: 'Leave this study?' })
    expect(api.leaveStudy).not.toHaveBeenCalled()
    await user.click(within(dialog).getByRole('button', { name: 'Leave study' }))

    expect(api.leaveStudy).toHaveBeenCalledWith('s-1')
    expect(await screen.findByText('Study hub')).toBeInTheDocument()
    expect(storage.removeItem).toHaveBeenCalledWith('study-draft:s-1:1')
    expect(storage.removeItem).toHaveBeenCalledWith(DRAFT_KEY)
  })
})
