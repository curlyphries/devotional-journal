/** Shared fixtures for the profile and growth-plan page tests. */
import type { Catalog, TopicCard } from '../../api/guides'
import type { GrowthPlan } from '../../api/growthPlans'
import type { GrowthProfile } from '../../api/profile'

export function makeTopic(overrides: Partial<TopicCard> = {}): TopicCard {
  return {
    key: 'anxiety',
    category: 'peace',
    title: 'Anxiety',
    summary: 'When worry will not let go.',
    lesson_count: 5,
    stages: ['adult'],
    traits: ['patience'],
    sensitive: false,
    stage_note: null,
    enrollment: null,
    ...overrides,
  }
}

export const catalog: Catalog = {
  life_stages: [
    { key: 'child', title: 'Child', note: 'Read together with a grown-up.' },
    { key: 'teen', title: 'Teen', note: 'School, friends and questions.' },
    { key: 'young_adult', title: 'Young adult', note: 'Starting out.' },
    { key: 'adult', title: 'Adult', note: 'Work, family and responsibility.' },
    { key: 'senior', title: 'Senior', note: 'Later seasons of life.' },
  ],
  situations: [
    { key: 'parent', title: 'Parent' },
    { key: 'student', title: 'Student' },
    { key: 'caregiver', title: 'Caregiver' },
  ],
  faith_backgrounds: [
    { key: 'new', title: 'New to faith' },
    { key: 'lifelong', title: 'Lifelong believer' },
  ],
  categories: [
    {
      key: 'peace',
      title: 'Peace and refuge',
      summary: 'For anxious days.',
      topics: [makeTopic(), makeTopic({ key: 'grief', title: 'Grief', sensitive: true })],
    },
    {
      key: 'foundations',
      title: 'Foundations',
      summary: 'The basics.',
      topics: [makeTopic({ key: 'prayer_basics', category: 'foundations', title: 'Learning to pray' })],
    },
  ],
  traits: [
    { key: 'patience', title: 'Patience', definition: 'Staying steady when things are slow or hard.' },
    { key: 'kindness', title: 'Kindness', definition: 'Doing good to others without being asked.' },
    { key: 'humility', title: 'Humility', definition: 'Seeing yourself truthfully before God.' },
    { key: 'courage', title: 'Courage', definition: 'Doing what is right when it costs you.' },
    { key: 'gratitude', title: 'Gratitude', definition: 'Noticing and giving thanks for what you have been given.' },
    { key: 'self_control', title: 'Self-control', definition: 'Choosing what is good over what is easy.' },
  ],
  assessment: {
    scale: '1 = not at all true of me, 5 = very true of me',
    items: [
      { key: 'prayer', area: 'practices', text: 'I pray most days.' },
      { key: 'scripture', area: 'practices', text: 'I read the Bible regularly.' },
      { key: 'peace', area: 'inner', text: 'I feel at peace most days.' },
    ],
  },
}

export const DISCLAIMER = 'This is a reflection to help you think, not a diagnosis.'

export function makeProfile(overrides: Partial<GrowthProfile> = {}): GrowthProfile {
  return {
    exists: false,
    life_stage: null,
    situations: [],
    faith_background: null,
    needs: [],
    desired_traits: [],
    about_me: '',
    profiling_enabled: true,
    assessment: null,
    spiritual: {
      practices: [
        { key: 'prayer', label: 'Prayer', score: null },
        { key: 'scripture', label: 'Bible reading', score: null },
      ],
      strengths: [],
      growth_areas: [],
      studies_completed: 0,
      lessons_completed: 0,
      entries_with_feedback: 0,
      top_themes: [],
    },
    inner_life: {
      items: [{ key: 'peace', label: 'Peace', score: null }],
      mood_counts: {},
      recurring_themes: [],
      understanding_avg: null,
      resonance_avg: null,
      open_threads: 0,
    },
    insights: null,
    support: null,
    disclaimer: DISCLAIMER,
    ...overrides,
  }
}

