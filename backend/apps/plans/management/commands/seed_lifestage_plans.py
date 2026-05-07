"""
Seed life-stage and topical reading plans.

Each plan is hand-curated. Days are tuples of:
    (day_number, theme_en, theme_es, [passage_refs], [prompts_en])

theme_es is provided so navigation/snapshot displays in Spanish.
reflection_prompts_es is intentionally left empty for now and will be
filled in a content-translation pass.
"""

from django.core.management.base import BaseCommand

from apps.plans.models import ReadingPlan, ReadingPlanDay


def create_plan(slug, title_en, title_es, description_en, description_es,
                duration_days, category, days):
    """
    Idempotent plan creation.
    `days` is a list of tuples: (day_num, theme_en, theme_es, passages, prompts_en).
    """
    plan, created = ReadingPlan.objects.get_or_create(
        title_en=title_en,
        defaults={
            "title_es": title_es,
            "description_en": description_en,
            "description_es": description_es,
            "duration_days": duration_days,
            "category": category,
            "is_premium": False,
            "is_active": True,
            "is_public": True,
        },
    )
    if not created:
        return plan, False

    for day_num, theme_en, theme_es, passages, prompts in days:
        ReadingPlanDay.objects.create(
            plan=plan,
            day_number=day_num,
            theme_en=theme_en,
            theme_es=theme_es,
            passages=passages,
            reflection_prompts=prompts,
        )
    return plan, True


# ---------------------------------------------------------------------------
# 1. FAITH FOUNDATIONS — Owned Faith
# ---------------------------------------------------------------------------
OWNED_FAITH = [
    (1, "Inherited vs. Owned Faith", "Fe heredada vs. fe propia",
     ["Acts 17:10-12", "2 Timothy 1:5"],
     ["Whose faith are you living right now — yours, your parents', or your church's?",
      "What part of your faith do you only believe because someone told you to?",
      "What is one belief you have never personally tested in scripture?"]),
    (2, "Examining the Foundation", "Examinando los cimientos",
     ["Matthew 7:24-27", "1 Corinthians 3:10-15"],
     ["If everything you currently believe was stripped away, what would you rebuild on?",
      "Where do you sense your foundation is sand instead of rock?",
      "Which doctrine is the hardest for you to actually trust?"]),
    (3, "Doubt Is Not the Enemy", "La duda no es el enemigo",
     ["Mark 9:14-29", "Jude 1:22"],
     ["What doubt have you been afraid to name out loud?",
      "Who in your life is safe to doubt with — without being shamed?",
      "How does Jesus respond to the father's 'I believe — help my unbelief'?"]),
    (4, "Why Jesus, Not Just God?", "¿Por qué Jesús, no solo Dios?",
     ["John 14:1-11", "Hebrews 1:1-3"],
     ["Why do you (or don't you) believe Jesus is uniquely God?",
      "If Jesus is the exact representation of God, what does that change about how you see God?",
      "What would it cost you to follow Jesus specifically — not just be 'spiritual'?"]),
    (5, "The Cross at the Center", "La cruz en el centro",
     ["1 Corinthians 15:1-11", "Romans 5:6-11"],
     ["What did the cross actually accomplish — and have you received it personally?",
      "How does 'while we were still sinners' confront the way you try to earn God's love?",
      "What in your life are you still trying to atone for that Jesus already paid for?"]),
    (6, "Resurrection Changes Everything", "La resurrección lo cambia todo",
     ["1 Corinthians 15:12-28", "Acts 26:1-8"],
     ["If Jesus didn't rise, what's the worst-case truth about your life?",
      "If he did rise, what's the worst-case truth about how you're living now?",
      "What dead thing in your life needs resurrection power, not just self-help?"]),
    (7, "Repentance Is a Daily Posture", "El arrepentimiento es una postura diaria",
     ["2 Corinthians 7:8-11", "Acts 3:19-20"],
     ["What's the difference between worldly sorrow (regret) and godly sorrow (repentance)?",
      "What is one specific thing today you need to turn from?",
      "Where have you confused 'feeling bad' with actually changing direction?"]),
    (8, "Faith Is Not Feeling", "La fe no es un sentimiento",
     ["Hebrews 11:1-12", "Romans 4:13-25"],
     ["When did you last act in faith without feeling it?",
      "What would it look like this week to obey God when your emotions disagree?",
      "Where has waiting for the right feeling kept you stuck?"]),
    (9, "Belonging Before Behaving", "Pertenecer antes de comportarse",
     ["Romans 8:14-17", "1 John 3:1-3"],
     ["Do you relate to God more like a son/daughter or like an employee?",
      "How would today look different if you actually believed you were already loved?",
      "What disciplines change when belonging — not earning — is the foundation?"]),
    (10, "Walking It Out", "Caminándolo",
     ["Philippians 2:12-13", "Colossians 2:6-7"],
     ["What is the next obedient step that you have been avoiding?",
      "Who can walk this with you — and what are you going to ask them this week?",
      "What rhythm of grace do you need to put in place starting tomorrow?"]),
]


# ---------------------------------------------------------------------------
# 2. SPIRITUAL DISCIPLINES — Seven for the Long Haul
# ---------------------------------------------------------------------------
DISCIPLINES = [
    (1, "Prayer — The Practice of Presence", "Oración — La práctica de la presencia",
     ["Matthew 6:5-15", "Luke 11:1-13"],
     ["When did prayer last feel like presence rather than performance?",
      "What part of the Lord's Prayer exposes how you actually pray?",
      "What is one specific thing you will ask God for, daily, this week?"]),
    (2, "Scripture Meditation — Slow Reading", "Meditación bíblica — Lectura lenta",
     ["Psalm 1", "Joshua 1:8"],
     ["What does it mean to 'meditate day and night' on something — and when do you do that with anything?",
      "Pick one verse today. What happens when you read it 5 times slowly?",
      "Where is your fastest area of life that needs the slowest reading?"]),
    (3, "Fasting — Hunger That Reveals", "Ayuno — El hambre que revela",
     ["Matthew 6:16-18", "Isaiah 58:1-12"],
     ["What appetite — food, screens, validation — most masters you?",
      "What might fasting from that for 24 hours expose?",
      "Isaiah ties true fasting to justice. Whose burden are you carrying right now?"]),
    (4, "Sabbath — The Discipline of Stopping", "Sábado — La disciplina de detenerse",
     ["Genesis 2:1-3", "Mark 2:23-28"],
     ["When did you last stop, not because you were empty, but as worship?",
      "What part of your identity is built on never stopping?",
      "What would a real 24-hour sabbath cost you — and what would it give back?"]),
    (5, "Silence & Solitude — Stripping the Noise", "Silencio y soledad — Quitando el ruido",
     ["Mark 1:35-39", "1 Kings 19:9-13"],
     ["When did you last sit in silence with no input for 15 minutes?",
      "What does the noise in your life protect you from feeling?",
      "What did you hear from God in your last truly quiet moment?"]),
    (6, "Confession — Walking in the Light", "Confesión — Caminando en la luz",
     ["1 John 1:5-10", "James 5:16"],
     ["What sin have you confessed only to God to avoid the embarrassment of telling a person?",
      "Who is the one person you trust enough to confess to this week?",
      "What does it cost to keep secrets — and what does scripture promise when they come into the light?"]),
    (7, "Service — Love With Skin On It", "Servicio — Amor con piel encima",
     ["Mark 10:42-45", "Galatians 5:13-14"],
     ["Whom are you currently serving in a way that costs you something?",
      "Where has your 'helping' actually been about your reputation?",
      "What act of hidden service can you do this week — known only to God?"]),
]


# ---------------------------------------------------------------------------
# 3. ANXIETY & MENTAL HEALTH — Psalms for the Anxious Mind
# ---------------------------------------------------------------------------
ANXIETY = [
    (1, "Naming It", "Nombrándolo",
     ["Philippians 4:4-9", "Psalm 13"],
     ["What anxious thought has been on a loop in your head this week?",
      "Paul says 'do not be anxious about anything' — does that feel like comfort or condemnation today?",
      "What would it look like to bring this exact thing to God in prayer right now?"]),
    (2, "Casting Cares", "Echando las preocupaciones",
     ["1 Peter 5:6-11", "Psalm 55:22"],
     ["What care are you carrying that scripture says belongs to God?",
      "Why do you keep picking it back up after you 'give it to him'?",
      "What does it look like, practically, to cast something on God today?"]),
    (3, "Anxious About Tomorrow", "Ansioso por el mañana",
     ["Matthew 6:25-34", "Lamentations 3:22-26"],
     ["What 'tomorrow problem' are you trying to solve today?",
      "Where in your past has God provided when you were sure he wouldn't?",
      "What would it mean to seek the kingdom 'first' tomorrow morning?"]),
    (4, "When Fear Comes", "Cuando viene el miedo",
     ["Psalm 56", "Psalm 23"],
     ["David says 'when I am afraid, I trust in you.' What do you do when you're afraid?",
      "What does it look like for the Lord to be your shepherd in the next 24 hours?",
      "What is the 'valley' you're walking through right now?"]),
    (5, "God's Faithfulness in Past Trials", "La fidelidad de Dios en pruebas pasadas",
     ["Psalm 77", "Lamentations 3:19-26"],
     ["What's a past anxiety God carried you through that you've forgotten?",
      "Asaph remembers God's deeds when he can't feel his presence. What deed will you remember today?",
      "What would it change to write down 5 specific times God came through?"]),
    (6, "Renewing the Mind", "Renovando la mente",
     ["Romans 12:1-2", "Philippians 4:8"],
     ["What is the dominant 'pattern of this world' running in your head right now?",
      "Of Paul's list (true, noble, right, pure, lovely…), where is the gap in your thought life?",
      "What is one true thing you need to preach to yourself this week?"]),
    (7, "Peace That Passes Understanding", "Paz que sobrepasa el entendimiento",
     ["John 14:25-31", "Philippians 4:9"],
     ["When did you last experience a peace you couldn't explain?",
      "Jesus gives peace 'not as the world gives.' What's the difference you've felt?",
      "What practice from this week do you want to keep when the next anxious wave hits?"]),
]


