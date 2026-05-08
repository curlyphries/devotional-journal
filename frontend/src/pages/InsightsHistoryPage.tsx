import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { format, parseISO, subDays } from 'date-fns'
import { Link } from 'react-router-dom'
import {
  Calendar, Sparkles, ExternalLink, Loader2, Search,
  PenLine, MessageCircle, Filter, X, Lightbulb, Hash, Heart,
} from 'lucide-react'
import client from '../api/client'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface DailyReflection {
  id: string
  date: string
  scripture_reference: string
  ai_insight: string
  scripture_themes: string[]
  area_scores: Record<string, number>
  reflection: string
  gratitude: string
  struggle: string
}

interface JournalEntry {
  id: string
  date: string
  decrypted_content: string
  mood_tag?: string
  focus_themes?: string[]
  plan_day_info?: {
    passages: string[] | string
    theme_en: string
    theme_es?: string
    day_number?: number
  } | null
}

interface OpenThread {
  id: string
  thread_type: string
  status: string
  summary: string
  related_life_area: string
  created_at: string
  last_mentioned_at: string
  followup_count: number
  skip_count: number
}

type Source = 'all' | 'reflection' | 'journal' | 'thread'
type DateRange = '7d' | '30d' | '90d' | 'all'

interface TimelineItem {
  id: string
  source: 'reflection' | 'journal' | 'thread'
  date: string                // YYYY-MM-DD or full ISO
  scripture?: string
  preview: string
  themes: string[]
  mood?: string
  threadType?: string
  threadStatus?: string
  lifeArea?: string
  aiInsight?: string
  href: string
  searchHaystack: string      // pre-built lower-cased text for search
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SOURCE_META: Record<TimelineItem['source'], {
  label: string
  icon: React.ReactNode
  badgeClass: string
  borderClass: string
}> = {
  reflection: {
    label: 'Reflection',
    icon: <Lightbulb className="w-4 h-4" />,
    badgeClass: 'bg-purple-500/20 text-purple-300',
    borderClass: 'hover:border-purple-500/40',
  },
  journal: {
    label: 'Journal',
    icon: <PenLine className="w-4 h-4" />,
    badgeClass: 'bg-amber-500/20 text-amber-300',
    borderClass: 'hover:border-amber-500/40',
  },
  thread: {
    label: 'Thread',
    icon: <MessageCircle className="w-4 h-4" />,
    badgeClass: 'bg-cyan-500/20 text-cyan-300',
    borderClass: 'hover:border-cyan-500/40',
  },
}

const MOODS = ['grateful', 'struggling', 'convicted', 'peaceful', 'fired_up'] as const
const DATE_RANGES: { value: DateRange; label: string }[] = [
  { value: '7d', label: 'Last 7 days' },
  { value: '30d', label: 'Last 30 days' },
  { value: '90d', label: 'Last 90 days' },
  { value: 'all', label: 'All time' },
]

// JournalPage embeds metadata as JSON inside HTML comments. Extract the
// aiInsight field and strip the block from the user-visible preview.
const META_OPEN = '<!-- DJ_META_START -->'
const META_CLOSE = '<!-- DJ_META_END -->'

function extractFromJournalContent(content: string): { preview: string; aiInsight?: string } {
  const startIdx = content.indexOf(META_OPEN)
  const endIdx = content.indexOf(META_CLOSE)
  if (startIdx === -1 || endIdx === -1 || endIdx <= startIdx) {
    return { preview: content.trim() }
  }

  const metaJson = content.slice(startIdx + META_OPEN.length, endIdx).trim()
  const userText = content.slice(endIdx + META_CLOSE.length).trim()

  let aiInsight: string | undefined
  try {
    const meta = JSON.parse(metaJson)
    aiInsight = meta.aiInsight || undefined
  } catch {
    /* malformed metadata — silently fall through */
  }

  return { preview: userText, aiInsight }
}

function preview(text: string, max = 240): string {
  const trimmed = text.trim().replace(/\s+/g, ' ')
  if (trimmed.length <= max) return trimmed
  return trimmed.slice(0, max).replace(/\s+\S*$/, '') + '…'
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

export default function InsightsHistoryPage() {
  const [source, setSource] = useState<Source>('all')
  const [dateRange, setDateRange] = useState<DateRange>('30d')
  const [search, setSearch] = useState('')
  const [moodFilter, setMoodFilter] = useState<string | null>(null)
  const [themeFilter, setThemeFilter] = useState<string | null>(null)

  // The DRF backend uses pagination for some endpoints (returns a wrapper
  // {count, next, previous, results}) and a flat array for others. Handle both.
  const unwrap = <T,>(payload: unknown): T[] => {
    if (Array.isArray(payload)) return payload as T[]
    if (payload && typeof payload === 'object' && Array.isArray((payload as { results?: unknown }).results)) {
      return (payload as { results: T[] }).results
    }
    return []
  }

  const { data: reflections = [], isLoading: rLoad } = useQuery<DailyReflection[]>({
    queryKey: ['insights-reflections'],
    queryFn: async () => unwrap<DailyReflection>((await client.get('/reflections/')).data),
  })

  const { data: journalEntries = [], isLoading: jLoad } = useQuery<JournalEntry[]>({
    queryKey: ['insights-journal'],
    queryFn: async () => unwrap<JournalEntry>((await client.get('/journal/')).data),
  })

  const { data: threads = [], isLoading: tLoad } = useQuery<OpenThread[]>({
    queryKey: ['insights-threads'],
    queryFn: async () => unwrap<OpenThread>((await client.get('/threads/active/')).data),
  })

  const isLoading = rLoad || jLoad || tLoad

  // --- Build the unified timeline ----------------------------------------
  const timeline: TimelineItem[] = useMemo(() => {
    const items: TimelineItem[] = []

    for (const r of reflections) {
      const text = r.reflection || r.struggle || r.gratitude || ''
      items.push({
        id: r.id,
        source: 'reflection',
        date: r.date,
        scripture: r.scripture_reference || undefined,
        preview: preview(text || r.ai_insight || ''),
        themes: r.scripture_themes || [],
        aiInsight: r.ai_insight || undefined,
        href: `/reflection/${r.id}`,
        searchHaystack: [
          text,
          r.scripture_reference,
          r.ai_insight,
          (r.scripture_themes || []).join(' '),
        ].filter(Boolean).join(' ').toLowerCase(),
      })
    }

    for (const e of journalEntries) {
      const { preview: userPreview, aiInsight } = extractFromJournalContent(
        e.decrypted_content || ''
      )
      const passages = e.plan_day_info?.passages
      const scriptureRef = Array.isArray(passages)
        ? passages[0]
        : (typeof passages === 'string' ? passages : undefined)
      items.push({
        id: e.id,
        source: 'journal',
        date: e.date,
        scripture: scriptureRef,
        preview: preview(userPreview),
        themes: e.focus_themes || [],
        mood: e.mood_tag || undefined,
        aiInsight,
        href: `/journal/${e.id}`,
        searchHaystack: [
          userPreview,
          scriptureRef,
          e.plan_day_info?.theme_en,
          (e.focus_themes || []).join(' '),
          e.mood_tag,
        ].filter(Boolean).join(' ').toLowerCase(),
      })
    }

    for (const t of threads) {
      items.push({
        id: t.id,
        source: 'thread',
        date: t.last_mentioned_at || t.created_at,
        preview: t.summary,
        themes: t.related_life_area ? [t.related_life_area] : [],
        threadType: t.thread_type,
        threadStatus: t.status,
        lifeArea: t.related_life_area || undefined,
        href: '/threads',
        searchHaystack: [t.summary, t.thread_type, t.related_life_area]
          .filter(Boolean).join(' ').toLowerCase(),
      })
    }

    items.sort((a, b) => (b.date || '').localeCompare(a.date || ''))
    return items
  }, [reflections, journalEntries, threads])

  // --- Compute date floor based on range ---------------------------------
  const dateFloor = useMemo(() => {
    if (dateRange === 'all') return null
    const days = dateRange === '7d' ? 7 : dateRange === '30d' ? 30 : 90
    return subDays(new Date(), days)
  }, [dateRange])

  // --- Apply filters -----------------------------------------------------
  const filteredTimeline = useMemo(() => {
    const q = search.trim().toLowerCase()
    return timeline.filter((item) => {
      if (source !== 'all' && item.source !== source) return false
      if (dateFloor) {
        try {
          if (parseISO(item.date) < dateFloor) return false
        } catch { /* skip unparseable */ }
      }
      if (moodFilter && item.source === 'journal' && item.mood !== moodFilter) return false
      if (themeFilter && !item.themes.includes(themeFilter)) return false
      if (q && !item.searchHaystack.includes(q)) return false
      return true
    })
  }, [timeline, source, dateFloor, moodFilter, themeFilter, search])

  // --- Stats (computed over the date-range slice, ignoring source/search) ---
  const stats = useMemo(() => {
    const inRange = timeline.filter((item) => {
      if (!dateFloor) return true
      try { return parseISO(item.date) >= dateFloor } catch { return true }
    })

    const journalInRange = inRange.filter((i) => i.source === 'journal')
    const reflectionInRange = inRange.filter((i) => i.source === 'reflection')
    const threadInRange = inRange.filter((i) => i.source === 'thread')

    const moodCounts: Record<string, number> = {}
    for (const i of journalInRange) {
      if (i.mood) moodCounts[i.mood] = (moodCounts[i.mood] || 0) + 1
    }
    const topMood = Object.entries(moodCounts).sort((a, b) => b[1] - a[1])[0]?.[0]

    const themeCounts: Record<string, number> = {}
    for (const i of inRange) {
      for (const th of i.themes) themeCounts[th] = (themeCounts[th] || 0) + 1
    }
    const topThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([t]) => t)

    return {
      journalCount: journalInRange.length,
      reflectionCount: reflectionInRange.length,
      threadCount: threadInRange.length,
      topMood,
      topThemes,
    }
  }, [timeline, dateFloor])

  // Available themes for the chip filter
  const availableThemes = stats.topThemes
  const availableMoods = useMemo(() => {
    const set = new Set<string>()
    timeline.forEach((i) => i.mood && set.add(i.mood))
    return MOODS.filter((m) => set.has(m))
  }, [timeline])

  const hasActiveFilters = source !== 'all' || dateRange !== '30d' || !!search || !!moodFilter || !!themeFilter
  const clearFilters = () => {
    setSource('all'); setDateRange('30d'); setSearch('')
    setMoodFilter(null); setThemeFilter(null)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-text-primary flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-amber-500" aria-hidden="true" />
          Insights
        </h1>
        <p className="text-sm text-text-secondary mt-1">
          Your reflections, journal entries, and open threads — searchable, filterable, in one place.
        </p>
      </div>

      {/* Stats strip */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <StatCard icon={<Lightbulb className="w-4 h-4" />} label="Reflections"
          value={stats.reflectionCount} accent="purple" />
        <StatCard icon={<PenLine className="w-4 h-4" />} label="Journal entries"
          value={stats.journalCount} accent="amber" />
        <StatCard icon={<MessageCircle className="w-4 h-4" />} label="Open threads"
          value={stats.threadCount} accent="cyan" />
        <StatCard icon={<Heart className="w-4 h-4" />} label="Top mood"
          value={stats.topMood ? prettyMood(stats.topMood) : '—'} accent="pink" />
        <StatCard icon={<Hash className="w-4 h-4" />} label="Top theme"
          value={stats.topThemes[0] || '—'} accent="green" />
      </div>

      {/* Filters */}
      <div className="card space-y-3">
        {/* Search */}
        <div className="relative">
          <Search className="w-4 h-4 text-text-secondary absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" aria-hidden="true" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search reflections, entries, scripture refs, themes…"
            className="w-full pl-10 pr-10 py-2 bg-bg-elevated border border-border rounded-lg text-text-primary placeholder:text-text-secondary focus:outline-none focus:ring-2 focus:ring-amber-500/40"
          />
          {search && (
            <button
              onClick={() => setSearch('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary"
              aria-label="Clear search"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Source + date range chips */}
        <div className="flex flex-wrap items-center gap-2">
          <FilterGroup label="Source">
            {(['all', 'reflection', 'journal', 'thread'] as const).map((s) => (
              <Chip key={s} active={source === s} onClick={() => setSource(s)}>
                {s === 'all' ? 'All' : SOURCE_META[s].label + 's'}
              </Chip>
            ))}
          </FilterGroup>

          <div className="hidden md:block w-px h-6 bg-border mx-1" aria-hidden="true" />

          <FilterGroup label="Date">
            {DATE_RANGES.map((r) => (
              <Chip key={r.value} active={dateRange === r.value} onClick={() => setDateRange(r.value)}>
                {r.label}
              </Chip>
            ))}
          </FilterGroup>
        </div>

        {/* Mood + theme refinements (only when relevant) */}
        {(availableMoods.length > 0 || availableThemes.length > 0) && (
          <div className="flex flex-wrap items-center gap-2">
            {availableMoods.length > 0 && (
              <FilterGroup label="Mood">
                <Chip active={moodFilter === null} onClick={() => setMoodFilter(null)}>Any</Chip>
                {availableMoods.map((m) => (
                  <Chip key={m} active={moodFilter === m} onClick={() => setMoodFilter(m)}>
                    {prettyMood(m)}
                  </Chip>
                ))}
              </FilterGroup>
            )}
            {availableThemes.length > 0 && (
              <FilterGroup label="Theme">
                <Chip active={themeFilter === null} onClick={() => setThemeFilter(null)}>Any</Chip>
                {availableThemes.map((th) => (
                  <Chip key={th} active={themeFilter === th} onClick={() => setThemeFilter(th)}>
                    {th}
                  </Chip>
                ))}
              </FilterGroup>
            )}
          </div>
        )}

        {hasActiveFilters && (
          <div className="flex justify-end">
            <button
              onClick={clearFilters}
              className="text-sm text-text-secondary hover:text-text-primary inline-flex items-center gap-1"
            >
              <X className="w-3.5 h-3.5" /> Clear filters
            </button>
          </div>
        )}
      </div>

      {/* Timeline */}
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-amber-500 animate-spin" />
        </div>
      ) : filteredTimeline.length === 0 ? (
        <div className="card text-center py-12">
          <Sparkles className="w-12 h-12 text-gray-500 mx-auto mb-4" aria-hidden="true" />
          <p className="text-text-secondary">
            {hasActiveFilters
              ? 'No matches for the current filters.'
              : 'Nothing here yet — write your first journal entry or reflection to start building your insights.'}
          </p>
          {hasActiveFilters && (
            <button onClick={clearFilters} className="mt-4 text-amber-400 hover:text-amber-300 text-sm">
              Clear filters
            </button>
          )}
          {!hasActiveFilters && (
            <div className="mt-4 flex items-center justify-center gap-3">
              <Link to="/journal/new" className="text-amber-400 hover:text-amber-300 text-sm">Write a journal entry →</Link>
              <Link to="/reflection" className="text-purple-400 hover:text-purple-300 text-sm">Start a reflection →</Link>
            </div>
          )}
        </div>
      ) : (
        <ol className="space-y-3" aria-label="Insights timeline">
          {filteredTimeline.map((item) => (
            <TimelineCard key={`${item.source}-${item.id}`} item={item} />
          ))}
        </ol>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function StatCard({ icon, label, value, accent }: {
  icon: React.ReactNode
  label: string
  value: string | number
  accent: 'purple' | 'amber' | 'cyan' | 'pink' | 'green'
}) {
  const accentMap: Record<string, string> = {
    purple: 'text-purple-400',
    amber: 'text-amber-400',
    cyan: 'text-cyan-400',
    pink: 'text-pink-400',
    green: 'text-green-400',
  }
  return (
    <div className="card p-3">
      <div className={`flex items-center gap-2 text-xs font-medium ${accentMap[accent]} mb-1`}>
        {icon}
        <span className="uppercase tracking-wide">{label}</span>
      </div>
      <div className="text-xl font-bold text-text-primary truncate" title={String(value)}>
        {value}
      </div>
    </div>
  )
}

function FilterGroup({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-1.5 flex-wrap">
      <span className="text-xs uppercase tracking-wide text-text-secondary mr-1 inline-flex items-center gap-1">
        <Filter className="w-3 h-3" aria-hidden="true" /> {label}
      </span>
      {children}
    </div>
  )
}

function Chip({ active, onClick, children }: {
  active: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      onClick={onClick}
      className={`px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
        active
          ? 'bg-amber-500 text-black'
          : 'bg-bg-elevated text-text-secondary hover:text-text-primary border border-border'
      }`}
    >
      {children}
    </button>
  )
}

function TimelineCard({ item }: { item: TimelineItem }) {
  const meta = SOURCE_META[item.source]
  let dateLabel = item.date
  try { dateLabel = format(parseISO(item.date), 'MMM d, yyyy') } catch { /* keep raw */ }

  return (
    <li className={`card transition-colors ${meta.borderClass}`}>
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="flex items-center gap-2 flex-wrap">
          <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${meta.badgeClass}`}>
            {meta.icon}
            {meta.label}
          </span>
          <span className="text-sm text-text-secondary">
            <Calendar className="w-3.5 h-3.5 inline mr-1" aria-hidden="true" />
            {dateLabel}
          </span>
          {item.scripture && (
            <Link
              to={`/bible?passage=${encodeURIComponent(item.scripture)}`}
              className="text-amber-400 hover:text-amber-300 text-sm inline-flex items-center gap-1"
            >
              {item.scripture}
              <ExternalLink className="w-3 h-3" aria-hidden="true" />
            </Link>
          )}
        </div>
        {item.threadStatus && (
          <span className="text-xs px-2 py-0.5 rounded-full bg-bg-elevated text-text-secondary">
            {item.threadStatus.replace(/_/g, ' ')}
          </span>
        )}
      </div>

      {/* Tags */}
      {(item.mood || item.themes.length > 0 || item.threadType) && (
        <div className="flex flex-wrap gap-1 mb-2">
          {item.mood && (
            <Tag color="pink">{prettyMood(item.mood)}</Tag>
          )}
          {item.threadType && (
            <Tag color="cyan">{item.threadType}</Tag>
          )}
          {item.themes.slice(0, 4).map((t) => (
            <Tag key={t} color="purple">{t}</Tag>
          ))}
        </div>
      )}

      {/* Preview */}
      {item.preview && (
        <p className="text-text-primary text-sm leading-relaxed whitespace-pre-wrap">
          {item.preview}
        </p>
      )}

      {/* AI insight */}
      {item.aiInsight && (
        <div className="mt-3 p-3 bg-bg-elevated/60 rounded-lg border border-amber-500/20">
          <div className="flex items-center gap-2 mb-1">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" aria-hidden="true" />
            <span className="text-xs font-medium text-amber-400 uppercase tracking-wide">
              AI Insight
            </span>
          </div>
          <div className="text-text-secondary text-xs whitespace-pre-wrap leading-relaxed line-clamp-4">
            {item.aiInsight}
          </div>
        </div>
      )}

      {/* Footer link */}
      <div className="mt-3">
        <Link
          to={item.href}
          className="text-sm text-text-secondary hover:text-text-primary inline-flex items-center gap-1"
        >
          {item.source === 'thread' ? 'Manage in Threads' : 'Open full entry'}
          <ExternalLink className="w-3.5 h-3.5" aria-hidden="true" />
        </Link>
      </div>
    </li>
  )
}

function Tag({ color, children }: { color: 'pink' | 'purple' | 'cyan'; children: React.ReactNode }) {
  const map = {
    pink: 'bg-pink-500/15 text-pink-300',
    purple: 'bg-purple-500/15 text-purple-300',
    cyan: 'bg-cyan-500/15 text-cyan-300',
  } as const
  return <span className={`text-xs px-2 py-0.5 rounded ${map[color]}`}>{children}</span>
}

function prettyMood(mood: string): string {
  switch (mood) {
    case 'grateful': return 'Grateful'
    case 'struggling': return 'Struggling'
    case 'convicted': return 'Convicted'
    case 'peaceful': return 'Peaceful'
    case 'fired_up': return 'Fired Up'
    default: return mood
  }
}

