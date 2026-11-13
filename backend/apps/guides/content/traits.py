"""
Character traits a person can choose to grow in (growth plans).

Each trait gives a plain definition, passages that teach it, a place where
Jesus shows it, the study topics that build it, and a small menu of
short-term and long-term goals. Goals count faithful attempts, not
perfection: growth in character is God's work in a person as much as
their own effort.
"""

from apps.guides.catalog import L

TRAITS = [
    {
        "key": "love",
        "title": L("Love", "Amor"),
        "definition": L(
            "Love is choosing another person's good and acting on it, whether or not you feel warm "
            "toward them. It is not only a feeling, and it is not letting people harm you; it begins "
            "with being loved by God first.",
            "El amor es buscar el bien de otra persona y actuar en consecuencia, sientas o no cariño en "
            "ese momento. No es solo un sentimiento, ni es permitir que te hagan daño; empieza por "
            "saberte amado por Dios primero.",
        ),
        "refs": ["1 Corinthians 13:4-7", "1 John 4:7-12", "John 13:34-35", "Mark 12:28-31"],
        "jesus": {
            "ref": "John 15:9-13",
            "note": L(
                "On the night before he dies, Jesus tells his friends he loves them as the Father loves "
                "him, and that the greatest love gives its life for others.",
                "La noche antes de morir, Jesús les dice a sus amigos que los ama como el Padre lo ama a "
                "él, y que el amor más grande da la vida por los demás.",
            ),
        },
        "topics": ["loving_god", "loving_others"],
        "short_goals": [
            {"title": L("Do one small thing for someone near you that they did not ask for and may never notice.",
                        "Haz algo pequeño por alguien cercano que no te lo pidió y que quizá nunca lo note."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Loving others study.",
                        "Completa las dos primeras lecciones del estudio sobre amar a los demás."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Pray by name for one person you find hard to love, asking God to do them good.",
                        "Ora por nombre por una persona a la que te cuesta amar y pídele a Dios que le haga bien."),
             "kind": "prayer", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Give someone your full attention for ten minutes: phone away, listening more than talking.",
                        "Dale a alguien toda tu atención durante diez minutos: sin teléfono y escuchando más que hablando."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Loving God and Loving others studies.",
                        "Completa ocho lecciones entre los estudios sobre amar a Dios y amar a los demás."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write a few lines: where did you love well, and where did you fall short?",
                        "Una vez por semana escribe unas líneas: ¿dónde amaste bien y dónde te quedaste corto?"),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Who was easy to love this week, who was hard, and what did you do about it?",
            "¿A quién te fue fácil amar esta semana, a quién te costó, y qué hiciste al respecto?",
        ),
    },
    {
        "key": "joy",
        "title": L("Joy", "Gozo"),
        "definition": L(
            "Joy is a settled gladness in God and his gifts that can live alongside sorrow. It is not "
            "constant cheerfulness or pretending things are fine; it is noticing what is good, and who "
            "gave it, even on hard days.",
            "El gozo es una alegría profunda en Dios y en sus regalos, que puede convivir con la tristeza. "
            "No es estar siempre de buen humor ni fingir que todo está bien; es notar lo bueno, y a quien "
            "lo dio, aun en los días difíciles.",
        ),
        "refs": ["Psalm 16:8-11", "Habakkuk 3:17-19", "1 Peter 1:6-9"],
        "jesus": {
            "ref": "Luke 10:17-21",
            "note": L(
                "When his friends return glad from their mission, Jesus is filled with joy in the Holy "
                "Spirit and thanks the Father aloud for making these things known to the small and simple.",
                "Cuando sus amigos regresan contentos de su misión, Jesús se llena de gozo en el Espíritu "
                "Santo y da gracias al Padre en voz alta por dar a conocer estas cosas a los pequeños y "
                "sencillos.",
            ),
        },
        "topics": ["joy", "gratitude"],
        "short_goals": [
            {"title": L("Stop once a day to enjoy one good thing on purpose (a meal, a face, the sky) and thank God for it.",
                        "Detente una vez al día a disfrutar algo bueno a propósito (una comida, un rostro, el cielo) "
                        "y dale gracias a Dios por ello."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Joy study.",
                        "Completa las dos primeras lecciones del estudio sobre el gozo."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write down one thing that made you glad today, however small.",
                        "Cada noche anota una cosa que te alegró hoy, por pequeña que sea."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Sing, hum or listen to one song of praise during your day.",
                        "Canta, tararea o escucha una canción de alabanza durante tu día."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Joy and Gratitude studies.",
                        "Completa ocho lecciones entre los estudios sobre el gozo y la gratitud."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write about one hard thing and one good thing from the week, and tell God about both.",
                        "Una vez por semana escribe sobre algo difícil y algo bueno de la semana, y cuéntale ambas "
                        "cosas a Dios."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "What gave you real gladness this week, and what tried to steal it?",
            "¿Qué te dio verdadera alegría esta semana, y qué intentó quitártela?",
        ),
    },
    {
        "key": "peace",
        "title": L("Peace", "Paz"),
        "definition": L(
            "Peace is a settled heart that rests in God's care even when life is not settled, and that "
            "works to mend things between people. It is not the absence of problems or avoiding every "
            "hard conversation.",
            "La paz es un corazón sereno que descansa en el cuidado de Dios aunque la vida no esté en "
            "calma, y que busca reparar lo que está roto entre las personas. No es la ausencia de "
            "problemas ni evitar toda conversación difícil.",
        ),
        "refs": ["Philippians 4:6-7", "Isaiah 26:3-4", "John 14:25-27", "Matthew 5:9"],
        "jesus": {
            "ref": "Mark 4:35-41",
            "note": L(
                "In a storm that terrifies experienced fishermen, Jesus is asleep in the boat; woken, he "
                "stills the wind and the waves with a word.",
                "En una tormenta que aterra a pescadores con experiencia, Jesús duerme en la barca; al "
                "despertarlo, calma el viento y las olas con una palabra.",
            ),
        },
        "topics": ["anxiety", "rest"],
        "short_goals": [
            {"title": L("When a worry rises, turn it into a one-sentence request to God and add one thing you are thankful for.",
                        "Cuando surja una preocupación, conviértela en una petición de una frase a Dios y añade "
                        "algo por lo que das gracias."),
             "kind": "prayer", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Anxiety study.",
                        "Completa las dos primeras lecciones del estudio sobre la ansiedad."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Before bed, name one thing you cannot fix tonight and write beside it: this is in God's hands.",
                        "Antes de dormir, nombra una cosa que no puedes arreglar esta noche y escribe al lado: "
                        "esto queda en manos de Dios."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Take five quiet minutes with no screen and no task: sit, breathe slowly, and remember that God is with you.",
                        "Toma cinco minutos de quietud sin pantalla ni tareas: siéntate, respira despacio y "
                        "recuerda que Dios está contigo."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Anxiety and Rest studies.",
                        "Completa ocho lecciones entre los estudios sobre la ansiedad y el descanso."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, ask whether you are at odds with anyone, and write one small step toward peace you could take.",
                        "Una vez por semana pregúntate si estás en conflicto con alguien y escribe un paso pequeño "
                        "que podrías dar hacia la paz."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "When did you feel most at rest this week, and what kept unsettling you?",
            "¿Cuándo te sentiste más en paz esta semana, y qué fue lo que más te inquietó?",
        ),
    },
    {
        "key": "patience",
        "title": L("Patience", "Paciencia"),
        "definition": L(
            "Patience is staying steady and kind when people, plans or God move slower than you want. "
            "It is not passivity or pretending you are not frustrated; it is choosing not to let the "
            "delay decide how you treat people.",
            "La paciencia es mantenerte firme y amable cuando las personas, los planes o Dios van más "
            "lento de lo que quieres. No es pasividad ni fingir que no te frustras; es decidir que la "
            "demora no determine cómo tratas a los demás.",
        ),
        "refs": ["James 1:19-20", "Psalm 37:7-9", "James 5:7-8", "Ephesians 4:1-3"],
        "jesus": {
            "ref": "Luke 9:51-56",
            "note": L(
                "Rejected by a village, Jesus refuses his disciples' wish to retaliate and simply walks "
                "on to the next one.",
                "Rechazado por una aldea, Jesús se niega al deseo de sus discípulos de tomar represalias y "
                "simplemente sigue a la siguiente.",
            ),
        },
        "topics": ["patience", "waiting", "anger"],
        "short_goals": [
            {"title": L("When you feel rushed or irritated, pause for one slow breath before you answer.",
                        "Cuando te sientas apurado o irritado, haz una respiración lenta antes de responder."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Patience study.",
                        "Completa las dos primeras lecciones del estudio sobre la paciencia."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about a moment you waited well or badly today.",
                        "Cada noche escribe una frase sobre un momento en que esperaste bien o mal hoy."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Choose one daily wait (a queue, traffic, a slow person) and use it to pray for someone "
                        "instead of reaching for your phone.",
                        "Elige una espera diaria (una fila, el tráfico, alguien lento) y úsala para orar por "
                        "alguien en lugar de sacar el teléfono."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Patience, Waiting and Anger studies.",
                        "Completa ocho lecciones entre los estudios sobre la paciencia, la espera y el enojo."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write about one thing you are still waiting for and what the waiting is teaching you.",
                        "Una vez por semana escribe sobre algo que sigues esperando y lo que esa espera te está "
                        "enseñando."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Where did you find it easier to wait this week, and where was it hardest?",
            "¿Dónde te resultó más fácil esperar esta semana, y dónde fue más difícil?",
        ),
    },
    {
        "key": "kindness",
        "title": L("Kindness", "Amabilidad"),
        "definition": L(
            "Kindness is love made practical: noticing what someone needs and doing something about it, "
            "in words or deeds. It is not being nice so that people like you, and it does not depend on "
            "whether they deserve it.",
            "La amabilidad es el amor hecho práctico: notar lo que alguien necesita y hacer algo al "
            "respecto, con palabras o con hechos. No es ser agradable para caerle bien a la gente, ni "
            "depende de que el otro lo merezca.",
        ),
        "refs": ["Ephesians 4:31-32", "Luke 6:32-36", "Titus 3:4-7"],
        "jesus": {
            "ref": "Mark 10:46-52",
            "note": L(
                "A crowd tells a blind beggar to be quiet. Jesus stops, has him called over, and asks "
                "what he wants him to do for him.",
                "La multitud manda callar a un mendigo ciego. Jesús se detiene, pide que lo llamen y le "
                "pregunta qué quiere que haga por él.",
            ),
        },
        "topics": ["loving_others", "friendship"],
        "short_goals": [
            {"title": L("Say one specific, sincere word of encouragement to someone each day.",
                        "Dile cada día a alguien una palabra de ánimo sincera y concreta."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Loving others study.",
                        "Completa las dos primeras lecciones del estudio sobre amar a los demás."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about a kindness you gave or received today.",
                        "Cada noche escribe una frase sobre un gesto amable que diste o recibiste hoy."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Do one kind thing nobody asked for: carry something, write a note, let someone go first, make the call.",
                        "Haz un gesto amable que nadie te pidió: carga algo, escribe una nota, cede el paso, haz "
                        "esa llamada."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Loving others and Friendship studies.",
                        "Completa ocho lecciones entre los estudios sobre amar a los demás y la amistad."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write about someone you find it hard to be kind to, and one small kindness you could offer them.",
                        "Una vez por semana escribe sobre alguien con quien te cuesta ser amable y un gesto "
                        "pequeño que podrías ofrecerle."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Who did you notice this week that you might have walked past before?",
            "¿En quién te fijaste esta semana que antes quizá habrías pasado de largo?",
        ),
    },
    {
        "key": "goodness",
        "title": L("Goodness", "Bondad"),
        "definition": L(
            "Goodness is doing what is right and helpful because it is right, including when no one is "
            "watching. It is not looking good or earning God's approval; it grows out of having already "
            "received his grace.",
            "La bondad es hacer lo correcto y lo que ayuda porque es lo correcto, también cuando nadie "
            "mira. No es aparentar ni ganarse la aprobación de Dios; nace de haber recibido ya su gracia.",
        ),
        "refs": ["Galatians 6:9-10", "Micah 6:6-8", "Ephesians 2:8-10"],
        "jesus": {
            "ref": "Mark 3:1-5",
            "note": L(
                "Watched by people hoping to accuse him, Jesus asks whether it is right to do good on "
                "the day of rest, and then heals a man's hand in front of them.",
                "Vigilado por quienes buscan acusarlo, Jesús pregunta si está bien hacer el bien en el día "
                "de descanso, y luego sana la mano de un hombre delante de todos.",
            ),
        },
        "topics": ["loving_others", "service"],
        "short_goals": [
            {"title": L("Do one right thing you would normally skip because no one would know: return it, clean it up, "
                        "finish it properly.",
                        "Haz algo correcto que normalmente dejarías pasar porque nadie se enteraría: devuélvelo, "
                        "límpialo, termínalo bien."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Service study.",
                        "Completa las dos primeras lecciones del estudio sobre el servicio."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about a chance to do good that you took today, "
                        "or one you want to take tomorrow.",
                        "Cada noche escribe una frase sobre una oportunidad de hacer el bien que aprovechaste hoy, "
                        "o una que quieres aprovechar mañana."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Once a week, do something good for your neighbourhood, school, workplace or church that is not your job.",
                        "Una vez por semana haz algo bueno por tu barrio, escuela, trabajo o iglesia que no te "
                        "corresponda hacer."),
             "kind": "practice", "target_count": 8, "days": 60},
            {"title": L("Complete eight lessons across the Loving others and Service studies.",
                        "Completa ocho lecciones entre los estudios sobre amar a los demás y el servicio."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write down one good thing you saw God do through someone else, and one he did through you.",
                        "Una vez por semana anota algo bueno que viste a Dios hacer por medio de otra persona, "
                        "y algo que hizo por medio de ti."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Where did you choose what was right this week when something easier was on offer?",
            "¿Dónde elegiste lo correcto esta semana cuando había una opción más fácil?",
        ),
    },
    {
        "key": "faithfulness",
        "title": L("Faithfulness", "Fidelidad"),
        "definition": L(
            "Faithfulness is being someone God and people can count on: keeping your word and showing "
            "up, especially in small things, over a long time. It is not never failing; it is coming "
            "back each time you do.",
            "La fidelidad es ser alguien con quien Dios y los demás pueden contar: cumplir tu palabra y "
            "estar presente, sobre todo en lo pequeño, a lo largo del tiempo. No es no fallar nunca; es "
            "volver cada vez que fallas.",
        ),
        "refs": ["Luke 16:10-12", "Lamentations 3:22-24", "Matthew 25:19-23"],
        "jesus": {
            "ref": "John 17:1-5",
            "note": L(
                "Praying on the night before the cross, Jesus tells the Father he has finished the work "
                "he was given to do.",
                "Orando la noche antes de la cruz, Jesús le dice al Padre que ha terminado la obra que le "
                "encargó.",
            ),
        },
        "topics": ["perseverance", "priorities"],
        "short_goals": [
            {"title": L("Pick one small commitment (a time, a chore, a promise) and keep it each day, on time.",
                        "Elige un compromiso pequeño (una hora, una tarea, una promesa) y cúmplelo cada día, a tiempo."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Priorities study.",
                        "Completa las dos primeras lecciones del estudio sobre las prioridades."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about a promise you kept today or one you need to make right.",
                        "Cada noche escribe una frase sobre una promesa que cumpliste hoy o una que necesitas reparar."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Keep a daily time with God at the same time and place, even if it is only five minutes.",
                        "Mantén un momento diario con Dios a la misma hora y en el mismo lugar, aunque sean solo "
                        "cinco minutos."),
             "kind": "prayer", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Perseverance and Priorities studies.",
                        "Completa ocho lecciones entre los estudios sobre la perseverancia y las prioridades."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, look over what you said you would do. Finish one thing, or tell the person "
                        "honestly that you cannot.",
                        "Una vez por semana revisa lo que dijiste que harías. Termina una cosa, o dile con "
                        "honestidad a la persona que no podrás."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Where did you keep your word this week, and is there anything you need to go back and finish?",
            "¿Dónde cumpliste tu palabra esta semana, y hay algo que necesites retomar y terminar?",
        ),
    },
    {
        "key": "gentleness",
        "title": L("Gentleness", "Mansedumbre"),
        "definition": L(
            "Gentleness is strength under control: handling people with care, especially in their "
            "weaknesses and mistakes. It is not weakness or never saying hard things; it is saying and "
            "doing them in a way that does not crush.",
            "La mansedumbre es fuerza bajo control: tratar a las personas con cuidado, sobre todo en sus "
            "debilidades y errores. No es debilidad ni callar siempre lo difícil; es decirlo y hacerlo "
            "de una manera que no aplaste.",
        ),
        "refs": ["Proverbs 15:1-4", "Galatians 6:1-2", "1 Peter 3:15-16"],
        "jesus": {
            "ref": "Matthew 11:28-30",
            "note": L(
                "Jesus invites worn-out, burdened people to come to him, tells them his heart is gentle "
                "and not harsh, and says that with him they will find rest.",
                "Jesús invita a los cansados y agobiados a venir a él, les dice que su corazón es manso y "
                "no duro, y que con él encontrarán descanso.",
            ),
        },
        "topics": ["anger", "conflict", "words"],
        "short_goals": [
            {"title": L("When you need to correct or disagree with someone, lower your voice and slow down before you speak.",
                        "Cuando tengas que corregir a alguien o no estés de acuerdo, baja la voz y habla más despacio."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Words study.",
                        "Completa las dos primeras lecciones del estudio sobre las palabras."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, recall one conversation and write: was my tone gentle or sharp?",
                        "Cada noche recuerda una conversación y escribe: ¿mi tono fue suave o áspero?"),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Before sending a message you wrote while upset, wait, reread it, and soften one line.",
                        "Antes de enviar un mensaje que escribiste molesto, espera, vuelve a leerlo y suaviza una línea."),
             "kind": "practice", "target_count": 10, "days": 30},
            {"title": L("Complete eight lessons across the Anger, Conflict and Words studies.",
                        "Completa ocho lecciones entre los estudios sobre el enojo, el conflicto y las palabras."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, pray for someone whose weakness or mistake irritates you, "
                        "asking God to help you carry it with them.",
                        "Una vez por semana ora por alguien cuya debilidad o error te irrita, y pídele a Dios "
                        "que te ayude a sobrellevarlo junto a esa persona."),
             "kind": "prayer", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Where did you handle someone's mistake or weakness with care this week, and where was that hardest?",
            "¿Dónde trataste con cuidado el error o la debilidad de alguien esta semana, y dónde te costó más?",
        ),
    },
    {
        "key": "self_control",
        "title": L("Self-control", "Dominio propio"),
        "definition": L(
            "Self-control is being able to say no to an impulse so that you can say yes to something "
            "better. It is not white-knuckled willpower or hating your desires; the Bible calls it a "
            "fruit the Spirit grows, practised one small choice at a time.",
            "El dominio propio es poder decirle no a un impulso para decirle sí a algo mejor. No es pura "
            "fuerza de voluntad ni odiar tus deseos; la Biblia lo llama fruto que el Espíritu hace "
            "crecer, y se practica en una decisión pequeña a la vez.",
        ),
        "refs": ["Galatians 5:22-25", "Titus 2:11-14", "1 Corinthians 9:24-27", "Proverbs 25:28"],
        "jesus": {
            "ref": "Matthew 4:1-11",
            "note": L(
                "Hungry and alone in the wilderness, Jesus is offered three shortcuts and turns each one "
                "down, answering every time from Scripture.",
                "Con hambre y solo en el desierto, a Jesús le ofrecen tres atajos y rechaza cada uno, "
                "respondiendo siempre con la Escritura.",
            ),
        },
        "topics": ["self_control", "temptation"],
        "short_goals": [
            {"title": L("Pick one impulse (a snack, a scroll, a sharp reply) and when it comes, wait ten minutes before deciding.",
                        "Elige un impulso (un antojo, revisar el teléfono, una respuesta cortante) y, cuando "
                        "aparezca, espera diez minutos antes de decidir."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Self-control study.",
                        "Completa las dos primeras lecciones del estudio sobre el dominio propio."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about a moment you paused before acting, or wish you had.",
                        "Cada noche escribe una frase sobre un momento en que hiciste una pausa antes de actuar, "
                        "o en que te hubiera gustado hacerla."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Keep one simple limit you choose (a bedtime, a screen-free hour, a spending cap). "
                        "When you miss, begin again the next day.",
                        "Mantén un límite sencillo que tú elijas (una hora de dormir, una hora sin pantallas, un "
                        "tope de gasto). Cuando falles, vuelve a empezar al día siguiente."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Self-control and Temptation studies.",
                        "Completa ocho lecciones entre los estudios sobre el dominio propio y la tentación."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write down when your impulses are strongest (tired, hungry, lonely, stressed) "
                        "and one thing that helped.",
                        "Una vez por semana anota cuándo son más fuertes tus impulsos (cansancio, hambre, soledad, "
                        "estrés) y una cosa que te ayudó."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "What impulse did you manage to pause this week, and what makes pausing hardest?",
            "¿Qué impulso lograste frenar esta semana, y qué es lo que más te dificulta hacer una pausa?",
        ),
    },
    {
        "key": "humility",
        "title": L("Humility", "Humildad"),
        "definition": L(
            "Humility is seeing yourself truthfully before God, neither above nor beneath other people, "
            "so that you are free to listen, learn and serve. It is not putting yourself down or "
            "pretending you have no gifts.",
            "La humildad es verte con verdad delante de Dios, ni por encima ni por debajo de los demás, "
            "y así quedar libre para escuchar, aprender y servir. No es menospreciarte ni fingir que no "
            "tienes dones.",
        ),
        "refs": ["Philippians 2:3-8", "Luke 18:9-14", "1 Peter 5:5-7"],
        "jesus": {
            "ref": "John 13:1-5",
            "note": L(
                "Knowing the Father has put everything in his hands, Jesus gets up from the table, ties a "
                "towel around his waist and washes his friends' feet.",
                "Sabiendo que el Padre ha puesto todo en sus manos, Jesús se levanta de la mesa, se ata una "
                "toalla a la cintura y les lava los pies a sus amigos.",
            ),
        },
        "topics": ["humility", "grace"],
        "short_goals": [
            {"title": L("In one conversation a day, ask a question and listen to the whole answer before giving your own view.",
                        "En una conversación al día, haz una pregunta y escucha toda la respuesta antes de dar tu opinión."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Humility study.",
                        "Completa las dos primeras lecciones del estudio sobre la humildad."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one thing you learned from someone else today, or one thing you got wrong.",
                        "Cada noche escribe algo que aprendiste hoy de otra persona, o algo en lo que te equivocaste."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Give someone else the credit, the better seat or the last word, and leave it at that.",
                        "Cédele a otra persona el mérito, el mejor lugar o la última palabra, y déjalo así."),
             "kind": "practice", "target_count": 12, "days": 30},
            {"title": L("Complete eight lessons across the Humility and Grace studies.",
                        "Completa ocho lecciones entre los estudios sobre la humildad y la gracia."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write about a time you were corrected or disagreed with, and what was true in it.",
                        "Una vez por semana escribe sobre una ocasión en que te corrigieron o te llevaron la "
                        "contraria, y qué había de cierto en ello."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "When was it easy to listen, admit a mistake or take a lower place this week, and when did pride push back?",
            "¿Cuándo te resultó fácil escuchar, reconocer un error o ceder el lugar esta semana, y cuándo se "
            "resistió tu orgullo?",
        ),
    },
    {
        "key": "courage",
        "title": L("Courage", "Valentía"),
        "definition": L(
            "Courage is doing the right or loving thing while you are still afraid, because God is with "
            "you. It is not the absence of fear, and it is not recklessness or being loud.",
            "La valentía es hacer lo correcto o lo amoroso aunque todavía tengas miedo, porque Dios está "
            "contigo. No es la ausencia de miedo, ni es imprudencia ni hablar más fuerte que los demás.",
        ),
        "refs": ["Joshua 1:6-9", "Psalm 27:1-3", "2 Timothy 1:6-8"],
        "jesus": {
            "ref": "John 18:4-9",
            "note": L(
                "When armed men come to arrest him at night, Jesus steps forward, says who he is, and "
                "asks them to let his friends go.",
                "Cuando hombres armados llegan de noche a arrestarlo, Jesús da un paso al frente, dice "
                "quién es y pide que dejen ir a sus amigos.",
            ),
        },
        "topics": ["courage", "fear"],
        "short_goals": [
            {"title": L("Do one small thing you have been putting off because it scares you: make the call, ask the question, say hello.",
                        "Haz una cosa pequeña que has estado posponiendo porque te da miedo: haz la llamada, haz "
                        "la pregunta, saluda."),
             "kind": "practice", "target_count": 3, "days": 7},
            {"title": L("Complete the first two lessons of the Courage study.",
                        "Completa las dos primeras lecciones del estudio sobre la valentía."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each morning, tell God what you are most nervous about today and ask him to go with you into it.",
                        "Cada mañana dile a Dios qué es lo que más te pone nervioso hoy y pídele que te acompañe."),
             "kind": "prayer", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Once a week, take one step toward something right that frightens you, and tell a trusted person you did it.",
                        "Una vez por semana da un paso hacia algo correcto que te asusta, y cuéntale a una persona "
                        "de confianza que lo hiciste."),
             "kind": "practice", "target_count": 8, "days": 60},
            {"title": L("Complete eight lessons across the Courage and Fear studies.",
                        "Completa ocho lecciones entre los estudios sobre la valentía y el temor."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write down one fear, what it tells you will happen, and what is true about God in that place.",
                        "Una vez por semana anota un temor, lo que ese temor te dice que pasará, y lo que es verdad "
                        "acerca de Dios en esa situación."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "What did you do this week even though you were afraid, and what fear is still holding you back?",
            "¿Qué hiciste esta semana a pesar del miedo, y qué temor todavía te detiene?",
        ),
    },
    {
        "key": "wisdom",
        "title": L("Wisdom", "Sabiduría"),
        "definition": L(
            "Wisdom is knowing how to live well before God in real situations: seeing what matters and "
            "choosing accordingly. It is not cleverness, having an opinion on everything, or never "
            "needing advice; it starts with asking.",
            "La sabiduría es saber vivir bien delante de Dios en situaciones reales: ver lo que importa y "
            "elegir de acuerdo con eso. No es ser muy listo, opinar de todo ni no necesitar consejo; "
            "empieza por pedirla.",
        ),
        "refs": ["James 1:5-8", "Proverbs 2:1-6", "James 3:13-17"],
        "jesus": {
            "ref": "Luke 2:46-52",
            "note": L(
                "At twelve, Jesus sits among the teachers, listening and asking questions; then he goes "
                "home with his parents and keeps growing in wisdom.",
                "A los doce años, Jesús se sienta entre los maestros, escuchando y haciendo preguntas; luego "
                "vuelve a casa con sus padres y sigue creciendo en sabiduría.",
            ),
        },
        "topics": ["decisions", "scripture"],
        "short_goals": [
            {"title": L("Before one decision each day, however small, pause and ask God for wisdom in a single sentence.",
                        "Antes de una decisión cada día, por pequeña que sea, detente y pídele a Dios sabiduría "
                        "en una sola frase."),
             "kind": "prayer", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Decisions study.",
                        "Completa las dos primeras lecciones del estudio sobre las decisiones."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about a choice you made today and what you would keep or change.",
                        "Cada noche escribe una frase sobre una decisión que tomaste hoy y qué mantendrías o cambiarías."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Read a few verses from Proverbs and choose one thought to carry with you through the day.",
                        "Lee unos versículos de Proverbios y elige una idea para llevar contigo durante el día."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Decisions and Scripture studies.",
                        "Completa ocho lecciones entre los estudios sobre las decisiones y la Biblia."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write about a decision in front of you: what you know, what you do not, "
                        "and who you could ask for advice.",
                        "Una vez por semana escribe sobre una decisión que tienes por delante: lo que sabes, lo "
                        "que no sabes y a quién podrías pedirle consejo."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Where did you ask for wisdom this week, from God or from someone else, and what did you do with it?",
            "¿Dónde pediste sabiduría esta semana, a Dios o a otra persona, y qué hiciste con ella?",
        ),
    },
    {
        "key": "forgiveness",
        "title": L("Forgiveness", "Perdón"),
        "definition": L(
            "Forgiveness is releasing someone from the debt of what they did to you and handing justice "
            "to God, because you have been forgiven much. It is not saying it did not matter, forgetting, "
            "or going back to a place where you are being harmed; often it is a choice made many times.",
            "El perdón es soltar a alguien de la deuda de lo que te hizo y dejar la justicia en manos de "
            "Dios, porque a ti se te ha perdonado mucho. No es decir que no importó, ni olvidar, ni "
            "volver a un lugar donde te hacen daño; muchas veces es una decisión que se toma una y otra vez.",
        ),
        "refs": ["Psalm 103:8-12", "Matthew 18:21-22", "Colossians 3:12-13", "Romans 12:17-21"],
        "jesus": {
            "ref": "Luke 23:32-34",
            "note": L(
                "While he is being crucified, Jesus asks the Father to forgive the people doing it.",
                "Mientras lo crucifican, Jesús le pide al Padre que perdone a quienes lo están haciendo.",
            ),
        },
        "topics": ["forgiveness", "grace", "conflict"],
        "short_goals": [
            {"title": L("Tell God honestly, in a sentence or two, about one hurt you are still carrying and who caused it.",
                        "Cuéntale a Dios con honestidad, en una o dos frases, una herida que todavía cargas y quién la causó."),
             "kind": "prayer", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Forgiveness study.",
                        "Completa las dos primeras lecciones del estudio sobre el perdón."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Write a few lines about how God has forgiven you, and one thing you find hard to let go of.",
                        "Escribe unas líneas sobre cómo Dios te ha perdonado a ti, y una cosa que te cuesta soltar."),
             "kind": "reflection", "target_count": 3, "days": 7},
        ],
        "long_goals": [
            {"title": L("When the memory of a wrong returns, tell God you choose again to leave it with him. "
                        "Then, if you can, ask one good thing for that person.",
                        "Cuando vuelva el recuerdo de una ofensa, dile a Dios que decides otra vez dejarla con él. "
                        "Luego, si puedes, pide algo bueno para esa persona."),
             "kind": "prayer", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Forgiveness, Grace and Conflict studies.",
                        "Completa ocho lecciones entre los estudios sobre el perdón, la gracia y el conflicto."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Where it is safe and wise, take one step toward mending a relationship: an apology you owe "
                        "or an honest talk. If unsure, ask someone you trust first.",
                        "Donde sea seguro y prudente, da un paso para reparar una relación: una disculpa que debes "
                        "o una conversación honesta. Si dudas, pide antes consejo a alguien de confianza."),
             "kind": "practice", "target_count": 3, "days": 90},
        ],
        "check_in_question": L(
            "What are you finding easier to release this week, and what still stings when you remember it?",
            "¿Qué te está resultando más fácil soltar esta semana, y qué te sigue doliendo al recordarlo?",
        ),
    },
    {
        "key": "gratitude",
        "title": L("Gratitude", "Gratitud"),
        "definition": L(
            "Gratitude is noticing what you have been given and saying thank you, to God and to people. "
            "It is not denying what is hard or comparing yourself with those worse off; it is refusing "
            "to let the hard things be the only things you see.",
            "La gratitud es notar lo que has recibido y dar las gracias, a Dios y a las personas. No es "
            "negar lo difícil ni compararte con quienes están peor; es no dejar que lo difícil sea lo "
            "único que ves.",
        ),
        "refs": ["1 Thessalonians 5:16-18", "Psalm 103:1-5", "Colossians 3:15-17"],
        "jesus": {
            "ref": "Luke 22:14-20",
            "note": L(
                "At his last meal with his friends, knowing what the night will bring, Jesus takes the "
                "bread and the cup and gives thanks.",
                "En su última cena con sus amigos, sabiendo lo que traerá la noche, Jesús toma el pan y la "
                "copa y da gracias.",
            ),
        },
        "topics": ["gratitude", "contentment"],
        "short_goals": [
            {"title": L("Each evening, write down three specific things from today you are thankful for.",
                        "Cada noche anota tres cosas concretas de hoy por las que das gracias."),
             "kind": "reflection", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Gratitude study.",
                        "Completa las dos primeras lecciones del estudio sobre la gratitud."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Thank one person, out loud or in writing, for something specific they did.",
                        "Dale las gracias a una persona, en voz alta o por escrito, por algo concreto que hizo."),
             "kind": "practice", "target_count": 3, "days": 7},
        ],
        "long_goals": [
            {"title": L("Before you eat, stop and thank God for the food and for one other thing from the day.",
                        "Antes de comer, detente y dale gracias a Dios por la comida y por otra cosa del día."),
             "kind": "prayer", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Gratitude and Contentment studies.",
                        "Completa ocho lecciones entre los estudios sobre la gratitud y el contentamiento."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write a short note or message of thanks to someone who has shaped your life.",
                        "Una vez por semana escribe una nota o mensaje breve de agradecimiento a alguien que ha "
                        "marcado tu vida."),
             "kind": "practice", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "What are you most thankful for this week, and what did you nearly overlook?",
            "¿Qué es lo que más agradeces de esta semana, y qué estuviste a punto de pasar por alto?",
        ),
    },
    {
        "key": "honesty",
        "title": L("Honesty", "Honestidad"),
        "definition": L(
            "Honesty is telling the truth and living it: your words match the facts, and the person "
            "people see is the person you are, before God, others and yourself. It is not bluntness or "
            "saying everything you think; truth is spoken in love.",
            "La honestidad es decir la verdad y vivirla: que tus palabras coincidan con los hechos y que "
            "la persona que los demás ven sea la que eres, ante Dios, ante otros y ante ti. No es ser "
            "brusco ni decir todo lo que piensas; la verdad se dice con amor.",
        ),
        "refs": ["Ephesians 4:25", "Colossians 3:9-10", "Psalm 15:1-3", "1 John 1:8-9"],
        "jesus": {
            "ref": "John 18:33-37",
            "note": L(
                "Questioned by the governor who can have him put to death, Jesus answers plainly and "
                "says he was born to be a witness to the truth.",
                "Interrogado por el gobernador que puede mandarlo a la muerte, Jesús responde con claridad "
                "y dice que nació para ser testigo de la verdad.",
            ),
        },
        "topics": ["words", "conflict"],
        "short_goals": [
            {"title": L("When you catch yourself exaggerating, shading a story or making an excuse, stop and say it straight.",
                        "Cuando te descubras exagerando, acomodando una historia o poniendo una excusa, detente y "
                        "dilo tal como es."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Words study.",
                        "Completa las dos primeras lecciones del estudio sobre las palabras."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, tell God one thing about your day exactly as it was, without tidying it up, "
                        "and write one sentence about it.",
                        "Cada noche cuéntale a Dios una cosa de tu día tal como fue, sin maquillarla, y escribe "
                        "una frase sobre ella."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("When someone who cares about you asks how you are, give them a true answer.",
                        "Cuando alguien que te quiere te pregunte cómo estás, respóndele con la verdad."),
             "kind": "practice", "target_count": 8, "days": 30},
            {"title": L("Complete eight lessons across the Words and Conflict studies.",
                        "Completa ocho lecciones entre los estudios sobre las palabras y el conflicto."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, ask yourself where you were tempted to look better than you are, and write what you did.",
                        "Una vez por semana pregúntate dónde tuviste la tentación de aparentar más de lo que eres, "
                        "y escribe qué hiciste."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Where was it costly to tell the truth this week, and is there anything you need to set straight?",
            "¿Dónde te costó decir la verdad esta semana, y hay algo que necesites aclarar?",
        ),
    },
    {
        "key": "generosity",
        "title": L("Generosity", "Generosidad"),
        "definition": L(
            "Generosity is giving freely from what you have (money, time, attention, skill, a place at "
            "your table) because everything you have was first a gift. It is not about the amount, and "
            "it is not a way to get more back from God.",
            "La generosidad es dar con libertad de lo que tienes (dinero, tiempo, atención, habilidades, "
            "un lugar en tu mesa) porque todo lo que tienes fue primero un regalo. No se trata de la "
            "cantidad, ni es una manera de conseguir que Dios te devuelva más.",
        ),
        "refs": ["2 Corinthians 9:6-8", "Luke 21:1-4", "1 Timothy 6:17-19", "Acts 20:33-35"],
        "jesus": {
            "ref": "Mark 6:34-44",
            "note": L(
                "His friends want to send a hungry crowd away. Jesus has them bring the little food they "
                "have, blesses it, and shares it out until everyone has eaten.",
                "Sus amigos quieren despedir a una multitud hambrienta. Jesús les pide que traigan la poca "
                "comida que tienen, la bendice y la reparte hasta que todos comen.",
            ),
        },
        "topics": ["money", "service"],
        "short_goals": [
            {"title": L("Give something away: a little money, an hour of your time, or something you own that someone else needs more.",
                        "Regala algo: un poco de dinero, una hora de tu tiempo, o algo tuyo que otra persona "
                        "necesita más."),
             "kind": "practice", "target_count": 3, "days": 7},
            {"title": L("Complete the first two lessons of the Money study.",
                        "Completa las dos primeras lecciones del estudio sobre el dinero."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one thing you received today that you did not earn.",
                        "Cada noche anota una cosa que recibiste hoy sin habértela ganado."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Once a week, give time or help to one person or cause, and do it without mentioning it to anyone.",
                        "Una vez por semana dedica tiempo o ayuda a una persona o causa, y hazlo sin contárselo a nadie."),
             "kind": "practice", "target_count": 8, "days": 60},
            {"title": L("Complete eight lessons across the Money and Service studies.",
                        "Completa ocho lecciones entre los estudios sobre el dinero y el servicio."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a month, look at where your money and free time went, and choose one amount or one hour "
                        "to give on purpose next month.",
                        "Una vez al mes revisa en qué se fueron tu dinero y tu tiempo libre, y elige una cantidad "
                        "o una hora para dar a propósito el mes siguiente."),
             "kind": "reflection", "target_count": 3, "days": 90},
        ],
        "check_in_question": L(
            "What did you give this week (time, money, attention), and how did it feel to let it go?",
            "¿Qué diste esta semana (tiempo, dinero, atención), y cómo te sentiste al soltarlo?",
        ),
    },
    {
        "key": "contentment",
        "title": L("Contentment", "Contentamiento"),
        "definition": L(
            "Contentment is being at peace with what you have and where you are today, because God is "
            "with you in it. It is not giving up on change or pretending you want nothing; it is not "
            "needing the next thing in order to be all right.",
            "El contentamiento es estar en paz con lo que tienes y con el lugar donde estás hoy, porque "
            "Dios está contigo ahí. No es renunciar a que las cosas cambien ni fingir que no deseas nada; "
            "es no necesitar lo siguiente para estar bien.",
        ),
        "refs": ["Philippians 4:11-13", "1 Timothy 6:6-8", "Hebrews 13:5-6"],
        "jesus": {
            "ref": "John 4:31-34",
            "note": L(
                "When his friends urge him to eat, Jesus tells them that what truly feeds him is doing "
                "the will of the one who sent him.",
                "Cuando sus amigos le insisten en que coma, Jesús les dice que lo que de verdad lo alimenta "
                "es hacer la voluntad de quien lo envió.",
            ),
        },
        "topics": ["contentment", "money", "gratitude"],
        "short_goals": [
            {"title": L("When you catch yourself comparing or wanting more, name one thing you already have and thank God for it.",
                        "Cuando te descubras comparándote o deseando algo más, nombra una cosa que ya tienes y "
                        "dale gracias a Dios por ella."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Contentment study.",
                        "Completa las dos primeras lecciones del estudio sobre el contentamiento."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, finish this sentence in writing: today I had enough of...",
                        "Cada noche completa por escrito esta frase: hoy tuve suficiente de..."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Go through the day without the one thing that most feeds comparison for you (a feed, a shop, a catalogue).",
                        "Pasa el día sin eso que más alimenta tu comparación (una red social, una tienda, un catálogo)."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Contentment, Money and Gratitude studies.",
                        "Completa ocho lecciones entre los estudios sobre el contentamiento, el dinero y la gratitud."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write down one thing you wanted and did not get, and tell God honestly how you feel about it.",
                        "Una vez por semana anota algo que querías y no obtuviste, y cuéntale a Dios con "
                        "honestidad cómo te sientes al respecto."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "When did what you have feel like enough this week, and what stirred up wanting more?",
            "¿Cuándo sentiste esta semana que lo que tienes es suficiente, y qué despertó el deseo de tener más?",
        ),
    },
    {
        "key": "perseverance",
        "title": L("Perseverance", "Perseverancia"),
        "definition": L(
            "Perseverance is continuing to do what is right and to trust God when it is hard, slow or "
            "unrewarded. It is not gritting your teeth alone or never resting; it is taking the next "
            "faithful step and getting up again after a fall.",
            "La perseverancia es seguir haciendo lo correcto y confiando en Dios cuando es difícil, lento "
            "o nadie lo reconoce. No es apretar los dientes a solas ni no descansar nunca; es dar el "
            "siguiente paso fiel y levantarte de nuevo después de caer.",
        ),
        "refs": ["Hebrews 12:1-3", "James 1:2-4", "Romans 5:3-5"],
        "jesus": {
            "ref": "Mark 14:32-42",
            "note": L(
                "In the garden, deeply distressed, Jesus asks for another way, yields to the Father's "
                "will, and then gets up to face what is coming.",
                "En el huerto, profundamente angustiado, Jesús pide otro camino, se entrega a la voluntad "
                "del Padre y luego se levanta para enfrentar lo que viene.",
            ),
        },
        "topics": ["perseverance", "hope"],
        "short_goals": [
            {"title": L("Choose one good thing you tend to give up on and do the smallest version of it each day (five minutes counts).",
                        "Elige algo bueno que sueles abandonar y haz cada día su versión más pequeña (cinco "
                        "minutos cuentan)."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Perseverance study.",
                        "Completa las dos primeras lecciones del estudio sobre la perseverancia."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about where you kept going today, "
                        "and one place you want to try again tomorrow.",
                        "Cada noche escribe una frase sobre dónde seguiste adelante hoy, y un punto en el que "
                        "quieres volver a intentarlo mañana."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Keep up one small daily practice you have chosen. When you miss a day, simply start again the next.",
                        "Mantén una práctica diaria pequeña que tú elijas. Cuando falles un día, simplemente "
                        "retómala al siguiente."),
             "kind": "practice", "target_count": 60, "days": 90},
            {"title": L("Complete eight lessons across the Perseverance and Hope studies.",
                        "Completa ocho lecciones entre los estudios sobre la perseverancia y la esperanza."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, bring God the thing that tires you most and ask for strength for just the next seven days.",
                        "Una vez por semana llévale a Dios lo que más te cansa y pídele fuerzas solo para los "
                        "próximos siete días."),
             "kind": "prayer", "target_count": 4, "days": 30},
        ],
        "check_in_question": L(
            "What tempted you to give up this week, and what or who helped you keep going?",
            "¿Qué te tentó a rendirte esta semana, y qué o quién te ayudó a seguir?",
        ),
    },
    {
        "key": "compassion",
        "title": L("Compassion", "Compasión"),
        "definition": L(
            "Compassion is letting someone else's pain reach you and moving toward them to help. It is "
            "not pity from a distance or fixing people; often it is simply staying, listening and doing "
            "the one thing you can.",
            "La compasión es dejar que el dolor de otra persona te alcance y acercarte para ayudar. No es "
            "lástima desde lejos ni arreglarle la vida a nadie; muchas veces es simplemente quedarte, "
            "escuchar y hacer lo que sí puedes.",
        ),
        "refs": ["Luke 10:30-37", "2 Corinthians 1:3-4", "Psalm 103:13-14", "Romans 12:15"],
        "jesus": {
            "ref": "Luke 7:11-15",
            "note": L(
                "Meeting a widow on her way to bury her only son, Jesus is moved with compassion, speaks "
                "to her first, and gives her son back to her.",
                "Al encontrarse con una viuda que va a enterrar a su único hijo, Jesús se conmueve, le "
                "habla primero a ella y le devuelve a su hijo.",
            ),
        },
        "topics": ["loving_others", "suffering"],
        "short_goals": [
            {"title": L("Ask someone who is having a hard time how they really are, and listen without offering a fix.",
                        "Pregúntale a alguien que la está pasando mal cómo está de verdad, y escucha sin ofrecer soluciones."),
             "kind": "practice", "target_count": 3, "days": 7},
            {"title": L("Complete the first two lessons of the Loving others study.",
                        "Completa las dos primeras lecciones del estudio sobre amar a los demás."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each day, pray by name for one person who is hurting: sick, grieving, lonely or afraid.",
                        "Cada día ora por nombre por una persona que sufre: enferma, de duelo, sola o con miedo."),
             "kind": "prayer", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Once a week, do one practical thing for someone who is struggling: a meal, a ride, a visit, a message.",
                        "Una vez por semana haz algo práctico por alguien que la está pasando mal: una comida, "
                        "un mandado, una visita, un mensaje."),
             "kind": "practice", "target_count": 8, "days": 60},
            {"title": L("Complete eight lessons across the Loving others and Suffering studies.",
                        "Completa ocho lecciones entre los estudios sobre amar a los demás y el sufrimiento."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write about someone whose situation you find hard to understand, "
                        "and try to describe their week from the inside.",
                        "Una vez por semana escribe sobre alguien cuya situación te cuesta entender, e intenta "
                        "describir su semana desde adentro."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "Whose pain did you notice this week, and what did you do with what you noticed?",
            "¿El dolor de quién notaste esta semana, y qué hiciste con lo que notaste?",
        ),
    },
    {
        "key": "hope",
        "title": L("Hope", "Esperanza"),
        "definition": L(
            "Hope is a confident expectation that God will keep his promises and that the worst thing "
            "is never the last thing. It is not optimism or wishing; it rests on who God is and on Jesus "
            "being raised, so it can hold even when you cannot see how.",
            "La esperanza es confiar con firmeza en que Dios cumplirá sus promesas y en que lo peor nunca "
            "es lo último. No es optimismo ni ilusión; descansa en quién es Dios y en que Jesús resucitó, "
            "por eso puede sostenerse aun cuando no ves cómo.",
        ),
        "refs": ["Romans 15:13", "1 Peter 1:3-5", "Romans 8:24-25", "Isaiah 40:28-31"],
        "jesus": {
            "ref": "Luke 23:39-43",
            "note": L(
                "Dying on the cross, Jesus hears a criminal beside him ask to be remembered, and promises "
                "that man a place with him.",
                "Muriendo en la cruz, Jesús escucha a un criminal a su lado pedirle que se acuerde de él, y "
                "le promete un lugar junto a él.",
            ),
        },
        "topics": ["hope", "eternity"],
        "short_goals": [
            {"title": L("Each morning, tell God one thing you are hoping for and one thing you fear will never change.",
                        "Cada mañana dile a Dios una cosa que esperas y una que temes que nunca cambie."),
             "kind": "prayer", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Hope study.",
                        "Completa las dos primeras lecciones del estudio sobre la esperanza."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write down one small sign of good you saw today.",
                        "Cada noche anota una pequeña señal de bien que viste hoy."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Once a week, encourage someone who is discouraged: tell them one true reason you have hope for them.",
                        "Una vez por semana anima a alguien que está desanimado: dile una razón verdadera por la "
                        "que tienes esperanza para esa persona."),
             "kind": "practice", "target_count": 8, "days": 60},
            {"title": L("Complete eight lessons across the Hope and Eternity studies.",
                        "Completa ocho lecciones entre los estudios sobre la esperanza y la eternidad."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write down one way God has been faithful to you before, and read back over the list.",
                        "Una vez por semana anota una manera en que Dios te ha sido fiel antes, y vuelve a leer la lista."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "What are you looking forward to this week, and where does hope feel thin?",
            "¿Qué esperas con ilusión esta semana, y dónde sientes que te falta esperanza?",
        ),
    },
    {
        "key": "trust",
        "title": L("Trust", "Confianza"),
        "definition": L(
            "Trust is leaning your weight on God's character when you cannot see the outcome, and "
            "acting on what he has said. It is not having no questions or no fear; it is bringing both "
            "to him instead of carrying them alone.",
            "La confianza es apoyarte en el carácter de Dios cuando no puedes ver el resultado, y actuar "
            "según lo que él ha dicho. No es no tener preguntas ni miedo; es llevarle ambas cosas en vez "
            "de cargarlas a solas.",
        ),
        "refs": ["Proverbs 3:5-6", "Psalm 62:5-8", "Jeremiah 17:7-8", "Psalm 56:3-4"],
        "jesus": {
            "ref": "Luke 23:44-46",
            "note": L(
                "With his last breath on the cross, Jesus entrusts himself into the Father's hands.",
                "Con su último aliento en la cruz, Jesús se encomienda en las manos del Padre.",
            ),
        },
        "topics": ["refuge", "waiting", "doubt"],
        "short_goals": [
            {"title": L("Each morning, open your hands, name one thing you cannot control today, "
                        "and tell God you are leaving it with him.",
                        "Cada mañana abre las manos, nombra una cosa que hoy no puedes controlar y dile a Dios "
                        "que la dejas con él."),
             "kind": "prayer", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Refuge study.",
                        "Completa las dos primeras lecciones del estudio sobre el refugio."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about where you relied on God today and where you relied only on yourself.",
                        "Cada noche escribe una frase sobre dónde te apoyaste en Dios hoy y dónde te apoyaste "
                        "solo en ti."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Once a week, take one step you believe is right but have been putting off until you felt sure.",
                        "Una vez por semana da un paso que crees correcto pero has pospuesto hasta sentirte seguro."),
             "kind": "practice", "target_count": 8, "days": 60},
            {"title": L("Complete eight lessons across the Refuge, Waiting and Doubt studies.",
                        "Completa ocho lecciones entre los estudios sobre el refugio, la espera y las dudas."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, write down honestly one question or doubt you have for God, "
                        "and one thing you still know to be true of him.",
                        "Una vez por semana escribe con honestidad una pregunta o duda que tienes para Dios, y "
                        "una cosa que sigues sabiendo que es verdad acerca de él."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "What did you hand over to God this week, and what are you still gripping tightly?",
            "¿Qué le entregaste a Dios esta semana, y qué sigues agarrando con fuerza?",
        ),
    },
    {
        "key": "purity",
        "title": L("Purity", "Pureza"),
        "definition": L(
            "Purity is an undivided heart: wanting what God wants in what you look at, dwell on and do "
            "with your body, and treating every person as a person, never an object. It is not shame "
            "about being human or a record of never slipping; it begins with a clean heart God gives, "
            "and begins again each time you return to him.",
            "La pureza es un corazón no dividido: querer lo que Dios quiere en lo que miras, en lo que "
            "piensas y en lo que haces con tu cuerpo, y tratar a cada persona como persona, nunca como "
            "objeto. No es avergonzarte de ser humano ni llevar la cuenta de no fallar nunca; empieza con "
            "un corazón limpio que Dios da, y vuelve a empezar cada vez que regresas a él.",
        ),
        "refs": ["Psalm 51:10-12", "Philippians 4:8-9", "Matthew 5:8", "1 Corinthians 6:19-20"],
        "jesus": {
            "ref": "Hebrews 4:14-16",
            "note": L(
                "Jesus knows temptation from the inside: he faced it fully and did not give in. So he "
                "meets us with understanding and welcomes us when we come to him for mercy and help.",
                "Jesús conoce la tentación desde adentro: la enfrentó de lleno y no cedió. Por eso nos "
                "entiende y nos recibe cuando acudimos a él en busca de misericordia y ayuda.",
            ),
        },
        "topics": ["temptation", "self_control", "grace"],
        "short_goals": [
            {"title": L("When something you are looking at or dwelling on pulls you where you do not want to go, "
                        "turn away and put your attention on one good thing.",
                        "Cuando algo que miras o en lo que piensas te lleve a donde no quieres ir, apártate y pon "
                        "tu atención en una cosa buena."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Temptation study.",
                        "Completa las dos primeras lecciones del estudio sobre la tentación."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each morning, ask God in one sentence for a clean heart today. If you slipped yesterday, "
                        "tell him simply and receive his forgiveness.",
                        "Cada mañana pídele a Dios en una frase un corazón limpio para hoy. Si ayer fallaste, "
                        "díselo con sencillez y recibe su perdón."),
             "kind": "prayer", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Choose one guard for your eyes and mind (a screen-free bedroom, a filter, a time limit) and keep it. "
                        "If you break it, restart the same day.",
                        "Elige una medida para cuidar tus ojos y tu mente (dormitorio sin pantallas, un filtro, un "
                        "límite de tiempo) y mantenla. Si la rompes, retómala ese mismo día."),
             "kind": "practice", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Temptation, Self-control and Grace studies.",
                        "Completa ocho lecciones entre los estudios sobre la tentación, el dominio propio y la gracia."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, talk honestly with one trusted person about how you are doing, "
                        "or write it to God if you are not ready for that yet.",
                        "Una vez por semana habla con honestidad con una persona de confianza sobre cómo vas, "
                        "o escríbeselo a Dios si todavía no te sientes listo para eso."),
             "kind": "reflection", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "What helped you keep your heart and attention where you want them this week, "
            "and where do you need grace to begin again?",
            "¿Qué te ayudó esta semana a mantener tu corazón y tu atención donde quieres, y dónde necesitas "
            "gracia para volver a empezar?",
        ),
    },
    {
        "key": "servanthood",
        "title": L("Servanthood", "Espíritu de servicio"),
        "definition": L(
            "Servanthood is using your strength, time and position for other people's good rather than "
            "your own importance. It is not being a doormat or never resting; it is choosing the towel "
            "freely, as Jesus did.",
            "Tener espíritu de servicio es usar tus fuerzas, tu tiempo y tu posición para el bien de "
            "otros y no para tu propia importancia. No es dejar que te pisoteen ni no descansar nunca; "
            "es tomar la toalla libremente, como lo hizo Jesús.",
        ),
        "refs": ["Galatians 5:13-14", "1 Peter 4:10-11", "Matthew 25:34-40", "John 13:12-15"],
        "jesus": {
            "ref": "Mark 10:42-45",
            "note": L(
                "When his friends jostle for the best places, Jesus tells them that he himself did not "
                "come to be waited on but to serve, and to give his life for others.",
                "Cuando sus amigos se disputan los mejores puestos, Jesús les dice que él mismo no vino a "
                "que lo atiendan, sino a servir y a dar su vida por otros.",
            ),
        },
        "topics": ["service", "humility"],
        "short_goals": [
            {"title": L("Do one task at home, school or work that is not yours and that nobody likes, without being asked.",
                        "Haz una tarea en casa, en la escuela o en el trabajo que no te toca y que a nadie le "
                        "gusta, sin que te la pidan."),
             "kind": "practice", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Service study.",
                        "Completa las dos primeras lecciones del estudio sobre el servicio."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Each evening, write one sentence about someone who served you today "
                        "and how you might do the same for another.",
                        "Cada noche escribe una frase sobre alguien que te sirvió hoy y cómo podrías hacer lo "
                        "mismo por otra persona."),
             "kind": "reflection", "target_count": 5, "days": 7},
        ],
        "long_goals": [
            {"title": L("Once a week, give an hour to serving someone outside your household: a neighbour, your church, a person in need.",
                        "Una vez por semana dedica una hora a servir a alguien fuera de tu casa: un vecino, tu "
                        "iglesia, una persona necesitada."),
             "kind": "practice", "target_count": 8, "days": 60},
            {"title": L("Complete eight lessons across the Service and Humility studies.",
                        "Completa ocho lecciones entre los estudios sobre el servicio y la humildad."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Each morning, ask God who you can serve today, and then watch for the answer.",
                        "Cada mañana pregúntale a Dios a quién puedes servir hoy, y luego mantente atento a la respuesta."),
             "kind": "prayer", "target_count": 20, "days": 30},
        ],
        "check_in_question": L(
            "Who did you serve this week without being asked, and how did you feel when no one noticed?",
            "¿A quién serviste esta semana sin que te lo pidieran, y cómo te sentiste cuando nadie lo notó?",
        ),
    },
    {
        "key": "prayerfulness",
        "title": L("Prayerfulness", "Vida de oración"),
        "definition": L(
            "Prayerfulness is living in honest conversation with God: turning to him through the day "
            "with thanks, needs, questions and silence. It is not long or polished words, and God does "
            "not love you more for the minutes you log; it is a relationship you keep returning to.",
            "Una vida de oración es vivir en conversación honesta con Dios: acudir a él a lo largo del día "
            "con gratitud, necesidades, preguntas y silencio. No se trata de palabras largas ni pulidas, "
            "y Dios no te ama más por los minutos que acumules; es una relación a la que vuelves una y "
            "otra vez.",
        ),
        "refs": ["Matthew 6:5-8", "Matthew 6:9-13", "Romans 8:26-27", "Psalm 145:18-19"],
        "jesus": {
            "ref": "Mark 1:35-38",
            "note": L(
                "After an exhausting day, with everyone looking for him, Jesus gets up while it is still "
                "dark and goes somewhere quiet to pray.",
                "Después de un día agotador, y con todos buscándolo, Jesús se levanta cuando todavía está "
                "oscuro y se va a un lugar tranquilo a orar.",
            ),
        },
        "topics": ["prayer", "loving_god"],
        "short_goals": [
            {"title": L("Set aside five minutes at a fixed time to talk with God: one thank you, one need, one person.",
                        "Aparta cinco minutos a una hora fija para hablar con Dios: un agradecimiento, una "
                        "necesidad, una persona."),
             "kind": "prayer", "target_count": 5, "days": 7},
            {"title": L("Complete the first two lessons of the Prayer study.",
                        "Completa las dos primeras lecciones del estudio sobre la oración."),
             "kind": "study", "target_count": 2, "days": 7},
            {"title": L("Write a few honest lines to God as a letter: what is on your mind, and what you want to ask.",
                        "Escríbele a Dios unas líneas honestas, como una carta: qué tienes en la mente y qué "
                        "quieres pedirle."),
             "kind": "reflection", "target_count": 3, "days": 7},
        ],
        "long_goals": [
            {"title": L("Pray the Lord's Prayer slowly once a day, stopping at one line to make it your own.",
                        "Ora el Padrenuestro despacio una vez al día, deteniéndote en una línea para hacerla tuya."),
             "kind": "prayer", "target_count": 20, "days": 30},
            {"title": L("Complete eight lessons across the Prayer and Loving God studies.",
                        "Completa ocho lecciones entre los estudios sobre la oración y amar a Dios."),
             "kind": "study", "target_count": 8, "days": 60},
            {"title": L("Once a week, pray with another person, aloud and briefly: at a meal, on a call, or at bedtime with a child.",
                        "Una vez por semana ora con otra persona, en voz alta y brevemente: en una comida, por "
                        "teléfono o al acostar a un niño."),
             "kind": "practice", "target_count": 12, "days": 90},
        ],
        "check_in_question": L(
            "When did you turn to God this week, and what made it easy or hard to do?",
            "¿Cuándo acudiste a Dios esta semana, y qué te lo hizo fácil o difícil?",
        ),
    },
]