# ---------------------------------------------------------------------------
# 4. ANGER & SELF-CONTROL — Slow to Anger
# ---------------------------------------------------------------------------
ANGER = [
    (1, "The Roots of Anger", "Las raíces del enojo",
     ["James 1:19-21", "Proverbs 14:29"],
     ["What was the last thing that made you blow up — and what was underneath it?",
      "Where did you learn to handle anger the way you do?",
      "Anger reveals what you love or fear. What did your last outburst reveal?"]),
    (2, "Slow to Anger Is Who God Is", "Tardo para la ira es quién Dios es",
     ["Exodus 34:6-7", "Psalm 103:8-14"],
     ["God describes himself first as 'slow to anger.' How would your family describe you?",
      "Where have you experienced God's patience that you have not extended to others?",
      "What would 'slow to anger' look like in your most-triggered relationship?"]),
    (3, "Don't Sin in Your Anger", "No pequen en su enojo",
     ["Ephesians 4:26-27", "Psalm 4:4"],
     ["When does your anger cross the line from feeling to sinning?",
      "What 'foothold' has unprocessed anger given the enemy in your life?",
      "What is one thing you have not let the sun go down on that you need to address tonight?"]),
    (4, "Words That Wound", "Palabras que hieren",
     ["Proverbs 15:1-4", "James 3:1-12"],
     ["What's the last sentence you said in anger that you wish you could take back?",
      "Whose tongue do you most need to imitate — and whose do you avoid?",
      "What conversation do you keep replaying because of what was said in anger?"]),
    (5, "Repair: How to Apologize", "Restaurar: cómo pedir disculpas",
     ["Matthew 5:21-26", "Luke 19:1-10"],
     ["Whom do you owe an apology that you have been avoiding?",
      "What's the difference between 'sorry you feel that way' and Zacchaeus-style restitution?",
      "What concrete repair can you make this week?"]),
    (6, "Generational Patterns", "Patrones generacionales",
     ["Exodus 20:5-6", "Ezekiel 18:14-17"],
     ["What anger pattern did you inherit from a parent or guardian?",
      "Ezekiel says you don't have to repeat your father's sins. What chain breaks with you?",
      "Who in the next generation is watching how you handle anger?"]),
    (7, "Self-Control as Spirit-Fruit", "Dominio propio como fruto del Espíritu",
     ["Galatians 5:16-26", "Proverbs 16:32"],
     ["Self-control is fruit, not willpower. Where are you white-knuckling instead of yielding?",
      "What rhythm of life starves the flesh and feeds the Spirit?",
      "Who can hold you accountable for the next 30 days, specifically with anger?"]),
]


# ---------------------------------------------------------------------------
# 5. GRIEF & LOSS — Lament: Walking with God in Sorrow
# ---------------------------------------------------------------------------
GRIEF = [
    (1, "Permission to Grieve", "Permiso para lamentar",
     ["John 11:28-37", "Ecclesiastes 3:1-8"],
     ["Where have you been told (or told yourself) you should be 'over it' by now?",
      "Jesus wept even knowing the resurrection was coming. What does that mean for your tears?",
      "What loss are you not letting yourself feel?"]),
    (2, "The Discipline of Lament", "La disciplina del lamento",
     ["Psalm 13", "Lamentations 3:1-20"],
     ["David asks 'how long, O Lord' four times. What's your honest 'how long'?",
      "When did you last bring a complaint directly to God instead of around him?",
      "What would your prayer sound like if you let it be raw?"]),
    (3, "Job — When Friends Fail", "Job — Cuando los amigos fallan",
     ["Job 1:13-22", "Job 2:11-13"],
     ["What's the dumbest thing someone said to you in your grief?",
      "Who has been a 'sit with you in silence for 7 days' kind of friend?",
      "Whom can you sit with — without explaining their pain — this week?"]),
    (4, "When God Feels Absent", "Cuando Dios parece ausente",
     ["Psalm 22:1-11", "Psalm 88"],
     ["When did you last feel forsaken by God — and did you tell him?",
      "Psalm 88 ends without resolution. What does it mean that scripture allows that?",
      "What is the truth you can hold onto when feelings disappear?"]),
    (5, "Hope That Refuses to Lie", "Esperanza que se niega a mentir",
     ["Lamentations 3:21-26", "Romans 8:18-25"],
     ["What 'steadfast love that never ceases' has shown up even in the dark?",
      "Where are you tempted to fake hope to comfort others?",
      "What does it mean for creation itself to groan with you?"]),
    (6, "The Comfort of Christ", "El consuelo de Cristo",
     ["2 Corinthians 1:3-7", "Matthew 5:4"],
     ["Who has been the 'God of all comfort' to you with skin on?",
      "What comfort have you received that you can pass to someone else?",
      "Whom are you uniquely positioned to comfort because of what you've lost?"]),
    (7, "Resurrection Hope", "Esperanza de resurrección",
     ["1 Thessalonians 4:13-18", "Revelation 21:1-5"],
     ["What does it mean to 'grieve, but not as those without hope'?",
      "What in this loss will be made new — and what won't, in this life?",
      "What promise from Revelation 21 do you most need to hold onto today?"]),
    (8, "Honoring What Was", "Honrando lo que fue",
     ["Psalm 116:15", "2 Samuel 1:17-27"],
     ["What is one specific gift you received from what (or whom) you lost?",
      "How can you honor them this week in a tangible way?",
      "What would 'lamenting like David lamented' look like for you?"]),
    (9, "The Slow Road Back", "El camino lento de regreso",
     ["Psalm 30", "Isaiah 61:1-3"],
     ["Where have you seen morning come after a long night?",
      "Where are you still in the night — and is that okay?",
      "What 'oil of gladness' for 'mourning' might God be slowly giving you?"]),
    (10, "Carrying It Forward", "Llevándolo hacia adelante",
     ["John 16:20-22", "Revelation 7:13-17"],
     ["What part of you is forever changed by this loss?",
      "How might God use what you've walked through for someone else?",
      "What is the rhythm — yearly, weekly — by which you'll keep remembering?"]),
]


# ---------------------------------------------------------------------------
# 6. YOUNG MEN — Identity Before Achievement
# ---------------------------------------------------------------------------
YOUNG_MEN = [
    (1, "Made on Purpose", "Hecho a propósito",
     ["Psalm 139:13-18", "Ephesians 2:10"],
     ["What lie about who you are have you been believing the longest?",
      "If God already knows everything about you and still made you on purpose, what changes?",
      "What 'good work' might God already be preparing you for?"]),
    (2, "Whose Voice Are You Listening To?", "¿A qué voz estás escuchando?",
     ["Proverbs 13:20", "1 Corinthians 15:33"],
     ["Whose voice has the most influence over how you see yourself?",
      "Which 5 people are you actually becoming like?",
      "Whose voice do you need to mute or unfollow this week?"]),
    (3, "Flee Youthful Passions", "Huye de las pasiones juveniles",
     ["2 Timothy 2:22", "1 Corinthians 6:18-20"],
     ["Paul says 'flee' — not negotiate. From what specifically do you need to literally run?",
      "Where have you been trying to manage a sin you should be fleeing?",
      "Who are the 'those who call on the Lord' you're pursuing alongside?"]),
    (4, "Your Body Is Not Your Own", "Tu cuerpo no te pertenece",
     ["1 Corinthians 6:12-20", "Romans 6:12-14"],
     ["What does it actually mean that your body is a temple — and how does that change tonight?",
      "What 'lawful but not beneficial' habit currently masters you?",
      "What instrument of righteousness can your body become this week?"]),
    (5, "Screens, Lust, and What Feeds It", "Pantallas, lujuria y lo que la alimenta",
     ["Job 31:1", "Matthew 5:27-30"],
     ["Job 'made a covenant with my eyes.' What would that covenant look like for your phone?",
      "What boredom or pain are you medicating with porn or fantasy?",
      "Whom can you tell, by name, about your last failure — within 7 days?"]),
    (6, "Learning to Work", "Aprendiendo a trabajar",
     ["Proverbs 6:6-11", "2 Thessalonians 3:6-12"],
     ["Where in your life are you the 'sluggard' the proverb describes?",
      "What's the next hard thing you should be doing that you're avoiding?",
      "What does it look like to work 'as for the Lord' at your current job or school?"]),
    (7, "Honor Your Parents — Even When It's Hard", "Honra a tus padres — aun cuando es difícil",
     ["Ephesians 6:1-3", "Proverbs 23:22"],
     ["What's the hardest thing about honoring your parents right now?",
      "Honor doesn't mean agreement — what does honor look like when you disagree?",
      "What is one specific way you can honor a parent this week?"]),
    (8, "Choose Your Friends Well", "Elige bien tus amigos",
     ["Proverbs 17:17", "Proverbs 27:17"],
     ["Who actually sharpens you toward Christ — and who dulls you?",
      "What friendship are you keeping out of comfort that's costing you?",
      "Who is the brother you'd call at 2 a.m. if you were tempted? Do you have one?"]),
    (9, "Money, Debt, and Freedom", "Dinero, deuda y libertad",
     ["Proverbs 22:7", "Hebrews 13:5-6"],
     ["What does your spending reveal about what you actually love?",
      "Where has debt — financial or emotional — quietly enslaved you?",
      "What would 'be content with what you have' look like this month?"]),
    (10, "First Job, First Failures", "Primer trabajo, primeros fracasos",
     ["Colossians 3:22-24", "Proverbs 16:3"],
     ["What's the most recent failure you're tempted to hide?",
      "How do you commit your work to the Lord on a Monday morning?",
      "Who is one older man you could ask to mentor you this year?"]),
    (11, "Friendship vs. Romance", "Amistad vs. romance",
     ["Song of Solomon 8:4", "Proverbs 4:23"],
     ["What 'almost-relationship' are you in that needs definition?",
      "How are you guarding your heart — and hers, or his?",
      "What kind of man do you want to be three years before getting married?"]),
    (12, "Calling vs. Career", "Llamado vs. carrera",
     ["Ephesians 4:1-3", "1 Corinthians 7:17-24"],
     ["Are you choosing your career out of conviction or fear?",
      "What unique gifts has God given you — and how might they serve his kingdom?",
      "If money were not a factor, what would you do with your life?"]),
    (13, "Owning Your Faith", "Apropiándote de tu fe",
     ["Acts 17:10-12", "Romans 14:5"],
     ["Where have you been a lazy Berean — accepting what you've been told without checking?",
      "What's a tough question about Christianity you've never let yourself ask?",
      "What's one resource you'll engage this month to think harder about your faith?"]),
    (14, "The Man God Is Looking For", "El hombre que Dios busca",
     ["Ezekiel 22:30", "Micah 6:8"],
     ["Where might God be calling you to 'stand in the gap' for someone else?",
      "Of justice, mercy, and walking humbly — which is your weakest right now?",
      "Who, ten years from now, will be glad you became this kind of man?"]),
]


