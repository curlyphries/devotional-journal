import { ChangeEvent, useMemo, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Archive, BookOpen, CheckCircle2, Loader2, PlayCircle, Sparkles } from 'lucide-react'
import { getPassage, parsePassageReference } from '../api/bible'
import {
  getStudySessionSummary,
  getStudySessions,
  markStudySessionDay,
  archiveStudySession,
  resumeStudySession,
  StudyGuideSession,
  StudySessionStatus,
} from '../api/study'

type SessionFilter = 'all' | StudySessionStatus

type ParsedStudyReference = {
  book: string
  chapter: number
  verseStart?: number
  verseEnd?: number
  translation: string
}

function formatDate(value: string) {
  return new Date(value).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

function parseStudyReference(reference: string): ParsedStudyReference | null {
  const trimmed = reference.trim()
  if (!trimmed) return null

  const translationMatch = trimmed.match(/\(([^)]+)\)\s*$/)
  const translation = translationMatch?.[1]?.trim().toUpperCase() || 'KJV'
  const withoutTranslation = trimmed.replace(/\([^)]+\)\s*$/, '').trim()

  const basicParsed = parsePassageReference(withoutTranslation)
  if (basicParsed) {
    return {
      ...basicParsed,
      translation,
    }
  }

  const multiWordMatch = withoutTranslation.match(/^((?:\d\s+)?[A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(\d+)(?::(\d+)(?:-(\d+))?)?$/)
  if (!multiWordMatch) return null

  return {
    book: multiWordMatch[1].trim(),
    chapter: parseInt(multiWordMatch[2], 10),
    verseStart: multiWordMatch[3] ? parseInt(multiWordMatch[3], 10) : undefined,
    verseEnd: multiWordMatch[4] ? parseInt(multiWordMatch[4], 10) : undefined,
    translation,
  }
}

function StudyDayScriptureQuote({ scripture }: { scripture: string }) {
  const parsed = useMemo(() => parseStudyReference(scripture), [scripture])

  const { data, isLoading, isError } = useQuery({
    queryKey: ['studyScriptureQuote', scripture],
    queryFn: async () => {
      if (!parsed) return null

      try {
        return await getPassage(
          parsed.book,
          parsed.chapter,
          parsed.translation,
          parsed.verseStart,
          parsed.verseEnd
        )
      } catch {
        if (parsed.translation !== 'KJV') {
          return getPassage(
            parsed.book,
            parsed.chapter,
            'KJV',
            parsed.verseStart,
            parsed.verseEnd
          )
        }
        throw new Error('Unable to load scripture quote')
      }
    },
    enabled: !!parsed,
    staleTime: 60 * 60 * 1000,
  })

  if (!parsed) {
    return <p className="text-xs text-gray-500 mt-2">Could not parse scripture reference automatically.</p>
  }

  if (isLoading) {
    return <p className="text-xs text-gray-500 mt-2">Loading scripture quote...</p>
  }

  if (isError || !data?.full_text) {
    return <p className="text-xs text-gray-500 mt-2">Scripture text unavailable right now.</p>
  }

  const quoteText = data.full_text.length > 340 ? `${data.full_text.slice(0, 340)}...` : data.full_text

  return (
    <blockquote className="mt-2 p-3 bg-gray-900/60 border border-gray-700 rounded-md text-sm text-gray-300 italic leading-relaxed">
      "{quoteText}"
    </blockquote>
  )
}

export default function StudyTracker() {
  const queryClient = useQueryClient()
  const [filter, setFilter] = useState<SessionFilter>('all')
  const [expandedSessionId, setExpandedSessionId] = useState<string | null>(null)
  const [noteDrafts, setNoteDrafts] = useState<Record<string, string>>({})

  const { data: summary, isLoading: isSummaryLoading } = useQuery({
    queryKey: ['studySessionSummary'],
    queryFn: getStudySessionSummary,
    staleTime: 60000,
  })

  const { data: sessions = [], isLoading: isSessionsLoading } = useQuery({
    queryKey: ['studySessions', filter],
    queryFn: () => getStudySessions(filter === 'all' ? undefined : filter),
  })

  const markDayMutation = useMutation({
    mutationFn: ({ sessionId, day, completed, note }: { sessionId: string; day: number; completed: boolean; note?: string }) =>
      markStudySessionDay(sessionId, { day, completed, note }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['studySessions'] })
      queryClient.invalidateQueries({ queryKey: ['studySessionSummary'] })
    },
  })

  const archiveMutation = useMutation({
    mutationFn: (sessionId: string) => archiveStudySession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['studySessions'] })
      queryClient.invalidateQueries({ queryKey: ['studySessionSummary'] })
    },
  })

  const resumeMutation = useMutation({
    mutationFn: (sessionId: string) => resumeStudySession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['studySessions'] })
      queryClient.invalidateQueries({ queryKey: ['studySessionSummary'] })
    },
  })

  const stats = useMemo(() => {
    return {
      total: summary?.total_sessions ?? 0,
      active: summary?.active_sessions ?? 0,
      completed: summary?.completed_sessions ?? 0,
      avg: summary?.average_progress_percentage ?? 0,
    }
  }, [summary])

  if (isSummaryLoading || isSessionsLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-6 h-6 text-amber-500 animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-3 sm:grid-cols-4">
        <div className="bg-gray-800/60 border border-gray-700 rounded-lg p-4">
          <p className="text-gray-400 text-xs uppercase tracking-wide">Total Studies</p>
          <p className="text-2xl font-semibold text-white mt-1">{stats.total}</p>
        </div>
        <div className="bg-gray-800/60 border border-gray-700 rounded-lg p-4">
          <p className="text-gray-400 text-xs uppercase tracking-wide">Active</p>
          <p className="text-2xl font-semibold text-purple-300 mt-1">{stats.active}</p>
        </div>
        <div className="bg-gray-800/60 border border-gray-700 rounded-lg p-4">
          <p className="text-gray-400 text-xs uppercase tracking-wide">Completed</p>
          <p className="text-2xl font-semibold text-green-300 mt-1">{stats.completed}</p>
        </div>
        <div className="bg-gray-800/60 border border-gray-700 rounded-lg p-4">
          <p className="text-gray-400 text-xs uppercase tracking-wide">Avg Progress</p>
          <p className="text-2xl font-semibold text-amber-300 mt-1">{stats.avg}%</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {(['all', 'active', 'completed', 'archived'] as SessionFilter[]).map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
              filter === status
                ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                : 'bg-gray-800 text-gray-300 border border-gray-700 hover:text-white'
            }`}
          >
            {status === 'all' ? 'All' : status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>

      {sessions.length === 0 && (
        <div className="text-center py-10 bg-gray-900/40 border border-gray-800 rounded-xl">
          <Sparkles className="w-10 h-10 text-gray-600 mx-auto mb-3" />
          <p className="text-gray-300">No study guides in this category yet.</p>
          <p className="text-gray-500 text-sm mt-1">Generate a Deep Dive from Devotional or Journal to start tracking.</p>
        </div>
      )}

      {sessions.map((session: StudyGuideSession) => {
        const isExpanded = expandedSessionId === session.id
        const studyPlan = session.guide_data?.study_plan || []

        return (
          <div key={session.id} className="bg-gray-900/60 border border-gray-800 rounded-xl p-4">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h4 className="text-white font-semibold">{session.guide_data?.title || session.source_reference}</h4>
                <p className="text-gray-400 text-sm mt-1">
                  {session.source_type === 'devotional_passage' ? 'Devotional' : 'Journal'} • {session.source_reference}
                </p>
                <p className="text-gray-500 text-xs mt-1">Started {formatDate(session.started_at)}</p>
              </div>

              <div className="flex items-center gap-2">
                <span className={`px-2 py-1 rounded text-xs border ${
                  session.status === 'completed'
                    ? 'bg-green-500/20 text-green-300 border-green-500/30'
                    : session.status === 'archived'
                    ? 'bg-gray-700/50 text-gray-300 border-gray-600'
                    : 'bg-purple-500/20 text-purple-300 border-purple-500/30'
                }`}>
                  {session.status}
                </span>
                <button
                  onClick={() => setExpandedSessionId(isExpanded ? null : session.id)}
                  className="px-3 py-1.5 bg-gray-800 text-gray-200 rounded-lg hover:bg-gray-700 text-sm"
                >
                  {isExpanded ? 'Hide' : 'Open'}
                </button>
                {session.status !== 'archived' ? (
                  <button
                    onClick={() => archiveMutation.mutate(session.id)}
                    className="p-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700"
                    title="Archive session"
                  >
                    <Archive className="w-4 h-4" />
                  </button>
                ) : (
                  <button
                    onClick={() => resumeMutation.mutate(session.id)}
                    className="p-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700"
                    title="Resume session"
                  >
                    <PlayCircle className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>

            <div className="mt-3">
              <div className="w-full h-2 bg-gray-800 rounded-full">
                <div
                  className="h-2 bg-amber-500 rounded-full transition-all"
                  style={{ width: `${session.progress_percentage}%` }}
                />
              </div>
              <div className="flex items-center justify-between text-xs text-gray-400 mt-1">
                <span>{session.progress_percentage}% complete</span>
                <span>
                  {session.completed_days.length}/{session.total_days} days
                </span>
              </div>
            </div>

            {isExpanded && (
              <div className="mt-4 space-y-3">
                {studyPlan.length === 0 && (
                  <div className="text-sm text-gray-400 bg-gray-800/60 rounded-lg p-3">
                    No day-by-day study plan is available for this guide.
                  </div>
                )}

                {studyPlan.map((day) => {
                  const isCompleted = session.completed_days.includes(day.day)
                  const noteKey = `${session.id}:${day.day}`
                  const noteValue = noteDrafts[noteKey] ?? session.day_notes?.[String(day.day)] ?? ''

                  return (
                    <div key={day.day} className="bg-gray-800/50 border border-gray-700 rounded-lg p-3">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="text-amber-400 text-sm font-semibold">Day {day.day}: {day.focus}</p>
                          <p className="text-gray-400 text-xs mt-1">{day.scripture}</p>
                          <StudyDayScriptureQuote scripture={day.scripture} />
                          <p className="text-gray-300 text-sm mt-2">{day.practice}</p>
                        </div>
                        <button
                          onClick={() => markDayMutation.mutate({
                            sessionId: session.id,
                            day: day.day,
                            completed: !isCompleted,
                            note: noteValue,
                          })}
                          className={`px-3 py-1.5 rounded-lg text-sm flex items-center gap-1 ${
                            isCompleted
                              ? 'bg-green-500/20 text-green-300 border border-green-500/30'
                              : 'bg-gray-700 text-gray-200 border border-gray-600'
                          }`}
                        >
                          <CheckCircle2 className="w-4 h-4" />
                          {isCompleted ? 'Completed' : 'Mark Done'}
                        </button>
                      </div>

                      <div className="mt-3">
                        <label className="text-xs text-gray-400">Notes for this day</label>
                        <textarea
                          value={noteValue}
                          onChange={(event: ChangeEvent<HTMLTextAreaElement>) => {
                            const nextValue = event.target.value
                            setNoteDrafts((prev: Record<string, string>) => ({ ...prev, [noteKey]: nextValue }))
                          }}
                          className="w-full mt-1 bg-gray-900 border border-gray-700 rounded-md p-2 text-sm text-gray-200 min-h-[72px]"
                          placeholder="What did you learn or apply today?"
                        />
                        <button
                          onClick={() => markDayMutation.mutate({
                            sessionId: session.id,
                            day: day.day,
                            completed: isCompleted,
                            note: noteValue,
                          })}
                          className="mt-2 px-3 py-1.5 bg-purple-500/20 text-purple-300 rounded-md text-xs hover:bg-purple-500/30"
                        >
                          Save Day Note
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )
      })}

      {(markDayMutation.isPending || archiveMutation.isPending || resumeMutation.isPending) && (
        <div className="fixed bottom-4 right-4 bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 flex items-center gap-2">
          <Loader2 className="w-4 h-4 animate-spin" />
          Updating study tracker...
        </div>
      )}

      {sessions.length > 0 && (
        <div className="text-xs text-gray-500 flex items-center gap-2">
          <BookOpen className="w-3 h-3" />
          Tip: Keep one note per day to make your spiritual patterns easier to review later.
        </div>
      )}
    </div>
  )
}
