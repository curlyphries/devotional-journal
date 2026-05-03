import { useRef, useState } from 'react'
import { Share2, Download, X, Loader2 } from 'lucide-react'

interface ShareCardProps {
  /** Card variant determines the visual style */
  variant: 'streak' | 'achievement' | 'plan_complete'
  /** Main number or stat to highlight */
  headline: string
  /** Subtitle text */
  subtitle: string
  /** Optional detail line */
  detail?: string
  /** Trigger element — renders the share button inline */
  children?: React.ReactNode
}

const GRADIENT_MAP = {
  streak: 'from-amber-600 via-orange-600 to-red-600',
  achievement: 'from-emerald-600 via-green-600 to-teal-600',
  plan_complete: 'from-blue-600 via-indigo-600 to-purple-600',
}

const ICON_MAP = {
  streak: '🔥',
  achievement: '🏆',
  plan_complete: '📖',
}

export default function ShareCard({
  variant,
  headline,
  subtitle,
  detail,
}: ShareCardProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const cardRef = useRef<HTMLDivElement>(null)

  const handleDownload = async () => {
    if (!cardRef.current) return
    setIsGenerating(true)

    try {
      // Use html2canvas-style approach via canvas API
      const canvas = document.createElement('canvas')
      const scale = 2 // Retina
      canvas.width = 600 * scale
      canvas.height = 400 * scale
      const ctx = canvas.getContext('2d')
      if (!ctx) return

      ctx.scale(scale, scale)

      // Background gradient
      const gradientColors: Record<string, [string, string]> = {
        streak: ['#d97706', '#dc2626'],
        achievement: ['#059669', '#0d9488'],
        plan_complete: ['#2563eb', '#7c3aed'],
      }
      const [startColor, endColor] = gradientColors[variant] || gradientColors.streak
      const grad = ctx.createLinearGradient(0, 0, 600, 400)
      grad.addColorStop(0, startColor)
      grad.addColorStop(1, endColor)
      ctx.fillStyle = grad
      ctx.beginPath()
      ctx.roundRect(0, 0, 600, 400, 24)
      ctx.fill()

      // Decorative circles
      ctx.fillStyle = 'rgba(255,255,255,0.05)'
      ctx.beginPath()
      ctx.arc(500, 80, 120, 0, Math.PI * 2)
      ctx.fill()
      ctx.beginPath()
      ctx.arc(80, 350, 80, 0, Math.PI * 2)
      ctx.fill()

      // Icon
      ctx.font = '48px serif'
      ctx.textAlign = 'center'
      ctx.fillText(ICON_MAP[variant], 300, 100)

      // Headline
      ctx.fillStyle = '#ffffff'
      ctx.font = 'bold 56px system-ui, -apple-system, sans-serif'
      ctx.textAlign = 'center'
      ctx.fillText(headline, 300, 190)

      // Subtitle
      ctx.fillStyle = 'rgba(255,255,255,0.9)'
      ctx.font = '24px system-ui, -apple-system, sans-serif'
      ctx.fillText(subtitle, 300, 240)

      // Detail
      if (detail) {
        ctx.fillStyle = 'rgba(255,255,255,0.7)'
        ctx.font = '18px system-ui, -apple-system, sans-serif'
        ctx.fillText(detail, 300, 285)
      }

      // Branding
      ctx.fillStyle = 'rgba(255,255,255,0.4)'
      ctx.font = '14px system-ui, -apple-system, sans-serif'
      ctx.fillText('Devotional Journal', 300, 370)

      // Download
      const url = canvas.toDataURL('image/png')
      const a = document.createElement('a')
      a.href = url
      a.download = `devotional-${variant}-${Date.now()}.png`
      document.body.appendChild(a)
      a.click()
      a.remove()
    } finally {
      setIsGenerating(false)
    }
  }

  const handleShare = async () => {
    if (!navigator.share) {
      handleDownload()
      return
    }

    // Generate the blob for native sharing
    if (!cardRef.current) return
    setIsGenerating(true)

    try {
      const canvas = document.createElement('canvas')
      const scale = 2
      canvas.width = 600 * scale
      canvas.height = 400 * scale
      const ctx = canvas.getContext('2d')
      if (!ctx) return

      ctx.scale(scale, scale)
      const gradientColors: Record<string, [string, string]> = {
        streak: ['#d97706', '#dc2626'],
        achievement: ['#059669', '#0d9488'],
        plan_complete: ['#2563eb', '#7c3aed'],
      }
      const [startColor, endColor] = gradientColors[variant] || gradientColors.streak
      const grad = ctx.createLinearGradient(0, 0, 600, 400)
      grad.addColorStop(0, startColor)
      grad.addColorStop(1, endColor)
      ctx.fillStyle = grad
      ctx.beginPath()
      ctx.roundRect(0, 0, 600, 400, 24)
      ctx.fill()
      ctx.fillStyle = 'rgba(255,255,255,0.05)'
      ctx.beginPath()
      ctx.arc(500, 80, 120, 0, Math.PI * 2)
      ctx.fill()
      ctx.font = '48px serif'
      ctx.textAlign = 'center'
      ctx.fillText(ICON_MAP[variant], 300, 100)
      ctx.fillStyle = '#ffffff'
      ctx.font = 'bold 56px system-ui, -apple-system, sans-serif'
      ctx.fillText(headline, 300, 190)
      ctx.fillStyle = 'rgba(255,255,255,0.9)'
      ctx.font = '24px system-ui, -apple-system, sans-serif'
      ctx.fillText(subtitle, 300, 240)
      if (detail) {
        ctx.fillStyle = 'rgba(255,255,255,0.7)'
        ctx.font = '18px system-ui, -apple-system, sans-serif'
        ctx.fillText(detail, 300, 285)
      }
      ctx.fillStyle = 'rgba(255,255,255,0.4)'
      ctx.font = '14px system-ui, -apple-system, sans-serif'
      ctx.fillText('Devotional Journal', 300, 370)

      canvas.toBlob(async (blob) => {
        if (!blob) return
        const file = new File([blob], `devotional-${variant}.png`, { type: 'image/png' })
        try {
          await navigator.share({
            title: subtitle,
            text: `${headline} - ${subtitle}`,
            files: [file],
          })
        } catch {
          // User cancelled share — that's fine
        }
      }, 'image/png')
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="p-1.5 text-text-secondary hover:text-amber-400 rounded-lg hover:bg-gray-800 transition-colors"
        title="Share"
      >
        <Share2 className="w-4 h-4" />
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="bg-bg-secondary rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden">
            {/* Preview */}
            <div
              ref={cardRef}
              className={`bg-gradient-to-br ${GRADIENT_MAP[variant]} p-10 text-center relative overflow-hidden`}
            >
              <div className="absolute top-4 right-4 w-32 h-32 rounded-full bg-white/5" />
              <div className="absolute bottom-4 left-4 w-20 h-20 rounded-full bg-white/5" />
              <div className="relative z-10">
                <span className="text-5xl mb-4 block">{ICON_MAP[variant]}</span>
                <h2 className="text-4xl font-bold text-white mb-2">{headline}</h2>
                <p className="text-white/90 text-lg">{subtitle}</p>
                {detail && <p className="text-white/70 text-sm mt-2">{detail}</p>}
                <p className="text-white/40 text-xs mt-8">Devotional Journal</p>
              </div>
            </div>

            {/* Actions */}
            <div className="p-4 flex items-center gap-3">
              <button
                onClick={handleShare}
                disabled={isGenerating}
                className="flex-1 flex items-center justify-center gap-2 py-3 bg-amber-500 hover:bg-amber-400 text-black font-medium rounded-xl transition-colors disabled:opacity-50"
              >
                {isGenerating ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Share2 className="w-4 h-4" />
                )}
                Share
              </button>
              <button
                onClick={handleDownload}
                disabled={isGenerating}
                className="flex items-center justify-center gap-2 py-3 px-5 bg-gray-700 hover:bg-gray-600 text-text-primary font-medium rounded-xl transition-colors disabled:opacity-50"
              >
                <Download className="w-4 h-4" />
                Save
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="p-3 text-text-secondary hover:text-text-primary hover:bg-gray-700 rounded-xl transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