# ---------------------------------------------------------------------------
# 7. YOUNG WOMEN — Anchored: Identity, Worth, Beauty
# ---------------------------------------------------------------------------
YOUNG_WOMEN = [
    (1, "Fearfully and Wonderfully Made", "Asombrosa y maravillosamente hecha",
     ["Psalm 139:13-18", "Genesis 1:27"],
     ["What lie about your worth have you been carrying since you were a kid?",
      "What does it mean that you bear the image of God — body, soul, and mind?",
      "If God 'fearfully and wonderfully' made you, what does that change about how you treat yourself?"]),
    (2, "Beauty That Does Not Fade", "Belleza que no se desvanece",
     ["1 Peter 3:3-4", "Proverbs 31:30"],
     ["How much of your time and money goes into beauty that fades?",
      "Where have you confused appearing godly with actually fearing the Lord?",
      "What 'unfading' beauty would your closest friend say is growing in you?"]),
    (3, "Whose Voices Are Shaping You?", "¿Qué voces te están moldeando?",
     ["Proverbs 13:20", "Philippians 4:8"],
     ["Whose voice has the most influence over how you see your body?",
      "What three accounts on your phone leave you feeling worse about yourself?",
      "What is one source of input you need to add — and one you need to cut?"]),
    (4, "Modesty as Freedom, Not Bondage", "Modestia como libertad, no esclavitud",
     ["1 Timothy 2:9-10", "1 Corinthians 6:19-20"],
     ["How is modesty about you, not about other people's gaze?",
      "Where have you used (or hidden) your body for power or for protection?",
      "What does it look like to dress your body with the dignity God gave it?"]),
    (5, "Friendships Worth Keeping", "Amistades que vale la pena mantener",
     ["Ruth 1:14-18", "Proverbs 27:6"],
     ["Who is the Ruth — or the Naomi — in your life right now?",
      "What friendship is keeping you small and afraid to grow?",
      "Whose 'wounds' have you needed to receive lately, even when they hurt?"]),
    (6, "Honor Your Parents", "Honra a tus padres",
     ["Ephesians 6:1-3", "Proverbs 1:8-9"],
     ["What's the hardest thing about honoring your parents in this season?",
      "Where might their experience be wisdom you've been dismissing?",
      "What is one specific way you can honor a parent this week, even silently?"]),
    (7, "Your Body in an Image Culture", "Tu cuerpo en una cultura de imagen",
     ["Psalm 139:14", "Romans 12:1-2"],
     ["What does it mean to present your body 'as a living sacrifice'?",
      "Where has the world's pattern about your body crept into your self-talk?",
      "Who is the woman you'd want a 14-year-old girl to look at and become?"]),
    (8, "Anxiety, Comparison, and Contentment", "Ansiedad, comparación y contentamiento",
     ["Philippians 4:11-13", "2 Corinthians 10:12"],
     ["Whom do you most often compare yourself to — and what does that reveal?",
      "Paul learned contentment. What practice would you have to learn it through?",
      "Where can you say, today, 'I have learned in this to be content'?"]),
    (9, "Singleness as a Gift, Not a Waiting Room", "La soltería como don, no como sala de espera",
     ["1 Corinthians 7:32-35", "Psalm 73:25-26"],
     ["What are you postponing 'until I'm married'?",
      "How might your singleness, right now, be uniquely useful to God?",
      "Whom in your life is being loved well because you are single?"]),
    (10, "Boldness in a Quiet World", "Valentía en un mundo silencioso",
     ["Esther 4:13-16", "Acts 16:13-15"],
     ["For what 'such a time as this' might God have placed you?",
      "Where are you keeping your faith private to keep the peace?",
      "What's one bold step of faith you've been avoiding?"]),
    (11, "Wisdom Over Impulse", "Sabiduría sobre impulso",
     ["Proverbs 31:25-26", "James 1:5-8"],
     ["What recent decision did you make from impulse rather than wisdom?",
      "When you 'lack wisdom,' do you actually ask God — or just power through?",
      "Who is the wise older woman you should be learning from?"]),
    (12, "A Woman Who Fears the Lord", "Una mujer que teme al Señor",
     ["Proverbs 31:30", "Luke 10:38-42"],
     ["Are you a Martha or a Mary in your faith life right now — and why?",
      "What does 'fearing the Lord' actually feel like for you?",
      "What 'one thing necessary' have you been missing while distracted by many?"]),
    (13, "Owning Your Faith", "Apropiándote de tu fe",
     ["Acts 17:10-12", "Hebrews 11:1-6"],
     ["What's a hard question about Christianity you've been afraid to ask?",
      "Whose answers have you accepted without checking against scripture?",
      "What does faith of your own — not your mom's, not your church's — look like?"]),
    (14, "Becoming Who God Made You", "Convirtiéndote en quien Dios te hizo",
     ["Ephesians 2:10", "Jeremiah 29:11-14"],
     ["What 'good works' has God prepared specifically for you?",
      "Where have you been waiting for permission you don't actually need?",
      "Who, ten years from now, will be glad you became this woman?"]),
]


# ---------------------------------------------------------------------------
# 8. SINGLE & DATING — Pursuing With Honor
# ---------------------------------------------------------------------------
DATING = [
    (1, "God's Heart for Marriage", "El corazón de Dios para el matrimonio",
     ["Genesis 2:18-25", "Ephesians 5:31-32"],
     ["What's your deepest fear or hope around marriage right now?",
      "Marriage is meant to picture Christ and the church. What does that mean for how you date?",
      "If marriage is a covenant, not a contract, what changes in how you pursue?"]),
    (2, "Guard Your Heart, Not Your Feelings", "Guarda tu corazón, no tus sentimientos",
     ["Proverbs 4:23-27", "Song of Solomon 8:4"],
     ["What does 'guarding your heart' actually look like in dating?",
      "Where have you let emotions outrun wisdom in past relationships?",
      "Who in your life is honest enough to tell you when you're moving too fast?"]),
    (3, "Friendship Before Romance", "Amistad antes que romance",
     ["Proverbs 17:17", "Ecclesiastes 4:9-12"],
     ["Could you describe the person you're interested in as your friend first?",
      "What kind of friend are you — and would you marry someone like that?",
      "Whose 'cord of three strands' is your relationship — or could be?"]),
    (4, "Sexual Integrity in a Pornified Culture", "Integridad sexual en una cultura pornográfica",
     ["1 Thessalonians 4:1-8", "Hebrews 13:4"],
     ["Where is your sexual integrity being shaped by culture more than scripture?",
      "What boundary have you crossed — physical or digital — that you need to confess?",
      "Whom can you bring into your sexual integrity as accountability?"]),
    (5, "The Hidden Cost of 'Trying It Out'", "El costo oculto de 'probarlo'",
     ["Proverbs 5:1-23", "1 Corinthians 6:18-20"],
     ["What does Proverbs 5 say is the long-term cost of sexual sin?",
      "How has 'just hooking up' or 'just living together' shaped people you know?",
      "What good thing are you giving up by 'trying out' something premature?"]),
    (6, "What to Look For in a Spouse", "Qué buscar en un cónyuge",
     ["Proverbs 31:10-12", "1 Timothy 3:1-7"],
     ["What three qualities matter most to you — and are they shallow or substantive?",
      "What about the person you're dating would you brag about in 30 years?",
      "What's one weakness in them that, if it never changes, you can live with?"]),
    (7, "Equally Yoked", "Yugo igual",
     ["2 Corinthians 6:14-7:1", "1 Corinthians 7:39"],
     ["What does 'unequally yoked' actually mean — beyond just 'they're not Christian'?",
      "If your spouse will shape your soul, what soul are you currently dating?",
      "What conviction are you tempted to soften to keep this relationship?"]),
    (8, "When Relationships End Well", "Cuando las relaciones terminan bien",
     ["Ecclesiastes 3:1-8", "Philippians 4:6-9"],
     ["What relationship may need to end — and how do you end it with honor?",
      "What has a past relationship taught you about yourself?",
      "Where are you holding on out of fear of being alone?"]),
    (9, "Waiting Well", "Esperando bien",
     ["Psalm 27:14", "Lamentations 3:25-26"],
     ["What does 'waiting on the Lord' look like in dating versus settling?",
      "What discipline are you avoiding because you're 'waiting for marriage'?",
      "How is the waiting itself shaping you?"]),
    (10, "Contentment as a Discipline", "Contentamiento como disciplina",
     ["Philippians 4:11-13", "1 Timothy 6:6-8"],
     ["What would actually change if you got married tomorrow — and what wouldn't?",
      "Where is loneliness preaching to you that God isn't enough?",
      "What does it mean to learn contentment in this exact season?"]),
]

