import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Home, BookOpen, Calendar, Book, Trophy, Lightbulb,
  ChevronDown, ChevronRight, Flame, Download, Search,
  Sparkles, Heart, HelpCircle, ArrowRight, MessageCircle
} from 'lucide-react'

interface FeatureSection {
  id: string
  icon: React.ReactNode
  title: string
  tagline: string
  color: string
  link?: string
  content: React.ReactNode
}

function Accordion({ section }: { section: FeatureSection }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="border border-gray-700 rounded-xl overflow-hidden transition-all hover:border-gray-600">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center gap-4 p-5 text-left"
      >
        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${section.color}`}>
          {section.icon}
        </div>
        <div className="flex-1">
          <h3 className="text-text-primary font-semibold">{section.title}</h3>
          <p className="text-text-secondary text-sm">{section.tagline}</p>
        </div>
        {isOpen
          ? <ChevronDown className="w-5 h-5 text-text-secondary" />
          : <ChevronRight className="w-5 h-5 text-text-secondary" />
        }
      </button>
      {isOpen && (
        <div className="px-5 pb-5 pt-0">
          <div className="border-t border-gray-700 pt-4 text-text-secondary text-sm leading-relaxed space-y-3">
            {section.content}
            {section.link && (
              <Link
                to={section.link}
                className="inline-flex items-center gap-1.5 text-amber-400 hover:text-amber-300 font-medium mt-2"
              >
                Go to {section.title} <ArrowRight className="w-4 h-4" />
              </Link>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

const features: FeatureSection[] = [
  {
    id: 'dashboard',
    icon: <Home className="w-5 h-5" />,
    title: 'Dashboard',
    tagline: 'Your daily home base — everything at a glance',
    color: 'bg-amber-500/20 text-amber-400',
    link: '/',
    content: (
      <>
        <p>
          The Dashboard is the first thing you see when you open the app. It shows your <strong className="text-text-primary">current streak</strong>, today's date, and quick access to everything.
        </p>
        <p><strong className="text-text-primary">What you'll find here:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">Streak badge</strong> — Your consecutive journaling days. At 3+ days, a share button appears so you can share your milestone.</li>
          <li><strong className="text-text-primary">Daily Pulse</strong> — If you have an active Focus, you'll see today's curated scripture passage and reflection prompt.</li>
          <li><strong className="text-text-primary">Reading Plan card</strong> — Tap to jump directly to today's reading in your active plan.</li>
          <li><strong className="text-text-primary">Focus card</strong> — Shows your current spiritual focus intention and progress.</li>
          <li><strong className="text-text-primary">Quick Actions</strong> — One-tap access to start journaling, open your Bible, or begin a reflection.</li>
          <li><strong className="text-text-primary">Speak Your Mind</strong> — Type anything on your heart and the AI will find relevant scripture and prompts.</li>
        </ul>
        <p className="text-amber-400/80 text-xs mt-3">
          Tip: If you're new, the Dashboard will walk you through setting up your first Focus and Reading Plan.
        </p>
      </>
    ),
  },
  {
    id: 'journal',
    icon: <BookOpen className="w-5 h-5" />,
    title: 'Journal',
    tagline: 'Write freely — your entries are encrypted and private',
    color: 'bg-blue-500/20 text-blue-400',
    link: '/journal',
    content: (
      <>
        <p>
          Your personal space to process what God is showing you. Every entry is <strong className="text-text-primary">encrypted</strong> — only you can read your journal.
        </p>
        <p><strong className="text-text-primary">How to use it:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">New entry</strong> — Tap the "+" or "New Entry" button. Write whatever's on your heart.</li>
          <li><strong className="text-text-primary">Mood tag</strong> — Pick how you're feeling: Grateful, Peaceful, Convicted, Struggling, or Fired Up. This tracks patterns over time.</li>
          <li><strong className="text-text-primary">Scripture link</strong> — Connect your entry to a passage you're studying.</li>
          <li><strong className="text-text-primary">AI Deep Dive</strong> — After writing, ask the AI to generate a study guide based on what you wrote. Great for going deeper.</li>
          <li><strong className="text-text-primary">History</strong> — The Journal page shows all past entries. Filter by date or search.</li>
        </ul>
        <p className="text-amber-400/80 text-xs mt-3">
          Tip: Journaling daily builds your streak and unlocks milestones. Even a few sentences count.
        </p>
      </>
    ),
  },
  {
    id: 'plans',
    icon: <Calendar className="w-5 h-5" />,
    title: 'Reading Plans',
    tagline: 'Structured multi-day Bible reading — AI-generated or handcrafted',
    color: 'bg-green-500/20 text-green-400',
    link: '/plans',
    content: (
      <>
        <p>
          Reading Plans guide you through scripture over multiple days. Each day has specific passages, a theme, and a reflection prompt.
        </p>
        <p><strong className="text-text-primary">Two ways to get a plan:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">Browse existing plans</strong> — Pre-built plans like "Gospel of John - 7 Days" or community plans.</li>
          <li><strong className="text-text-primary">Build your own</strong> — Tap "Create Plan" and choose:
            <ul className="list-disc list-inside ml-4 mt-1 space-y-1">
              <li><strong className="text-text-primary">AI Mode</strong> — Describe a topic (e.g., "patience in suffering") and pick a duration. The AI generates a full plan with passages and themes.</li>
              <li><strong className="text-text-primary">Manual Mode</strong> — Hand-pick passages for each day yourself.</li>
            </ul>
          </li>
        </ul>
        <p><strong className="text-text-primary">Using a plan:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li>Tap <strong className="text-text-primary">"Start Plan"</strong> to enroll. You'll see it on your Dashboard.</li>
          <li>Each day, tap the plan card to read today's passages.</li>
          <li>After reading, tap <strong className="text-text-primary">"Mark Complete"</strong> to advance to the next day.</li>
          <li>Use the <strong className="text-text-primary">"My Plans"</strong> filter to see plans you've created.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'focus',
    icon: <Book className="w-5 h-5" />,
    title: 'Focus',
    tagline: 'Set a spiritual intention — the AI curates scripture around it',
    color: 'bg-purple-500/20 text-purple-400',
    link: '/devotional',
    content: (
      <>
        <p>
          Focus is the heart of your daily devotional experience. You set an <strong className="text-text-primary">intention</strong> — what you want to grow in — and the AI curates scripture passages and reflection prompts tailored to it.
        </p>
        <p><strong className="text-text-primary">How it works:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">Set your focus</strong> — Write something like "I want to be more patient with my kids" or "Help me trust God with my finances."</li>
          <li><strong className="text-text-primary">Pick themes</strong> — Select life areas that relate (faith, integrity, relationships, etc.).</li>
          <li><strong className="text-text-primary">Choose duration</strong> — Daily, weekly, or monthly focus.</li>
          <li><strong className="text-text-primary">Daily passages</strong> — Each day, the AI selects a scripture passage that speaks to your focus, with a stylized quote and reflection prompts.</li>
          <li><strong className="text-text-primary">Respond</strong> — Write your reflection directly on the passage. Your response is saved and tracked.</li>
        </ul>
        <p className="text-amber-400/80 text-xs mt-3">
          Tip: A weekly focus works best for most people. It gives enough time to sit with a theme without feeling rushed.
        </p>
      </>
    ),
  },
  {
    id: 'progress',
    icon: <Trophy className="w-5 h-5" />,
    title: 'Progress',
    tagline: 'Track growth, earn milestones, manage your journey',
    color: 'bg-yellow-500/20 text-yellow-400',
    link: '/progress',
    content: (
      <>
        <p>
          Progress brings together everything about your spiritual growth in one place. It has five tabs:
        </p>
        <ul className="list-disc list-inside space-y-2 ml-2">
          <li><strong className="text-text-primary">Studies</strong> — Track your active reading plans and study sessions.</li>
          <li><strong className="text-text-primary">Journey</strong> — Set personal growth goals with a timeline. Create a journey like "30 Days of Patience" with a goal statement, success definition, and focus areas. Track your progress day by day.</li>
          <li><strong className="text-text-primary">Achievements</strong> — Milestones you've earned (e.g., "First Week Streak," "50 Journal Entries"). Each achievement has a <strong className="text-text-primary">share button</strong> to create a shareable image.</li>
          <li><strong className="text-text-primary">Growth</strong> — Visual charts of your life area scores over time. See which areas you're growing in and which need attention.</li>
          <li><strong className="text-text-primary">Follow-ups</strong> — Topics the AI detected in your writing that deserve follow-up. Struggles you mentioned, commitments you made, questions left unanswered. The AI checks in so nothing falls through the cracks.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'insights',
    icon: <Lightbulb className="w-5 h-5" />,
    title: 'Insights',
    tagline: 'Browse your reflection and journal history with context',
    color: 'bg-orange-500/20 text-orange-400',
    link: '/insights',
    content: (
      <>
        <p>
          Insights gives you a searchable history of your reflections and journal entries. Unlike the Journal page (which is just entries), Insights shows the <strong className="text-text-primary">full context</strong> — the scripture you were reading, the life area scores you gave, and the AI insights generated.
        </p>
        <p><strong className="text-text-primary">Best used for:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li>Looking back at what God has been teaching you over weeks or months.</li>
          <li>Preparing for a small group or accountability conversation.</li>
          <li>Noticing patterns in your spiritual life you might miss day-to-day.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'threads',
    icon: <MessageCircle className="w-5 h-5" />,
    title: 'Open Threads',
    tagline: "Things you're still wrestling with — the AI follows up so nothing falls through the cracks",
    color: 'bg-cyan-500/20 text-cyan-400',
    link: '/threads',
    content: (
      <>
        <p>
          A <strong className="text-text-primary">thread</strong> is something you mentioned in a journal entry that the AI thinks is worth following up on — a struggle you're battling, a commitment you made, a tough decision, an unanswered question, a relationship under tension, or something vulnerable you shared. Threads make sure those conversations don't disappear into a sea of past entries.
        </p>
        <p><strong className="text-text-primary">How threads appear:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li>You write a journal entry (any length over ~30 words).</li>
          <li>In the background, your configured AI (Ollama or Anthropic) reads the entry and identifies up to a few significant items.</li>
          <li>An <strong className="text-text-primary">Open Thread</strong> is created for each, encrypted with your key just like the journal entry.</li>
          <li>You'll see the count on the Dashboard ("Open threads") and the full list on the Threads page.</li>
        </ul>
        <p><strong className="text-text-primary">The six thread types:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-red-400">Struggle</strong> — battles you're in the middle of (anxiety, anger, lust, comparison)</li>
          <li><strong className="text-green-400">Commitment</strong> — promises you made to yourself or to God ("I'm going to start praying daily")</li>
          <li><strong className="text-blue-400">Question</strong> — things you're wondering about and haven't resolved</li>
          <li><strong className="text-purple-400">Relationship</strong> — tension or a hard conversation pending with someone</li>
          <li><strong className="text-yellow-400">Decision</strong> — a fork in the road you're weighing</li>
          <li><strong className="text-pink-400">Confession</strong> — something vulnerable you shared and want to remember walking through</li>
        </ul>
        <p><strong className="text-text-primary">How to manage threads:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li>Periodically — every few days for active threads — you'll see a quick check-in card while journaling: "How's that going?" Tap <strong className="text-text-primary">Better / Same / Worse / Resolved</strong>.</li>
          <li>On the Threads page, you can <strong className="text-text-primary">Resolve</strong> (with an optional note), <strong className="text-text-primary">Defer</strong> (snooze for 7 days), or <strong className="text-text-primary">Drop</strong> any thread you don't want to track.</li>
          <li>If you skip a thread three times, the system automatically defers it — it won't badger you forever.</li>
          <li>Threads max out at 3 follow-ups by default; after that they auto-close to keep your inbox clean.</li>
        </ul>
        <p className="text-amber-400/80 text-xs mt-3">
          Privacy: thread summaries and original-context quotes are encrypted with your per-user key. Even with database access, no one can read them. Detection happens server-side via your configured AI provider — set <code className="bg-bg-elevated px-1 rounded">LLM_BACKEND=ollama</code> in your .env if you want detection to run on a local Ollama instance only.
        </p>
      </>
    ),
  },
  {
    id: 'reflection',
    icon: <Heart className="w-5 h-5" />,
    title: 'Daily Reflection',
    tagline: 'End-of-day check-in — scripture, gratitude, and self-assessment',
    color: 'bg-pink-500/20 text-pink-400',
    link: '/reflection',
    content: (
      <>
        <p>
          The Daily Reflection is a guided end-of-day exercise. It walks you through several steps:
        </p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">Scripture</strong> — What did you read today? Link a passage.</li>
          <li><strong className="text-text-primary">Reflection</strong> — What stood out? What is God saying to you?</li>
          <li><strong className="text-text-primary">Life area scores</strong> — Rate yourself 1-10 on areas like faith, integrity, relationships, health, and purpose. This builds your growth chart over time.</li>
          <li><strong className="text-text-primary">Gratitude</strong> — What are you thankful for today?</li>
          <li><strong className="text-text-primary">Struggle</strong> — What's weighing on you? (The AI may follow up on this later.)</li>
          <li><strong className="text-text-primary">Tomorrow's intention</strong> — What do you want to focus on tomorrow?</li>
        </ul>
        <p className="text-amber-400/80 text-xs mt-3">
          Tip: You don't have to fill out every field. Even just the scripture + reflection is valuable. The AI insight is generated after you submit.
        </p>
      </>
    ),
  },
  {
    id: 'bible',
    icon: <Search className="w-5 h-5" />,
    title: 'Bible & Highlights',
    tagline: 'Read scripture, highlight verses, add notes',
    color: 'bg-teal-500/20 text-teal-400',
    link: '/bible',
    content: (
      <>
        <p>
          A built-in Bible reader so you never have to leave the app. Currently supports <strong className="text-text-primary">KJV</strong>.
        </p>
        <p><strong className="text-text-primary">Key features:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">Browse</strong> — Navigate by book, chapter, and verse.</li>
          <li><strong className="text-text-primary">Search</strong> — Find verses by keyword.</li>
          <li><strong className="text-text-primary">Highlight</strong> — Tap a verse to highlight it in yellow, green, blue, pink, or orange.</li>
          <li><strong className="text-text-primary">Notes</strong> — Add a personal note to any highlighted verse.</li>
          <li><strong className="text-text-primary">Export</strong> — Download all your highlights as a Markdown file from Settings.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'ai',
    icon: <Sparkles className="w-5 h-5" />,
    title: 'AI Features',
    tagline: 'How the AI assists your study — and how to configure it',
    color: 'bg-indigo-500/20 text-indigo-400',
    content: (
      <>
        <p>
          The app uses AI to enhance your Bible study — never to replace it. Here's where AI shows up:
        </p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">Focus passages</strong> — AI selects scripture relevant to your intention.</li>
          <li><strong className="text-text-primary">Reflection prompts</strong> — AI generates questions based on what you read.</li>
          <li><strong className="text-text-primary">Plan generation</strong> — AI builds multi-day reading plans from a topic.</li>
          <li><strong className="text-text-primary">"Speak Your Mind"</strong> — Freeform AI conversation about scripture on the Dashboard.</li>
          <li><strong className="text-text-primary">Journal deep dive</strong> — AI generates a study guide from your journal entry.</li>
          <li><strong className="text-text-primary">Thread detection</strong> — AI notices struggles and commitments in your writing and follows up later.</li>
          <li><strong className="text-text-primary">Daily reflection insight</strong> — After submitting a reflection, the AI offers a brief encouraging insight.</li>
        </ul>
        <p className="mt-3"><strong className="text-text-primary">Configuring your AI provider:</strong></p>
        <p>
          Go to <strong className="text-text-primary">Settings → AI Provider</strong>. Options include:
        </p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">System Default</strong> — Uses the server's configured AI (no setup needed).</li>
          <li><strong className="text-text-primary">OpenAI / Anthropic / OpenRouter</strong> — Bring your own API key for higher quality or specific models.</li>
          <li><strong className="text-text-primary">Ollama</strong> — Run AI locally on your own machine for complete privacy.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'export',
    icon: <Download className="w-5 h-5" />,
    title: 'Export & Share',
    tagline: 'Download your data or share milestones with others',
    color: 'bg-emerald-500/20 text-emerald-400',
    link: '/settings',
    content: (
      <>
        <p>
          Your data belongs to you. Export everything from <strong className="text-text-primary">Settings → Export Your Data</strong>.
        </p>
        <p><strong className="text-text-primary">Export options:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">Full Data Export</strong> — ZIP file with all your data as JSON. Good for backups or switching apps.</li>
          <li><strong className="text-text-primary">Journal (Markdown)</strong> — All entries formatted with dates, moods, and content. Print-friendly.</li>
          <li><strong className="text-text-primary">Highlights (Markdown)</strong> — Your verse highlights grouped by book. Great for Bible study groups.</li>
          <li><strong className="text-text-primary">Growth Report (Markdown)</strong> — Stats summary with life area averages, mood distribution, and resolved threads.</li>
        </ul>
        <p className="mt-3"><strong className="text-text-primary">Sharing:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li><strong className="text-text-primary">Streak share</strong> — On the Dashboard, tap the share icon on your streak badge (appears at 3+ days).</li>
          <li><strong className="text-text-primary">Achievement share</strong> — In Progress → Achievements, tap share on any unlocked milestone.</li>
          <li>On mobile, uses your phone's native share sheet. On desktop, downloads a PNG image.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'streak',
    icon: <Flame className="w-5 h-5" />,
    title: 'Streaks & Engagement',
    tagline: 'How streaks work and why consistency matters',
    color: 'bg-red-500/20 text-red-400',
    content: (
      <>
        <p>
          Your <strong className="text-text-primary">journal streak</strong> counts consecutive days with at least one journal entry. It resets to zero if you miss a day.
        </p>
        <p><strong className="text-text-primary">Streak saver:</strong></p>
        <p>
          If it's after 6 PM and you haven't journaled today, a gentle reminder pops up: "Don't lose your streak!" Tap "Journal Now" to quick-start an entry. You can dismiss it for the day.
        </p>
        <p><strong className="text-text-primary">Why it matters:</strong></p>
        <p>
          Spiritual growth is built on consistency, not intensity. A 3-sentence entry every day is more transformative than a 3-page entry once a month. The streak is a tool to help you build the habit.
        </p>
      </>
    ),
  },
]

export default function HelpPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div>
        <div className="flex items-center gap-3 mb-2">
          <HelpCircle className="w-8 h-8 text-amber-500" />
          <h1 className="text-2xl font-bold text-text-primary">How to Use Devotional Journal</h1>
        </div>
        <p className="text-text-secondary">
          A guide to every feature in the app. Tap any section to expand it.
        </p>
      </div>

      {/* Quick Start */}
      <div className="bg-gradient-to-r from-amber-900/30 to-purple-900/20 border border-amber-500/30 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-text-primary mb-3">Quick Start</h2>
        <div className="text-text-secondary text-sm space-y-2">
          <p>New here? Here's the fastest path to value:</p>
          <ol className="list-decimal list-inside space-y-1.5 ml-2">
            <li><strong className="text-text-primary">Set a Focus</strong> — Go to <Link to="/devotional" className="text-amber-400 hover:underline">Focus</Link> and write what you want to grow in.</li>
            <li><strong className="text-text-primary">Read today's passage</strong> — The AI will curate scripture for you on the Dashboard.</li>
            <li><strong className="text-text-primary">Write a journal entry</strong> — Even 2-3 sentences. This starts your streak.</li>
            <li><strong className="text-text-primary">Do a Daily Reflection</strong> — Rate your life areas and note one thing you're grateful for.</li>
            <li><strong className="text-text-primary">Come back tomorrow</strong> — Consistency is the whole game.</li>
          </ol>
        </div>
      </div>

      {/* Feature Sections */}
      <div className="space-y-3">
        {features.map((section) => (
          <Accordion key={section.id} section={section} />
        ))}
      </div>

      {/* Footer */}
      <div className="text-center text-text-secondary text-sm pb-8">
        <p>Built for men who want to grow in faith, one day at a time.</p>
        <p className="mt-1 text-text-secondary/60">
          Questions? Reach out to <a href="mailto:david@curlyphries.net" className="text-amber-400 hover:underline">david@curlyphries.net</a>
        </p>
      </div>
    </div>
  )
}