export function makeFullProfile(overrides: Partial<GrowthProfile> = {}): GrowthProfile {
  return makeProfile({
    exists: true,
    life_stage: 'adult',
    situations: ['parent'],
    faith_background: 'new',
    needs: ['anxiety'],
    desired_traits: ['patience'],
    about_me: 'I work nights.',
    assessment: {
      taken_at: '2026-11-10T09:00:00Z',
      answers: { prayer: 4, peace: 2 },
      trait_ratings: { patience: 2, kindness: 4 },
      history: [
        { taken_at: '2026-10-01T09:00:00Z', practices_avg: 3, inner_avg: null },
        { taken_at: '2026-11-10T09:00:00Z', practices_avg: 4, inner_avg: 2.5 },
      ],
    },
    spiritual: {
      practices: [
        { key: 'prayer', label: 'Prayer', score: 4 },
        { key: 'scripture', label: 'Bible reading', score: null },
      ],
      strengths: [{ trait: 'kindness', title: 'Kindness', score: 4 }],
      growth_areas: [{ trait: 'patience', title: 'Patience', score: 2 }],
      studies_completed: 1,
      lessons_completed: 7,
      entries_with_feedback: 12,
      top_themes: [{ theme: 'trust', count: 5 }],
    },
    inner_life: {
      items: [{ key: 'peace', label: 'Peace', score: 2 }],
      mood_counts: { grateful: 6, struggling: 3 },
      recurring_themes: [{ theme: 'work stress', count: 4 }],
      understanding_avg: 4.2,
      resonance_avg: 3.5,
      open_threads: 2,
    },
    insights: {
      generated_at: '2026-11-11T10:00:00Z',
      provider: 'ollama',
      model: 'llama3.1:8b',
      local: true,
      summary: 'You are showing up steadily, even in a tiring season.',
      items: [
        {
          id: 'i1',
          area: 'spiritual',
          title: 'Prayer is a steady habit',
          text: 'You pray most days.',
          evidence: ['You rated “I pray most days” 4 of 5.'],
          accurate: null,
        },
        {
          id: 'i2',
          area: 'inner',
          title: 'Work weighs on you',
          text: 'Work stress keeps coming up.',
          evidence: ['“work stress” appears in 4 recent entries.'],
          accurate: null,
        },
      ],
      encouragement: 'Keep going gently.',
      suggested_topics: [makeTopic()],
      suggested_traits: [{ key: 'patience', title: 'Patience' }],
    },
    ...overrides,
  })
}

export function makePlan(overrides: Partial<GrowthPlan> = {}): GrowthPlan {
  return {
    id: 'p1',
    trait: { key: 'patience', title: 'Patience', definition: 'Staying steady when things are slow or hard.' },
    why: 'I snap at my kids when I am tired.',
    status: 'active',
    started_at: '2026-11-01',
    target_date: '2027-01-30',
    baseline_rating: 2,
    current_rating: 3,
    scripture: [{ reference: 'James 1:2-4' }, { reference: 'Galatians 5:22-23' }],
    jesus: { reference: 'Mark 10:13-16', note: 'He made time for the children when others were in a hurry.' },
    check_in_question: 'When were you patient this week, and when were you not?',
    topics: [makeTopic({ enrollment: { id: 's1', status: 'active', current_lesson: 2, completed_lessons: [1] } })],
    goals: [
      {
        id: 'g1',
        horizon: 'short',
        title: 'Pause and breathe before answering',
        kind: 'practice',
        target_count: 5,
        progress_count: 2,
        percent: 40,
        due_date: '2026-11-20',
        status: 'active',
        overdue: false,
        auto: false,
      },
      {
        id: 'g2',
        horizon: 'short',
        title: 'Complete two lessons on patience',
        kind: 'study',
        target_count: 2,
        progress_count: 1,
        percent: 50,
        due_date: '2026-11-25',
        status: 'active',
        overdue: false,
        auto: true,
      },
      {
        id: 'g3',
        horizon: 'long',
        title: 'Finish the patience study',
        kind: 'study',
        target_count: 1,
        progress_count: 0,
        percent: 0,
        due_date: '2027-01-30',
        status: 'active',
        overdue: false,
        auto: true,
      },
      {
        id: 'g4',
        horizon: 'long',
        title: 'Pray for patience each morning',
        kind: 'prayer',
        target_count: 30,
        progress_count: 30,
        percent: 100,
        due_date: '2026-12-30',
        status: 'done',
        overdue: false,
        auto: false,
      },
    ],
    checkins: [{ id: 'c1', date: '2026-11-08', rating: 3, note: 'Better at bedtime.' }],
    goal_source: 'catalog',
    personalize_error: null,
    progress: {
      percent: 35,
      stage: 'building',
      stage_label: 'Building the habit',
      short_percent: 45,
      long_percent: 50,
      goals_done: 1,
      goals_total: 4,
      rating_change: 1,
      days_in: 12,
      days_total: 90,
      lessons_done: 1,
      check_in_due: true,
      summary: 'You are twelve days in and practising regularly.',
    },
    ...overrides,
  }
}