# ---------------------------------------------------------------------------
# 9. MARRIAGE — One Flesh, Built to Last
# ---------------------------------------------------------------------------
MARRIAGE = [
    (1, "Two Becoming One", "Dos siendo uno",
     ["Genesis 2:18-25", "Mark 10:6-9"],
     ["What does 'one flesh' mean to you in this season — and where is the seam still showing?",
      "Where are you still operating like roommates instead of one?",
      "What did you assume about marriage that has not turned out to be true?"]),
    (2, "Love That Lasts", "Amor que perdura",
     ["1 Corinthians 13:1-13", "Ephesians 5:1-2"],
     ["Read 1 Cor 13 with your spouse's name in place of 'love.' Where does it hurt?",
      "Which of those qualities are you weakest at — and what does that cost?",
      "What is one specific way you can love this week that costs you something?"]),
    (3, "Mutual Submission", "Sumisión mutua",
     ["Ephesians 5:21", "Philippians 2:3-4"],
     ["What does 'submitting to one another out of reverence for Christ' look like in your home?",
      "Where is one of you carrying more of this verse than the other?",
      "What 'interest' of your spouse have you been ignoring?"]),
    (4, "Husbands — Love as Christ Loved", "Esposos — Amen como Cristo amó",
     ["Ephesians 5:25-33", "1 Peter 3:7"],
     ["Where would your wife say you 'gave yourself up' for her this month?",
      "Where might you be 'lording' over instead of laying down?",
      "What are you doing this week to nourish her — body, soul, and mind?"]),
    (5, "Wives — Strong Respect, Soft Heart", "Esposas — Respeto firme, corazón suave",
     ["Ephesians 5:22-24", "1 Peter 3:1-6"],
     ["Where does your husband most need to feel respected — and not get it?",
      "Where has 'speaking truth' become criticism in your home?",
      "What is the tone of voice your kids are most often hearing from you?"]),
    (6, "Listen First, Speak Second", "Escuchar primero, hablar después",
     ["James 1:19-21", "Proverbs 18:13"],
     ["When was the last time you actually listened — without composing your reply?",
      "What does your spouse keep trying to say that you keep cutting off?",
      "What's one question you can ask tonight, and just listen?"]),
    (7, "Conflict Without Sin", "Conflicto sin pecado",
     ["Ephesians 4:26-32", "Matthew 18:15-17"],
     ["What sin are you currently 'letting the sun go down' on?",
      "What pattern shows up every time you fight?",
      "What is the next conversation you need to initiate — not avoid?"]),
    (8, "Forgiveness — The Daily Discipline", "Perdón — La disciplina diaria",
     ["Colossians 3:12-14", "Matthew 18:21-35"],
     ["What unforgiveness are you nursing right now — and how is it shaping your home?",
      "Forgiveness is not pretending it didn't happen. What does real forgiveness look like here?",
      "What's the difference between 'I forgive you' and 'I trust you again'?"]),
    (9, "Sex as Gift", "El sexo como don",
     ["1 Corinthians 7:1-5", "Song of Solomon 7:10"],
     ["What's your current pattern around sex — frequency, initiation, openness?",
      "Where is one of you withholding, and what's underneath that?",
      "What conversation about sex have you been avoiding for years?"]),
    (10, "Money — One Purse", "Dinero — Una sola bolsa",
     ["Proverbs 13:11", "1 Timothy 6:6-10"],
     ["What does money fight #1 reveal about what each of you fears?",
      "Where is your spending preaching different sermons than your stated values?",
      "What financial decision have you been avoiding making together?"]),
    (11, "In-Laws & Origin Families", "Suegros y familias de origen",
     ["Genesis 2:24", "Ruth 1:14-18"],
     ["Where have you not actually 'left' your family of origin?",
      "What pattern from your parents' marriage are you replaying?",
      "How are you honoring your spouse's family — even the hard ones?"]),
    (12, "Parenting Together", "Criando juntos",
     ["Deuteronomy 6:6-9", "Proverbs 22:6"],
     ["Where do you most disagree on parenting — and how does the disagreement play out?",
      "What does the kids' view of your marriage teach them about God?",
      "What is one decision you need to make as 'we,' not 'me'?"]),
    (13, "Surviving Hard Seasons", "Sobreviviendo temporadas difíciles",
     ["Ecclesiastes 4:9-12", "Job 2:9-10"],
     ["What is the hardest season your marriage has survived — and what kept you?",
      "Where in this current season are you tempted to give up?",
      "Whose marriage do you know that has weathered worse — and what did they do?"]),
    (14, "A Marriage That Points to Christ", "Un matrimonio que señala a Cristo",
     ["Ephesians 5:31-32", "Revelation 19:6-9"],
     ["What about your marriage actually points to the gospel?",
      "Where is your marriage preaching a false gospel right now?",
      "What is one thing you want to be true of your marriage in 10 years — that requires changing today?"]),
]


# ---------------------------------------------------------------------------
# 10. NEW HUSBAND — First Five Years
# ---------------------------------------------------------------------------
NEW_HUSBAND = [
    (1, "Leaving and Cleaving", "Dejar y unirse",
     ["Genesis 2:24", "Matthew 19:4-6"],
     ["Where have you not actually 'left' your parents — emotionally, financially, or in loyalty?",
      "What habit from single life are you still living in your marriage?",
      "What does 'cleaving' look like in this exact week?"]),
    (2, "She Is Not You", "Ella no es tú",
     ["1 Peter 3:7", "Philippians 2:3-4"],
     ["Where do you assume she processes things the way you do — and get frustrated when she doesn't?",
      "What does 'living with her in an understanding way' require you to learn?",
      "What is one thing about her that you have been trying to change instead of receive?"]),
    (3, "The Death of Your Hobbies vs. Headship", "La muerte de tus pasatiempos vs. liderazgo",
     ["Ephesians 5:25", "Mark 10:42-45"],
     ["What hobby or pattern from singleness needs to be laid down for this marriage?",
      "Where have you confused 'leading' with 'getting your way'?",
      "What sacrifice have you not actually been willing to make?"]),
    (4, "Listen, Husband, Listen", "Escucha, esposo, escucha",
     ["James 1:19", "Proverbs 18:13"],
     ["What is she trying to tell you that you keep solving instead of hearing?",
      "When did you last ask 'how are you?' and stay for the real answer?",
      "What's the difference between fixing it and being with her in it?"]),
    (5, "Initiating Spiritual Leadership", "Iniciando el liderazgo espiritual",
     ["Joshua 24:14-15", "Ephesians 5:25-27"],
     ["What does spiritual leadership in your marriage actually look like — beyond a vague feeling?",
      "When did you last pray with her, out loud, by name?",
      "What is one rhythm — weekly, daily — you can take responsibility to start?"]),
    (6, "Money Fights and How to Stop Them", "Peleas de dinero y cómo detenerlas",
     ["Proverbs 21:5", "Luke 14:28-30"],
     ["What's the one money fight you keep having — and what's actually underneath it?",
      "Where is your spending preaching a sermon she heard but you didn't say?",
      "What is the next concrete budget conversation you need to initiate?"]),
    (7, "When She's Hard to Love", "Cuando es difícil amarla",
     ["1 Corinthians 13:4-8", "1 Peter 4:8"],
     ["What is the version of her you're committed to — including the parts you didn't know about?",
      "Where has 'love covers a multitude of sins' become enabling instead of grace?",
      "What does it mean to 'choose' her again this week?"]),
    (8, "Sexual Pursuit and Patience", "Búsqueda sexual y paciencia",
     ["Proverbs 5:18-19", "1 Corinthians 7:1-5"],
     ["Where are you pursuing her body without pursuing her heart?",
      "Where have you confused entitlement with covenant?",
      "What conversation about sex have you both been avoiding?"]),
    (9, "Friendship Outside the Marriage", "Amistad fuera del matrimonio",
     ["Proverbs 27:17", "2 Timothy 2:22"],
     ["Who are the men sharpening you — by name?",
      "What unhealthy friendship do you need to grieve and move on from?",
      "Whom do you need to reach out to this week, even if it's awkward?"]),
    (10, "Apologize and Mean It", "Discúlpate y dilo en serio",
     ["James 5:16", "Ephesians 4:32"],
     ["When was the last time you fully apologized — naming what you did, no 'but'?",
      "What 'sorry you feel that way' apology do you owe her now as a real apology?",
      "What's the cost of saying 'I was wrong' to your wife this week?"]),
]


# ---------------------------------------------------------------------------
# 11. FATHERHOOD — Fathered to Father
# ---------------------------------------------------------------------------
FATHERHOOD = [
    (1, "A Father's Unique Calling", "El llamado único de un padre",
     ["Ephesians 6:1-4", "Deuteronomy 6:4-9"],
     ["What kind of father do you want your kids to have — and how close are you?",
      "What did your dad get right that you should keep?",
      "What did your dad get wrong that the chain breaks with you?"]),
    (2, "Provision Beyond Money", "Provisión más allá del dinero",
     ["1 Timothy 5:8", "Proverbs 24:3-4"],
     ["Of presence, protection, and provision — which one is hardest for you to give?",
      "Where has 'I'm working hard for them' become an excuse?",
      "What does your family need from you tonight that no money can buy?"]),
    (3, "Presence Over Presents", "Presencia sobre regalos",
     ["Malachi 4:6", "Luke 11:11-13"],
     ["When was the last time you were fully present with each child — phone down, eyes up?",
      "What's the gift you keep giving that they don't actually need?",
      "What would change if you came home like Christ comes to his church?"]),
    (4, "Discipline in Love", "Disciplina en amor",
     ["Hebrews 12:5-11", "Proverbs 13:24"],
     ["Where has your discipline been about your anger, not their character?",
      "What does discipline 'for our good, that we may share his holiness' look like?",
      "What's the next conversation about discipline you and your spouse need to have?"]),
    (5, "Words That Build or Break", "Palabras que construyen o destruyen",
     ["Proverbs 18:21", "Colossians 3:21"],
     ["What's the last sentence one of your kids heard from you — and was it life or death?",
      "What word is your child desperate to hear from you?",
      "What pattern of words from your dad are you repeating?"]),
    (6, "Blessing Your Children", "Bendiciendo a tus hijos",
     ["Genesis 27:27-29", "Mark 10:13-16"],
     ["When was the last time you spoke a specific blessing over each child?",
      "What about each child do you see that they don't see yet?",
      "What rhythm of blessing — bedtime, weekly, special — could you start?"]),
    (7, "Repenting to Your Kids", "Arrepentirte ante tus hijos",
     ["James 5:16", "Matthew 5:23-24"],
     ["What do you owe one of your kids an apology for — and have you given it?",
      "What does it teach them when you say 'I was wrong, please forgive me'?",
      "What's stopping you from doing this tonight?"]),
    (8, "Modeling, Not Lecturing", "Modelar, no sermonear",
     ["Philippians 4:9", "1 Corinthians 11:1"],
     ["What sermon are you preaching with your life that contradicts your words?",
      "If your kids became exactly what you do (not say), what would they become?",
      "What is one specific area where modeling needs to start replacing lecturing?"]),
    (9, "Family Worship", "Adoración familiar",
     ["Deuteronomy 6:6-9", "Joshua 24:14-15"],
     ["What 'as for me and my house' rhythm exists in your home — actually exists?",
      "What's keeping you from a 5-minute scripture-and-prayer time with your kids?",
      "What did your home growing up teach you about God — and what do yours teach?"]),
    (10, "When You're Tired", "Cuando estás cansado",
     ["Isaiah 40:28-31", "Matthew 11:28-30"],
     ["When did you last admit, out loud, that you're exhausted as a dad?",
      "Where are you running on willpower instead of grace?",
      "What rhythm of rest and renewal do you need to restart?"]),
    (11, "Fathering When Your Father Didn't", "Siendo padre cuando el tuyo no lo fue",
     ["Psalm 27:10", "2 Corinthians 5:17"],
     ["What did your father not give you that you're determined your kids will have?",
      "Where does the absence still ache — and how is the ache leaking onto your kids?",
      "What would it look like to be fathered by God before fathering your kids today?"]),
    (12, "Daughters Need Their Fathers", "Las hijas necesitan a sus padres",
     ["Luke 8:40-56", "Proverbs 4:1-9"],
     ["What is your daughter learning about male attention from how you treat her mother?",
      "What is your daughter learning about her worth from how you look at her?",
      "What's one specific way to delight in her this week?"]),
    (13, "Sons Need Their Fathers' Eyes", "Los hijos necesitan los ojos de sus padres",
     ["1 Samuel 17:38-40", "1 Chronicles 28:9"],
     ["What does your son believe about himself based on how you see him?",
      "Where have you been more critic than coach?",
      "What 'David moment' is your son in — needing you to see him for who he's becoming?"]),
    (14, "The Father You Point Them To", "El Padre al que los señalas",
     ["John 14:6-11", "Hebrews 12:9-10"],
     ["What about God do your kids learn from how you father them?",
      "Where is your fathering preaching a false picture of God?",
      "What's one truth about the Father you want your kids to know — that they have to learn from you first?"]),
]


