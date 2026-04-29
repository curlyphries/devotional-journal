import { useState } from 'react'
import { Trophy, TrendingUp, MessageCircle, BookOpen } from 'lucide-react'
import Milestones from '../components/Milestones'
import GrowthVisualization from '../components/GrowthVisualization'
import ThreadPrompts from '../components/ThreadPrompts'
import StudyTracker from '../components/StudyTracker'

type TabType = 'milestones' | 'growth' | 'threads' | 'studies'

export default function ProgressPage() {
  const [activeTab, setActiveTab] = useState<TabType>('studies')

  const tabs = [
    { id: 'studies' as TabType, label: 'Studies', icon: BookOpen },
    { id: 'milestones' as TabType, label: 'Achievements', icon: Trophy },
    { id: 'growth' as TabType, label: 'Growth', icon: TrendingUp },
    { id: 'threads' as TabType, label: 'Follow-ups', icon: MessageCircle },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Your Progress</h1>
        <p className="text-text-secondary mt-1">Track your spiritual growth journey</p>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-2 border-b border-gray-700 pb-2">
        {tabs.map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
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
