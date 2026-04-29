import { useState } from 'react'
import { Flame, X } from 'lucide-react'

interface StreakSaverModalProps {
  isOpen: boolean
  streakCount: number
  onDismiss: () => void
  onJournalNow: () => void
}

export default function StreakSaverModal({ 
  isOpen, 
  streakCount, 
  onDismiss, 
  onJournalNow 
}: StreakSaverModalProps) {
  const [isClosing, setIsClosing] = useState(false)

  if (!isOpen) return null

  const handleDismiss = () => {
    setIsClosing(true)
    setTimeout(() => {
      onDismiss()
      setIsClosing(false)
    }, 200)
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 animate-fadeIn">
      <div className={`bg-gradient-to-br from-amber-900/30 to-orange-900/20 border-2 border-amber-500/50 rounded-2xl max-w-md w-full p-6 shadow-2xl transition-all ${isClosing ? 'opacity-0 scale-95' : 'opacity-100 scale-100'}`}>
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-amber-500/20 rounded-full flex items-center justify-center animate-pulse">
              <Flame className="w-6 h-6 text-amber-500" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-text-primary">
                Your {streakCount}-day streak is waiting!
              </h3>
              <p className="text-text-secondary text-sm">
                Don't let it slip away
              </p>
            </div>
          </div>
          <button
            onClick={handleDismiss}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5 text-text-secondary" />
          </button>
        </div>

        {/* Body */}
        <div className="mb-6">
          <p className="text-text-secondary leading-relaxed">
            We noticed you haven't journaled today. Just <strong className="text-text-primary">2 minutes</strong> of reflection can keep your streak alive.
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={onJournalNow}
            className="flex-1 px-4 py-3 bg-amber-500 hover:bg-amber-400 text-purple-900 rounded-lg font-semibold transition-colors"
          >
            Get Back on Track
          </button>
          <button
            onClick={handleDismiss}
            className="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
          >
            Maybe Later
          </button>
        </div>

        {/* Footer Note */}
        <p className="text-center text-text-secondary text-xs mt-4">
          We'll remind you again tomorrow if you miss today
        </p>
      </div>
    </div>
  )
}