# ---------------------------------------------------------------------------
# 12. MOTHERHOOD — Strong & Tender
# ---------------------------------------------------------------------------
MOTHERHOOD = [
    (1, "A Mother's Unique Calling", "El llamado único de una madre",
     ["Proverbs 31:25-31", "Titus 2:3-5"],
     ["What kind of mother do you want your kids to remember — and how close are you?",
      "What did your mom get right that you want to keep?",
      "What did your mom get wrong that the chain breaks with you?"]),
    (2, "When You Feel Invisible", "Cuando te sientes invisible",
     ["Genesis 16:6-13", "1 Samuel 1:9-18"],
     ["Like Hagar — when did you last feel seen by 'the God who sees'?",
      "Where are you doing hidden, holy work that no one notices?",
      "What does it mean that God is the one who sees — even when no one else does?"]),
    (3, "Nurture Without Smothering", "Nutrir sin asfixiar",
     ["1 Thessalonians 2:7-8", "Proverbs 31:27"],
     ["Where are you holding on too tightly to one of your kids?",
      "What 'help' have you been giving that's actually disabling them?",
      "What do they need to do for themselves that you keep doing for them?"]),
    (4, "Discipline With Grace", "Disciplina con gracia",
     ["Hebrews 12:5-11", "Proverbs 22:6"],
     ["When did your discipline last come from anger instead of love?",
      "What did your mom teach you about discipline — and what are you re-teaching?",
      "What does grace-soaked discipline actually look like in this season?"]),
    (5, "Words That Shape", "Palabras que moldean",
     ["Proverbs 31:26", "Ephesians 4:29"],
     ["What's the soundtrack your kids hear in your voice all day?",
      "What sentence does your child rehearse silently because of how you said it?",
      "What word does your child most need to hear from you this week?"]),
    (6, "Modeling Faith", "Modelando la fe",
     ["2 Timothy 1:5", "Deuteronomy 6:6-9"],
     ["What faith are your kids actually catching from you — not just hearing about?",
      "Lois → Eunice → Timothy. Whom is yours being passed to?",
      "What's one rhythm of faith you want them to remember from your home?"]),
    (7, "When You've Lost It", "Cuando has explotado",
     ["Ephesians 4:31-32", "James 1:19-20"],
     ["What was the last time you yelled at your kids — and what was actually underneath?",
      "What apology have you not given because you're embarrassed?",
      "How do you teach repentance — by repenting in front of them?"]),
    (8, "Sister-Mothers — Community", "Hermanas-madres — Comunidad",
     ["Titus 2:3-5", "Proverbs 27:17"],
     ["Who is the older woman speaking life into your mothering right now?",
      "Whom are you investing in as a younger mother?",
      "What's stopping you from picking up the phone this week?"]),
    (9, "When Sleep Is Gone", "Cuando ya no hay sueño",
     ["Psalm 127:1-2", "Mark 1:35"],
     ["Where is exhaustion making decisions you'll regret?",
      "What rhythm of even small rest do you need to fight for?",
      "Even Jesus rose 'while it was still dark' to be with the Father. What is yours?"]),
    (10, "Mothering When Your Mother Wasn't There", "Siendo madre cuando la tuya no lo fue",
     ["Psalm 27:10", "2 Corinthians 1:3-4"],
     ["What did your mother not give you that your kids will?",
      "Where does that ache still leak out — onto your kids, your spouse, yourself?",
      "What would it look like to be mothered by God before you mother today?"]),
    (11, "Sons Honoring Mothers", "Hijos honrando a las madres",
     ["Proverbs 1:8", "John 19:25-27"],
     ["What is your son learning about women from watching you be loved (or not)?",
      "What does your son need to know from you that only a mom can say?",
      "What's one way you're shaping him into a man who honors women?"]),
    (12, "Daughters and Identity", "Hijas e identidad",
     ["Proverbs 31", "Esther 4:13-14"],
     ["What is your daughter learning about her worth from how you see your own?",
      "What's one bold faith story you can share with your daughter this week?",
      "Whom is she going to be 10 years from now — and what's your part?"]),
    (13, "Letting Them Go", "Dejarlos ir",
     ["1 Samuel 1:27-28", "Luke 15:11-32"],
     ["What stage of letting go are you in — and is it earlier than you wanted?",
      "Like Hannah — what would 'I have lent him to the Lord' look like for you?",
      "What grip do you need to loosen this season?"]),
    (14, "A Higher Mother — The Father Who Never Leaves", "Una Madre superior — El Padre que nunca abandona",
     ["Isaiah 49:15", "Luke 13:34"],
     ["Where do you feel most inadequate as a mom — and what does Isaiah 49 say?",
      "What's the difference between being a 'good mom' and pointing your kids to Christ?",
      "What truth about God do you want your kids to know — even if you can't say it perfectly?"]),
]


# ---------------------------------------------------------------------------
# 13. NEW FATHER — Welcoming a Child
# ---------------------------------------------------------------------------
NEW_FATHER = [
    (1, "A Child Arrives", "Llega un hijo",
     ["Psalm 127:3-5", "Luke 2:6-7"],
     ["What did you not expect about being a father in these first weeks?",
      "Where is the 'gift from the Lord' getting buried under exhaustion or fear?",
      "What does it mean that this child is on loan from God?"]),
    (2, "Sleep Deprivation as Discipleship", "Privación de sueño como discipulado",
     ["Psalm 127:1-2", "Mark 1:35"],
     ["Where is the exhaustion exposing what's underneath your patience and self-control?",
      "How does this season retrain you to depend on grace, not adrenaline?",
      "What is one rhythm — even 5 minutes — you can keep with God this week?"]),
    (3, "Watching Her Become a Mother", "Verla convertirse en madre",
     ["Proverbs 31:28-29", "1 Peter 3:7"],
     ["What does your wife need to hear from you that no one else can say?",
      "Where is she carrying weight you're not seeing?",
      "What's one specific way you can serve her in this 24 hours?"]),
    (4, "When the Baby Cries and You Can't Fix It", "Cuando el bebé llora y no puedes arreglarlo",
     ["Psalm 56:8", "Hebrews 4:14-16"],
     ["When you can't fix it, what comes out of you — and what does that reveal?",
      "What does it teach you that God 'puts our tears in his bottle'?",
      "Where do you need to be helpless before God this week?"]),
    (5, "Identity Shift — Dad Now", "Cambio de identidad — Ahora papá",
     ["Ephesians 1:3-6", "1 John 3:1"],
     ["What part of your old identity is dying — and is that grief okay?",
      "What part of your old life are you holding too tightly?",
      "How does being God's child shape how you father yours?"]),
    (6, "First Memories of God", "Primeros recuerdos de Dios",
     ["Deuteronomy 6:6-9", "2 Timothy 1:5"],
     ["What is the first memory of God you want this child to have?",
      "What rhythm do you want to start now while they don't even know?",
      "What did your home teach you about God — and what do you want to be different?"]),
    (7, "Money Pressure", "Presión de dinero",
     ["Philippians 4:19", "Matthew 6:25-34"],
     ["What 'tomorrow' fear about money is loudest right now?",
      "Where has 'providing for them' become an idol?",
      "What does seeking the kingdom first look like with a baby in the house?"]),
    (8, "Fear of Failing", "Miedo a fallar",
     ["Joshua 1:9", "Philippians 1:6"],
     ["What's your dominant fear about being a father?",
      "Where is that fear about you, not about them?",
      "What does it mean that God 'began a good work' — including in you?"]),
    (9, "Praying Over a Sleeping Child", "Orando sobre un hijo dormido",
     ["Numbers 6:24-26", "Mark 10:13-16"],
     ["What blessing do you want to speak over this child as they sleep?",
      "When did you last just lay your hand on them and pray, no agenda?",
      "What rhythm of bedtime prayer — for and with them — do you want to start?"]),
    (10, "Being There and Present", "Estar ahí y presente",
     ["Malachi 4:6", "Deuteronomy 6:7"],
     ["What does presence — not just proximity — actually look like as a new dad?",
      "Where is your phone competing with your child for your eyes?",
      "What is the next 60 minutes you'll guard, completely undivided, for them?"]),
]


