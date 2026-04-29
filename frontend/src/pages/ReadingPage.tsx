import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import { ChevronLeft, Save } from 'lucide-react'

const MOODS = [
  { id: 'grateful', emoji: '🙏', label: 'Grateful' },
  { id: 'struggling', emoji: '😔', label: 'Struggling' },
  { id: 'convicted', emoji: '💭', label: 'Convicted' },
  { id: 'peaceful', emoji: '😌', label: 'Peaceful' },
  { id: 'fired_up', emoji: '🔥', label: 'Fired Up' },
]

export default function ReadingPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [journalContent, setJournalContent] = useState('')
  const [selectedMood, setSelectedMood] = useState('')
  const [isSaving, setIsSaving] = useState(false)

  const handleSave = async () => {
    setIsSaving(true)
    // API call would go here
    setTimeout(() => {
      setIsSaving(false)
      navigate('/')
    }, 1000)
  }

  return (
    <div className="space-y-8">
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
      >
        <ChevronLeft className="w-5 h-5" />
        {t('common.back')}
      </button>

      <div className="card">
        <div className="mb-6">
          <h2 className="text-sm font-medium text-accent-secondary mb-2">
            Day 7 of 30 - Psalms Journey
          </h2>
          <h1 className="text-2xl font-bold text-text-primary">
            Psalm 23:1-6
          </h1>
        </div>

        <div className="scripture-text mb-8">
          <p className="text-text-primary leading-relaxed">
            The Lord is my shepherd; I shall not want. He maketh me to lie down
            in green pastures: he leadeth me beside the still waters. He
            restoreth my soul: he leadeth me in the paths of righteousness for
            his name's sake. Yea, though I walk through the valley of the shadow
            of death, I will fear no evil: for thou art with me; thy rod and thy
            staff they comfort me. Thou preparest a table before me in the
            presence of mine enemies: thou anointest my head with oil; my cup
            runneth over. Surely goodness and mercy shall follow me all the days
            of my life: and I will dwell in the house of the Lord for ever.
          </p>
        </div>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-text-primary mb-4">
          {t('reading.reflectionPrompts')}
        </h2>

        <ul className="space-y-3">
          <li className="flex items-start gap-3">
            <span className="text-accent-primary font-bold">1.</span>
            <span className="text-text-primary">
              What area of your life do you need to trust God as your shepherd
              right now?
            </span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-accent-primary font-bold">2.</span>
            <span className="text-text-primary">
              When was the last time you felt God restore your soul? What did
              that look like?
            </span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-accent-primary font-bold">3.</span>
            <span className="text-text-primary">
              What "valley" are you walking through, and how can you remember
              God's presence in it?
            </span>
          </li>
        </ul>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-text-primary mb-4">
          {t('reading.journalEntry')}
        </h2>

        <textarea
          value={journalContent}
          onChange={(e) => setJournalContent(e.target.value)}
          placeholder="Write your thoughts, prayers, and reflections..."
          className="input w-full h-48 resize-none mb-6"
        />

        <div className="mb-6">
          <label className="block text-sm font-medium text-text-primary mb-3">
            {t('reading.moodTag')}
          </label>
          <div className="flex flex-wrap gap-2">
            {MOODS.map((mood) => (
              <button
                key={mood.id}
                onClick={() => setSelectedMood(mood.id)}
                className={`px-4 py-2 rounded-lg border transition-colors ${
                  selectedMood === mood.id
                    ? 'border-accent-primary bg-accent-primary/10 text-accent-primary'
                    : 'border-border text-text-secondary hover:border-text-secondary'
                }`}
              >
                <span className="mr-2">{mood.emoji}</span>
                {mood.label}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleSave}
          disabled={isSaving || !journalContent.trim()}
          className="btn-primary flex items-center gap-2"
        >
          <Save className="w-4 h-4" />
          {isSaving ? t('common.loading') : t('reading.saveEntry')}
        </button>
      </div>
    </div>
  )
}
