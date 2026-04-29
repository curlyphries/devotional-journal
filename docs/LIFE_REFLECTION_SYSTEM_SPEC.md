# Life Reflection & Scripture Alignment System

**Version:** 2.0  
**Last Updated:** March 31, 2026  
**Status:** FINAL DESIGN - Ready for Implementation

---

## Table of Contents

1. [Vision](#vision)
2. [Target Audience](#target-audience)
3. [Core Concepts](#core-concepts)
4. [User Journey Framework](#user-journey-framework)
5. [Data Models](#data-models)
6. [Open Threads Accountability System](#open-threads-accountability-system)
7. [AI Crew Architecture](#ai-crew-architecture)
8. [Pop-up Thread Reminders UX](#pop-up-thread-reminders-ux)
9. [AI Provider Integration](#ai-provider-integration)
10. [User Experience Flows](#user-experience-flows)
11. [API Endpoints](#api-endpoints)
12. [Implementation Phases](#implementation-phases)
13. [Privacy & Security](#privacy--security)

---

## Vision

A devotional system that helps men (young adult through senior, single through divorced) not just read scripture, but **measure how they're living it**. The system captures daily reflections, extracts themes from scripture, and uses AI to provide insights on alignment between what they read and how they lived.

**Key Differentiators:**
- User-driven goals (not prescriptive plans)
- AI-powered accountability that ensures nothing falls through the cracks
- Open Threads system tracks unresolved struggles/commitments
- Weekly/monthly AI crew analysis (not daily - respects user's time)

---

## Target Audience

| Life Stage | Key Struggles | Focus Areas |
|------------|---------------|-------------|
| **Young Adult (18-25)** | Identity, purpose, temptation, direction | Self-control, purpose discovery, integrity foundation |
| **Single Adult (25-40)** | Loneliness, career pressure, dating/purity | Relationships, work/calling, patience |
| **Married (any age)** | Leadership, provision, communication | Family, servant leadership, sacrifice |
| **Father** | Time management, modeling faith, discipline | Fatherhood, legacy, consistency |
| **Divorced/Rebuilding** | Shame, starting over, co-parenting | Healing, forgiveness, new identity |
| **Senior (60+)** | Legacy, health, relevance | Wisdom sharing, finishing well, gratitude |

---

## Core Concepts

### The Alignment Loop

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DAILY ALIGNMENT LOOP                             │
│                                                                          │
│   MORNING                    EVENING                    WEEKLY           │
│   ────────                   ───────                    ──────           │
│   ┌─────────┐               ┌─────────┐               ┌─────────┐       │
│   │ Read    │               │ Reflect │               │ Review  │       │
│   │Scripture│──────────────▶│ on Day  │──────────────▶│ Trends  │       │
│   └─────────┘               └─────────┘               └─────────┘       │
│        │                         │                         │            │
│        ▼                         ▼                         ▼            │
│   ┌─────────┐               ┌─────────┐               ┌─────────┐       │
│   │ Extract │               │ Score   │               │ AI Crew │       │
│   │ Themes  │               │ Areas   │               │ Insights│       │
│   └─────────┘               └─────────┘               └─────────┘       │
│                                                                          │
│   "What does God                "How did I                "Where am I   │
│    say about X?"                 live this?"               growing?"    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Seven Life Areas

| Area | Description | Scripture Tags |
|------|-------------|----------------|
| **Integrity** | Honesty, keeping word, character | truth, honest, lie, deceive, promise, faithful |
| **Relationships** | Family, friends, community | love, neighbor, brother, wife, children, father |
| **Work** | Career, calling, provision, purpose | work, labor, diligent, lazy, serve, calling |
| **Self-Control** | Temptation, discipline, emotions | tempt, flesh, spirit, desire, anger, patient |
| **Faith** | Prayer, study, obedience, trust | pray, trust, faith, believe, obey, word |
| **Service** | Helping others, generosity | give, serve, help, poor, generous, sacrifice |
| **Growth** | Learning, humility, transformation | learn, humble, grow, renew, transform, wisdom |

---

## User Journey Framework

### User-Driven Goals (Not Prescriptive)

Users define their own journey. The system adapts to their goals.

#### Goal Categories

| Category | Example Goals | Scripture Focus |
|----------|---------------|-----------------|
| **Breaking a Habit** | Quit porn, stop lying, control anger | Self-control, renewal |
| **Building a Habit** | Daily prayer, consistent presence with family | Discipline, faithfulness |
| **Healing/Recovery** | Process divorce, forgive someone, grieve loss | Restoration, forgiveness |
| **Relationship Repair** | Reconnect with estranged child, rebuild trust | Reconciliation, love |
| **Identity/Purpose** | Find direction after job loss, discover calling | Identity in Christ, purpose |
| **Leadership Growth** | Become better father, lead at work with integrity | Servant leadership |
| **Spiritual Foundation** | First-time faith exploration, return after years away | Basics of faith |

#### Journey Setup (Day 0)

```
┌─────────────────────────────────────────────────────────────────┐
│  WHAT DO YOU WANT TO ACCOMPLISH?                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Choose your focus (select 1-2):                                │
│  ○ Break a destructive pattern                                  │
│  ○ Build a new discipline                                       │
│  ○ Heal from something painful                                  │
│  ○ Repair a relationship                                        │
│  ○ Find direction/purpose                                       │
│  ○ Grow as a leader (home/work)                                │
│  ○ Strengthen my faith foundation                               │
│                                                                  │
│  Duration: [7] [14] [21] [30] [90] days                         │
│                                                                  │
│  In your own words, what does success look like?                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ "I want to go 30 days without looking at porn and       │    │
│  │  actually be present with my kids in the evenings"      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Which life areas matter most for this goal?                    │
│  ☑ Self-Control    ☑ Relationships    ☐ Work                   │
│  ☐ Integrity       ☐ Faith            ☐ Service    ☐ Growth    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Reading Plan Options

| Mode | Description | Best For |
|------|-------------|----------|
| **AI-Suggested** | AI suggests daily readings based on goal | New to Bible, wants structure |
| **Self-Directed** | User picks their own passages | Experienced, has specific books in mind |
| **Hybrid** | AI suggests, user can swap any day | Most users |

---

## Data Models

### 1. LifeArea (Reference Data)

```python
class LifeArea(models.Model):
    """
    Core life domains for self-assessment.
    Pre-seeded, not user-editable.
    """
    AREA_CHOICES = [
        ('integrity', 'Integrity & Honesty'),
        ('relationships', 'Relationships & Family'),
        ('work', 'Work & Purpose'),
        ('self_control', 'Self-Control & Discipline'),
        ('faith', 'Faith & Spiritual Practice'),
        ('service', 'Service & Generosity'),
        ('growth', 'Growth & Humility'),
    ]
    
    code = models.CharField(max_length=20, primary_key=True, choices=AREA_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    scripture_tags = models.JSONField()  # Keywords that map to this area
    reflection_prompts = models.JSONField()  # Default prompts per area
```

### 2. UserJourney (User's Personal Goal)

```python
class UserJourney(models.Model):
    """
    User's personal journey with their own goals.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Journey basics
    title = models.CharField(max_length=200)  # User can name it
    duration_days = models.PositiveIntegerField(default=30)
    started_at = models.DateTimeField()
    
    # User's goal definition
    goal_categories = models.JSONField()  # ["breaking_habit", "relationship_repair"]
    goal_statement = models.TextField()  # Their words
    success_definition = models.TextField()  # What does "done" look like?
    focus_areas = models.JSONField()  # ["self_control", "relationships"]
    
    # Optional: specific thing they're working on (encrypted for privacy)
    encrypted_specific_struggle = models.BinaryField(null=True)
    
    # Reading plan
    reading_mode = models.CharField(max_length=20)  # 'ai_suggested', 'self_directed', 'hybrid'
    reading_plan = models.ForeignKey(ReadingPlan, null=True, blank=True)
    custom_readings = models.JSONField(default=list)  # If not using a plan
    
    # Progress
    current_day = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True)
    
    # Outcome
    completion_reflection = models.TextField(blank=True)
    next_journey = models.ForeignKey('self', null=True, blank=True)  # Chain journeys
```

### 3. DailyReflection (User's Evening Entry)

```python
class DailyReflection(models.Model):
    """
    User's end-of-day reflection tied to their scripture reading.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journey = models.ForeignKey(UserJourney, null=True, blank=True)
    date = models.DateField()
    
    # Link to what they read
    scripture_reference = models.CharField(max_length=200)
    scripture_themes = models.JSONField()  # AI-extracted: ["trust", "guidance"]
    
    # Free-form reflection (encrypted)
    encrypted_reflection = models.BinaryField()
    
    # Life area self-assessments (1-5 scale)
    area_scores = models.JSONField()
    # Example: {"integrity": 4, "faith": 3, "self_control": 2}
    
    # Quick prompts
    gratitude_note = models.TextField(blank=True)
    struggle_note = models.TextField(blank=True)
    tomorrow_intention = models.TextField(blank=True)
    
    # AI insight (generated weekly, not daily)
    ai_insight = models.TextField(blank=True)
    ai_provider_used = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
```

**Area Score Scale:**

| Score | Meaning |
|-------|---------|
| 1 | Completely missed the mark |
| 2 | Struggled significantly |
| 3 | Mixed - some wins, some failures |
| 4 | Lived it out mostly well |
| 5 | Fully aligned with scripture |

### 4. AlignmentTrend (Aggregated Analytics)

```python
class AlignmentTrend(models.Model):
    """
    Weekly/monthly aggregated alignment scores per life area.
    Computed by Celery task, not real-time.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journey = models.ForeignKey(UserJourney, null=True, blank=True)
    
    period_type = models.CharField(max_length=10)  # 'week' or 'month'
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Aggregated scores per area
    area_averages = models.JSONField()
    # Example: {"integrity": 3.5, "faith": 4.2, "self_control": 2.8}
    
    # Change from previous period
    area_deltas = models.JSONField()
    # Example: {"integrity": +0.3, "faith": -0.1, "self_control": +0.5}
    
    # AI Crew generated summary
    ai_summary = models.TextField(blank=True)
    
    # Patterns detected
    patterns = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
```

### 5. AIProviderConfig (User's AI Preferences)

```python
class AIProviderConfig(models.Model):
    """
    User's AI backend configuration.
    Allows users to bring their own AI.
    """
    PROVIDER_CHOICES = [
        ('system_ollama', 'System Default (Homelab Ollama)'),
        ('user_ollama', 'My Ollama Instance'),
        ('openai', 'OpenAI API'),
        ('anthropic', 'Anthropic Claude'),
        ('openrouter', 'OpenRouter (Multiple Models)'),
        ('groq', 'Groq (Fast Inference)'),
        ('local_llamacpp', 'Local llama.cpp Server'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES, default='system_ollama')
    encrypted_api_key = models.BinaryField(null=True, blank=True)
    base_url = models.URLField(blank=True)
    model_name = models.CharField(max_length=100, blank=True)
    
    # Fallback to system if user's provider fails
    fallback_to_system = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## Open Threads Accountability System

### Concept

When a user mentions something they're struggling with, working on, or want to address, the system captures it as an **Open Thread**. The AI ensures nothing falls through the cracks.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      OPEN THREADS LIFECYCLE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   USER MENTIONS              SYSTEM TRACKS              FOLLOW-UP        │
│   ─────────────              ─────────────              ─────────        │
│                                                                          │
│   "I've been              ┌─────────────────┐                           │
│    struggling with   ───▶ │  OPEN THREAD    │                           │
│    my temper lately"      │  Status: open   │                           │
│                           │  Days: 0        │                           │
│                           └────────┬────────┘                           │
│                                    │                                     │
│   Day 3: No mention                │                                     │
│                           ┌────────▼────────┐                           │
│   Pop-up prompt:          │  FOLLOW-UP      │                           │
│   "How's your temper  ◀───│  TRIGGERED      │                           │
│    going?"                └────────┬────────┘                           │
│                                    │                                     │
│   User responds:                   │                                     │
│   "Better" ────────────────────────┼──▶ Log progress                    │
│   "Same" ──────────────────────────┼──▶ Keep tracking                   │
│   "Worse" ─────────────────────────┼──▶ Flag for weekly review          │
│   "Skip" ──────────────────────────┼──▶ Defer (3 skips = auto-defer)    │
│                                    │                                     │
│   "Mark Resolved" ─────────────────┴──▶ Close thread, celebrate         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### OpenThread Model

```python
class OpenThread(models.Model):
    """
    Tracks unresolved topics, struggles, or commitments the user has mentioned.
    """
    THREAD_TYPE_CHOICES = [
        ('struggle', 'Struggle/Challenge'),
        ('commitment', 'Commitment Made'),
        ('question', 'Unanswered Question'),
        ('relationship', 'Relationship Issue'),
        ('decision', 'Pending Decision'),
        ('confession', 'Something Shared'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open - Active'),
        ('following_up', 'Following Up'),
        ('progressing', 'User Reports Progress'),
        ('resolved', 'Resolved'),
        ('deferred', 'User Chose to Defer'),
        ('dropped', 'User Chose to Drop'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journey = models.ForeignKey(UserJourney, null=True, blank=True)
    
    # What was mentioned
    thread_type = models.CharField(max_length=20, choices=THREAD_TYPE_CHOICES)
    encrypted_summary = models.BinaryField()  # Brief summary
    encrypted_original_context = models.BinaryField()  # Full original text
    related_life_area = models.CharField(max_length=20, blank=True)
    
    # Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    last_mentioned_at = models.DateTimeField(auto_now_add=True)
    last_followup_at = models.DateTimeField(null=True, blank=True)
    
    # Follow-up settings
    followup_after_days = models.PositiveIntegerField(default=3)
    followup_count = models.PositiveIntegerField(default=0)
    max_followups = models.PositiveIntegerField(default=3)
    skip_count = models.PositiveIntegerField(default=0)
    
    # Resolution
    resolved_at = models.DateTimeField(null=True, blank=True)
    encrypted_resolution_note = models.BinaryField(null=True, blank=True)
    
    @property
    def days_since_mentioned(self):
        return (timezone.now() - self.last_mentioned_at).days
    
    @property
    def needs_followup(self):
        if self.status not in ['open', 'following_up']:
            return False
        if self.followup_count >= self.max_followups:
            return False
        if self.skip_count >= 3:  # Auto-defer after 3 skips
            return False
        return self.days_since_mentioned >= self.followup_after_days
```

### ThreadPrompt Model

```python
class ThreadPrompt(models.Model):
    """
    Quick check-in prompts shown to user during journal entry.
    """
    RESPONSE_CHOICES = [
        ('better', 'Better'),
        ('same', 'Same'),
        ('worse', 'Worse'),
        ('yes', 'Yes'),
        ('no', 'No'),
        ('skipped', 'Skipped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    thread = models.ForeignKey(OpenThread, on_delete=models.CASCADE)
    reflection = models.ForeignKey(DailyReflection, on_delete=models.CASCADE)
    
    prompt_text = models.CharField(max_length=200)
    response = models.CharField(max_length=20, choices=RESPONSE_CHOICES, null=True)
    
    # Did they choose to write more?
    expanded = models.BooleanField(default=False)
    encrypted_expanded_response = models.BinaryField(null=True, blank=True)
    
    shown_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
```

### Thread Detection (AI Task)

```python
THREAD_DETECTION_PROMPT = """
Analyze this user reflection for significant topics that should be tracked:

USER'S REFLECTION:
{reflection_text}

STRUGGLE NOTED: {struggle_note}

Look for:
1. STRUGGLES: Things they're battling ("I've been struggling with...", "I can't seem to...")
2. COMMITMENTS: Things they're committing to ("I'm going to...", "Starting tomorrow...")
3. RELATIONSHIP ISSUES: People/relationships with tension ("My wife and I...", "My son...")
4. DECISIONS: Choices they're wrestling with ("I don't know if I should...")
5. CONFESSIONS: Vulnerable shares ("I haven't told anyone...", "The truth is...")

For each significant item found, return:
{
    "threads": [
        {
            "type": "struggle|commitment|relationship|decision|confession",
            "summary": "Brief 10-word summary",
            "life_area": "integrity|relationships|work|self_control|faith|service|growth",
            "quote": "Exact words from their reflection"
        }
    ]
}

If nothing significant, return: {"threads": []}
Be selective - not every mention is a thread.
"""
```

### Follow-up Rules

| Scenario | Behavior |
|----------|----------|
| Thread open, no mention for 3+ days | Show pop-up prompt |
| User responds "Better" | Log progress, offer to close |
| User responds "Same" | Keep tracking |
| User responds "Worse" | Flag for weekly review attention |
| User clicks "Skip" | Increment skip count |
| 3 skips | Auto-defer thread for 2 weeks |
| User marks "Resolved" | Close thread, celebrate in weekly review |
| 3 follow-ups with no engagement | Auto-defer |

---

## Pop-up Thread Reminders UX

### Flow: Journal Entry with Thread Prompts

When user opens evening reflection, show quick check-ins for open threads:

```
┌───────────────────────────────────────────────────────────────────┐
│ QUICK CHECK-IN                                          [1 of 2] │
│ ─────────────────────────────────────────────────────────────────│
│                                                                   │
│  You mentioned struggling with your temper (5 days ago)          │
│                                                                   │
│  How's that going?                                               │
│                                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │ Better  │  │ Same    │  │ Worse   │  │ Skip    │             │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘             │
│                                                                   │
│  [Want to write more about this?]  ○ Yes  ● No                   │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### Thread-Specific Quick Prompts

| Thread Type | Quick Prompt | Response Options |
|-------------|--------------|------------------|
| **Struggle** | "How's [X] going?" | Better / Same / Worse / Skip |
| **Commitment** | "Did you [X] today?" | Yes / No / Skip |
| **Relationship** | "Any progress with [person]?" | Yes / Not yet / Skip |
| **Decision** | "Made a decision on [X]?" | Yes / Still thinking / Skip |

### Journal Field Injection

If user clicks "Yes, I want to write more", inject a prompt into the journal:

```
┌─────────────────────────────────────────────────────────────────┐
│ 📌 THREAD PROMPT: Your temper                                    │
│ ───────────────────────────────────────────────────────────────  │
│ You said it's [better/same/worse]. What happened?               │
│                                                                  │
│ ┌───────────────────────────────────────────────────────────┐   │
│ │                                                            │   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                    [Remove]     │
└─────────────────────────────────────────────────────────────────┘
```

### Rules for Showing Prompts

1. **Max 2 prompts per session** - Don't overwhelm
2. **Prioritize by age** - Oldest unaddressed threads first
3. **Rotate if skipped** - Don't show same thread next day
4. **Respect "defer"** - Deferred threads don't prompt for 2 weeks
5. **Celebrate resolution** - Offer to close if "Better" + expanded response

---

## AI Crew Architecture

### Crew Overview

A CrewAI-based system with specialized agents that provide multi-perspective guidance.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DEVOTIONAL GUIDANCE CREW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  SCRIPTURE  │  │   MENTOR    │  │  PATTERN    │  │  JOURNEY    │    │
│  │  SCHOLAR    │  │   AGENT     │  │  ANALYST    │  │  GUIDE      │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │                │            │
│         ▼                ▼                ▼                ▼            │
│  "Here's what      "Here's how      "I notice you     "Based on your   │
│   scripture says    a wise older     struggle on       goal, here's     │
│   about this..."    man might        Fridays..."       your progress"   │
│                     approach this"                                       │
│                                                                          │
│                         ┌─────────────┐                                 │
│                         │ COORDINATOR │                                 │
│                         │   AGENT     │                                 │
│                         └─────────────┘                                 │
│                               │                                         │
│                               ▼                                         │
│                    Unified, coherent guidance                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Role | Personality |
|-------|------|-------------|
| **Scripture Scholar** | Biblical context, relevant passages | Academic but accessible, not preachy |
| **Mentor Agent** | Practical life wisdom | Direct, warm, experienced - like a trusted older brother |
| **Pattern Analyst** | Detects trends, identifies triggers | Observational, data-driven, non-judgmental |
| **Journey Guide** | Tracks goal progress, manages open threads | Encouraging, focused, accountability |
| **Coordinator** | Synthesizes into coherent guidance | Balanced, concise (max 150 words) |

### Crew Schedule

| Frequency | What Runs | Purpose |
|-----------|-----------|---------|
| **Daily** | Thread Detection only | Scan reflections for new threads (lightweight) |
| **Weekly (Sunday)** | Full Crew Review | Pattern analysis, thread follow-ups, week summary |
| **Monthly (1st)** | Monthly Recap | Trend analysis, threads resolved, growth areas |
| **On-demand** | User requests insight | Full crew analysis of specific question |

### Example Crew Output (Weekly Review)

```
COORDINATOR OUTPUT:

This week you read through Proverbs 4 - "guard your heart" hit close 
to home given what you're working on.

I noticed Fridays are still your hardest nights - 3 of the last 4 
weeks show the same pattern. You're not weak; you're tired and alone, 
which is when every man is most vulnerable.

You're 9 for 12 days so far - that's 75%. Real progress.

One thought: What if you planned something specific for Friday evening 
before it arrives? Not willpower in the moment, but a different 
situation entirely.

What could Friday night look like if you designed it intentionally?
```

### CrewAI Implementation

```python
class DevotionalCrew:
    """AI Crew for personalized devotional guidance."""
    
    def __init__(self, llm_base_url: str, model: str):
        self.llm = Ollama(base_url=llm_base_url, model=model)
        self._create_agents()
    
    def _create_agents(self):
        self.scripture_scholar = Agent(
            role="Scripture Scholar",
            goal="Provide biblical context and relevant passages",
            backstory="""You are a biblical scholar who makes scripture accessible. 
            You understand Hebrew and Greek context but explain things simply. 
            You never preach - you illuminate.""",
            llm=self.llm
        )
        
        self.mentor = Agent(
            role="Wise Mentor",
            goal="Offer practical life wisdom",
            backstory="""You are a man who has lived through struggles - addiction, 
            divorce, career failure, rebuilding. You speak from experience, not theory. 
            You're direct but kind. You never shame.""",
            llm=self.llm
        )
        
        self.pattern_analyst = Agent(
            role="Pattern Analyst",
            goal="Identify trends, triggers, and patterns",
            backstory="""You analyze behavioral patterns without judgment. You notice 
            what the user might not see - timing, triggers, correlations.""",
            llm=self.llm
        )
        
        self.journey_guide = Agent(
            role="Journey Guide",
            goal="Track goal progress, manage open threads, suggest next steps",
            backstory="""You are an accountability partner who remembers the user's 
            goal and gently keeps them oriented toward it. You track open threads 
            and ensure nothing falls through the cracks.""",
            llm=self.llm
        )
        
        self.coordinator = Agent(
            role="Guidance Coordinator",
            goal="Synthesize insights into coherent, actionable guidance",
            backstory="""You take multiple perspectives and weave them into a single, 
            unified message. You're concise - never more than 150 words. You end with 
            a question or gentle challenge, not a lecture.""",
            llm=self.llm
        )
    
    def generate_weekly_review(self, context: dict) -> str:
        """Generate weekly review with full crew."""
        # ... crew task orchestration
        pass
    
    def generate_monthly_recap(self, context: dict) -> str:
        """Generate monthly recap with trend analysis."""
        # ... crew task orchestration
        pass
    
    def detect_threads(self, reflection_text: str) -> list[dict]:
        """Lightweight thread detection (runs daily)."""
        # ... single agent task
        pass
```

### Personality Customization (Future)

Reserved for future iterations. Architecture supports:
- Adjustable agent personalities
- User preference for tone (more direct, less religious language, etc.)
- Conversation mode (back-and-forth with crew)

---

## AI Provider Integration

### Provider Abstraction Layer

```python
class AIProvider(ABC):
    """Abstract base for all AI providers."""
    
    @abstractmethod
    def generate(self, prompt: str, system: str = None) -> str:
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        pass


class SystemOllamaProvider(AIProvider):
    """Homelab Ollama - always available as fallback."""
    base_url = "http://100.114.78.21:11434"  # Rincewind
    model = "llama3.1:8b"


class UserOllamaProvider(AIProvider):
    """User's own Ollama instance."""
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model


class OpenAIProvider(AIProvider):
    """OpenAI API integration."""
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model


def get_ai_provider(user: User) -> AIProvider:
    """Factory function to get user's configured provider."""
    config = AIProviderConfig.objects.filter(user=user).first()
    
    if not config or config.provider == 'system_ollama':
        return SystemOllamaProvider()
    
    try:
        provider = _create_provider(config)
        if provider.health_check():
            return provider
    except Exception:
        pass
    
    if config.fallback_to_system:
        return SystemOllamaProvider()
    
    raise AIProviderUnavailable("User's AI provider is not accessible")
```

---

## User Experience Flows

### Morning (5 min)

1. Open app → See today's scripture
2. Read passage (can switch translations)
3. See AI-extracted themes
4. Optional: Write morning intention

### Evening (5-10 min)

1. Open app → **Pop-up thread check-ins** (max 2)
2. Review today's scripture themes
3. Free-form reflection (encrypted)
4. Rate relevant life areas (1-5)
5. Quick prompts:
   - "What are you grateful for?"
   - "Where did you struggle?"
   - "What's one intention for tomorrow?"
6. Submit → Thread detection runs in background

### Weekly (Sunday)

1. **AI Crew generates weekly review**
2. See week's alignment trends (charts)
3. Review patterns detected
4. Open threads status
5. Set focus area for next week

### Monthly (1st of month)

1. **AI Crew generates monthly recap**
2. Trend analysis across the month
3. Threads resolved this month
4. Growth areas highlighted
5. Suggested focus for next month

---

## API Endpoints

### Journey Endpoints
```
POST   /api/v1/journeys/                       # Create new journey
GET    /api/v1/journeys/                       # List user's journeys
GET    /api/v1/journeys/active/                # Get active journey
GET    /api/v1/journeys/{id}/                  # Get specific journey
PATCH  /api/v1/journeys/{id}/                  # Update journey
POST   /api/v1/journeys/{id}/complete/         # Mark journey complete
```

### Reflection Endpoints
```
GET    /api/v1/reflections/today/              # Get today's entry + thread prompts
POST   /api/v1/reflections/                    # Create daily reflection
GET    /api/v1/reflections/                    # List user's reflections
GET    /api/v1/reflections/{date}/             # Get specific day
PATCH  /api/v1/reflections/{date}/             # Update reflection
```

### Thread Endpoints
```
GET    /api/v1/threads/                        # List open threads
GET    /api/v1/threads/{id}/                   # Get specific thread
POST   /api/v1/threads/{id}/respond/           # Respond to thread prompt
POST   /api/v1/threads/{id}/resolve/           # Mark thread resolved
POST   /api/v1/threads/{id}/defer/             # Defer thread
POST   /api/v1/threads/{id}/drop/              # Drop thread
```

### AI Endpoints
```
POST   /api/v1/ai/extract-themes/              # Extract themes from scripture
GET    /api/v1/ai/weekly-review/               # Get/generate weekly review
GET    /api/v1/ai/monthly-recap/               # Get/generate monthly recap
POST   /api/v1/ai/health-check/                # Test AI provider connection
```

### Configuration Endpoints
```
GET    /api/v1/ai/config/                      # Get user's AI config
PUT    /api/v1/ai/config/                      # Update AI config
POST   /api/v1/ai/config/test/                 # Test provider connection
```

### Analytics Endpoints
```
GET    /api/v1/analytics/trends/               # Get alignment trends
GET    /api/v1/analytics/trends/{area}/        # Trends for specific area
GET    /api/v1/analytics/export/               # Export all data
```

---

## Implementation Phases

### Phase 1: Core Reflection (MVP)
- [ ] LifeArea model + seed data
- [ ] UserJourney model
- [ ] DailyReflection model
- [ ] Basic CRUD API
- [ ] Theme extraction (system Ollama only)

### Phase 2: Open Threads System
- [ ] OpenThread model
- [ ] ThreadPrompt model
- [ ] Thread detection (daily Celery task)
- [ ] Pop-up prompt API
- [ ] Thread response handling

### Phase 3: AI Crew (Weekly/Monthly)
- [ ] CrewAI integration
- [ ] Weekly review generation (Sunday task)
- [ ] Monthly recap generation (1st of month task)
- [ ] AlignmentTrend model + computation

### Phase 4: User AI Integration
- [ ] AIProviderConfig model
- [ ] Provider abstraction layer
- [ ] OpenAI, Anthropic, user Ollama support
- [ ] Health check and fallback logic

### Phase 5: Frontend Integration
- [ ] Journey setup flow
- [ ] Daily reflection with thread prompts
- [ ] Weekly/monthly review display
- [ ] Thread management UI
- [ ] Trend visualization

---

## Privacy & Security

### Data Encryption
- All reflection content encrypted at rest (user's encryption key)
- Open thread summaries encrypted
- AI provider API keys encrypted

### Data Ownership
- User can export all their data (JSON)
- User can delete all data permanently
- No data shared with third parties
- AI providers only see current context, not history

### AI Privacy Options

| Setting | Behavior |
|---------|----------|
| `system_only` | Only homelab Ollama, never external |
| `user_provider` | User's configured provider, fallback to system |
| `no_ai` | Disable all AI features, manual reflection only |

---

## AI Agent Health Check System

### Deployment Modes

The system supports two deployment modes to separate your personal homelab infrastructure from public distribution:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Standalone** | Self-contained health checks, local alerts only | Public users installing on their own machines |
| **Homelab** | Full Rincewind agent integration with autonomous remediation | Your environment only (curlyphries homelab) |

Mode is set via environment variable:
```bash
HEALTH_CHECK_MODE=standalone  # Default for public users
HEALTH_CHECK_MODE=homelab     # Your environment only
```

---

### Standalone Mode (Default - Public Users)

Self-contained health monitoring with no external dependencies.

**Features:**
- Health checks run locally every 5 minutes
- Failures logged to application logs
- Optional email alerts (if SMTP configured)
- Optional webhook alerts (Discord, Slack, etc.)
- No Rincewind/Zammad integration

**Configuration:**
```python
# .env for standalone users
HEALTH_CHECK_MODE=standalone
HEALTH_ALERT_EMAIL=user@example.com      # Optional
HEALTH_ALERT_WEBHOOK=https://...         # Optional (Discord, Slack)
HEALTH_ALERT_LOG_ONLY=true               # Default: just log failures
```

**Health Check Components (Standalone):**

| Component | Check Method | Healthy Criteria | Alert Action |
|-----------|--------------|------------------|--------------|
| **User's Ollama** | `GET /api/tags` | Response < 10s | Log + optional email/webhook |
| **Celery Workers** | `celery inspect ping` | Workers respond | Log + optional email/webhook |
| **Redis** | `PING` | Response OK | Log + optional email/webhook |
| **Database** | Simple query | Query succeeds | Log + optional email/webhook |

**Standalone Alert Service:**
```python
class StandaloneAlertService:
    """Alert service for standalone deployments."""
    
    def send_alert(self, incident: dict):
        """Send alert via configured channels."""
        # Always log
        logger.error(f"Health check failed: {incident}")
        
        # Optional email
        if settings.HEALTH_ALERT_EMAIL:
            self._send_email_alert(incident)
        
        # Optional webhook (Discord, Slack, etc.)
        if settings.HEALTH_ALERT_WEBHOOK:
            self._send_webhook_alert(incident)
    
    def _send_email_alert(self, incident: dict):
        send_mail(
            subject=f"[Devotional Journal] {incident['component']} Health Check Failed",
            message=f"Component: {incident['component']}\nError: {incident['error']}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.HEALTH_ALERT_EMAIL],
        )
    
    def _send_webhook_alert(self, incident: dict):
        httpx.post(settings.HEALTH_ALERT_WEBHOOK, json={
            "content": f"⚠️ Health Check Failed: {incident['component']}",
            "embeds": [{
                "title": incident['component'],
                "description": incident['error'],
                "color": 15158332  # Red
            }]
        })
```

---

### Homelab Mode (Your Environment Only)

Full integration with your Rincewind AI agent stack for autonomous remediation.

**Requirements (your infrastructure only):**
- Rincewind Agent API: `http://100.114.78.21:8101/api`
- Plex Agent (Zammad): `http://100.106.22.80:8100/api`
- System Ollama: `http://100.114.78.21:11434`

**Configuration:**
```python
# .env for your homelab
HEALTH_CHECK_MODE=homelab
RINCEWIND_API_URL=http://100.114.78.21:8101/api
PLEX_AGENT_URL=http://100.106.22.80:8100/api
SYSTEM_OLLAMA_URL=http://100.114.78.21:11434
```

**Health Check Flow (Homelab):**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HOMELAB HEALTH CHECK FLOW                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Every 5 minutes         ┌─────────────────┐                           │
│   ┌─────────────┐         │  Health Check   │                           │
│   │ Health      │────────▶│  Results        │                           │
│   │ Monitor     │         │                 │                           │
│   └─────────────┘         │  ✓ Ollama: OK   │                           │
│                           │  ✗ Crew: FAIL   │                           │
│                           │  ✓ Celery: OK   │                           │
│                           └────────┬────────┘                           │
│                                    │                                     │
│                           Failure detected                               │
│                                    │                                     │
│                           ┌────────▼────────┐                           │
│                           │  Rincewind      │                           │
│                           │  Agent API      │                           │
│                           │  POST /api/     │                           │
│                           │  incidents      │                           │
│                           └────────┬────────┘                           │
│                                    │                                     │
│                           ┌────────▼────────┐                           │
│                           │  Autonomous     │                           │
│                           │  Remediation    │                           │
│                           │  - Restart svc  │                           │
│                           │  - Clear cache  │                           │
│                           │  - Alert admin  │                           │
│                           └─────────────────┘                           │
│                                                                          │
│   If Rincewind unreachable → Fallback to Zammad ticket                  │
│   If Zammad unreachable → Log critical error                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Health Check Components (Homelab):**

| Component | Check Method | Healthy Criteria | Remediation |
|-----------|--------------|------------------|-------------|
| **System Ollama** | `GET /api/tags` | Response < 5s, model available | Restart ollama service |
| **CrewAI Agents** | Test inference | Each agent responds | Restart devotional-crew service |
| **Celery Workers** | `celery inspect ping` | Workers respond | Restart celery workers |
| **Redis** | `PING` | Response OK | Restart redis service |
| **Database** | Simple query | Query succeeds | Alert admin (no auto-restart) |

**Homelab Health Service:**
```python
class HomelabHealthService:
    """Health service with Rincewind integration."""
    
    RINCEWIND_API = settings.RINCEWIND_API_URL
    PLEX_AGENT_API = settings.PLEX_AGENT_URL
    
    def _escalate_to_rincewind(self, health_check: AgentHealthCheck):
        """Escalate to Rincewind for autonomous remediation."""
        severity = 'high' if health_check.component == 'system_ollama' else 'medium'
        
        incident = AgentIncident.objects.create(
            component=health_check.component,
            health_check=health_check,
            severity=severity,
            status='escalated',
            description=f"{health_check.component} failed: {health_check.error_message}",
            escalated_at=timezone.now()
        )
        
        # Determine remediation action
        remediation_map = {
            'system_ollama': 'restart_service:ollama',
            'celery_workers': 'restart_service:devotional-celery',
            'redis': 'restart_service:redis',
            'crew_': 'restart_service:devotional-crew',
        }
        
        action = next(
            (cmd for prefix, cmd in remediation_map.items() 
             if health_check.component.startswith(prefix)), 
            None
        )
        
        try:
            response = httpx.post(
                f"{self.RINCEWIND_API}/incidents",
                json={
                    "source": "devotional-journal",
                    "component": health_check.component,
                    "severity": severity,
                    "description": incident.description,
                    "suggested_action": action,
                    "incident_id": str(incident.id),
                },
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()
            
            incident.rincewind_ticket_id = result.get('ticket_id', '')
            incident.remediation_action = action
            incident.status = 'remediating'
            incident.save()
            
        except Exception as e:
            # Fallback to Zammad
            incident.status = 'failed'
            incident.remediation_result = f"Rincewind unreachable: {e}"
            incident.save()
            self._create_zammad_ticket(incident)
    
    def _create_zammad_ticket(self, incident: AgentIncident):
        """Fallback: Create Zammad ticket via Plex Agent."""
        try:
            httpx.post(
                f"{self.PLEX_AGENT_API}/tickets/create",
                json={
                    "title": f"[AUTO] {incident.component} Health Check Failed",
                    "body": f"Component: {incident.component}\n"
                            f"Severity: {incident.severity}\n"
                            f"Description: {incident.description}\n\n"
                            f"Rincewind was unreachable. Manual intervention required.",
                    "priority": "high" if incident.severity in ['high', 'critical'] else "normal",
                    "source": "devotional-journal-health-monitor"
                },
                timeout=10.0
            )
        except Exception:
            logger.critical(f"ALL ESCALATION FAILED: {incident}")
```

**Service Registration (Homelab Only):**
```python
def register_with_rincewind():
    """Register this service with Rincewind for monitoring."""
    if settings.HEALTH_CHECK_MODE != 'homelab':
        return
    
    try:
        httpx.post(
            f"{settings.RINCEWIND_API_URL}/services/register",
            json={
                "service_name": "devotional-journal",
                "health_endpoint": "http://devotional.homelab.local/api/v1/health/",
                "components": [
                    "system_ollama", "crew_scripture_scholar", "crew_mentor",
                    "crew_pattern_analyst", "crew_journey_guide", "crew_coordinator",
                    "celery_workers", "redis"
                ],
                "remediation_actions": {
                    "restart_service:ollama": "sudo systemctl restart ollama",
                    "restart_service:devotional-celery": "docker compose restart celery",
                    "restart_service:redis": "docker compose restart redis",
                    "restart_service:devotional-crew": "docker compose restart web"
                }
            },
            timeout=10.0
        )
    except Exception as e:
        logger.warning(f"Failed to register with Rincewind: {e}")
```

---

### Data Models (Both Modes)

```python
class AgentHealthCheck(models.Model):
    """Records health check results."""
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('degraded', 'Degraded'),
        ('unhealthy', 'Unhealthy'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    component = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response_time_ms = models.IntegerField(null=True)
    error_message = models.TextField(blank=True)
    details = models.JSONField(default=dict)
    checked_at = models.DateTimeField(auto_now_add=True)


class AgentIncident(models.Model):
    """Tracks incidents (homelab mode only uses full fields)."""
    SEVERITY_CHOICES = [
        ('low', 'Low'), ('medium', 'Medium'), 
        ('high', 'High'), ('critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('detected', 'Detected'), ('escalated', 'Escalated'),
        ('remediating', 'Remediating'), ('resolved', 'Resolved'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    component = models.CharField(max_length=50)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    description = models.TextField()
    
    # Homelab-only fields
    rincewind_ticket_id = models.CharField(max_length=100, blank=True)
    remediation_action = models.CharField(max_length=100, blank=True)
    remediation_result = models.TextField(blank=True)
    
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True)
```

---

### Health Check API Endpoints

```
GET    /api/v1/health/                         # Overall system health
GET    /api/v1/health/agents/                  # All agent health status
GET    /api/v1/health/incidents/               # Recent incidents
POST   /api/v1/health/check/                   # Trigger manual health check
```

---

### Celery Task

```python
@shared_task
def run_agent_health_checks():
    """Periodic health check task - runs every 5 minutes."""
    if settings.HEALTH_CHECK_MODE == 'homelab':
        service = HomelabHealthService()
    else:
        service = StandaloneHealthService()
    
    results = service.run_all_checks()
    healthy = sum(1 for r in results if r.status == 'healthy')
    
    if healthy < len(results):
        logger.warning(f"Health: {healthy}/{len(results)} components healthy")
    
    return {'healthy': healthy, 'total': len(results)}
```

---

## Technical Notes

### Homelab Integration (Your Environment Only)
- System Ollama: `http://100.114.78.21:11434` (Rincewind, llama3.1:8b)
- Rincewind Agent API: `http://100.114.78.21:8101/api`
- Plex Agent (Zammad): `http://100.106.22.80:8100/api`

### Standalone Defaults (Public Users)
- User configures their own Ollama URL
- No external agent dependencies
- Optional email/webhook alerts

### Celery Tasks
- `detect_threads` - Runs after each reflection submission
- `compute_weekly_trends` - Runs Sunday midnight
- `generate_weekly_review` - Runs Sunday after trends
- `generate_monthly_recap` - Runs 1st of month
- `cleanup_old_ai_cache` - Runs daily
- `run_agent_health_checks` - Runs every 5 minutes

### Encryption
- Uses existing `shared.encryption` module
- User's `encryption_key_salt` for all personal data

---

## Design Decisions Log

| Decision | Rationale |
|----------|-----------|
| Weekly AI insights, not daily | Respects user's time, more meaningful patterns |
| User-driven goals, not prescriptive plans | Personal ownership increases engagement |
| Open Threads system | Ensures accountability without nagging |
| Max 2 pop-up prompts per session | Prevents overwhelm |
| 3 skips = auto-defer | Respects user's choice not to engage |
| Personality customization deferred | Keep MVP simple, add later |
| Conversation mode deferred | Keep MVP simple, add later |

---

*Document Version: 2.0*  
*Created: March 31, 2026*  
*Status: FINAL DESIGN - Ready for Implementation*