# ---------------------------------------------------------------------------
# 14. PARENTING TEENS — Letting Go With Love
# ---------------------------------------------------------------------------
PARENTING_TEENS = [
    (1, "When Your Child Becomes a Stranger", "Cuando tu hijo se vuelve un extraño",
     ["Luke 2:41-52", "Proverbs 22:6"],
     ["What about your teen has changed that you don't know how to navigate?",
      "Where are you parenting the kid they were instead of the person they're becoming?",
      "What did you do at their age that you've forgotten?"]),
    (2, "Listen More Than Lecture", "Escuchar más que sermonear",
     ["James 1:19-20", "Proverbs 18:13"],
     ["When did you last hear your teen — without composing a response or correction?",
      "What is one thing they keep trying to tell you that you keep dismissing?",
      "What question can you ask this week that's not a setup for a sermon?"]),
    (3, "Trust, Lost and Earned", "Confianza, perdida y ganada",
     ["Luke 19:17", "Proverbs 11:13"],
     ["Where has trust between you and your teen broken — and on whose side?",
      "What 'small thing' have you not been faithful with — that's eroded their trust?",
      "What concrete step can you take this week to rebuild?"]),
    (4, "Their World Is Not Your World", "Su mundo no es el tuyo",
     ["1 Chronicles 12:32", "Acts 17:22-23"],
     ["What about your teen's culture do you not understand — and have refused to learn?",
      "Like Paul in Athens — what's worth quoting from their world to reach them?",
      "What is one piece of their music, their app, their friend group you should engage?"]),
    (5, "When They're Hurting", "Cuando están sufriendo",
     ["2 Corinthians 1:3-4", "Mark 9:23-24"],
     ["What pain in your teen's life are you minimizing because it 'won't matter in 10 years'?",
      "When did you last just sit with them in pain — without trying to fix it?",
      "What unbelief in you is making it hard to bring their pain to God?"]),
    (6, "Anxiety and Depression at Home", "Ansiedad y depresión en casa",
     ["Psalm 34:18", "Philippians 4:6-7"],
     ["What signs of anxiety or depression have you noticed but not addressed?",
      "Where have you confused 'tough love' with avoiding the hard conversation?",
      "Whom — counselor, doctor, pastor — do you need to bring in?"]),
    (7, "Sex, Screens, and the Hard Conversations", "Sexo, pantallas y conversaciones difíciles",
     ["1 Thessalonians 4:1-8", "Ephesians 5:3-4"],
     ["What conversation about sex or screens have you been postponing for years?",
      "What did you wish your parents had said to you that they didn't?",
      "What is one specific thing you'll address this month — not 'someday'?"]),
    (8, "When They Question Your Faith", "Cuando cuestionan tu fe",
     ["Acts 17:10-12", "1 Peter 3:13-16"],
     ["When your teen pushes back on faith — what does it expose in you?",
      "What's the difference between defending the faith and shutting down the question?",
      "Whose questions did Jesus answer with another question? Could you?"]),
    (9, "Letting Natural Consequences Teach", "Dejar que las consecuencias naturales enseñen",
     ["Galatians 6:7-8", "Luke 15:14-17"],
     ["Where have you been rescuing your teen from a consequence they need to feel?",
      "What 'pigpen moment' might be what brings them back to themselves?",
      "What is the next consequence you need to let stand?"]),
    (10, "Apologizing to a Teenager", "Disculparte con un adolescente",
     ["James 5:16", "Ephesians 4:32"],
     ["What do you owe your teen an apology for — that you've avoided because of pride?",
      "What does it teach them when you go first — naming what you did wrong?",
      "What conversation will you initiate this week?"]),
    (11, "Praying for Prodigals", "Orando por los pródigos",
     ["Luke 15:11-32", "2 Peter 3:9"],
     ["What part of your teen's heart feels like it has 'walked off into the far country'?",
      "How is the father in Luke 15 a model — and a comfort?",
      "How does this story shape how you'll receive them when they come home?"]),
    (12, "When They Fail Spectacularly", "Cuando fallan estrepitosamente",
     ["Romans 8:28-39", "Lamentations 3:22-23"],
     ["What recent failure do you need to receive — not fix?",
      "How is God using this for good, even when you can't see it?",
      "Where do you need new mercies tomorrow morning?"]),
    (13, "Releasing Them to God", "Soltándolos a Dios",
     ["1 Samuel 1:27-28", "Psalm 127:3-5"],
     ["What grip on your teen do you need to loosen this week?",
      "Like Hannah — what does 'lending them to the Lord' look like for you?",
      "What fear of losing them is making you over-control?"]),
    (14, "Long Obedience in the Same Direction", "Larga obediencia en la misma dirección",
     ["Hebrews 12:1-3", "Philippians 1:6"],
     ["What habit of love are you committed to, even when it's not bearing fruit yet?",
      "Where do you need to keep showing up, week after week, regardless?",
      "What story about your teen do you want to tell in 10 years — and what part of it starts today?"]),
]


# ---------------------------------------------------------------------------
# 15. LEADERSHIP — Servant First
# ---------------------------------------------------------------------------
LEADERSHIP = [
    (1, "All Authority Is Given", "Toda autoridad es dada",
     ["John 19:8-11", "Romans 13:1-7"],
     ["What does it change to know all your authority is on loan from God?",
      "Where have you been leading like the authority is yours, not lent?",
      "Whom do you owe accountability that you've been avoiding?"]),
    (2, "Lead Like a Servant", "Dirige como siervo",
     ["Mark 10:42-45", "Philippians 2:3-11"],
     ["Where has your leadership become more about being served than serving?",
      "Whose feet does Jesus model washing — and whose are you avoiding?",
      "What's one specific way you can serve someone you're leading this week?"]),
    (3, "Character Before Competence", "Carácter antes que competencia",
     ["1 Timothy 3:1-7", "Titus 1:5-9"],
     ["Of the Pauline lists, where is your weakest character muscle?",
      "What competency are you using to cover for a character gap?",
      "Who gets to confront your character — and have you given them permission?"]),
    (4, "Casting Vision", "Proyectando visión",
     ["Habakkuk 2:2-3", "Proverbs 29:18"],
     ["Can you write your vision in one sentence — for your family, team, life?",
      "Where do those you lead seem to 'cast off restraint' because the vision is fuzzy?",
      "What's one place you need to slow down and 'make it plain on tablets'?"]),
    (5, "Decision-Making in Fog", "Tomando decisiones en la niebla",
     ["James 1:5-8", "Proverbs 3:5-6"],
     ["What decision are you avoiding because you don't have full information?",
      "Where are you leaning on your own understanding instead of asking God?",
      "Whose wisdom — beyond yours — should shape this next call?"]),
    (6, "Hard Conversations", "Conversaciones difíciles",
     ["Ephesians 4:15", "Proverbs 27:5-6"],
     ["What hard conversation have you been delaying — and what's the cost of the delay?",
      "Where has 'keeping the peace' become enabling?",
      "What does it look like to speak the truth in love this week?"]),
    (7, "Leading When You Don't Feel Like It", "Liderar cuando no te apetece",
     ["Nehemiah 6:1-19", "1 Corinthians 16:13"],
     ["What 'distraction' or 'attack' is currently pulling you off the wall?",
      "Where are you tempted to come down because of fear or fatigue?",
      "What does it mean for you to 'be on your guard' this week?"]),
    (8, "Pride and Blind Spots", "Orgullo y puntos ciegos",
     ["Proverbs 16:18", "Galatians 6:1-3"],
     ["What blind spot has someone tried to point out that you've dismissed?",
      "Where has success made you stop listening?",
      "Whom can you ask, this week, 'What are you seeing in me that I'm not seeing?'"]),
    (9, "Burnout and Sabbath", "Agotamiento y descanso",
     ["1 Kings 19:1-18", "Mark 6:30-32"],
     ["What signs of Elijah-style burnout are showing up in you?",
      "Where has work become an idol you can't put down?",
      "What rhythm of stop, eat, sleep, and presence do you need to restart?"]),
    (10, "Succession", "Sucesión",
     ["2 Timothy 2:1-7", "Numbers 27:18-23"],
     ["Whom are you actively training to replace you?",
      "Where has insecurity made you hold on to control?",
      "What's the next responsibility you should hand off — for their sake and yours?"]),
    (11, "When You Fail Publicly", "Cuando fallas públicamente",
     ["2 Samuel 12:1-15", "Psalm 51"],
     ["When did you last fail publicly — and how did you handle it?",
      "Where are you tempted to spin instead of repent?",
      "What does Psalm 51-style repentance look like for your last failure?"]),
    (12, "Leading Your Boss / Leading Up", "Liderando hacia arriba",
     ["Daniel 1:8-21", "Genesis 39:1-6"],
     ["Where can you serve and influence the leader above you — even when you disagree?",
      "What conviction must you not compromise — and how do you hold it without arrogance?",
      "Like Joseph or Daniel, what excellence can you bring this week?"]),
    (13, "A Leader's Loneliness", "La soledad del líder",
     ["1 Samuel 30:1-6", "John 6:66-69"],
     ["Where have you been carrying the weight of leadership alone?",
      "Whom can you 'strengthen yourself in the Lord' with this week?",
      "What's the difference between being alone and being lonely as a leader?"]),
    (14, "A Leader's Epitaph", "El epitafio de un líder",
     ["Acts 13:36", "2 Timothy 4:6-8"],
     ["What do you want said at your funeral about how you led?",
      "Like David, who 'served the purpose of God in his generation' — what's your generation's purpose?",
      "What do you need to start, stop, or change this year to become that?"]),
]


