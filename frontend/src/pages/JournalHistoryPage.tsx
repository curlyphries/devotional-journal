import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Plus, Filter, Loader2, Book, Lightbulb } from 'lucide-react'
import { getJournalEntries } from '../api/journal'

const MOOD_LABELS: Record<string, { emoji: string; label: string; color: string }> = {
  grateful: { emoji: '🙏', label: 'Grateful', color: 'bg-success/20 text-success' },
  struggling: { emoji: '😔', label: 'Struggling', color: 'bg-text-secondary/20 text-text-secondary' },
  convicted: { emoji: '💭', label: 'Convicted', color: 'bg-accent-primary/20 text-accent-primary' },
  peaceful: { emoji: '😌', label: 'Peaceful', color: 'bg-accent-secondary/20 text-accent-secondary' },
  fired_up: { emoji: '🔥', label: 'Fired Up', color: 'bg-danger/20 text-danger' },
}

// Parse the journal content to extract metadata and actual content
function parseJournalContent(content: string): {
  planTitle?: string
  dayNumber?: string
  theme?: string
  passage?: string
  userContent: string
} {
  const lines = content.split('\n')
  let planTitle: string | undefined
  let dayNumber: string | undefined
  let theme: string | undefined
  let passage: string | undefined
  let contentStartIndex = 0

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    // Match **Plan Title** - Day X
    const planMatch = line.match(/^\*\*(.+?)\*\*\s*-\s*Day\s*(\d+)/)
    if (planMatch) {
      planTitle = planMatch[1]
      dayNumber = planMatch[2]
      contentStartIndex = i + 1
      continue
    }
    
    // Match **Theme:** X
    const themeMatch = line.match(/^\*\*Theme:\*\*\s*(.+)/)
    if (themeMatch) {
      theme = themeMatch[1]
      contentStartIndex = i + 1
      continue
    }
    
    // Match **Passage:** X
    const passageMatch = line.match(/^\*\*Passage:\*\*\s*(.+)/)
    if (passageMatch) {
      passage = passageMatch[1]
      contentStartIndex = i + 1
      continue
    }
    
    // Skip separator lines
    if (line === '---') {
      contentStartIndex = i + 1
      continue
    }
    
    // If we hit actual content, stop parsing metadata
    if (line && !line.startsWith('**')) {
      break
    }
  }

  const userContent = lines.slice(contentStartIndex).join('\n').trim()
  
  return { planTitle, dayNumber, theme, passage, userContent }
}

export default function JournalHistoryPage() {
  const { t } = useTranslation()
  const [filterMood, setFilterMood] = useState('')

  const { data: entries = [], isLoading, error } = useQuery({
    queryKey: ['journalEntries', filterMood],
    queryFn: () => getJournalEntries(filterMood ? { mood: filterMood } : undefined),
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-text-primary">
          {t('journal.history')}
        </h1>

        <Link to="/journal/new" className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          {t('journal.newEntry')}
        </Link>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-text-secondary">
          <Filter className="w-4 h-4" />
          <span className="text-sm">{t('journal.filterByMood')}:</span>
        </div>
        <select
          value={filterMood}
          onChange={(e) => setFilterMood(e.target.value)}
          className="input py-1 px-3"
        >
          <option value="">{t('journal.allMoods')}</option>
          {Object.entries(MOOD_LABELS).map(([id, { label }]) => (
            <option key={id} value={id}>
              {label}
            </option>
          ))}
        </select>
      </div>

      <div className="space-y-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 text-amber-500 animate-spin" />
          </div>
        ) : error ? (
          <div className="card text-center py-12">
            <p className="text-red-400">Failed to load entries</p>
          </div>
        ) : entries.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-text-secondary">{t('journal.noEntries')}</p>
            <Link to="/journal/new" className="btn-primary mt-4 inline-flex items-center gap-2">
              <Plus className="w-4 h-4" />
              Create Your First Entry
            </Link>
          </div>
        ) : (
          entries.map((entry) => {
            const parsed = parseJournalContent(entry.content_preview || '')
            
            return (
              <Link
                key={entry.id}
                to={`/journal/${entry.id}`}
                className="card block hover:border-accent-secondary transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <span className="text-sm text-text-secondary">
                      {new Date(entry.date).toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </span>
                    
                    {/* Show plan/passage context if present */}
                    {parsed.planTitle && (
                      <div className="flex items-center gap-2 mt-1">
                        <Book className="w-3 h-3 text-amber-500" />
                        <span className="text-amber-500 text-xs">
                          {parsed.planTitle} • Day {parsed.dayNumber}
                        </span>
                        {parsed.passage && (
                          <span className="text-gray-400 text-xs">• {parsed.passage}</span>
                        )}
                      </div>
                    )}
                    
                    {parsed.theme && (
                      <div className="flex items-center gap-1 mt-1">
                        <Lightbulb className="w-3 h-3 text-amber-500/70" />
                        <span className="text-gray-400 text-xs italic">{parsed.theme}</span>
                      </div>
                    )}
                  </div>
                  
                  {entry.mood_tag && MOOD_LABELS[entry.mood_tag] && (
                    <span
                      className={`text-xs px-2 py-1 rounded flex-shrink-0 ${MOOD_LABELS[entry.mood_tag]?.color || ''}`}
                    >
                      {MOOD_LABELS[entry.mood_tag]?.emoji}{' '}
                      {MOOD_LABELS[entry.mood_tag]?.label}
                    </span>
                  )}
                </div>
                
                {/* Show actual user content, not the metadata */}
                <p className="text-text-primary line-clamp-2">
                  {parsed.userContent || entry.content_preview}
                </p>
              </Link>
            )
          })
        )}
      </div>
    </div>
  )
}
