import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Trophy, TrendingUp, MessageCircle, BookOpen, Target, ScrollText } from 'lucide-react'
import Milestones from '../components/Milestones'
import GrowthVisualization from '../components/GrowthVisualization'
import ThreadPrompts from '../components/ThreadPrompts'
import StudyTracker from '../components/StudyTracker'
import GrowthReviews from '../components/GrowthReviews'
import JourneyPage from './JourneyPage'

type TabType = 'milestones' | 'growth' | 'threads' | 'studies' | 'journey' | 'reviews'

export default function ProgressPage() {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState<TabType>('studies')

  const tabs = [
    { id: 'studies' as TabType, label: 'Studies', icon: BookOpen },
    { id: 'journey' as TabType, label: 'Journey', icon: Target },
    { id: 'milestones' as TabType, label: 'Achievements', icon: Trophy },
    { id: 'growth' as TabType, label: 'Growth', icon: TrendingUp },
    { id: 'reviews' as TabType, label: t('progress.tabs.reviews'), icon: ScrollText },
    { id: 'threads' as TabType, label: 'Follow-ups', icon: MessageCircle },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Your Progress</h1>
        <p className="text-text-secondary mt-1">Track your spiritual growth journey</p>
      </div>

      {/* Tab Navigation */}
      {/* One row that scrolls sideways on narrow screens instead of overflowing the page */}
      <div
        role="tablist"
        aria-label={t('progress.tabs.label')}
        className="flex gap-2 overflow-x-auto border-b border-border pb-2 -mx-4 px-4 sm:mx-0 sm:px-0"
      >
        {tabs.map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex shrink-0 items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-colors ${
                activeTab === tab.id
                  ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  : 'text-text-secondary hover:text-text-primary hover:bg-gray-800'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          )
        })}
      </div>

      {/* Tab Content */}
      <div>
        {activeTab === 'studies' && <StudyTracker />}
        {activeTab === 'milestones' && <Milestones />}
        {activeTab === 'growth' && <GrowthVisualization />}
        {activeTab === 'reviews' && <GrowthReviews />}
        {activeTab === 'journey' && <JourneyPage />}
        {activeTab === 'threads' && (
          <div className="space-y-4">
            <p className="text-text-secondary">
              These are topics you've mentioned that we're following up on. 
              Share updates or mark them as resolved.
            </p>
            <ThreadPrompts maxPrompts={10} />
          </div>
        )}
      </div>
    </div>
  )
}