# ---------------------------------------------------------------------------
# 16. WORKPLACE & PROVISION — Work as Worship
# ---------------------------------------------------------------------------
WORK = [
    (1, "Work as Worship", "Trabajo como adoración",
     ["Colossians 3:17, 23-24", "Genesis 2:15"],
     ["What would change if your next 8 hours were aimed at the Lord, not just the boss?",
      "Where has work become a curse instead of a calling?",
      "What's one specific way to work 'with all your heart' this week?"]),
    (2, "Money: Master or Servant?", "Dinero: ¿amo o siervo?",
     ["Matthew 6:19-24", "1 Timothy 6:6-10"],
     ["What does your spending in the last 30 days reveal about your true treasure?",
      "Where has money quietly become master?",
      "What 'love of money' decision do you need to confess?"]),
    (3, "Honest Weights", "Pesas honestas",
     ["Proverbs 11:1", "Leviticus 19:35-36"],
     ["Where in your work are you tempted to a 'small' dishonesty for your own benefit?",
      "What expense report, time sheet, or bid have you padded?",
      "What does integrity look like at the granular level of your work?"]),
    (4, "Integrity Under Pressure", "Integridad bajo presión",
     ["Daniel 6:1-23", "Proverbs 10:9"],
     ["What conviction is currently being tested at work?",
      "Where are you tempted to silence your faith to keep the peace?",
      "What did Daniel risk — and what would you risk if it cost you?"]),
    (5, "Ambition vs. Idolatry", "Ambición vs. idolatría",
     ["Habakkuk 2:9-11", "Luke 12:13-21"],
     ["When does ambition cross the line into idolatry for you?",
      "What 'bigger barns' are you currently building?",
      "What is the soul-question you keep avoiding by working harder?"]),
    (6, "Boss You Can't Respect", "Jefe que no puedes respetar",
     ["1 Peter 2:18-25", "Ephesians 6:5-9"],
     ["How do you serve a boss whose decisions you disagree with — without bitterness?",
      "Where has resentment quietly poisoned your work?",
      "What does following Christ look like under unfair authority this week?"]),
    (7, "Coworkers and Faith", "Compañeros y fe",
     ["Colossians 4:5-6", "1 Peter 3:15-16"],
     ["Whose name in your workplace would you have a hard time praying for — and why?",
      "Where has your faith been hidden out of fear?",
      "What 'gentle and respectful' word can you say this week?"]),
    (8, "Job Loss, Job Change", "Pérdida de empleo, cambio de empleo",
     ["Philippians 4:11-13", "Psalm 37:25"],
     ["What does your identity rest on when the job is gone?",
      "Where have you confused 'God's calling' with 'this paycheck'?",
      "What is God forming in you in the in-between?"]),
    (9, "Margin, Sabbath, and Contentment", "Margen, descanso y contentamiento",
     ["Exodus 20:8-11", "1 Timothy 6:6-8"],
     ["What part of your week never stops?",
      "Where has 'godliness with contentment' been replaced by hustle?",
      "What does sabbath look like in your specific job?"]),
    (10, "Generosity From What You Earn", "Generosidad de lo que ganas",
     ["2 Corinthians 9:6-15", "Luke 6:38"],
     ["What does your giving — time and money — actually reveal about your trust in God?",
      "Where could you be generous in a way that costs you something?",
      "What 'cheerful giver' rhythm do you want to build this year?"]),
]


# ---------------------------------------------------------------------------
# 17. RECOVERY — Twelve Steps Through Scripture
# ---------------------------------------------------------------------------
RECOVERY = [
    (1, "Powerless", "Sin poder",
     ["Romans 7:14-25", "Proverbs 28:13"],
     ["What addiction or pattern are you finally willing to admit you cannot beat?",
      "What lies have you told yourself about being 'in control'?",
      "What specifically do you need to name out loud, today?"]),
    (2, "A Power Greater", "Un Poder mayor",
     ["Philippians 4:13", "Psalm 18:1-3"],
     ["When have you tried 'self-help' approaches and watched them fail?",
      "What does 'a power greater than yourself' mean to you in concrete terms?",
      "Where is God asking to be more than a concept this week?"]),
    (3, "The Decision to Surrender", "La decisión de rendirse",
     ["Joshua 24:14-15", "Luke 15:17-20"],
     ["Like the prodigal — what 'coming to your senses' moment is on the table?",
      "What would it mean to turn your will and life over to God today?",
      "What's the first concrete step of surrender — not feeling, but action?"]),
    (4, "Searching Inventory", "Inventario sincero",
     ["Psalm 139:23-24", "Lamentations 3:40"],
     ["What patterns of harm — to yourself and others — has your addiction created?",
      "Where have you been afraid to look honestly at your life?",
      "What is one resentment you've been carrying that you need to write down?"]),
    (5, "Confession Out Loud", "Confesión en voz alta",
     ["James 5:16", "1 John 1:8-10"],
     ["To whom — not just God — do you need to confess?",
      "What does scripture promise will happen when secrets come into the light?",
      "Whom can you call this week and confess specifically?"]),
    (6, "Ready to Be Changed", "Listo para ser cambiado",
     ["Philippians 1:6", "2 Corinthians 5:17"],
     ["What 'character defect' do you actually want to keep — and what does that reveal?",
      "Where is your readiness for change still partial?",
      "What does 'new creation' have to mean for it to mean anything?"]),
    (7, "Asking for the Change", "Pidiendo el cambio",
     ["1 John 5:14-15", "Matthew 7:7-11"],
     ["What specific change have you not directly asked God to make in you?",
      "Where have you wanted change without asking?",
      "What does it look like to humbly ask God today, by name?"]),
    (8, "Listing Those Harmed", "Listando a quienes herí",
     ["Matthew 5:23-24", "Proverbs 28:13"],
     ["Whom have you harmed in your addiction — and have you let yourself remember?",
      "What lie are you telling yourself about who 'wasn't really hurt'?",
      "What are the names — even if hard to write?"]),
    (9, "Making Amends", "Restitución",
     ["Luke 19:1-10", "Proverbs 16:6"],
     ["Like Zacchaeus — what does restitution look like in your specific case?",
      "Whom can you make amends to this week, without it harming them more?",
      "What conversation have you been afraid of that needs to happen?"]),
    (10, "Daily Inventory", "Inventario diario",
     ["Ephesians 4:26-27", "Lamentations 3:22-23"],
     ["What from today did you not handle well — and what does repair look like?",
      "Where did you slip — and what's the difference between slipping and giving up?",
      "What rhythm of 'clean every night' will you commit to?"]),
    (11, "Prayer and Meditation", "Oración y meditación",
     ["Philippians 4:6-9", "Mark 1:35"],
     ["Where is prayer a discipline of recovery, not just performance?",
      "What does 'his will, not mine' actually look like this week?",
      "What practice will you keep when feelings pass?"]),
    (12, "Carry This to Others", "Llevar esto a otros",
     ["2 Corinthians 1:3-4", "1 Peter 3:15"],
     ["Whom in your life is one or two steps behind you on this road?",
      "How can your story serve someone else without becoming about you again?",
      "What does ongoing service in recovery look like in this season?"]),
]


def seed_plan_owned_faith():
    return create_plan(
        slug="owned-faith",
        title_en="Owned Faith — From Inherited to Personal",
        title_es="Fe propia — De heredada a personal",
        description_en=(
            "A 10-day journey for anyone moving from a faith handed to them "
            "into a faith they actually own. Designed for honest doubt, "
            "real questions, and a foundation that holds."
        ),
        description_es=(
            "Un recorrido de 10 días para quienes pasan de una fe heredada "
            "a una fe que realmente les pertenece. Diseñado para la duda honesta, "
            "preguntas reales y un fundamento que se sostiene."
        ),
        duration_days=10, category="faith", days=OWNED_FAITH,
    )


def seed_plan_disciplines():
    return create_plan(
        slug="seven-disciplines",
        title_en="Seven Disciplines for the Long Haul",
        title_es="Siete disciplinas para el largo plazo",
        description_en=(
            "One classical spiritual discipline per day — prayer, scripture, "
            "fasting, sabbath, silence, confession, service. Practical, ancient, "
            "and aimed at building rhythms that survive seasons of dryness."
        ),
        description_es=(
            "Una disciplina espiritual clásica por día — oración, Escritura, "
            "ayuno, sábado, silencio, confesión, servicio. Práctico, antiguo, "
            "y orientado a construir ritmos que sobreviven temporadas de sequedad."
        ),
        duration_days=7, category="disciplines", days=DISCIPLINES,
    )


def seed_plan_anxiety():
    return create_plan(
        slug="psalms-anxious",
        title_en="Psalms for the Anxious Mind",
        title_es="Salmos para la mente ansiosa",
        description_en=(
            "Seven days anchored in scripture for anyone wrestling with anxiety, "
            "panic, or the loop of overwhelming thoughts. Practical, gospel-soaked, "
            "and not afraid to name fear honestly."
        ),
        description_es=(
            "Siete días anclados en la Escritura para cualquiera que luche con "
            "ansiedad, pánico o pensamientos abrumadores. Práctico, lleno del evangelio, "
            "y sin miedo de nombrar el temor honestamente."
        ),
        duration_days=7, category="anxiety", days=ANXIETY,
    )


def seed_plan_anger():
    return create_plan(
        slug="slow-to-anger",
        title_en="Slow to Anger — Roots, Repair, and Self-Control",
        title_es="Tardo para la ira — Raíces, restauración y dominio propio",
        description_en=(
            "Seven days for the man (or woman) who keeps blowing up and is tired "
            "of it. Looks at the roots, the words, the repair, the generational "
            "patterns, and how the Spirit produces self-control."
        ),
        description_es=(
            "Siete días para el hombre (o mujer) que sigue explotando y está cansado. "
            "Mira las raíces, las palabras, la restauración, los patrones generacionales, "
            "y cómo el Espíritu produce dominio propio."
        ),
        duration_days=7, category="anger", days=ANGER,
    )


def seed_plan_grief():
    return create_plan(
        slug="lament-grief",
        title_en="Lament — Walking with God in Sorrow",
        title_es="Lamento — Caminando con Dios en el dolor",
        description_en=(
            "Ten days through the discipline of lament for anyone walking through "
            "loss — death, divorce, miscarriage, job loss, broken trust. Honest "
            "psalms, Job, and resurrection hope that refuses to rush past the pain."
        ),
        description_es=(
            "Diez días a través de la disciplina del lamento para quienes atraviesan "
            "una pérdida — muerte, divorcio, aborto espontáneo, pérdida de empleo, "
            "confianza rota. Salmos honestos, Job y esperanza de resurrección que "
            "se niega a apresurarse más allá del dolor."
        ),
        duration_days=10, category="grief", days=GRIEF,
    )


