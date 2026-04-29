import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { format } from 'date-fns'
import { Link } from 'react-router-dom'
import { 
  BookOpen, 
  Calendar, 
  ChevronLeft,
  Sparkles,
  ExternalLink,
  Loader2,
  Filter
} from 'lucide-react'
import client from '../api/client'

interface DailyReflection {
  id: string
  date: string
  scripture_reference: string
  ai_insight: string
  scripture_themes: string[]
  area_scores: Record<string, number>
}

interface JournalEntry {
  id: string
  date: string
  plan_day?: {
    passages: string
    theme_en: string
  }
  decrypted_content: string
}

const fetchReflections = async (): Promise<DailyReflection[]> => {
  const response = await client.get('/reflections/')
  return response.data
}

const fetchJournalEntries = async (): Promise<JournalEntry[]> => {
  const response = await client.get('/journal/')
  return response.data
}

export default function InsightsHistoryPage() {
  const [viewMode, setViewMode] = useState<'reflections' | 'journal'>('reflections')
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null)

  const { data: reflections = [], isLoading: reflectionsLoading } = useQuery({
    queryKey: ['reflections-history'],
    queryFn: fetchReflections,
    enabled: viewMode === 'reflections'
  })

  const { data: journalEntries = [], isLoading: journalLoading } = useQuery({
    queryKey: ['journal-history'],
    queryFn: fetchJournalEntries,
    enabled: viewMode === 'journal'
  })

  // Extract AI insights from journal entries
  const journalInsights = journalEntries
    .map(entry => {
      const content = entry.decrypted_content || ''
      const aiInsightMatch = content.match(/<!-- AI_INSIGHT_START -->([\s\S]*?)<!-- AI_INSIGHT_END -->/)
      return {
        ...entry,
        ai_insight: aiInsightMatch ? aiInsightMatch[1].trim() : null
      }
    })
    .filter(entry => entry.ai_insight)

  // Get all unique themes
  const allThemes = Array.from(
    new Set(
      reflections.flatMap(r => r.scripture_themes || [])
    )
  ).sort()

  // Filter reflections by theme
  const filteredReflections = selectedTheme
    ? reflections.filter(r => r.scripture_themes?.includes(selectedTheme))
    : reflections

  const isLoading = reflectionsLoading || journalLoading

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            to="/dashboard"
            className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
            Back
          </Link>
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-amber-500" />
            <h1 className="text-2xl font-bold text-text-primary">Devotional Insights History</h1>
          </div>
        </div>
      </div>

      {/* View Mode Toggle */}
      <div className="flex gap-2">
        <button
          onClick={() => setViewMode('reflections')}
          className={`px-4 py-2 rounded-lg transition-colors ${
            viewMode === 'reflections'
              ? 'bg-purple-500 text-white'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            Daily Reflections
          </div>
        </button>
        <button
          onClick={() => setViewMode('journal')}
          className={`px-4 py-2 rounded-lg transition-colors ${
            viewMode === 'journal'
              ? 'bg-amber-500 text-white'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            Journal Insights
          </div>
        </button>
      </div>

      {/* Theme Filter */}
      {viewMode === 'reflections' && allThemes.length > 0 && (
        <div className="card">
          <div className="flex items-center gap-2 mb-3">
            <Filter className="w-4 h-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-400">Filter by Theme</span>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedTheme(null)}
              className={`px-3 py-1 rounded-full text-sm transition-colors ${
                selectedTheme === null
                  ? 'bg-purple-500 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              All
            </button>
            {allThemes.map(theme => (
              <button
                key={theme}
                onClick={() => setSelectedTheme(theme)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  selectedTheme === theme
                    ? 'bg-purple-500 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {theme}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-amber-500 animate-spin" />
        </div>
      )}

      {/* Reflections View */}
      {viewMode === 'reflections' && !isLoading && (
        <div className="space-y-4">
          {filteredReflections.length === 0 ? (
            <div className="card text-center py-12">
              <Sparkles className="w-12 h-12 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400">No devotional insights yet</p>
              <p className="text-sm text-gray-500 mt-2">
                Complete daily reflections to build your insights history
              </p>
            </div>
          ) : (
            filteredReflections.map(reflection => (
              <div key={reflection.id} className="card hover:border-purple-500/30 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                      <BookOpen className="w-5 h-5 text-purple-400" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">
                        {format(new Date(reflection.date), 'MMMM d, yyyy')}
                      </p>
                      {reflection.scripture_reference && (
                        <Link
                          to={`/bible?passage=${encodeURIComponent(reflection.scripture_reference)}`}
                          className="text-amber-400 hover:text-amber-300 font-medium flex items-center gap-1"
                        >
                          {reflection.scripture_reference}
                          <ExternalLink className="w-3 h-3" />
                        </Link>
                      )}
                    </div>
                  </div>
                  {reflection.scripture_themes && reflection.scripture_themes.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {reflection.scripture_themes.slice(0, 3).map(theme => (
                        <span
                          key={theme}
                          className="px-2 py-0.5 bg-purple-500/20 text-purple-300 text-xs rounded"
                        >
                          {theme}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {reflection.ai_insight && (
                  <div className="mt-4 p-4 bg-gray-800/50 rounded-lg border border-purple-500/20">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles className="w-4 h-4 text-amber-400" />
                      <span className="text-sm font-medium text-amber-400">AI Insight</span>
                    </div>
                    <div className="text-gray-300 text-sm whitespace-pre-wrap leading-relaxed">
                      {reflection.ai_insight}
                    </div>
                  </div>
                )}

                <Link
                  to={`/reflection/${reflection.id}`}
                  className="mt-4 text-purple-400 hover:text-purple-300 text-sm flex items-center gap-1"
                >
                  View full reflection
                  <ChevronLeft className="w-4 h-4 rotate-180" />
                </Link>
              </div>
            ))
          )}
        </div>
      )}

      {/* Journal Insights View */}
      {viewMode === 'journal' && !isLoading && (
        <div className="space-y-4">
          {journalInsights.length === 0 ? (
            <div className="card text-center py-12">
              <Sparkles className="w-12 h-12 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400">No journal insights yet</p>
              <p className="text-sm text-gray-500 mt-2">
                Journal entries with AI-generated insights will appear here
              </p>
            </div>
          ) : (
            journalInsights.map(entry => (
              <div key={entry.id} className="card hover:border-amber-500/30 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-amber-500/20 rounded-lg flex items-center justify-center">
                      <Calendar className="w-5 h-5 text-amber-400" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">
                        {format(new Date(entry.date), 'MMMM d, yyyy')}
                      </p>
                      {entry.plan_day?.passages && (
                        <Link
                          to={`/bible?passage=${encodeURIComponent(entry.plan_day.passages)}`}
                          className="text-amber-400 hover:text-amber-300 font-medium flex items-center gap-1"
                        >
                          {entry.plan_day.passages}
                          <ExternalLink className="w-3 h-3" />
                        </Link>
                      )}
                    </div>
                  </div>
                  {entry.plan_day?.theme_en && (
                    <span className="px-2 py-0.5 bg-amber-500/20 text-amber-300 text-xs rounded">
                      {entry.plan_day.theme_en}
                    </span>
                  )}
                </div>

                {entry.ai_insight && (
                  <div className="mt-4 p-4 bg-gray-800/50 rounded-lg border border-amber-500/20">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles className="w-4 h-4 text-amber-400" />
                      <span className="text-sm font-medium text-amber-400">Devotional Insight</span>
                    </div>
                    <div className="text-gray-300 text-sm whitespace-pre-wrap leading-relaxed">
                      {entry.ai_insight}
                    </div>
                  </div>
                )}

                <Link
                  to={`/journal/${entry.id}`}
                  className="mt-4 text-amber-400 hover:text-amber-300 text-sm flex items-center gap-1"
                >
                  View journal entry
                  <ChevronLeft className="w-4 h-4 rotate-180" />
                </Link>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}
