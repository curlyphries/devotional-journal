import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { renderWithApp } from '../test/renderWithApp'
import PlansPage from './PlansPage'
import * as plansApi from '../api/plans'
import * as promptsApi from '../api/prompts'
import type { PlanCategoryGroup, ReadingPlan } from '../api/plans'

vi.mock('../api/plans', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/plans')>()
  return {
    ...actual,
    getPlans: vi.fn(),
    getEnrolledPlans: vi.fn(),
    getPlanCategories: vi.fn(),
  }
})
vi.mock('../api/prompts', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/prompts')>()
  return { ...actual, getAiStatus: vi.fn() }
})
// The Bible reader is not under test here and pulls in a great deal.
vi.mock('../components/ScriptureReader', () => ({ default: () => null }))

const api = vi.mocked(plansApi)
const prompts = vi.mocked(promptsApi)

const groups: PlanCategoryGroup[] = [
  {
    key: 'faith',
    title: 'Faith',
    categories: [
      { value: 'general', label: 'General', plan_count: 2 },
      { value: 'prayer', label: 'Prayer', plan_count: 0 },
    ],
  },
  {
    key: 'heart',
    title: 'Heart and Mind',
    categories: [
      { value: 'grief', label: 'Grief and Loss', plan_count: 1 },
      { value: 'anxiety', label: 'Anxiety and Peace', plan_count: 0 },
    ],
  },
  {
    key: 'relationships',
    title: 'Relationships and Family',
    categories: [{ value: 'motherhood', label: 'Motherhood', plan_count: 0 }],
  },
]

const plan = (overrides: Partial<ReadingPlan> = {}): ReadingPlan => ({
  id: 'p-1',
  title: 'Walking through loss',
  description: 'Seven days in the Psalms.',
  duration_days: 7,
  category: 'grief',
  category_label: 'Grief and Loss',
  is_premium: false,
  is_public: true,
  is_owned: false,
  ...overrides,
})

beforeEach(() => {
  vi.clearAllMocks()
  api.getPlans.mockResolvedValue([plan()])
  api.getEnrolledPlans.mockResolvedValue([])
  api.getPlanCategories.mockResolvedValue(groups)
  prompts.getAiStatus.mockResolvedValue({
    backend: 'ollama', model: 'm', reachable: true, configured: true, source: 'server',
    local: true, consent_required: false, code: null, suggestion: null,
  } as Awaited<ReturnType<typeof promptsApi.getAiStatus>>)
})

describe('PlansPage categories', () => {
  it('offers filters for categories that have plans, with counts, and says how many more exist', async () => {
    renderWithApp(<PlansPage />, { route: '/plans' })

    const filter = await screen.findByRole('group', { name: 'Filter plans by category' })
    await within(filter).findByRole('button', { name: 'Grief and Loss (1)' })
    expect(within(filter).getAllByRole('button').map((b) => b.textContent)).toEqual([
      'All Plans',
      'My Plans',
      'General (2)',
      'Grief and Loss (1)',
    ])
    // Empty categories are not dead-end filters, but the person is told they exist.
    expect(screen.getByText(/3 more categories have no plans yet/)).toBeInTheDocument()
  })

  it('filters by a category and shows its readable name on the plan', async () => {
    const user = userEvent.setup()
    renderWithApp(<PlansPage />, { route: '/plans' })

    await user.click(await screen.findByRole('button', { name: 'Grief and Loss (1)' }))

    await waitFor(() => expect(api.getPlans).toHaveBeenLastCalledWith('grief'))
    expect(screen.getByRole('button', { name: 'Grief and Loss (1)' })).toHaveAttribute('aria-pressed', 'true')
    expect(await screen.findByText('Walking through loss')).toBeInTheDocument()
    expect(screen.getByText('Grief and Loss')).toBeInTheDocument()
  })

  it('opens with the category named in the address, even one with no plans yet', async () => {
    api.getPlans.mockResolvedValue([])
    renderWithApp(<PlansPage />, { route: '/plans?category=motherhood' })

    await waitFor(() => expect(api.getPlans).toHaveBeenCalledWith('motherhood'))
    expect(await screen.findByRole('button', { name: 'Motherhood (0)' })).toHaveAttribute('aria-pressed', 'true')
  })

  it('still lists plans when the category list cannot be loaded', async () => {
    api.getPlanCategories.mockRejectedValue(new Error('offline'))
    renderWithApp(<PlansPage />, { route: '/plans' })

    expect(await screen.findByText('Walking through loss')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'All Plans' })).toBeInTheDocument()
    expect(screen.getByText('Grief and Loss')).toBeInTheDocument() // from the plan itself
  })

  it('the plan builder lists every category, grouped', async () => {
    const user = userEvent.setup()
    renderWithApp(<PlansPage />, { route: '/plans' })

    await user.click((await screen.findAllByRole('button', { name: /Build a Plan/ }))[0])
    const select = await screen.findByLabelText('Category')

    await waitFor(() => expect(within(select).getAllByRole('option')).toHaveLength(5))
    expect(within(select).getAllByRole('group').map((g) => g.getAttribute('label'))).toEqual([
      'Faith',
      'Heart and Mind',
      'Relationships and Family',
    ])
    await user.selectOptions(select, 'motherhood')
    expect((select as HTMLSelectElement).value).toBe('motherhood')
  })

  it('the builder falls back to General and says so when the list cannot be loaded', async () => {
    api.getPlanCategories.mockRejectedValue(new Error('offline'))
    const user = userEvent.setup()
    renderWithApp(<PlansPage />, { route: '/plans' })

    await user.click((await screen.findAllByRole('button', { name: /Build a Plan/ }))[0])
    const select = await screen.findByLabelText('Category')

    expect(await screen.findByText(/full category list could not be loaded/)).toBeInTheDocument()
    expect(within(select).getAllByRole('option').map((o) => o.textContent)).toEqual(['General'])
  })
})