def seed_plan_young_men():
    return create_plan(
        slug="young-men-identity",
        title_en="Young Men — Identity Before Achievement",
        title_es="Hombres jóvenes — Identidad antes que logro",
        description_en=(
            "Fourteen days for young men in the tension between who they want "
            "to be and who culture says they have to be. Identity, work, lust, "
            "money, friendship, calling — straight talk, real scripture."
        ),
        description_es=(
            "Catorce días para hombres jóvenes en la tensión entre quien quieren "
            "ser y quien la cultura dice que deben ser. Identidad, trabajo, lujuria, "
            "dinero, amistad, llamado — palabras directas, escritura real."
        ),
        duration_days=14, category="young_men", days=YOUNG_MEN,
    )


def seed_plan_young_women():
    return create_plan(
        slug="young-women-anchored",
        title_en="Young Women — Anchored: Identity, Worth, and Beauty",
        title_es="Mujeres jóvenes — Ancladas: Identidad, valor y belleza",
        description_en=(
            "Fourteen days for young women navigating identity in an image culture. "
            "Worth, beauty, friendship, modesty, comparison, calling, faith of your "
            "own — written to take you seriously, not flatter you."
        ),
        description_es=(
            "Catorce días para mujeres jóvenes navegando la identidad en una cultura "
            "de imagen. Valor, belleza, amistad, modestia, comparación, llamado, fe "
            "propia — escrito para tomarte en serio, no para halagarte."
        ),
        duration_days=14, category="young_women", days=YOUNG_WOMEN,
    )


def seed_plan_dating():
    return create_plan(
        slug="dating-with-honor",
        title_en="Pursuing With Honor — Single & Dating",
        title_es="Buscando con honor — Soltería y noviazgo",
        description_en=(
            "Ten days for the single or dating Christian wanting to pursue the "
            "next relationship with honor, integrity, and clear conviction. "
            "Realistic about lust, hopeful about covenant."
        ),
        description_es=(
            "Diez días para el cristiano soltero o de novio que quiere buscar "
            "la próxima relación con honor, integridad y convicción clara. "
            "Realista sobre la lujuria, esperanzado sobre el pacto."
        ),
        duration_days=10, category="dating", days=DATING,
    )


def seed_plan_marriage():
    return create_plan(
        slug="one-flesh-marriage",
        title_en="One Flesh — A Marriage Built to Last",
        title_es="Una sola carne — Un matrimonio para durar",
        description_en=(
            "Fourteen days through the hard, holy work of marriage: love, "
            "submission, sex, money, conflict, in-laws, parenting together, "
            "and the gospel-shape of covenant. For couples who want to grow."
        ),
        description_es=(
            "Catorce días a través del trabajo duro y santo del matrimonio: amor, "
            "sumisión, sexo, dinero, conflicto, suegros, criar juntos, y la "
            "forma evangélica del pacto. Para parejas que quieren crecer."
        ),
        duration_days=14, category="marriage", days=MARRIAGE,
    )


def seed_plan_new_husband():
    return create_plan(
        slug="new-husband",
        title_en="New Husband — First Five Years",
        title_es="Esposo nuevo — Primeros cinco años",
        description_en=(
            "Ten days for the man in his first 5 years of marriage. Leaving and "
            "cleaving, listening, money, sex, spiritual leadership, and the "
            "habits — good and bad — that get locked in early."
        ),
        description_es=(
            "Diez días para el hombre en sus primeros 5 años de matrimonio. "
            "Dejar y unirse, escuchar, dinero, sexo, liderazgo espiritual, y los "
            "hábitos — buenos y malos — que se fijan temprano."
        ),
        duration_days=10, category="husband_new", days=NEW_HUSBAND,
    )


def seed_plan_fatherhood():
    return create_plan(
        slug="fathered-to-father",
        title_en="Fathered to Father — A Dad's 14 Days",
        title_es="Engendrado para engendrar — 14 días para un papá",
        description_en=(
            "Fourteen days for fathers — presence, discipline, blessing, repentance, "
            "fathering when your dad didn't, daughters, sons, and the Father you "
            "ultimately point them to. Hard, hopeful, and honest."
        ),
        description_es=(
            "Catorce días para padres — presencia, disciplina, bendición, "
            "arrepentimiento, ser padre cuando el tuyo no lo fue, hijas, hijos, "
            "y el Padre al que finalmente los señalas. Duro, esperanzador y honesto."
        ),
        duration_days=14, category="fatherhood", days=FATHERHOOD,
    )


def seed_plan_motherhood():
    return create_plan(
        slug="strong-and-tender",
        title_en="Strong & Tender — A Mother's 14 Days",
        title_es="Fuerte y tierna — 14 días para una madre",
        description_en=(
            "Fourteen days for mothers — invisibility, nurture, discipline, words, "
            "modeling faith, sister-mothers, mothering when your mother wasn't there, "
            "letting them go, and the higher Mother who never leaves."
        ),
        description_es=(
            "Catorce días para madres — invisibilidad, nutrir, disciplina, palabras, "
            "modelar la fe, hermanas-madres, ser madre cuando la tuya no estuvo, "
            "dejarlos ir, y la Madre superior que nunca abandona."
        ),
        duration_days=14, category="motherhood", days=MOTHERHOOD,
    )


def seed_plan_new_father():
    return create_plan(
        slug="new-father-first-year",
        title_en="New Father — Welcoming a Child",
        title_es="Padre nuevo — Recibiendo un hijo",
        description_en=(
            "Ten days for the man in the first months of fatherhood. Sleep, identity, "
            "fear, money, watching her become a mother, praying over a sleeping child, "
            "and the rhythms that get set in this season."
        ),
        description_es=(
            "Diez días para el hombre en los primeros meses de la paternidad. Sueño, "
            "identidad, miedo, dinero, verla convertirse en madre, orar sobre un hijo "
            "dormido, y los ritmos que se establecen en esta temporada."
        ),
        duration_days=10, category="father_new", days=NEW_FATHER,
    )


def seed_plan_parenting_teens():
    return create_plan(
        slug="parenting-teens",
        title_en="Parenting Teens — Letting Go With Love",
        title_es="Criando adolescentes — Soltando con amor",
        description_en=(
            "Fourteen days for parents of teenagers. Listening, trust, hard "
            "conversations, anxiety and depression at home, prodigals, releasing "
            "them to God, and the long obedience that doesn't quit."
        ),
        description_es=(
            "Catorce días para padres de adolescentes. Escuchar, confianza, "
            "conversaciones difíciles, ansiedad y depresión en casa, pródigos, "
            "soltarlos a Dios, y la larga obediencia que no se rinde."
        ),
        duration_days=14, category="parenting_teens", days=PARENTING_TEENS,
    )


def seed_plan_leadership():
    return create_plan(
        slug="servant-first-leadership",
        title_en="Servant First — 14 Days of Christlike Leadership",
        title_es="Siervo primero — 14 días de liderazgo cristocéntrico",
        description_en=(
            "Fourteen days for anyone leading anyone — parents, managers, pastors, "
            "elders, founders. Authority, character, vision, hard conversations, "
            "burnout, succession, and a leader's epitaph."
        ),
        description_es=(
            "Catorce días para cualquiera que lidera a alguien — padres, gerentes, "
            "pastores, ancianos, fundadores. Autoridad, carácter, visión, "
            "conversaciones difíciles, agotamiento, sucesión y el epitafio de un líder."
        ),
        duration_days=14, category="leadership", days=LEADERSHIP,
    )


def seed_plan_work():
    return create_plan(
        slug="work-as-worship",
        title_en="Work as Worship — Faith on Monday Morning",
        title_es="Trabajo como adoración — Fe el lunes por la mañana",
        description_en=(
            "Ten days for the Christian who works. Money, integrity, ambition, "
            "difficult bosses, coworkers, job loss, sabbath, and generosity. "
            "Designed for the long obedience of Mondays."
        ),
        description_es=(
            "Diez días para el cristiano que trabaja. Dinero, integridad, ambición, "
            "jefes difíciles, compañeros, pérdida de empleo, descanso y generosidad. "
            "Diseñado para la larga obediencia de los lunes."
        ),
        duration_days=10, category="work", days=WORK,
    )


def seed_plan_recovery():
    return create_plan(
        slug="twelve-steps-scripture",
        title_en="Recovery — Twelve Steps Through Scripture",
        title_es="Recuperación — Doce pasos a través de la Escritura",
        description_en=(
            "Twelve days walking the classic recovery steps with scripture. "
            "Powerlessness, surrender, inventory, confession, amends, daily "
            "inventory, prayer, and carrying it to others. For the addict, the "
            "co-addict, and anyone who has lost the battle of self-control."
        ),
        description_es=(
            "Doce días recorriendo los pasos clásicos de recuperación con la "
            "Escritura. Impotencia, rendición, inventario, confesión, restitución, "
            "inventario diario, oración y llevarlo a otros. Para el adicto, el "
            "co-adicto y cualquiera que haya perdido la batalla del dominio propio."
        ),
        duration_days=12, category="recovery", days=RECOVERY,
    )


class Command(BaseCommand):
    help = "Seed life-stage and topical reading plans (Phase 1: foundational)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding life-stage reading plans...")

        seeders = [
            # Foundational
            seed_plan_owned_faith,
            seed_plan_disciplines,
            seed_plan_anxiety,
            seed_plan_anger,
            seed_plan_grief,
            # Young adult
            seed_plan_young_men,
            seed_plan_young_women,
            seed_plan_dating,
            # Marriage stage
            seed_plan_marriage,
            seed_plan_new_husband,
            # Parenting
            seed_plan_fatherhood,
            seed_plan_motherhood,
            seed_plan_new_father,
            seed_plan_parenting_teens,
            # Vocation
            seed_plan_leadership,
            seed_plan_work,
            seed_plan_recovery,
        ]
        for fn in seeders:
            plan, created = fn()
            tag = self.style.SUCCESS("created") if created else self.style.WARNING("exists")
            self.stdout.write(f"  [{tag}] {plan.title_en}")

        self.stdout.write(self.style.SUCCESS("Life-stage plans seeded."))
