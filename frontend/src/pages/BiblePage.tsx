import { useSearchParams, useNavigate } from 'react-router-dom'
import { ChevronLeft, Book } from 'lucide-react'
import ScriptureReader from '../components/ScriptureReader'

export default function BiblePage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const passage = searchParams.get('passage') || 'John 3:16'

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
        >
          <ChevronLeft className="w-5 h-5" />
          Back
        </button>
        <div className="flex items-center gap-2 text-amber-500">
          <Book className="w-5 h-5" />
          <span className="text-sm font-medium">Scripture Study</span>
        </div>
      </div>

      <ScriptureReader 
        reference={passage}
        defaultTranslation="KJV"
        showComparison={true}
      />
    </div>
  )
}
