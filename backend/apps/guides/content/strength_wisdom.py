"""Study library: Strength (when you need to stand, resist or keep going) and Wisdom (when you need to choose well)."""

from apps.guides.catalog import L

TOPICS = [
    # ======================================================================
    # STRENGTH
    # ======================================================================
    {
        "key": "perseverance",
        "category": "strength",
        "title": L("Perseverance: keeping going", "Perseverancia: seguir adelante"),
        "summary": L(
            "For when you are tired of trying and quitting looks sensible. Four readings on where "
            "strength comes from, what endurance builds in you, and the One who finished his own race.",
            "Para cuando te cansaste de intentarlo y rendirte parece lo más sensato. Cuatro lecturas "
            "sobre de dónde viene la fuerza, qué forma en ti la constancia y Aquel que terminó su "
            "propia carrera.",
        ),
        "keywords": [
            "persever", "endur", "quit", "weary", "exhaust", "discourag", "give up", "keep going",
            "burnout", "perseverancia", "rendir", "agota", "desanim", "aguant", "constancia",
            "seguir adelante", "ya no puedo",
        ],
        "situations": ["caregiver", "student", "job_seeking", "parent", "recovery", "ill", "leader"],
        "traits": ["perseverance", "hope", "faithfulness"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Some things are hard and take a long time. God helps you try again.",
                "Algunas cosas son difíciles y toman mucho tiempo. Dios te ayuda a intentarlo otra vez.",
            ),
            "teen": L(
                "For the class, the team, the habit or the faith you are tempted to drop because "
                "progress is slow.",
                "Para la materia, el equipo, el hábito o la fe que quieres dejar porque el avance es lento.",
            ),
            "young_adult": L(
                "When the degree, the job search or the life you hoped for is taking far longer than "
                "you planned.",
                "Cuando la carrera, la búsqueda de empleo o la vida que esperabas está tardando mucho "
                "más de lo planeado.",
            ),
            "adult": L(
                "For the long middle: the same duties every day, little thanks, and no finish line in sight.",
                "Para el largo trecho de en medio: los mismos deberes cada día, pocas gracias y "
                "ninguna meta a la vista.",
            ),
            "senior": L(
                "When the body slows and the road has been long, here is strength for finishing well.",
                "Cuando el cuerpo va más lento y el camino ha sido largo, aquí hay fuerza para terminar bien.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "perseverance-1",
                "ref": "Galatians 6:9-10",
                "title": L("When doing good wears you out", "Cuando hacer el bien cansa"),
                "truth": L(
                    "Paul assumes something we rarely admit: doing good wears people out. He does not "
                    "scold the tiredness. He gives a reason to continue: good done now is like seed in "
                    "the ground, and a harvest comes in its own time for those who do not give up. You "
                    "may not see it yet. Meanwhile he keeps the task small: do good to the people "
                    "within reach, as the chance comes.",
                    "Pablo da por hecho algo que casi nunca admitimos: hacer el bien cansa. No regaña "
                    "el cansancio. Da una razón para continuar: el bien que haces hoy es como semilla "
                    "en la tierra, y la cosecha llega a su tiempo para quien no se rinde. Quizá todavía "
                    "no la veas. Mientras tanto mantiene la tarea pequeña: hacer el bien a quienes "
                    "tienes cerca, cuando se presente la ocasión.",
                ),
                "simple": L(
                    "Doing good things can make you tired, like planting seeds and waiting. God says: "
                    "keep going. Something good is growing even when you cannot see it.",
                    "Hacer cosas buenas puede cansarte, como sembrar semillas y esperar. Dios dice: "
                    "sigue. Algo bueno está creciendo aunque no lo veas.",
                ),
                "ask": L(
                    "Where are you doing good with no visible result, and what would it look like to "
                    "keep sowing there for one more week?",
                    "¿Dónde estás haciendo el bien sin ver resultados, y cómo sería seguir sembrando "
                    "allí una semana más?",
                ),
                "kid_ask": L(
                    "What is something good that is hard for you to keep doing?",
                    "¿Qué cosa buena te cuesta seguir haciendo?",
                ),
                "do": L(
                    "Choose one good thing you have been close to dropping. Do it once more today, and "
                    "write down the date so you can look back later.",
                    "Elige una cosa buena que has estado a punto de dejar. Hazla una vez más hoy y "
                    "anota la fecha para poder mirar atrás después.",
                ),
                "kid_do": L(
                    "Do one helpful thing today without being asked, even if nobody notices.",
                    "Haz hoy algo para ayudar sin que te lo pidan, aunque nadie lo note.",
                ),
                "pray": L(
                    "God, I am worn out from doing this and seeing so little. Help me not to give up "
                    "today. I leave the harvest and its timing with you.",
                    "Dios, me cansa hacer esto y ver tan poco. Ayúdame a no rendirme hoy. Dejo la "
                    "cosecha y su tiempo en tus manos.",
                ),
            },
            {
                "key": "perseverance-2",
                "ref": "Isaiah 40:28-31",
                "title": L("Strength that is not your own", "Una fuerza que no es tuya"),
                "truth": L(
                    "Isaiah speaks to people worn down by years of hardship, who had begun to think "
                    "God had lost track of them. His answer starts with who God is: the Creator who "
                    "never tires and whose understanding has no bottom. Then the surprise: this God "
                    "gives strength to the worn out. Even the young and fit run out. Those who wait on "
                    "the Lord find their strength renewed: sometimes to soar, sometimes to run, and "
                    "often simply to keep walking without collapsing.",
                    "Isaías habla a un pueblo desgastado por años de dificultad, que empezaba a pensar "
                    "que Dios le había perdido la pista. Su respuesta empieza por quién es Dios: el "
                    "Creador que nunca se cansa y cuyo entendimiento no tiene fondo. Luego la sorpresa: "
                    "este Dios da fuerza a quien ya no puede más. Hasta los jóvenes y fuertes se agotan. "
                    "Quienes esperan en el Señor reciben fuerzas nuevas: a veces para volar, a veces "
                    "para correr, y muchas veces simplemente para seguir caminando sin desplomarse.",
                ),
                "simple": L(
                    "Everybody gets tired, even big strong people. God never gets tired, and he shares "
                    "his strength with us when we ask.",
                    "Todos nos cansamos, hasta la gente grande y fuerte. Dios nunca se cansa, y "
                    "comparte su fuerza con nosotros cuando se la pedimos.",
                ),
                "ask": L(
                    "Right now, do you need strength to soar, to run, or just to keep walking? What "
                    "would asking God for exactly that sound like?",
                    "Ahora mismo, ¿necesitas fuerza para volar, para correr o solo para seguir "
                    "caminando? ¿Cómo sonaría pedirle a Dios justo eso?",
                ),
                "kid_ask": L(
                    "When do you feel most tired or want to stop?",
                    "¿Cuándo sientes más cansancio o más ganas de parar?",
                ),
                "do": L(
                    "Before the hardest part of your day, stop for one minute. Tell God plainly that "
                    "you do not have the strength for it, and ask for his.",
                    "Antes de la parte más difícil de tu día, detente un minuto. Dile a Dios con "
                    "sencillez que no tienes fuerza para eso y pídele la suya.",
                ),
                "kid_do": L(
                    "Next time something feels too hard, stop and say: God, please give me strength. "
                    "Then try once more.",
                    "La próxima vez que algo te parezca muy difícil, detente y di: Dios, dame fuerza, "
                    "por favor. Luego inténtalo una vez más.",
                ),
                "pray": L(
                    "Lord, you do not grow tired, and I do. I have run out. Give me enough strength "
                    "for today's walk.",
                    "Señor, tú no te cansas, y yo sí. Se me acabaron las fuerzas. Dame la fuerza "
                    "suficiente para el camino de hoy.",
                ),
            },
            {
                "key": "perseverance-3",
                "ref": "James 1:2-4",
                "title": L("What the hard road is building", "Lo que el camino difícil va formando"),
                "truth": L(
                    "James is not telling you to feel happy about pain or to call a bad thing good. He "
                    "is saying that trials are not wasted. When faith is tested and holds, it produces "
                    "staying power: the ability to remain under a weight without running. And staying "
                    "power, given time, makes a person whole and grown up inside. You can count that "
                    "as a real gain and still wish the trial were over.",
                    "Santiago no te pide que te alegres del dolor ni que llames bueno a lo malo. Dice "
                    "que las pruebas no se desperdician. Cuando la fe es probada y resiste, produce "
                    "constancia: la capacidad de permanecer bajo un peso sin salir huyendo. Y la "
                    "constancia, con tiempo, va haciendo a la persona entera y madura por dentro. "
                    "Puedes contar eso como una ganancia real y aun así desear que la prueba termine.",
                ),
                "simple": L(
                    "Hard things can help us grow, like muscles get stronger when we use them. God "
                    "uses hard days to make us strong inside.",
                    "Las cosas difíciles nos pueden ayudar a crecer, como los músculos se fortalecen "
                    "cuando los usamos. Dios usa los días difíciles para hacernos fuertes por dentro.",
                ),
                "ask": L(
                    "Looking back at an earlier hard season, what did it build in you that you would "
                    "not have otherwise?",
                    "Al mirar una época difícil del pasado, ¿qué formó en ti que de otro modo no tendrías?",
                ),
                "kid_ask": L(
                    "What is something hard you can do now that you could not do before?",
                    "¿Qué cosa difícil puedes hacer ahora que antes no podías?",
                ),
                "do": L(
                    "Write two sentences: one naming what is hard right now, and one naming a quality "
                    "you would like this season to leave in you.",
                    "Escribe dos frases: una que nombre lo difícil de ahora y otra con una cualidad "
                    "que te gustaría que esta etapa dejara en ti.",
                ),
                "kid_do": L(
                    "Practice one hard thing for five minutes today, like reading, a sport or tying "
                    "your shoes.",
                    "Practica hoy cinco minutos algo que te cueste, como leer, un deporte o amarrarte "
                    "los zapatos.",
                ),
                "pray": L(
                    "God, I would not have chosen this. Since I am in it, do not let it be wasted. "
                    "Make me steady, and grow me up inside.",
                    "Dios, yo no habría elegido esto. Ya que estoy aquí, que no se desperdicie. Dame "
                    "firmeza y hazme crecer por dentro.",
                ),
            },
            {
                "key": "perseverance-4",
                "ref": "Hebrews 12:1-3",
                "title": L("Eyes on the one who finished", "La mirada en quien llegó a la meta"),
                "truth": L(
                    "The writer pictures faith as a long-distance race, not a sprint. Two instructions "
                    "come with it. Drop what slows you down, both the plain wrongs and the extra "
                    "weights. And fix your eyes on Jesus, who went ahead of you, endured the cross and "
                    "its shame for the joy on the other side, and finished. Thinking about what he "
                    "went through is offered as the remedy for a heart that is worn out and ready to quit.",
                    "El autor describe la fe como una carrera de fondo, no de velocidad. Da dos "
                    "indicaciones. Suelta lo que te frena: tanto lo que está claramente mal como el "
                    "peso que sobra. Y fija la mirada en Jesús, que fue delante de ti, soportó la cruz "
                    "y su vergüenza por el gozo que había al otro lado, y llegó a la meta. Pensar en lo "
                    "que él pasó se ofrece como remedio para el corazón agotado y a punto de abandonar.",
                ),
                "simple": L(
                    "Following God is like a long race. Jesus already ran it and finished. When you "
                    "want to stop, think about Jesus, who kept going and did not give up.",
                    "Seguir a Dios es como una carrera larga. Jesús ya la corrió y llegó al final. "
                    "Cuando quieras parar, piensa en Jesús, que siguió adelante y no se rindió.",
                ),
                "ask": L(
                    "What is one weight, not necessarily a sin, that is slowing you down and that you "
                    "could set aside this month?",
                    "¿Qué peso, no necesariamente un pecado, te está frenando y podrías dejar a un "
                    "lado este mes?",
                ),
                "kid_ask": L(
                    "Who cheers for you when something is hard?",
                    "¿Quién te anima cuando algo es difícil?",
                ),
                "do": L(
                    "This week, read one account of the crucifixion slowly (Mark 15 is short) and "
                    "notice each point where Jesus could have stopped and did not.",
                    "Esta semana lee despacio un relato de la crucifixión (Marcos 15 es breve) y "
                    "fíjate en cada momento en que Jesús pudo detenerse y no lo hizo.",
                ),
                "kid_do": L(
                    "Cheer for someone today who is doing something hard.",
                    "Anima hoy a alguien que esté haciendo algo difícil.",
                ),
                "pray": L(
                    "Jesus, you did not quit. Take my eyes off how far there is to go and put them on "
                    "you. Help me drop what I do not need to carry.",
                    "Jesús, tú no abandonaste. Quita mi mirada de lo mucho que falta y ponla en ti. "
                    "Ayúdame a soltar lo que no necesito cargar.",
                ),
            },
        ],
    },
    {
        "key": "courage",
        "category": "strength",
        "title": L("Courage when you are afraid", "Valor cuando tienes miedo"),
        "summary": L(
            "For when the right thing is also the frightening thing. Five stories of people who were "
            "in real danger or real doubt and acted anyway, and of the God who was with them.",
            "Para cuando lo correcto es también lo que da miedo. Cinco historias de personas que "
            "estuvieron en verdadero peligro o verdadera duda y actuaron de todos modos, y del Dios "
            "que estuvo con ellas.",
        ),
        "keywords": [
            "courag", "brave", "afraid", "scared", "coward", "bold", "intimidat", "stand up",
            "speak up", "valor", "valiente", "valentía", "cobard", "atrev", "enfrentar", "me da miedo",
        ],
        "situations": ["student", "leader", "military", "moving", "new_believer", "working"],
        "traits": ["courage", "trust", "faithfulness"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Being brave does not mean you are not scared. It means doing the right thing with "
                "God beside you.",
                "Ser valiente no es no tener miedo. Es hacer lo correcto con Dios a tu lado.",
            ),
            "teen": L(
                "For speaking up, standing apart from the crowd, or owning the truth when it would be "
                "easier to hide.",
                "Para alzar la voz, apartarte del grupo o decir la verdad cuando sería más fácil esconderte.",
            ),
            "young_adult": L(
                "For the first big steps: the move, the honest conversation, the path no one around "
                "you is taking.",
                "Para los primeros grandes pasos: la mudanza, la conversación honesta, el camino que "
                "nadie a tu alrededor está tomando.",
            ),
            "adult": L(
                "For the hard call at work, the truth your family needs to hear, the stand that could "
                "cost you.",
                "Para la decisión difícil en el trabajo, la verdad que tu familia necesita oír, la "
                "postura que puede costarte.",
            ),
            "senior": L(
                "For facing loss, change and frailty without shrinking, and for still saying what "
                "needs to be said.",
                "Para enfrentar pérdidas, cambios y fragilidad sin encogerte, y para seguir diciendo "
                "lo que hace falta decir.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "courage-1",
                "ref": "Joshua 1:6-9",
                "title": L("A command with a promise", "Un mandato con promesa"),
                "truth": L(
                    "Joshua has just lost Moses and inherited a job far too big for him. God tells him "
                    "three times to be strong and brave, which suggests Joshua felt neither. The "
                    "reason God gives is not that Joshua is capable or that the task is safe. It is "
                    "that God will be with him wherever he goes. Courage in the Bible is not the "
                    "absence of fear. It is moving forward because of who goes with you.",
                    "Josué acaba de perder a Moisés y hereda una tarea que le queda enorme. Dios le "
                    "dice tres veces que sea fuerte y valiente, lo que sugiere que Josué no se sentía "
                    "ni lo uno ni lo otro. La razón que Dios da no es que Josué sea capaz ni que la "
                    "tarea sea segura. Es que Dios estará con él dondequiera que vaya. En la Biblia el "
                    "valor no es ausencia de miedo. Es avanzar por quién va contigo.",
                ),
                "simple": L(
                    "Joshua had a big, scary job. God told him: be brave, because I am with you "
                    "everywhere you go. God is with you too.",
                    "Josué tenía un trabajo grande que daba miedo. Dios le dijo: sé valiente, porque "
                    "yo estoy contigo dondequiera que vayas. Dios también está contigo.",
                ),
                "ask": L(
                    "What are you avoiding because you feel unequal to it, and how does it change "
                    "things if God goes there with you?",
                    "¿Qué estás evitando porque sientes que no das la talla, y qué cambia si Dios va "
                    "allí contigo?",
                ),
                "kid_ask": L(
                    "What is something that feels scary to you right now?",
                    "¿Qué cosa te da miedo en este momento?",
                ),
                "do": L(
                    "Name the one step you have been putting off out of fear. Before you take it, say "
                    "out loud: God is with me in this.",
                    "Nombra el paso que has pospuesto por miedo. Antes de darlo, di en voz alta: Dios "
                    "está conmigo en esto.",
                ),
                "kid_do": L(
                    "When you feel scared today, whisper: God is with me. Then tell a grown-up how it went.",
                    "Cuando hoy sientas miedo, susurra: Dios está conmigo. Luego cuéntale a un adulto "
                    "cómo te fue.",
                ),
                "pray": L(
                    "God, I do not feel strong or brave. You have not asked me to feel it, but to go "
                    "with you. Be with me in the step I am afraid of.",
                    "Dios, no siento fuerza ni valor. No me pides sentirlo, sino ir contigo. "
                    "Acompáñame en el paso que me da miedo.",
                ),
            },
            {
                "key": "courage-2",
                "ref": "1 Samuel 17:45-47",
                "title": L("Whose fight is it?", "¿De quién es la pelea?"),
                "truth": L(
                    "David is a young shepherd facing a trained fighter far bigger than he is, and "
                    "everyone older has stayed back. What he says shows where his courage comes from. "
                    "He does not claim to be stronger. He says he comes in the name of the Lord, and "
                    "that the battle belongs to God. David still has to walk out there and use what is "
                    "in his hand. But he does not carry the weight of the outcome alone.",
                    "David es un joven pastor frente a un guerrero entrenado y mucho más grande que "
                    "él, y todos los mayores se han quedado atrás. Lo que dice muestra de dónde viene "
                    "su valor. No presume de ser más fuerte. Dice que viene en el nombre del Señor y "
                    "que la batalla le pertenece a Dios. David igual tiene que salir al frente y usar "
                    "lo que tiene en la mano. Pero no carga a solas el peso del resultado.",
                ),
                "simple": L(
                    "David was small and Goliath was huge. David was brave because he knew God is "
                    "bigger than any giant.",
                    "David era pequeño y Goliat era enorme. David fue valiente porque sabía que Dios "
                    "es más grande que cualquier gigante.",
                ),
                "ask": L(
                    "What giant are you facing as if the whole outcome depended on you? Which part is "
                    "yours to do, and which part is God's?",
                    "¿Qué gigante enfrentas como si todo el resultado dependiera de ti? ¿Qué parte te "
                    "toca a ti y cuál le toca a Dios?",
                ),
                "kid_ask": L(
                    "What feels like a giant to you?",
                    "¿Qué te parece un gigante a ti?",
                ),
                "do": L(
                    "Draw a line down a page. On the left, list what you can actually do about the "
                    "thing you fear. On the right, list what only God can do. Do one item on the left today.",
                    "Traza una línea en una hoja. A la izquierda anota lo que sí puedes hacer frente a "
                    "lo que temes. A la derecha, lo que solo Dios puede hacer. Haz hoy una cosa de la "
                    "izquierda.",
                ),
                "kid_do": L(
                    "Draw your giant very small and write GOD in big letters next to it.",
                    "Dibuja a tu gigante muy pequeño y escribe DIOS con letras grandes a su lado.",
                ),
                "pray": L(
                    "Lord, this looks much bigger than I am. It is not bigger than you. Show me my "
                    "part, and help me trust you with the rest.",
                    "Señor, esto se ve mucho más grande que yo. No es más grande que tú. Muéstrame mi "
                    "parte y ayúdame a confiarte lo demás.",
                ),
            },
            {
                "key": "courage-3",
                "ref": "Daniel 3:16-18",
                "title": L("Even if he does not", "Y aunque no lo haga"),
                "truth": L(
                    "Three young men are ordered to bow to a king's statue or die. Their answer has "
                    "two parts, and both matter. First: our God is able to rescue us. Second: even if "
                    "he does not, we still will not bow. Their courage does not rest on knowing how "
                    "the story ends. It rests on knowing who God is. This is the deepest kind of "
                    "courage: faithfulness that is not a bargain for a good outcome.",
                    "A tres jóvenes se les ordena inclinarse ante la estatua de un rey o morir. Su "
                    "respuesta tiene dos partes, y las dos importan. Primera: nuestro Dios puede "
                    "rescatarnos. Segunda: y aunque no lo haga, tampoco nos inclinaremos. Su valor no "
                    "depende de saber cómo termina la historia. Depende de saber quién es Dios. Este "
                    "es el valor más hondo: una fidelidad que no es un trato a cambio de un buen final.",
                ),
                "simple": L(
                    "A king told three friends to do something wrong. They said no, even though it was "
                    "very hard, because they wanted to obey God most of all.",
                    "Un rey les ordenó a tres amigos hacer algo malo. Dijeron que no, aunque era muy "
                    "difícil, porque lo que más querían era obedecer a Dios.",
                ),
                "ask": L(
                    "How would you finish this sentence about what you fear: God is able to…, and even "
                    "if he does not, I will…?",
                    "¿Cómo terminarías esta frase sobre lo que temes: Dios puede…, y aunque no lo "
                    "haga, yo…?",
                ),
                "kid_ask": L(
                    "When is it hard to say no to something wrong?",
                    "¿Cuándo te cuesta decir que no a algo que está mal?",
                ),
                "do": L(
                    "Notice one place where your obedience quietly depends on things turning out well. "
                    "Write your own two-part sentence about it and keep it where you will see it.",
                    "Fíjate en un lugar donde tu obediencia depende, en el fondo, de que todo salga "
                    "bien. Escribe tu propia frase de dos partes sobre eso y guárdala donde la veas.",
                ),
                "kid_do": L(
                    "Practice a kind, strong no with a grown-up: No, thank you, I will not do that.",
                    "Practica con un adulto un no amable y firme: No, gracias, eso no lo voy a hacer.",
                ),
                "pray": L(
                    "God, you are able. I ask you to rescue. And if your answer is different from what "
                    "I hope, keep me faithful anyway.",
                    "Dios, tú puedes. Te pido que rescates. Y si tu respuesta es distinta de la que "
                    "espero, mantenme fiel de todos modos.",
                ),
            },
            {
                "key": "courage-4",
                "ref": "Esther 4:13-16",
                "title": L("Brave, and not alone", "Valiente, y no a solas"),
                "truth": L(
                    "Esther is asked to risk her life by going to the king uninvited to plead for her "
                    "people. She knows the danger and says plainly that it may cost her life. Mordecai "
                    "does not promise she will be safe. He asks whether she might be in her position "
                    "for exactly this moment. Notice what Esther does before she acts: she asks her "
                    "whole community to fast with her for three days. She does not act alone, and she "
                    "does not rush. Then she goes.",
                    "A Ester le piden arriesgar la vida presentándose ante el rey sin ser llamada, "
                    "para interceder por su pueblo. Ella conoce el peligro y dice sin rodeos que puede "
                    "costarle la vida. Mardoqueo no le promete que estará a salvo. Le pregunta si "
                    "acaso no estará en ese lugar justo para este momento. Fíjate en lo que hace Ester "
                    "antes de actuar: pide a toda su comunidad que ayune con ella tres días. No actúa "
                    "sola ni con prisa. Y entonces va.",
                ),
                "simple": L(
                    "Esther had to do something very brave to help her people. First she asked her "
                    "people to stand with her. Brave people ask for help.",
                    "Ester tuvo que hacer algo muy valiente para ayudar a su pueblo. Primero pidió a "
                    "su gente que la acompañara. Los valientes piden ayuda.",
                ),
                "ask": L(
                    "What position, relationship or skill has been given to you that someone else "
                    "needs you to use bravely right now?",
                    "¿Qué lugar, relación o habilidad se te ha dado que alguien necesita que uses con "
                    "valentía ahora mismo?",
                ),
                "kid_ask": L(
                    "Who could you ask to help you be brave?",
                    "¿A quién podrías pedirle que te ayude a ser valiente?",
                ),
                "do": L(
                    "Before the hard conversation or decision, ask two people to pray for you, and "
                    "tell them the day and the hour.",
                    "Antes de la conversación o decisión difícil, pide a dos personas que oren por ti "
                    "y diles el día y la hora.",
                ),
                "kid_do": L(
                    "Stand up for someone who is being left out today: sit with them or invite them to play.",
                    "Hoy defiende a alguien a quien estén dejando de lado: siéntate a su lado o "
                    "invítalo a jugar.",
                ),
                "pray": L(
                    "Lord, maybe I am here for this. Give me people to stand with me, and then the "
                    "courage to go in.",
                    "Señor, quizá estoy aquí para esto. Dame personas que me acompañen, y luego el "
                    "valor para entrar.",
                ),
            },
            {
                "key": "courage-5",
                "ref": "Matthew 14:25-31",
                "title": L("When courage runs out halfway", "Cuando el valor se acaba a medio camino"),
                "truth": L(
                    "Peter does a brave thing: he steps out of the boat toward Jesus. Then he notices "
                    "the wind, fear takes over, and he starts to sink. He has just enough left for a "
                    "very short cry for help, and Jesus reaches out his hand at once and takes hold of "
                    "him. Jesus does ask about his doubt, but only after he has hold of him. Failing "
                    "partway through a brave act does not disqualify you. The hand comes first.",
                    "Pedro hace algo valiente: sale de la barca y va hacia Jesús. Luego se fija en el "
                    "viento, el miedo lo domina y empieza a hundirse. Apenas le alcanza para un grito "
                    "muy corto pidiendo ayuda, y Jesús enseguida extiende la mano y lo sostiene. Jesús "
                    "sí le pregunta por su duda, pero solo después de tenerlo agarrado. Fallar a mitad "
                    "de un acto valiente no te descalifica. Primero llega la mano.",
                ),
                "simple": L(
                    "Peter was brave, then he got scared and started to sink. He called to Jesus, and "
                    "Jesus caught him right away. Jesus helps us when our brave runs out.",
                    "Pedro fue valiente, luego le dio miedo y empezó a hundirse. Llamó a Jesús, y "
                    "Jesús lo agarró enseguida. Jesús nos ayuda cuando se nos acaba la valentía.",
                ),
                "ask": L(
                    "Where did you start bravely and then lose your nerve? What would it mean to call "
                    "out for help instead of quietly giving up?",
                    "¿Dónde empezaste con valentía y luego te faltó el ánimo? ¿Qué significaría pedir "
                    "ayuda en vez de rendirte en silencio?",
                ),
                "kid_ask": L(
                    "What do you do when you get scared in the middle of something?",
                    "¿Qué haces cuando te da miedo a la mitad de algo?",
                ),
                "do": L(
                    "Pick one thing you gave up on out of fear. Tell God about it honestly, then take "
                    "the next small step back toward it this week.",
                    "Elige algo que abandonaste por miedo. Cuéntaselo a Dios con honestidad y esta "
                    "semana da el siguiente paso pequeño para retomarlo.",
                ),
                "kid_do": L(
                    "Learn this short prayer for scary moments: Jesus, help me.",
                    "Aprende esta oración corta para los momentos de miedo: Jesús, ayúdame.",
                ),
                "pray": L(
                    "Jesus, I started well, and then I looked at the wind. I am sinking. Take hold of "
                    "me, and help me keep my eyes on you.",
                    "Jesús, empecé bien y luego miré el viento. Me estoy hundiendo. Sostenme y ayúdame "
                    "a no quitar los ojos de ti.",
                ),
            },
        ],
    },
    {
        "key": "temptation",
        "category": "strength",
        "title": L("Temptation: when you are pulled", "Tentación: cuando algo te arrastra"),
        "summary": L(
            "For when you want what you know will harm you or someone else. Four readings on how "
            "temptation works, the way out God provides, and the help Jesus gives to people who are "
            "struggling.",
            "Para cuando deseas lo que sabes que te hará daño a ti o a otra persona. Cuatro lecturas "
            "sobre cómo funciona la tentación, la salida que Dios provee y la ayuda que Jesús da a "
            "quien está luchando.",
        ),
        "keywords": [
            "tempt", "resist", "urge", "crav", "lust", "gave in", "giving in", "slipped", "weakness",
            "tenta", "impuls", "deseo", "caí", "recaer", "debilidad", "ceder", "cedí",
        ],
        "situations": ["student", "single", "dating", "married", "working", "new_believer", "recovery"],
        "traits": ["self_control", "purity", "faithfulness"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Sometimes you really want to do something you know is wrong. God understands and "
                "helps you choose well.",
                "A veces tienes muchas ganas de hacer algo que sabes que está mal. Dios te entiende y "
                "te ayuda a elegir bien.",
            ),
            "teen": L(
                "For what pulls at you on your phone, with your friends and in your own head when no "
                "one is watching.",
                "Para lo que te atrae en el teléfono, con tus amigos y en tu propia cabeza cuando "
                "nadie te ve.",
            ),
            "young_adult": L(
                "New freedom brings new pulls. Here is how to see them coming and where to turn "
                "before and after.",
                "La libertad nueva trae atracciones nuevas. Aquí verás cómo reconocerlas a tiempo y a "
                "dónde acudir antes y después.",
            ),
            "adult": L(
                "For the quiet compromises at work, at home and online that no one else would ever "
                "find out about.",
                "Para las pequeñas concesiones en el trabajo, en casa y en línea de las que nadie más "
                "se enteraría.",
            ),
            "senior": L(
                "Temptation changes shape with age: bitterness, complaint, giving up. The way out is "
                "the same.",
                "La tentación cambia de forma con los años: amargura, queja, rendirse. La salida es "
                "la misma.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "temptation-1",
                "ref": "1 Corinthians 10:12-13",
                "title": L("You are not the only one, and there is a way out",
                           "No eres la única persona, y hay una salida"),
                "truth": L(
                    "Two lies make temptation stronger: no one else struggles with this, and I have no "
                    "choice. Paul answers both. What pulls at you is common to people everywhere. And "
                    "God is faithful: he does not let the pull go beyond what you can bear, and with "
                    "it he provides a way out. The way out is usually ordinary: a door to walk "
                    "through, a phone to put down, a person to call. Paul begins with a warning: the "
                    "one who feels safest should watch their step.",
                    "Dos mentiras fortalecen la tentación: nadie más lucha con esto, y no tengo "
                    "opción. Pablo responde a las dos. Lo que te atrae es común a la gente de todas "
                    "partes. Y Dios es fiel: no deja que la presión pase de lo que puedes soportar, y "
                    "junto con ella da una salida. La salida suele ser muy común: una puerta por la "
                    "que salir, un teléfono que soltar, una persona a quien llamar. Pablo empieza con "
                    "una advertencia: quien se siente más seguro debe mirar bien dónde pisa.",
                ),
                "simple": L(
                    "Everyone sometimes wants to do wrong things. You are not the only one. God always "
                    "gives you a way to choose what is right.",
                    "Todos a veces queremos hacer cosas malas. No te pasa solo a ti. Dios siempre te "
                    "da una manera de elegir lo correcto.",
                ),
                "ask": L(
                    "Think of your most frequent temptation. What does the way out usually look like, "
                    "and at what point do you tend to walk past it?",
                    "Piensa en tu tentación más frecuente. ¿Cómo suele ser la salida, y en qué punto "
                    "sueles pasarla de largo?",
                ),
                "kid_ask": L(
                    "What is something wrong that you sometimes really want to do?",
                    "¿Qué cosa mala a veces tienes muchas ganas de hacer?",
                ),
                "do": L(
                    "Decide in advance on one exit for your most common temptation (leave the room, "
                    "text a friend, close the app) and use it the next time, early.",
                    "Decide de antemano una salida para tu tentación más común (salir del cuarto, "
                    "escribirle a un amigo, cerrar la aplicación) y úsala la próxima vez, pronto.",
                ),
                "kid_do": L(
                    "Make a plan with a grown-up: when I want to do something wrong, I will walk away "
                    "and come tell you.",
                    "Haz un plan con un adulto: cuando quiera hacer algo malo, me voy de ahí y vengo a "
                    "contártelo.",
                ),
                "pray": L(
                    "Faithful God, you say there is a way out. Show it to me today, and give me the "
                    "will to take it while it is still easy.",
                    "Dios fiel, tú dices que hay una salida. Muéstramela hoy y dame la voluntad de "
                    "tomarla mientras todavía es fácil.",
                ),
            },
            {
                "key": "temptation-2",
                "ref": "James 1:13-15",
                "title": L("How a pull becomes a fall", "Cómo un deseo se vuelve caída"),
                "truth": L(
                    "James clears up two things. God is never the one tempting you; he does not set "
                    "traps. And being tempted is not yet sin. The trouble begins inside, when a desire "
                    "of your own lures you and you start to feed it. James pictures it as something "
                    "that is conceived, grows and is born, and when fully grown brings death. That is "
                    "useful to know, because it means there are stages. The earlier you interrupt it, "
                    "the easier it is.",
                    "Santiago aclara dos cosas. Dios nunca es quien te tienta; él no pone trampas. Y "
                    "ser tentado todavía no es pecado. El problema empieza por dentro, cuando un deseo "
                    "propio te seduce y empiezas a alimentarlo. Santiago lo describe como algo que se "
                    "concibe, crece y nace, y que cuando madura trae muerte. Saberlo ayuda, porque "
                    "significa que hay etapas. Cuanto antes lo interrumpas, más fácil será.",
                ),
                "simple": L(
                    "Wanting something wrong is like a tiny seed. If you keep thinking about it, it "
                    "grows. It is easiest to stop when it is small.",
                    "Querer algo malo es como una semillita. Si sigues pensando en eso, crece. Es más "
                    "fácil detenerlo cuando es pequeño.",
                ),
                "ask": L(
                    "In your own pattern, what is the earliest stage, the first thought or the first "
                    "small permission, where you could stop it?",
                    "En tu propio patrón, ¿cuál es la etapa más temprana, el primer pensamiento o el "
                    "primer pequeño permiso, donde podrías detenerlo?",
                ),
                "kid_ask": L(
                    "What helps you stop thinking about something you should not do?",
                    "¿Qué te ayuda a dejar de pensar en algo que no debes hacer?",
                ),
                "do": L(
                    "Trace your last fall backward and write down the steps that led there. Circle the "
                    "first one. That is where to act next time.",
                    "Repasa hacia atrás tu última caída y anota los pasos que te llevaron ahí. "
                    "Encierra en un círculo el primero. Ahí es donde hay que actuar la próxima vez.",
                ),
                "kid_do": L(
                    "When a wrong idea pops up today, do something else right away: go outside, help "
                    "someone, or tell a grown-up.",
                    "Cuando hoy se te ocurra una mala idea, haz otra cosa enseguida: sal a jugar, "
                    "ayuda a alguien o cuéntale a un adulto.",
                ),
                "pray": L(
                    "God, you are not the one pulling me toward this. Help me see the desire early, "
                    "name it honestly, and stop feeding it.",
                    "Dios, no eres tú quien me empuja hacia esto. Ayúdame a ver el deseo a tiempo, a "
                    "nombrarlo con honestidad y a dejar de alimentarlo.",
                ),
            },
            {
                "key": "temptation-3",
                "ref": "Matthew 4:1-11",
                "title": L("Jesus was tempted too", "Jesús también fue tentado"),
                "truth": L(
                    "Jesus is hungry and alone after forty days in the wilderness when the temptations "
                    "come. They often arrive when we are depleted. Each one offers something good by a "
                    "wrong road: bread, safety, power, all without trusting the Father. Each time "
                    "Jesus answers with a truth from Scripture he already knew by heart. He does not "
                    "argue at length or lean on willpower. He stands on what God has said. And the "
                    "tempter, in the end, leaves.",
                    "Jesús tiene hambre y está solo tras cuarenta días en el desierto cuando llegan "
                    "las tentaciones. Suelen llegar cuando estamos sin fuerzas. Cada una ofrece algo "
                    "bueno por un camino equivocado: pan, seguridad, poder, todo sin confiar en el "
                    "Padre. Cada vez Jesús responde con una verdad de la Escritura que ya sabía de "
                    "memoria. No discute largamente ni se apoya en su fuerza de voluntad. Se afirma en "
                    "lo que Dios ha dicho. Y el tentador, al final, se va.",
                ),
                "simple": L(
                    "Jesus was hungry and tired, and he was tempted to do wrong. He remembered what "
                    "God says and said no. Jesus knows how it feels.",
                    "Jesús tenía hambre y cansancio, y fue tentado a hacer lo malo. Recordó lo que "
                    "Dios dice y dijo que no. Jesús sabe cómo se siente.",
                ),
                "ask": L(
                    "When are you most open to temptation: hungry, angry, lonely, tired? What truth "
                    "could you have ready for that moment?",
                    "¿Cuándo eres más vulnerable a la tentación: con hambre, con enojo, en soledad, "
                    "con cansancio? ¿Qué verdad podrías tener lista para ese momento?",
                ),
                "kid_ask": L(
                    "When is it hardest for you to choose well: when you are tired, hungry or upset?",
                    "¿Cuándo te cuesta más elegir bien: con cansancio, con hambre o con enojo?",
                ),
                "do": L(
                    "Choose one short Bible sentence that answers your usual temptation. Write it "
                    "where you will see it, and learn it by heart this week.",
                    "Elige una frase corta de la Biblia que responda a tu tentación habitual. "
                    "Escríbela donde la veas y apréndela de memoria esta semana.",
                ),
                "kid_do": L(
                    "Learn one short Bible sentence with a grown-up and say it together at bedtime.",
                    "Aprende con un adulto una frase corta de la Biblia y díganla juntos antes de dormir.",
                ),
                "pray": L(
                    "Jesus, you know what it is to be tempted while empty. Put your words in my mind "
                    "before I need them, and stand with me when I do.",
                    "Jesús, tú sabes lo que es ser tentado estando sin fuerzas. Pon tus palabras en mi "
                    "mente antes de que las necesite, y quédate conmigo cuando llegue el momento.",
                ),
            },
            {
                "key": "temptation-4",
                "ref": "Hebrews 4:14-16",
                "title": L("Where to go, before and after", "A dónde ir, antes y después"),
                "truth": L(
                    "After a failure, the instinct is to hide from God until you feel cleaner. This "
                    "passage says the opposite. Jesus is able to sympathize with our weaknesses, "
                    "because he was tempted in every way we are, yet did not sin. So we are told to "
                    "come near with confidence, to a throne of grace, to receive mercy for what has "
                    "gone wrong and help for the moment of need. Come when you are tempted. Come when "
                    "you have fallen. The welcome is the same.",
                    "Después de fallar, el instinto es esconderse de Dios hasta sentirse más limpio. "
                    "Este pasaje dice lo contrario. Jesús puede compadecerse de nuestras debilidades, "
                    "porque fue tentado en todo igual que nosotros, pero sin pecar. Por eso nos invita "
                    "a acercarnos con confianza a un trono de gracia, para recibir misericordia por lo "
                    "que salió mal y ayuda en el momento de necesidad. Ven cuando sientas la "
                    "tentación. Ven cuando hayas caído. La bienvenida es la misma.",
                ),
                "simple": L(
                    "Jesus understands when doing right is hard. You can always ask him for help, and "
                    "you can always tell him sorry. He will not send you away.",
                    "Jesús entiende cuando hacer lo correcto es difícil. Siempre puedes pedirle ayuda, "
                    "y siempre puedes pedirle perdón. Él no te va a rechazar.",
                ),
                "ask": L(
                    "After you give in, how long do you usually stay away from God, and what do you "
                    "imagine his face looks like when you come back?",
                    "Después de ceder, ¿cuánto tiempo sueles mantenerte lejos de Dios, y cómo imaginas "
                    "su rostro cuando regresas?",
                ),
                "kid_ask": L(
                    "How do you feel after you do something wrong? Who can you tell?",
                    "¿Cómo te sientes después de hacer algo malo? ¿A quién se lo puedes contar?",
                ),
                "do": L(
                    "The next time you fall, pray within the hour instead of waiting until you feel "
                    "worthy. If the same struggle keeps returning, tell one trusted person about it "
                    "this week.",
                    "La próxima vez que caigas, ora dentro de esa misma hora en vez de esperar a "
                    "sentir que lo mereces. Si la misma lucha vuelve una y otra vez, cuéntasela esta "
                    "semana a una persona de confianza.",
                ),
                "kid_do": L(
                    "If you do something wrong today, tell God sorry in one sentence and tell a "
                    "grown-up too.",
                    "Si hoy haces algo malo, pídele perdón a Dios en una frase y cuéntaselo también a "
                    "un adulto.",
                ),
                "pray": L(
                    "Jesus, you know this pull from the inside. I come as I am. I need mercy for what "
                    "I did and help for what is ahead.",
                    "Jesús, tú conoces esta lucha desde adentro. Vengo tal como estoy. Necesito "
                    "misericordia por lo que hice y ayuda para lo que viene.",
                ),
            },
        ],
    },
    {
        "key": "addiction",
        "category": "strength",
        "title": L("Addiction: finding freedom", "Adicción: hallar libertad"),
        "summary": L(
            "For anyone caught in something they cannot stop: alcohol, drugs, pornography, gambling, "
            "a screen. No shame here. Five readings on honesty, coming home, getting help, and "
            "starting again after a fall.",
            "Para quien está atrapado en algo que no logra dejar: alcohol, drogas, pornografía, "
            "apuestas, una pantalla. Aquí no hay vergüenza. Cinco lecturas sobre la honestidad, "
            "volver a casa, pedir ayuda y empezar de nuevo tras una caída.",
        ),
        "keywords": [
            "addict", "relaps", "sober", "sobriety", "alcohol", "drinking", "drunk", "drug", "porn",
            "gambl", "rehab", "can't stop", "adic", "recaí", "recaída", "sobrio", "sobriedad",
            "borrach", "droga", "apuest", "vicio", "no puedo dejar",
        ],
        "situations": ["recovery"],
        "traits": ["self_control", "honesty", "hope"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "If a screen, a substance or a secret has more hold on you than you want to admit, "
                "you are not bad and you are not alone. Tell an adult you trust.",
                "Si una pantalla, una sustancia o un secreto te tiene más atrapado de lo que "
                "quisieras admitir, no eres mala persona ni estás a solas. Cuéntaselo a un adulto de "
                "confianza.",
            ),
            "young_adult": L(
                "What began as relief or fun may have started making your decisions for you. It is "
                "not too late or too early to ask for help.",
                "Lo que empezó como alivio o diversión quizá ya esté decidiendo por ti. No es "
                "demasiado tarde ni demasiado pronto para pedir ayuda.",
            ),
            "adult": L(
                "For the thing you have hidden for years while keeping everything else running. "
                "Freedom begins with one honest conversation.",
                "Para eso que has escondido durante años mientras mantienes todo lo demás "
                "funcionando. La libertad empieza con una conversación honesta.",
            ),
            "senior": L(
                "It is never too late. Whether the struggle is decades old or began with loss or "
                "loneliness, help and mercy are still for you.",
                "Nunca es demasiado tarde. Sea una lucha de décadas o una que empezó con una pérdida "
                "o con la soledad, la ayuda y la misericordia siguen siendo para ti.",
            ),
        },
        "sensitive": True,
        "lessons": [
            {
                "key": "addiction-1",
                "ref": "Romans 7:15-25",
                "title": L("Doing the thing you hate", "Hacer lo que aborreces"),
                "truth": L(
                    "Paul describes something anyone caught in an addiction will recognize. He does "
                    "not understand his own behavior. He keeps doing what he hates and failing to do "
                    "the good he truly wants. He does not pretend that willpower is enough. He ends by "
                    "crying out for someone to rescue him, and then gives thanks, because there is a "
                    "rescuer: Jesus Christ. Freedom starts here. Not with trying harder in secret, but "
                    "with admitting you need help from outside yourself.",
                    "Pablo describe algo que reconocerá cualquiera que esté atrapado en una adicción. "
                    "No entiende su propia conducta. Sigue haciendo lo que aborrece y no logra hacer "
                    "el bien que de verdad quiere. No finge que la fuerza de voluntad alcance. Termina "
                    "clamando por alguien que lo rescate, y enseguida da gracias, porque hay un "
                    "rescatador: Jesucristo. La libertad empieza aquí. No con esforzarte más en "
                    "secreto, sino con admitir que necesitas ayuda que venga de fuera de ti.",
                ),
                "simple": L(
                    "Sometimes people keep doing something even when they want to stop. They need "
                    "help, and God wants to help them.",
                    "A veces las personas siguen haciendo algo aunque quieren dejarlo. Necesitan "
                    "ayuda, y Dios quiere ayudarlas.",
                ),
                "ask": L(
                    "What is the thing you keep doing that you do not want to do? Who else knows?",
                    "¿Qué es eso que sigues haciendo y no quieres hacer? ¿Quién más lo sabe?",
                ),
                "kid_ask": L(
                    "Is there something you find hard to stop doing, even when you want to?",
                    "¿Hay algo que te cuesta dejar de hacer, aunque quieras?",
                ),
                "do": L(
                    "Write one honest sentence that names what has a hold on you and for how long. "
                    "Then choose one person, a trusted friend, a pastor, a doctor or a counselor, and "
                    "read it to them this week.",
                    "Escribe una frase honesta que nombre lo que te tiene atrapado y desde cuándo. "
                    "Luego elige a una persona, un amigo de confianza, un pastor, un médico o un "
                    "consejero, y léesela esta semana.",
                ),
                "kid_do": L(
                    "If something is hard for you to stop, tell a grown-up you trust today. They will "
                    "help you.",
                    "Si hay algo que te cuesta dejar, cuéntaselo hoy a un adulto de confianza. Te va a "
                    "ayudar.",
                ),
                "pray": L(
                    "God, I keep doing what I hate, and I cannot stop by myself. I am not hiding it "
                    "from you anymore. Rescue me, and show me who to tell.",
                    "Dios, sigo haciendo lo que aborrezco y no puedo dejarlo por mi cuenta. Ya no te "
                    "lo escondo. Rescátame y muéstrame a quién contárselo.",
                ),
            },
            {
                "key": "addiction-2",
                "ref": "Luke 15:17-24",
                "title": L("The father who runs", "El padre que corre"),
                "truth": L(
                    "The son in this story has wasted everything and ended up hungry among pigs. He "
                    "rehearses a speech about how he is no longer worthy and heads home expecting, at "
                    "best, a hired worker's place. But his father sees him while he is still far off, "
                    "is moved with compassion, runs to him and embraces him before he has said a word. "
                    "Then come the robe, the ring and the feast. Jesus tells this story to show what "
                    "God is like toward people who come back. Shame says: clean yourself up first. The "
                    "father runs before anything has been fixed.",
                    "El hijo de esta historia lo ha malgastado todo y ha terminado con hambre entre "
                    "cerdos. Ensaya un discurso sobre que ya no es digno y emprende el regreso "
                    "esperando, cuando mucho, un lugar de jornalero. Pero su padre lo ve cuando "
                    "todavía está lejos, se conmueve, corre hacia él y lo abraza antes de que diga una "
                    "palabra. Luego vienen la ropa, el anillo y la fiesta. Jesús cuenta esta historia "
                    "para mostrar cómo es Dios con quienes regresan. La vergüenza dice: primero "
                    "arréglate. El padre corre antes de que nada esté arreglado.",
                ),
                "simple": L(
                    "A son made big mistakes and was scared to go home. His father ran to hug him. God "
                    "loves us like that, no matter what.",
                    "Un hijo cometió grandes errores y tenía miedo de volver a casa. Su papá corrió a "
                    "abrazarlo. Así nos ama Dios, pase lo que pase.",
                ),
                "ask": L(
                    "What speech have you been rehearsing for God? What happens in you when you "
                    "picture him running toward you before you have said it?",
                    "¿Qué discurso has estado ensayando para Dios? ¿Qué pasa dentro de ti al "
                    "imaginarlo corriendo hacia ti antes de que lo digas?",
                ),
                "kid_ask": L(
                    "How do you think the son felt when his father hugged him?",
                    "¿Cómo crees que se sintió el hijo cuando su papá lo abrazó?",
                ),
                "do": L(
                    "Today, pray without promising anything. Just come home: tell God where you have "
                    "been and let his welcome stand. Shame grows in secret, so tell one safe, trusted "
                    "person as well.",
                    "Hoy ora sin prometer nada. Solo vuelve a casa: dile a Dios dónde has estado y "
                    "deja que su bienvenida valga. La vergüenza crece en secreto, así que cuéntaselo "
                    "también a una persona segura y de confianza.",
                ),
                "kid_do": L(
                    "Give someone in your family a big hug and say: I love you no matter what.",
                    "Dale un abrazo grande a alguien de tu familia y dile: te quiero pase lo que pase.",
                ),
                "pray": L(
                    "Father, I am a long way off, and I do not feel I deserve to be called yours. I am "
                    "coming home anyway. Thank you for running.",
                    "Padre, estoy muy lejos y no siento que merezca llamarme tuyo. Vuelvo a casa de "
                    "todos modos. Gracias por correr hacia mí.",
                ),
            },
            {
                "key": "addiction-3",
                "ref": "Ecclesiastes 4:9-12",
                "title": L("Not by yourself", "No a solas"),
                "truth": L(
                    "The Teacher states it plainly: two people are better off than one, because when "
                    "one falls the other can help them up, and it is a hard thing to fall with nobody "
                    "there. Addiction feeds on isolation and secrecy. Almost no one gets free alone, "
                    "and needing other people is not a failure of faith. It is how God made us. Help "
                    "comes in many forms, and most people need more than one: a friend who knows the "
                    "truth, a recovery group, a pastor, a counselor, a doctor.",
                    "El Maestro lo dice sin rodeos: a dos personas les va mejor que a una, porque si "
                    "una cae la otra puede levantarla, y es duro caer sin nadie cerca. La adicción se "
                    "alimenta del aislamiento y del secreto. Casi nadie se libera a solas, y necesitar "
                    "a otros no es falta de fe. Así nos hizo Dios. La ayuda tiene muchas formas, y la "
                    "mayoría necesita más de una: un amigo que sepa la verdad, un grupo de "
                    "recuperación, un pastor, un consejero, un médico.",
                ),
                "simple": L(
                    "Two friends are stronger than one. When one falls down, the other helps them up. "
                    "God gives us people so we do not have to do hard things alone.",
                    "Dos amigos son más fuertes que uno. Cuando uno se cae, el otro lo ayuda a "
                    "levantarse. Dios nos da personas para no tener que hacer a solas las cosas difíciles.",
                ),
                "ask": L(
                    "Who would you call at the worst moment? If no name comes to mind, where could you "
                    "go this week to begin finding that person?",
                    "¿A quién llamarías en el peor momento? Si no te viene ningún nombre, ¿a dónde "
                    "podrías ir esta semana para empezar a encontrar a esa persona?",
                ),
                "kid_ask": L(
                    "Who helps you when you fall down or feel sad?",
                    "¿Quién te ayuda cuando te caes o sientes tristeza?",
                ),
                "do": L(
                    "This week, take one step toward help: find a recovery group near you or online "
                    "and attend once, or make an appointment with a doctor or counselor. If you use "
                    "alcohol or drugs heavily, talk to a doctor before stopping suddenly; with some "
                    "substances, stopping all at once can be dangerous.",
                    "Esta semana da un paso hacia la ayuda: busca un grupo de recuperación cerca de ti "
                    "o en línea y asiste una vez, o pide cita con un médico o consejero. Si consumes "
                    "mucho alcohol o drogas, habla con un médico antes de dejarlo de golpe; con "
                    "algunas sustancias, dejarlas de repente puede ser peligroso.",
                ),
                "kid_do": L(
                    "Thank someone who helps you, and ask them: is there anything I can help you with?",
                    "Dale las gracias a alguien que te ayuda y pregúntale: ¿puedo ayudarte en algo?",
                ),
                "pray": L(
                    "God, I have tried to do this alone, and it has not worked. Lead me to people who "
                    "can help lift me, and give me the courage to let them.",
                    "Dios, he intentado hacer esto a solas y no ha funcionado. Llévame a personas que "
                    "puedan ayudar a levantarme, y dame el valor de dejarme ayudar.",
                ),
            },
            {
                "key": "addiction-4",
                "ref": "Psalm 40:1-3",
                "title": L("Out of the pit, one step at a time", "Fuera del pozo, paso a paso"),
                "truth": L(
                    "David remembers being stuck in a pit of mud with nothing solid under his feet. He "
                    "cried out, and he waited, and God bent down and heard him, lifted him out, set "
                    "his feet on rock and made his steps steady. Notice the waiting. Rescue was real, "
                    "and it was not instant. Recovery is usually like that: a lifting out, and then "
                    "learning to walk on firm ground one step and one day at a time. David adds that "
                    "his story became a reason for others to trust God. Yours can too.",
                    "David recuerda haber estado atascado en un pozo de lodo, sin nada firme bajo los "
                    "pies. Clamó y esperó, y Dios se inclinó y lo escuchó, lo sacó, puso sus pies "
                    "sobre roca y afirmó sus pasos. Fíjate en la espera. El rescate fue real, y no fue "
                    "instantáneo. La recuperación suele ser así: ser sacado, y luego aprender a "
                    "caminar en suelo firme, un paso y un día a la vez. David añade que su historia "
                    "llegó a ser un motivo para que otros confiaran en Dios. La tuya también puede serlo.",
                ),
                "simple": L(
                    "David was stuck, like in deep mud. He called to God, and God pulled him out and "
                    "put him on solid ground. God helps people who are stuck.",
                    "David estaba atascado, como en lodo profundo. Llamó a Dios, y Dios lo sacó y lo "
                    "puso en suelo firme. Dios ayuda a quienes están atascados.",
                ),
                "ask": L(
                    "What would firm ground look like for you over just the next twenty-four hours?",
                    "¿Cómo sería para ti pisar suelo firme solo durante las próximas veinticuatro horas?",
                ),
                "kid_ask": L(
                    "Have you ever been stuck and needed someone to help you out?",
                    "¿Alguna vez te quedaste sin poder salir de algo y necesitaste que alguien te ayudara?",
                ),
                "do": L(
                    "Plan only today. Write down the hardest hour of your day and one thing you will "
                    "do during it instead: call someone, go for a walk, go to a meeting. Tomorrow, do "
                    "the same again.",
                    "Planea solo el día de hoy. Anota la hora más difícil de tu día y una cosa que "
                    "harás en ese momento en lugar de lo de siempre: llamar a alguien, salir a "
                    "caminar, ir a una reunión. Mañana, haz lo mismo otra vez.",
                ),
                "kid_do": L(
                    "Draw a picture of God lifting someone out of the mud onto a big rock.",
                    "Dibuja a Dios sacando a alguien del lodo y poniéndolo sobre una roca grande.",
                ),
                "pray": L(
                    "Lord, I am in the mud and I cannot climb out. Hear me. Lift me. Give me firm "
                    "ground for today, and I will ask again tomorrow.",
                    "Señor, estoy en el lodo y no puedo salir por mis fuerzas. Escúchame. Levántame. "
                    "Dame suelo firme para hoy, y mañana te lo volveré a pedir.",
                ),
            },
            {
                "key": "addiction-5",
                "ref": "Lamentations 3:19-24",
                "title": L("After a relapse", "Después de una recaída"),
                "truth": L(
                    "These lines were written among ruins, by someone whose soul sinks when he "
                    "remembers how bitter things have been. Then he deliberately calls something else "
                    "to mind, and it gives him hope: the Lord's faithful love has not run out. His "
                    "mercy arrives fresh each morning. It is not left over from yesterday, and "
                    "yesterday's failure did not use it up. A relapse is serious, and it is not the "
                    "end. It does not erase the days you stayed free or cancel the mercy waiting for "
                    "you this morning. Get up, tell someone today, and begin again.",
                    "Estas líneas se escribieron entre ruinas, por alguien cuya alma se hunde al "
                    "recordar lo amargo que ha sido todo. Entonces, a propósito, trae otra cosa a la "
                    "memoria, y eso le da esperanza: el amor fiel del Señor no se ha agotado. Su "
                    "misericordia llega nueva cada mañana. No es la que sobró de ayer, ni la gastó el "
                    "fracaso de ayer. Una recaída es seria, y no es el final. No borra los días en que "
                    "te mantuviste libre ni cancela la misericordia que te espera esta mañana. "
                    "Levántate, cuéntaselo a alguien hoy y empieza de nuevo.",
                ),
                "simple": L(
                    "Every morning God gives us a fresh start. Even after a bad day, his love is still "
                    "there when we wake up.",
                    "Cada mañana Dios nos da un nuevo comienzo. Aun después de un mal día, su amor "
                    "sigue ahí cuando despertamos.",
                ),
                "ask": L(
                    "When you fall, what do you tell yourself it means about you? What does this "
                    "passage say instead?",
                    "Cuando caes, ¿qué te dices que eso significa sobre ti? ¿Qué dice este pasaje en "
                    "cambio?",
                ),
                "kid_ask": L(
                    "What is something you would like a fresh start with?",
                    "¿En qué te gustaría tener un nuevo comienzo?",
                ),
                "do": L(
                    "If you have relapsed, tell your sponsor, counselor, doctor or a trusted friend "
                    "within a day; do not wait until you have good news to report. If you ever feel "
                    "hopeless or think about harming yourself, contact a crisis line or emergency "
                    "services right away.",
                    "Si recaíste, cuéntaselo a tu padrino o madrina, consejero, médico o a un amigo de "
                    "confianza antes de que pase un día; no esperes a tener buenas noticias que dar. "
                    "Si alguna vez sientes que no hay esperanza o piensas en hacerte daño, llama de "
                    "inmediato a una línea de crisis o a los servicios de emergencia.",
                ),
                "kid_do": L(
                    "Tomorrow morning, say: Thank you, God, for a brand-new day.",
                    "Mañana por la mañana di: Gracias, Dios, por un día nuevecito.",
                ),
                "pray": L(
                    "God, I fell again, and I am ashamed. Your mercy is new this morning, and I am "
                    "asking for it. Help me get up and tell the truth today.",
                    "Dios, caí otra vez y siento vergüenza. Tu misericordia es nueva esta mañana, y te "
                    "la pido. Ayúdame a levantarme y a decir la verdad hoy.",
                ),
            },
        ],
    },
    {
        "key": "self_control",
        "category": "strength",
        "title": L("Self-control and good habits", "Dominio propio y buenos hábitos"),
        "summary": L(
            "For when your appetites, your phone or your moods are running the day. Four readings on "
            "why self-control protects you, where it really comes from, and how small daily training "
            "adds up.",
            "Para cuando tus apetitos, tu teléfono o tus estados de ánimo dirigen el día. Cuatro "
            "lecturas sobre por qué el dominio propio te protege, de dónde viene en realidad y cómo "
            "suma el entrenamiento pequeño de cada día.",
        ),
        "keywords": [
            "self-control", "disciplin", "habits", "impulsive", "procrastin", "lazy", "willpower",
            "overeat", "binge", "screen time", "scrolling", "dominio propio", "hábito", "impulsiv",
            "pereza", "fuerza de voluntad", "antojo", "pantalla", "celular", "autocontrol",
        ],
        "situations": ["student", "working", "parent", "recovery"],
        "traits": ["self_control", "patience", "perseverance"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Sometimes your body wants to grab, shout or keep playing. God helps you learn to "
                "stop and choose.",
                "A veces tu cuerpo quiere agarrar, gritar o seguir jugando. Dios te ayuda a aprender "
                "a detenerte y elegir.",
            ),
            "teen": L(
                "For the phone at 1 a.m., the homework put off again, the thing you said you would "
                "stop. Change starts smaller than you think.",
                "Para el teléfono a la 1 de la mañana, la tarea pospuesta otra vez, eso que dijiste "
                "que ibas a dejar. El cambio empieza más pequeño de lo que crees.",
            ),
            "young_adult": L(
                "No one is setting your schedule now. Here is how to build a life you actually chose, "
                "one habit at a time.",
                "Ya nadie te pone el horario. Aquí verás cómo construir una vida que de verdad "
                "elegiste, un hábito a la vez.",
            ),
            "adult": L(
                "For food, drink, spending, screens and temper: the appetites that quietly take over "
                "a busy, tired life.",
                "Para la comida, la bebida, los gastos, las pantallas y el carácter: los apetitos que "
                "se adueñan en silencio de una vida ocupada y cansada.",
            ),
            "senior": L(
                "It is not too late to form a new habit or lay down an old one. Small, steady choices "
                "still shape the heart.",
                "No es tarde para formar un hábito nuevo o dejar uno viejo. Las decisiones pequeñas y "
                "constantes siguen dando forma al corazón.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "self_control-1",
                "ref": "Proverbs 25:28",
                "title": L("A city without walls", "Una ciudad sin murallas"),
                "truth": L(
                    "In the ancient world a city's walls were what kept it safe; a city with broken "
                    "walls belonged to whoever walked in. This proverb says a person without "
                    "self-control is like that. Whatever shows up, a craving, a mood, a notification, "
                    "an insult, gets to walk in and take over. Seen this way, self-control is not "
                    "about being strict or joyless. It is protection. It is what lets you, rather than "
                    "every passing impulse, decide what happens in your life.",
                    "En el mundo antiguo las murallas eran lo que mantenía a salvo a una ciudad; una "
                    "ciudad con las murallas rotas era de quien quisiera entrar. Este proverbio dice "
                    "que así es una persona sin dominio propio. Cualquier cosa que aparezca, un "
                    "antojo, un mal humor, una notificación, un insulto, entra y toma el mando. Visto "
                    "así, el dominio propio no es ser rígido ni vivir sin alegría. Es protección. Es "
                    "lo que te permite a ti, y no a cada impulso pasajero, decidir qué pasa en tu vida.",
                ),
                "simple": L(
                    "Long ago, cities had big walls to keep them safe. Self-control is like a wall: it "
                    "helps you stop and choose, so you do not get hurt or hurt someone else.",
                    "Hace mucho, las ciudades tenían murallas grandes que las protegían. El dominio "
                    "propio es como una muralla: te ayuda a detenerte y elegir, para no lastimarte ni "
                    "lastimar a otros.",
                ),
                "ask": L(
                    "Where is the gap in your wall: the place where an impulse most easily walks in "
                    "and takes over your day?",
                    "¿Dónde está la brecha en tu muralla: el lugar por donde un impulso entra con más "
                    "facilidad y se adueña de tu día?",
                ),
                "kid_ask": L(
                    "When is it hard for you to stop and wait?",
                    "¿Cuándo te cuesta detenerte y esperar?",
                ),
                "do": L(
                    "Pick one gap and put up one small barrier today: charge your phone outside the "
                    "bedroom, keep that snack out of the house, set a spending limit before you shop.",
                    "Elige una brecha y pon hoy una pequeña barrera: carga el teléfono fuera del "
                    "cuarto, no tengas ese antojo en casa, fija un límite de gasto antes de comprar.",
                ),
                "kid_do": L(
                    "Play a stop-and-go game with a grown-up, like freeze dance or red light, green "
                    "light, to practice stopping.",
                    "Juega con un adulto a un juego de parar y seguir, como las estatuas o el "
                    "semáforo, para practicar cómo detenerte.",
                ),
                "pray": L(
                    "God, some things walk right into my life and take over. Show me where the wall is "
                    "down, and help me rebuild it one stone at a time.",
                    "Dios, hay cosas que entran en mi vida y toman el mando. Muéstrame dónde está "
                    "caída la muralla y ayúdame a levantarla piedra por piedra.",
                ),
            },
            {
                "key": "self_control-2",
                "ref": "Galatians 5:22-25",
                "title": L("Fruit, not just willpower", "Fruto, no solo fuerza de voluntad"),
                "truth": L(
                    "Self-control comes at the end of a list Paul calls the fruit of the Spirit, "
                    "alongside love, joy, peace and patience. Fruit is not manufactured by gritting "
                    "your teeth. It grows on a branch that is connected and alive. That changes how "
                    "you go after self-control. You still make choices; Paul says to keep in step with "
                    "the Spirit, which is something you do. But the power is not all yours. You are "
                    "cooperating with God, who is at work in you, not performing for him.",
                    "El dominio propio aparece al final de una lista que Pablo llama el fruto del "
                    "Espíritu, junto al amor, el gozo, la paz y la paciencia. El fruto no se fabrica "
                    "apretando los dientes. Crece en una rama conectada y viva. Eso cambia la manera "
                    "de buscar el dominio propio. Sigues tomando decisiones; Pablo dice que andemos al "
                    "paso del Espíritu, y eso es algo que haces tú. Pero la fuerza no es toda tuya. "
                    "Colaboras con Dios, que obra en ti; no actúas para impresionarlo.",
                ),
                "simple": L(
                    "Self-control grows in us like fruit grows on a tree. God helps it grow. We help "
                    "by staying close to him.",
                    "El dominio propio crece en nosotros como la fruta crece en un árbol. Dios lo hace "
                    "crecer. Nosotros ayudamos quedándonos cerca de él.",
                ),
                "ask": L(
                    "Where have you been relying on willpower alone? What would it look like to ask "
                    "for God's help at the moment of choice, not only afterward?",
                    "¿Dónde has dependido solo de tu fuerza de voluntad? ¿Cómo sería pedirle ayuda a "
                    "Dios en el momento de elegir, y no solo después?",
                ),
                "kid_ask": L(
                    "What good fruit would you like God to grow in you: kindness, patience, self-control?",
                    "¿Qué frutos buenos te gustaría que Dios hiciera crecer en ti: bondad, paciencia, "
                    "dominio propio?",
                ),
                "do": L(
                    "Attach a ten-second prayer to the moment you usually give in. Before opening the "
                    "app, the fridge or your mouth, say: Spirit of God, lead me here.",
                    "Une una oración de diez segundos al momento en que sueles ceder. Antes de abrir "
                    "la aplicación, el refrigerador o la boca, di: Espíritu de Dios, guíame aquí.",
                ),
                "kid_do": L(
                    "Draw a tree, and on each fruit write one good thing you want God to grow in you.",
                    "Dibuja un árbol y en cada fruta escribe algo bueno que quieres que Dios haga "
                    "crecer en ti.",
                ),
                "pray": L(
                    "Holy Spirit, I cannot grow this by force. Grow it in me. Keep me close, and help "
                    "me take the next step with you.",
                    "Espíritu Santo, no puedo hacer crecer esto a la fuerza. Hazlo crecer en mí. "
                    "Mantenme cerca y ayúdame a dar el siguiente paso contigo.",
                ),
            },
            {
                "key": "self_control-3",
                "ref": "1 Corinthians 9:24-27",
                "title": L("Train, do not just try", "Entrena, no solo lo intentes"),
                "truth": L(
                    "Paul points to athletes. No runner wins by wishing on race day; they train for a "
                    "long time, saying no to many things for the sake of one thing they want more. He "
                    "says he lives the same way: not running without aim, but training his body so "
                    "that it serves him instead of ruling him. The lesson is practical. Self-control "
                    "in the big moment is built beforehand, in small, repeated, unglamorous choices. "
                    "And it is always for the sake of something better, not denial for its own sake.",
                    "Pablo señala a los atletas. Ningún corredor gana solo con desearlo el día de la "
                    "carrera; entrena mucho tiempo y dice que no a muchas cosas por una que quiere "
                    "más. Dice que él vive igual: no corre sin rumbo, sino que entrena su cuerpo para "
                    "que le sirva en lugar de mandarlo. La lección es práctica. El dominio propio en "
                    "el momento grande se construye antes, con decisiones pequeñas, repetidas y nada "
                    "vistosas. Y siempre es por algo mejor, no por negarse cosas porque sí.",
                ),
                "simple": L(
                    "Runners practice every day to get strong. We can practice good choices every day "
                    "too, a little at a time.",
                    "Los corredores practican todos los días para hacerse fuertes. Nosotros también "
                    "podemos practicar buenas decisiones cada día, poquito a poco.",
                ),
                "ask": L(
                    "What is the better thing you want, the prize, that makes saying no worth it? Can "
                    "you say it in one sentence?",
                    "¿Cuál es eso mejor que quieres, el premio, que hace que valga la pena decir que "
                    "no? ¿Puedes decirlo en una frase?",
                ),
                "kid_ask": L(
                    "What is something you got better at by practicing?",
                    "¿En qué has mejorado gracias a practicar?",
                ),
                "do": L(
                    "Choose one habit so small you cannot fail: two minutes, once a day, tied to "
                    "something you already do. Keep it for seven days before adding anything.",
                    "Elige un hábito tan pequeño que no puedas fallar: dos minutos, una vez al día, "
                    "unido a algo que ya haces. Mantenlo siete días antes de añadir otra cosa.",
                ),
                "kid_do": L(
                    "Pick one small job, like making your bed, and do it every day this week. Make a "
                    "chart and mark each day.",
                    "Elige una tarea pequeña, como tender tu cama, y hazla todos los días esta semana. "
                    "Haz una tabla y marca cada día.",
                ),
                "pray": L(
                    "Lord, I want the prize but I skip the training. Give me a clear picture of what I "
                    "am running for, and help me with today's small step.",
                    "Señor, quiero el premio pero me salto el entrenamiento. Dame una imagen clara de "
                    "aquello por lo que corro y ayúdame con el pequeño paso de hoy.",
                ),
            },
            {
                "key": "self_control-4",
                "ref": "Titus 2:11-14",
                "title": L("Grace is the teacher", "La gracia es la maestra"),
                "truth": L(
                    "You might expect self-control to be taught by rules, fear or shame. Paul says it "
                    "is taught by grace. The grace of God that brings salvation also trains us: to say "
                    "no to what harms, and to live sensible, upright lives now, while we wait with "
                    "hope. It all rests on what Jesus has done, giving himself to set us free and make "
                    "us his own. So when you fail, you do not go back to shame as your teacher. You go "
                    "back to grace, and grace says: you belong to me; try again.",
                    "Uno pensaría que el dominio propio se enseña con reglas, miedo o vergüenza. Pablo "
                    "dice que lo enseña la gracia. La gracia de Dios que trae salvación también nos "
                    "entrena: a decir que no a lo que daña y a vivir ahora con sensatez y rectitud, "
                    "mientras esperamos con esperanza. Todo descansa en lo que hizo Jesús, que se "
                    "entregó para liberarnos y hacernos suyos. Por eso, cuando fallas, no vuelves a la "
                    "vergüenza como maestra. Vuelves a la gracia, y la gracia dice: me perteneces; "
                    "inténtalo otra vez.",
                ),
                "simple": L(
                    "God does not teach us by being mean. He teaches us with love. When we mess up, he "
                    "helps us try again.",
                    "Dios no nos enseña con maltrato. Nos enseña con amor. Cuando nos equivocamos, nos "
                    "ayuda a intentarlo otra vez.",
                ),
                "ask": L(
                    "When you fail at self-control, whose voice do you hear: shame's or grace's? What "
                    "would grace say to you about last time?",
                    "Cuando te falla el dominio propio, ¿qué voz escuchas: la de la vergüenza o la de "
                    "la gracia? ¿Qué te diría la gracia sobre la última vez?",
                ),
                "kid_ask": L(
                    "How do you like to be helped when you make a mistake?",
                    "¿Cómo te gusta que te ayuden cuando te equivocas?",
                ),
                "do": L(
                    "The next time you slip, skip the speech of self-contempt. Tell God in one "
                    "sentence that you belong to him and want to learn, and then do the very next "
                    "right thing.",
                    "La próxima vez que tropieces, sáltate el discurso de desprecio hacia ti. Dile a "
                    "Dios en una frase que le perteneces y quieres aprender, y luego haz la siguiente "
                    "cosa correcta.",
                ),
                "kid_do": L(
                    "If you make a mistake today, say: I can try again. Then try again.",
                    "Si hoy te equivocas, di: puedo intentarlo otra vez. Y vuelve a intentarlo.",
                ),
                "pray": L(
                    "God, I have tried to change by being hard on myself. Let your grace be my "
                    "teacher. Train me to say no, and to say yes to what is good.",
                    "Dios, he tratado de cambiar tratándome con dureza. Que tu gracia sea mi maestra. "
                    "Entréname para decir que no, y para decir que sí a lo bueno.",
                ),
            },
        ],
    },
    {
        "key": "anger",
        "category": "strength",
        "title": L("Anger and resentment", "Enojo y resentimiento"),
        "summary": L(
            "For a short fuse, a slow burn, or a grudge you cannot put down. Five readings on what "
            "anger is telling you, how to slow it, and how to keep it from turning into harm.",
            "Para quien explota rápido, hierve despacio o carga un rencor que no logra soltar. Cinco "
            "lecturas sobre lo que el enojo te está diciendo, cómo frenarlo y cómo evitar que se "
            "convierta en daño.",
        ),
        "keywords": [
            "anger", "angry", "furious", "rage", "temper", "resent", "grudge", "bitter", "yell",
            "irritat", "lost it", "snapped", "enoj", "rabia", "furi", "rencor", "amarg", "grité",
            "gritar", "irrit", "exploté",
        ],
        "situations": ["parent", "married", "working", "caregiver", "divorced"],
        "traits": ["patience", "gentleness", "self_control"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Everyone gets mad sometimes. God can help you with big feelings so they do not hurt "
                "you or anyone else.",
                "Todos nos enojamos a veces. Dios puede ayudarte con los sentimientos grandes para "
                "que no te lastimen a ti ni a nadie más.",
            ),
            "teen": L(
                "For when parents, siblings, teachers or friends push you past your limit, and for "
                "what to do with it that you will not regret.",
                "Para cuando tus papás, hermanos, maestros o amigos te sacan de quicio, y para saber "
                "qué hacer con eso sin arrepentirte después.",
            ),
            "young_adult": L(
                "For anger at how you were treated, at unfairness, at yourself. It can become fuel or "
                "poison. Here is the difference.",
                "Para el enojo por cómo te trataron, por la injusticia, por tus propios errores. "
                "Puede volverse combustible o veneno. Aquí está la diferencia.",
            ),
            "adult": L(
                "For the sharp word to your children, the cold war at home, the resentment at work "
                "that follows you to bed.",
                "Para la palabra dura a tus hijos, la guerra fría en casa, el resentimiento del "
                "trabajo que te sigue hasta la cama.",
            ),
            "senior": L(
                "For old injuries that still burn, and for the irritability that comes with pain and "
                "loss. It is not too late to lay it down.",
                "Para las heridas viejas que todavía arden y la irritabilidad que llega con el dolor "
                "y las pérdidas. No es tarde para soltarlo.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "anger-1",
                "ref": "Ephesians 4:26-27",
                "title": L("Anger is not the sin", "El enojo no es el pecado"),
                "truth": L(
                    "Paul assumes you will be angry, and he does not call that sin. Anger is often the "
                    "right response to something truly wrong. What he warns about is what happens "
                    "next. He sets two limits: do not let anger carry you into doing harm, and do not "
                    "let it stay overnight. Anger kept and fed becomes an open door for evil to work "
                    "in you and in your relationships. So the question is rarely whether you felt "
                    "angry. It is what you did with it, and how long you held on to it.",
                    "Pablo da por hecho que te vas a enojar, y no lo llama pecado. Muchas veces el "
                    "enojo es la reacción correcta ante algo que de verdad está mal. Lo que advierte "
                    "es lo que viene después. Pone dos límites: no dejes que el enojo te lleve a hacer "
                    "daño, y no dejes que se quede a dormir. El enojo guardado y alimentado se vuelve "
                    "una puerta abierta para que el mal actúe en ti y en tus relaciones. Así que la "
                    "pregunta casi nunca es si sentiste enojo. Es qué hiciste con él y cuánto tiempo "
                    "lo retuviste.",
                ),
                "simple": L(
                    "Feeling mad is not bad. But we should not hurt people when we are mad, and we "
                    "should try to make things right before bedtime.",
                    "Sentir enojo no es malo. Pero no debemos lastimar a nadie cuando sentimos enojo, "
                    "y conviene arreglar las cosas antes de dormir.",
                ),
                "ask": L(
                    "What anger have you let stay past sundown, for days or for years? What has it "
                    "opened the door to?",
                    "¿Qué enojo has dejado quedarse más allá del atardecer, por días o por años? ¿A "
                    "qué le ha abierto la puerta?",
                ),
                "kid_ask": L(
                    "What does your body feel like when you are mad?",
                    "¿Qué siente tu cuerpo cuando te enojas?",
                ),
                "do": L(
                    "Before you sleep tonight, deal with one anger. Say the honest sentence to the "
                    "person, or, if that is not possible or safe, say it to God out loud and write it down.",
                    "Antes de dormir esta noche, atiende un enojo. Dile la frase honesta a la persona "
                    "o, si eso no es posible o seguro, díselo a Dios en voz alta y escríbelo.",
                ),
                "kid_do": L(
                    "When you feel mad today, say out loud: I feel mad because… Then take three slow breaths.",
                    "Cuando hoy sientas enojo, di en voz alta: siento enojo porque… Luego respira "
                    "despacio tres veces.",
                ),
                "pray": L(
                    "God, I am angry about … You already know. Keep me from doing harm with it, and "
                    "help me not carry it into tomorrow.",
                    "Dios, tengo enojo por … Tú ya lo sabes. Guárdame de hacer daño con él y ayúdame a "
                    "no cargarlo hasta mañana.",
                ),
            },
            {
                "key": "anger-2",
                "ref": "Genesis 4:3-7",
                "title": L("God's question to an angry man", "La pregunta de Dios a un hombre enojado"),
                "truth": L(
                    "Cain is furious because his brother's offering was accepted and his was not. "
                    "Before anything worse happens, God comes to him and asks what his anger is about. "
                    "It is an invitation to look underneath, where there seems to be jealousy and hurt "
                    "pride. Then God gives a warning and a dignity. Sin is crouching at the door like "
                    "an animal ready to spring, and Cain can, and must, master it. Anger is a moment "
                    "of decision. God meets you in that moment, asking what is really going on.",
                    "Caín está furioso porque la ofrenda de su hermano fue aceptada y la suya no. "
                    "Antes de que pase algo peor, Dios se le acerca y le pregunta por la causa de su "
                    "enojo. Es una invitación a mirar debajo, donde parece haber celos y orgullo "
                    "herido. Luego Dios le da una advertencia y una dignidad. El pecado está agazapado "
                    "a la puerta, como un animal listo para saltar, y Caín puede y debe dominarlo. El "
                    "enojo es un momento de decisión. Dios te sale al encuentro en ese momento y te "
                    "pregunta qué está pasando de verdad.",
                ),
                "simple": L(
                    "Cain was very mad at his brother. God asked him why, and told him he could choose "
                    "not to let his anger take over.",
                    "Caín estaba muy enojado con su hermano. Dios le preguntó por qué y le dijo que "
                    "podía elegir no dejar que el enojo lo dominara.",
                ),
                "ask": L(
                    "Take your most recent anger and answer God's question honestly. What is "
                    "underneath: fear, hurt, envy, shame, exhaustion?",
                    "Toma tu enojo más reciente y responde con honestidad la pregunta de Dios. ¿Qué "
                    "hay debajo: miedo, dolor, envidia, vergüenza, agotamiento?",
                ),
                "kid_ask": L(
                    "Last time you were mad, what was the feeling under the mad: sad, scared, left out?",
                    "La última vez que te enojaste, ¿qué sentías debajo del enojo: tristeza, miedo, "
                    "que te dejaron de lado?",
                ),
                "do": L(
                    "Next time anger rises, pause and finish this sentence before you speak: I am "
                    "angry because I feel …",
                    "La próxima vez que suba el enojo, haz una pausa y termina esta frase antes de "
                    "hablar: tengo enojo porque siento …",
                ),
                "kid_do": L(
                    "Draw a picture of your mad feeling. Then tell a grown-up what is under it.",
                    "Dibuja tu enojo. Luego cuéntale a un adulto qué hay debajo.",
                ),
                "pray": L(
                    "Lord, you ask me what my anger is about. Help me answer truthfully. Show me what "
                    "is underneath, and help me master this before it masters me.",
                    "Señor, me preguntas de dónde viene mi enojo. Ayúdame a responder con la verdad. "
                    "Muéstrame qué hay debajo y ayúdame a dominar esto antes de que me domine.",
                ),
            },
            {
                "key": "anger-3",
                "ref": "James 1:19-20",
                "title": L("Slow it down", "Más despacio"),
                "truth": L(
                    "James gives three speeds: be quick to listen, slow to speak, slow to become "
                    "angry. Most of us run them in reverse. His reason is blunt: human anger does not "
                    "produce the upright life God wants. It feels as though it will; in the heat of "
                    "the moment, anger seems like the way to fix things. It rarely is. The practical "
                    "wisdom here is about time. Nearly everything anger wants you to say will still be "
                    "available in an hour, and most of it you will no longer want to say.",
                    "Santiago marca tres velocidades: rapidez para escuchar, lentitud para hablar, "
                    "lentitud para enojarse. La mayoría las usamos al revés. Su razón es directa: el "
                    "enojo humano no produce la vida recta que Dios quiere. Parece que sí; en el calor "
                    "del momento, el enojo se siente como la manera de arreglar las cosas. Casi nunca "
                    "lo es. La sabiduría práctica aquí tiene que ver con el tiempo. Casi todo lo que "
                    "el enojo quiere que digas seguirá disponible dentro de una hora, y la mayor parte "
                    "ya no querrás decirla.",
                ),
                "simple": L(
                    "God says: listen fast, talk slow, and get mad slow. When we slow down, we make "
                    "better choices.",
                    "Dios dice: escucha rápido, habla despacio y enójate despacio. Cuando vamos más "
                    "lento, elegimos mejor.",
                ),
                "ask": L(
                    "In your last argument, what did the other person say that you did not really hear "
                    "because you were preparing your reply?",
                    "En tu última discusión, ¿qué dijo la otra persona que no escuchaste de verdad "
                    "porque estabas preparando tu respuesta?",
                ),
                "kid_ask": L(
                    "What helps you calm down when you feel like yelling?",
                    "¿Qué te ayuda a calmarte cuando tienes ganas de gritar?",
                ),
                "do": L(
                    "Set a rule for this week: when you feel the heat rise, wait before you answer. "
                    "Leave the room if you need to, and do not send the message until tomorrow.",
                    "Ponte una regla esta semana: cuando sientas que sube la temperatura, espera antes "
                    "de responder. Sal del cuarto si hace falta, y no envíes el mensaje hasta mañana.",
                ),
                "kid_do": L(
                    "Practice counting slowly to ten with a grown-up. Use it the next time you feel mad.",
                    "Practica con un adulto contar despacio hasta diez. Úsalo la próxima vez que te enojes.",
                ),
                "pray": L(
                    "God, make me quick to listen and slow to speak. When the heat rises today, give "
                    "me a pause long enough to choose.",
                    "Dios, dame prontitud para escuchar y calma para hablar. Cuando hoy suba la "
                    "temperatura, dame una pausa lo bastante larga para elegir.",
                ),
            },
            {
                "key": "anger-4",
                "ref": "Proverbs 15:1",
                "title": L("The gentle answer", "La respuesta suave"),
                "truth": L(
                    "This proverb describes two ways a tense moment can go. A harsh word stirs up more "
                    "anger; a gentle answer turns it away. It takes two to escalate, and either one "
                    "can stop. A gentle answer is not weakness, and it is not agreeing that the other "
                    "person is right. It is choosing your tone on purpose instead of matching theirs. "
                    "It is one of the few things fully within your power in a conflict, and it changes "
                    "more than you would expect.",
                    "Este proverbio describe dos rumbos que puede tomar un momento tenso. La palabra "
                    "áspera aviva el enojo; la respuesta suave lo aparta. Para que una discusión "
                    "escale hacen falta dos, y cualquiera de los dos puede frenar. Responder con "
                    "suavidad no es debilidad ni es darle la razón a la otra persona. Es elegir tu "
                    "tono a propósito en lugar de copiar el suyo. Es de las pocas cosas que dependen "
                    "por completo de ti en un conflicto, y cambia más de lo que uno esperaría.",
                ),
                "simple": L(
                    "Soft words help people calm down. Loud, mean words make a fight bigger. You can "
                    "choose soft words.",
                    "Las palabras suaves ayudan a que la gente se calme. Las palabras fuertes y feas "
                    "hacen más grande la pelea. Tú puedes elegir palabras suaves.",
                ),
                "ask": L(
                    "With whom do you most often match heat with heat? What would a gentle first "
                    "sentence sound like next time?",
                    "¿Con quién sueles responder al fuego con fuego? ¿Cómo sonaría una primera frase "
                    "suave la próxima vez?",
                ),
                "kid_ask": L(
                    "How do you feel when someone talks to you in a soft, kind voice?",
                    "¿Cómo te sientes cuando alguien te habla con voz suave y amable?",
                ),
                "do": L(
                    "In your next tense exchange, lower your voice on purpose, and start with what you "
                    "heard the other person say before saying anything of your own.",
                    "En tu próximo intercambio tenso, baja la voz a propósito y empieza repitiendo lo "
                    "que entendiste de la otra persona antes de decir lo tuyo.",
                ),
                "kid_do": L(
                    "Next time someone is grumpy with you, try answering in a quiet, kind voice and "
                    "see what happens.",
                    "La próxima vez que alguien te hable de mal humor, prueba responder con voz bajita "
                    "y amable, y mira qué pasa.",
                ),
                "pray": L(
                    "Lord, my tone gets away from me. Give me a gentle answer for the person who is "
                    "hardest for me today.",
                    "Señor, el tono se me escapa. Dame una respuesta suave para la persona que más me "
                    "cuesta hoy.",
                ),
            },
            {
                "key": "anger-5",
                "ref": "Romans 12:17-21",
                "title": L("Laying down the right to get even", "Soltar el derecho al desquite"),
                "truth": L(
                    "Resentment is anger that has moved in. Paul speaks to people who have truly been "
                    "wronged, and he does not say it did not matter. He says: do not pay back evil "
                    "with evil; as far as it depends on you, live at peace; and leave the settling of "
                    "accounts to God. That is not pretending nothing happened. It is handing the case "
                    "to a better judge, so that you no longer have to carry it. Then he goes further: "
                    "meet your enemy's need. Evil is not defeated by more evil. It is overcome by good.",
                    "El resentimiento es el enojo que se quedó a vivir. Pablo habla a personas que de "
                    "verdad han sido agraviadas, y no dice que no importó. Dice: no devuelvas mal por "
                    "mal; en lo que dependa de ti, vive en paz; y deja el ajuste de cuentas a Dios. "
                    "Eso no es fingir que no pasó nada. Es entregar el caso a un juez mejor, para que "
                    "ya no tengas que cargarlo. Luego va más lejos: atiende la necesidad de tu "
                    "enemigo. Al mal no se le vence con más mal. Se le vence con el bien.",
                ),
                "simple": L(
                    "When someone is mean to you, you do not have to be mean back. God sees what "
                    "happened. You can choose to do good instead.",
                    "Cuando alguien te trata mal, no tienes que tratarlo mal tú también. Dios ve lo "
                    "que pasó. Puedes elegir hacer el bien.",
                ),
                "ask": L(
                    "Whose debt are you still keeping a record of? What would it mean to hand that "
                    "file to God without saying it was nothing?",
                    "¿De quién sigues llevando la cuenta de lo que te debe? ¿Qué significaría "
                    "entregarle ese expediente a Dios sin decir que no fue nada?",
                ),
                "kid_ask": L(
                    "Is there someone you want to get back at? What could you do instead?",
                    "¿Hay alguien de quien te quieras desquitar? ¿Qué podrías hacer en vez de eso?",
                ),
                "do": L(
                    "Write the name and what they did, and beneath it: God, this case is yours. If "
                    "someone is harming you, or if your own anger frightens you or the people near "
                    "you, tell a counselor, doctor or pastor this week. Getting safe and getting help "
                    "is not revenge.",
                    "Escribe el nombre y lo que hizo, y debajo: Dios, este caso es tuyo. Si alguien te "
                    "está haciendo daño, o si tu propio enojo te asusta a ti o a quienes te rodean, "
                    "cuéntaselo esta semana a un consejero, médico o pastor. Ponerte a salvo y pedir "
                    "ayuda no es venganza.",
                ),
                "kid_do": L(
                    "Do one kind thing today for someone who was not kind to you. If someone keeps "
                    "hurting you, tell a grown-up.",
                    "Haz hoy algo amable por alguien que no fue amable contigo. Si alguien te sigue "
                    "lastimando, cuéntaselo a un adulto.",
                ),
                "pray": L(
                    "God, you saw what was done to me. I am tired of carrying it. I hand you the right "
                    "to settle it, and I ask for the strength to do good.",
                    "Dios, tú viste lo que me hicieron. Me cansé de cargarlo. Te entrego el derecho de "
                    "ajustar cuentas y te pido fuerza para hacer el bien.",
                ),
            },
        ],
    },
    # ======================================================================
    # WISDOM
    # ======================================================================
    {
        "key": "decisions",
        "category": "wisdom",
        "title": L("Decisions and God's guidance", "Decisiones y la guía de Dios"),
        "summary": L(
            "For a choice you keep turning over, or the fear of getting God's will wrong. Five "
            "readings on asking for wisdom, trusting, seeking counsel and then stepping forward "
            "without a magic formula.",
            "Para una decisión a la que le das vueltas, o el temor de equivocarte con la voluntad de "
            "Dios. Cinco lecturas sobre pedir sabiduría, confiar, buscar consejo y luego dar el paso "
            "sin fórmulas mágicas.",
        ),
        "keywords": [
            "decision", "decid", "choice", "choos", "guidance", "direction", "crossroad", "unsure",
            "confus", "god's will", "what should i do", "decisi", "elegir", "elecci", "rumbo",
            "indecis", "encrucijada", "voluntad de dios", "no sé qué hacer",
        ],
        "situations": ["student", "job_seeking", "moving", "dating", "single", "leader", "working"],
        "traits": ["wisdom", "trust", "prayerfulness"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "What to study, who to spend time with, what to say yes and no to: you can learn now "
                "how to choose well.",
                "Qué estudiar, con quién juntarte, a qué decir sí y a qué no: desde ahora puedes "
                "aprender a elegir bien.",
            ),
            "young_adult": L(
                "Career, city, relationship, church. If you are afraid of missing God's one right "
                "path, start here.",
                "Carrera, ciudad, pareja, iglesia. Si temes perderte el único camino correcto de "
                "Dios, empieza aquí.",
            ),
            "adult": L(
                "For decisions that affect other people: a job change, a move, a child's schooling, "
                "an aging parent's care.",
                "Para decisiones que afectan a otros: un cambio de trabajo, una mudanza, la escuela "
                "de un hijo, el cuidado de un padre o una madre mayor.",
            ),
            "senior": L(
                "Where to live, when to stop, what to give away, what to say while there is time. "
                "Wisdom is still promised to those who ask.",
                "Dónde vivir, cuándo parar, qué regalar, qué decir mientras hay tiempo. La sabiduría "
                "sigue prometida a quien la pide.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "decisions-1",
                "ref": "James 1:5",
                "title": L("Start by asking", "Empieza por pedir"),
                "truth": L(
                    "The first instruction for anyone who does not know what to do is simple: ask God. "
                    "James describes the God you are asking. He gives generously, to everyone, and "
                    "without scolding you for not knowing already. What is promised is wisdom, which "
                    "is not the same as a sign or a detailed map. Wisdom is the ability to see a "
                    "situation truly and act well in it. It usually comes the way wisdom tends to "
                    "come: gradually, through Scripture, prayer, thought and other people.",
                    "La primera indicación para quien no sabe qué hacer es sencilla: pídele a Dios. "
                    "Santiago describe al Dios a quien le pides. Da con generosidad, a todos, y sin "
                    "regañarte por no saberlo ya. Lo que promete es sabiduría, que no es lo mismo que "
                    "una señal o un mapa detallado. La sabiduría es la capacidad de ver una situación "
                    "como es y actuar bien en ella. Suele llegar como llega la sabiduría: poco a poco, "
                    "por medio de la Escritura, la oración, la reflexión y otras personas.",
                ),
                "simple": L(
                    "When you do not know what to do, you can ask God. He loves to help, and he never "
                    "makes fun of you for asking.",
                    "Cuando no sabes qué hacer, puedes preguntarle a Dios. A él le encanta ayudar y "
                    "nunca se burla de ti por preguntar.",
                ),
                "ask": L(
                    "What decision are you facing? Have you actually asked God for wisdom about it, or "
                    "only worried about it?",
                    "¿Qué decisión tienes delante? ¿De verdad le has pedido sabiduría a Dios, o solo "
                    "le has dado vueltas con preocupación?",
                ),
                "kid_ask": L(
                    "What is something you are not sure how to do or choose?",
                    "¿Qué cosa no sabes bien cómo hacer o elegir?",
                ),
                "do": L(
                    "Write the decision as a single question. Each morning this week, ask God for "
                    "wisdom about it in one sentence before you think about it any further.",
                    "Escribe la decisión como una sola pregunta. Cada mañana de esta semana, pídele a "
                    "Dios sabiduría sobre ella en una frase antes de seguir pensándola.",
                ),
                "kid_do": L(
                    "Next time you have to choose something, say first: God, please help me choose well.",
                    "La próxima vez que tengas que elegir algo, di primero: Dios, ayúdame a elegir bien.",
                ),
                "pray": L(
                    "God, I do not know what to do about … You give wisdom generously and without "
                    "scolding. I am asking.",
                    "Dios, no sé qué hacer con … Tú das sabiduría con generosidad y sin regaños. Te la "
                    "pido.",
                ),
            },
            {
                "key": "decisions-2",
                "ref": "Proverbs 3:5-6",
                "title": L("Trust, with your whole weight", "Confía, con todo tu peso"),
                "truth": L(
                    "This proverb does not tell you to stop thinking. It tells you not to rest your "
                    "full weight on your own understanding, as though it were all there is. You see "
                    "part of the picture; God sees all of it. Trusting him means bringing him into "
                    "every area, not only the ones marked spiritual, and being willing to be "
                    "redirected. The promise is not a life without hard choices. It is that he will "
                    "straighten the road ahead of you and get you where you need to go.",
                    "Este proverbio no te dice que dejes de pensar. Te dice que no cargues todo tu "
                    "peso sobre tu propio entendimiento, como si fuera lo único que hay. Tú ves una "
                    "parte del cuadro; Dios lo ve entero. Confiar en él es incluirlo en cada área, no "
                    "solo en las que llevan la etiqueta de espirituales, y aceptar que te cambie el "
                    "rumbo. La promesa no es una vida sin decisiones difíciles. Es que él enderezará "
                    "el camino que tienes delante y te llevará a donde necesitas llegar.",
                ),
                "simple": L(
                    "We cannot see everything, but God can. We can trust him to show us the way, like "
                    "holding a grown-up's hand in a busy place.",
                    "Nosotros no podemos verlo todo, pero Dios sí. Podemos confiar en que él nos "
                    "muestra el camino, como cuando tomas la mano de un adulto en un lugar lleno de gente.",
                ),
                "ask": L(
                    "Which area of your life have you been deciding about without really bringing God "
                    "into it: money, a relationship, your time?",
                    "¿En qué área de tu vida has estado decidiendo sin incluir de verdad a Dios: el "
                    "dinero, una relación, tu tiempo?",
                ),
                "kid_ask": L(
                    "When have you needed someone to show you the way?",
                    "¿Cuándo has necesitado que alguien te muestre el camino?",
                ),
                "do": L(
                    "List what you know and what you do not know about your decision. Beside the "
                    "second list, write: God sees this part. Pray over both lists.",
                    "Haz una lista de lo que sabes y otra de lo que no sabes sobre tu decisión. Junto "
                    "a la segunda escribe: Dios ve esta parte. Ora sobre las dos listas.",
                ),
                "kid_do": L(
                    "Take a walk with a grown-up and let them lead you for ten steps with your eyes "
                    "closed. Talk about what trusting feels like.",
                    "Sal a caminar con un adulto y deja que te guíe diez pasos con los ojos cerrados. "
                    "Hablen de cómo se siente confiar.",
                ),
                "pray": L(
                    "Lord, I have been leaning hard on what I can figure out. I trust you with the "
                    "part I cannot see. Straighten the path ahead.",
                    "Señor, me he apoyado demasiado en lo que logro entender. Te confío la parte que "
                    "no veo. Endereza el camino que tengo delante.",
                ),
            },
            {
                "key": "decisions-3",
                "ref": "Romans 12:1-2",
                "title": L("First, who you are becoming", "Primero, en quién te estás convirtiendo"),
                "truth": L(
                    "We tend to ask which option God wants. Paul begins somewhere else. Offer your "
                    "whole self to God, stop letting the world around you press you into its shape, "
                    "and let your mind be made new. The result, he says, is that you become able to "
                    "test and recognize what God's will is: what is good, pleasing and complete. "
                    "Discernment is not a code to crack. It is a capacity that grows in a person who "
                    "is being changed. Much of God's will concerns what kind of person makes the choice.",
                    "Solemos preguntar cuál opción quiere Dios. Pablo empieza por otro lado. Ofrece a "
                    "Dios todo lo que eres, deja de permitir que el mundo que te rodea te meta en su "
                    "molde y deja que tu mente sea renovada. El resultado, dice, es que llegas a ser "
                    "capaz de comprobar y reconocer cuál es la voluntad de Dios: lo bueno, lo que le "
                    "agrada, lo completo. Discernir no es descifrar un código. Es una capacidad que "
                    "crece en una persona que está siendo transformada. Buena parte de la voluntad de "
                    "Dios tiene que ver con qué clase de persona toma la decisión.",
                ),
                "simple": L(
                    "God cares most about who you are becoming: kind, honest and loving. When you grow "
                    "like that, you get better at choosing.",
                    "A Dios le importa sobre todo en quién te estás convirtiendo: alguien amable, "
                    "honesto y que ama. Cuando creces así, eliges cada vez mejor.",
                ),
                "ask": L(
                    "Set aside which option for a moment. Which choice would make you more loving, "
                    "more honest, more free to serve?",
                    "Deja a un lado por un momento cuál opción. ¿Qué elección te haría amar más, vivir "
                    "con más honestidad, tener más libertad para servir?",
                ),
                "kid_ask": L(
                    "What kind of person do you want to be on the inside when you grow up?",
                    "¿Qué clase de persona quieres ser por dentro cuando seas grande?",
                ),
                "do": L(
                    "Notice one way the pressure around you (what everyone expects, earns or posts) is "
                    "shaping this decision. Name it, and ask whether it deserves that much say.",
                    "Fíjate en una manera en que la presión de tu entorno (lo que todos esperan, ganan "
                    "o publican) está moldeando esta decisión. Nómbrala y pregúntate si merece tanta voz.",
                ),
                "kid_do": L(
                    "Choose one way to be kind or honest today, and do it.",
                    "Elige una manera de ser amable u honesto hoy, y hazla.",
                ),
                "pray": L(
                    "God, I offer you myself, not just this decision. Renew my mind, so that I can "
                    "recognize what is good when I see it.",
                    "Dios, te ofrezco todo lo que soy, no solo esta decisión. Renueva mi mente para "
                    "que reconozca lo bueno cuando lo vea.",
                ),
            },
            {
                "key": "decisions-4",
                "ref": "Proverbs 15:22",
                "title": L("Do not decide alone", "No decidas a solas"),
                "truth": L(
                    "The proverb is short and practical: plans made without advice tend to fail, and "
                    "plans made with many advisers tend to stand. God often answers a prayer for "
                    "wisdom through other people. Good counsel is not a vote among friends who will "
                    "tell you what you want to hear. It is the honest view of people who know you, who "
                    "know something about the matter, and who are free to disagree with you. Asking "
                    "for it takes humility, which is part of why it works.",
                    "El proverbio es breve y práctico: los planes hechos sin consejo suelen fracasar, "
                    "y los que cuentan con muchos consejeros suelen sostenerse. Muchas veces Dios "
                    "responde a la oración por sabiduría a través de otras personas. El buen consejo "
                    "no es una votación entre amigos que te dirán lo que quieres oír. Es la opinión "
                    "honesta de gente que te conoce, que sabe algo del asunto y que tiene libertad "
                    "para llevarte la contraria. Pedirlo exige humildad, y en parte por eso funciona.",
                ),
                "simple": L(
                    "Wise people ask for help before they decide. Grown-ups who love you can help you "
                    "see things you missed.",
                    "Las personas sabias piden ayuda antes de decidir. Los adultos que te quieren "
                    "pueden ayudarte a ver lo que se te pasó.",
                ),
                "ask": L(
                    "Who are two or three people who know you well and would tell you the truth? Have "
                    "you asked them, or only people who will agree?",
                    "¿Quiénes son dos o tres personas que te conocen bien y te dirían la verdad? ¿Les "
                    "has preguntado a ellas, o solo a quienes te darán la razón?",
                ),
                "kid_ask": L(
                    "Who do you ask when you need help deciding something?",
                    "¿A quién le preguntas cuando necesitas ayuda para decidir algo?",
                ),
                "do": L(
                    "This week, ask one wise person: what am I not seeing about this? Listen without "
                    "defending yourself, and write down what they say.",
                    "Esta semana pregúntale a una persona sabia: ¿qué no estoy viendo en esto? Escucha "
                    "sin defenderte y anota lo que te diga.",
                ),
                "kid_do": L(
                    "Ask a grown-up to tell you about a time they had to make a hard choice.",
                    "Pídele a un adulto que te cuente de alguna vez que tuvo que tomar una decisión difícil.",
                ),
                "pray": L(
                    "Lord, give me the humility to ask and the honesty to listen. Send me people who "
                    "will tell me the truth in love.",
                    "Señor, dame humildad para preguntar y honestidad para escuchar. Envíame personas "
                    "que me digan la verdad con amor.",
                ),
            },
            {
                "key": "decisions-5",
                "ref": "Psalm 32:8-9",
                "title": L("Then take the step", "Y luego da el paso"),
                "truth": L(
                    "God promises to teach you the way you should go and to counsel you with his eye "
                    "on you. Then comes a picture: do not be like a horse or mule that has no "
                    "understanding and must be steered with bit and bridle. God is not looking to yank "
                    "you from signal to signal. He wants to guide you as someone who understands, who "
                    "has learned his ways and can walk in them. So after you have asked, trusted and "
                    "listened, you are free to choose and move. His eye stays on you after the "
                    "decision as well as before it. A wrong turn does not put you beyond his care.",
                    "Dios promete enseñarte el camino que debes seguir y aconsejarte sin quitarte la "
                    "vista de encima. Luego viene una imagen: no seas como el caballo o la mula, que "
                    "no entienden y hay que dirigirlos con freno y rienda. Dios no busca moverte a "
                    "tirones, de señal en señal. Quiere guiarte como a alguien que entiende, que ha "
                    "aprendido sus caminos y puede andar en ellos. Así que después de pedir, confiar y "
                    "escuchar, tienes libertad para elegir y avanzar. Su mirada sigue sobre ti después "
                    "de la decisión igual que antes. Un giro equivocado no te deja fuera de su cuidado.",
                ),
                "simple": L(
                    "God promises to teach you the way to go and to keep his eyes on you. Even if you "
                    "make a mistake, he does not stop taking care of you.",
                    "Dios promete enseñarte el camino y tener siempre sus ojos sobre ti. Aunque te "
                    "equivoques, él no deja de cuidarte.",
                ),
                "ask": L(
                    "Are you waiting for a certainty God has not promised? What decision could you "
                    "make this week with the light you already have?",
                    "¿Estás esperando una certeza que Dios no ha prometido? ¿Qué decisión podrías "
                    "tomar esta semana con la luz que ya tienes?",
                ),
                "kid_ask": L(
                    "How does it feel to know God is always watching over you with love?",
                    "¿Cómo se siente saber que Dios siempre te cuida con amor?",
                ),
                "do": L(
                    "Set a date to decide. Before it, pray, think and ask counsel. On that day, "
                    "choose, tell someone, and take the first step without reopening the question "
                    "every hour.",
                    "Ponle fecha a tu decisión. Antes de ese día, ora, piensa y pide consejo. Ese día "
                    "elige, cuéntaselo a alguien y da el primer paso sin reabrir la pregunta a cada hora.",
                ),
                "kid_do": L(
                    "Make one small choice by yourself today, like which book to read, and thank God "
                    "for helping you learn to choose.",
                    "Toma hoy una decisión pequeña por tu cuenta, como qué libro leer, y dale gracias "
                    "a Dios por ayudarte a aprender a elegir.",
                ),
                "pray": L(
                    "God, I have asked and listened. Now I am going to choose. Keep your eye on me, "
                    "correct me if I am wrong, and go with me.",
                    "Dios, ya pedí y escuché. Ahora voy a elegir. No me quites la vista de encima, "
                    "corrígeme si me equivoco y ven conmigo.",
                ),
            },
        ],
    },
    {
        "key": "work",
        "category": "wisdom",
        "title": L("Work, study and calling", "Trabajo, estudio y vocación"),
        "summary": L(
            "For anyone with a job, a class load, a household to run, or no work right now. Five "
            "readings on why work is good, why it is hard, who it is for, and why your worth does not "
            "depend on it.",
            "Para quien tiene un empleo, una carga de estudios, una casa que sostener, o está sin "
            "trabajo ahora. Cinco lecturas sobre por qué el trabajo es bueno, por qué cuesta, para "
            "quién es y por qué tu valor no depende de él.",
        ),
        "keywords": [
            "work", "job", "career", "boss", "coworker", "unemploy", "laid off", "fired", "calling",
            "vocation", "homework", "exam", "trabaj", "empleo", "desemple", "despid", "jefe",
            "vocaci", "carrera", "estudi", "examen", "oficina",
        ],
        "situations": ["working", "job_seeking", "student", "retired", "parent", "leader"],
        "traits": ["faithfulness", "servanthood", "perseverance"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "School is your work right now, along with chores and maybe a first job. It matters "
                "to God more than you might think.",
                "Ahora tu trabajo es la escuela, junto con las tareas de casa y quizá un primer "
                "empleo. A Dios le importa más de lo que imaginas.",
            ),
            "young_adult": L(
                "For choosing a path, starting at the bottom, or wondering whether what you do all "
                "day means anything.",
                "Para elegir un camino, empezar desde abajo o preguntarte si lo que haces todo el día "
                "significa algo.",
            ),
            "adult": L(
                "For the long years of work, paid or unpaid, and for the seasons of too much of it or "
                "none at all.",
                "Para los largos años de trabajo, pagado o no, y para las épocas en que sobra o no hay.",
            ),
            "senior": L(
                "When paid work ends, the question of what you are for does not. There is still good "
                "work with your name on it.",
                "Cuando termina el trabajo pagado, no termina la pregunta de para qué estás aquí. "
                "Todavía hay un buen trabajo con tu nombre.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "work-1",
                "ref": "Genesis 2:15",
                "title": L("Work was there from the start", "El trabajo estuvo desde el principio"),
                "truth": L(
                    "Before anything had gone wrong in the world, God placed the first human in a "
                    "garden with a job: to work it and take care of it. So work is not a punishment or "
                    "a necessary evil. It is part of what people were made for. To tend something, to "
                    "bring order, to make things grow, to look after what has been entrusted to you: "
                    "this is to share in God's own care for his world. That is true of paid jobs, and "
                    "equally of study, raising children, caring for a parent and keeping a home.",
                    "Antes de que algo se torciera en el mundo, Dios puso al primer ser humano en un "
                    "huerto con un encargo: cultivarlo y cuidarlo. Así que el trabajo no es un castigo "
                    "ni un mal necesario. Es parte de aquello para lo que fuimos hechos. Atender algo, "
                    "poner orden, hacer crecer, cuidar lo que se te confió: eso es participar del "
                    "cuidado que Dios mismo tiene por su mundo. Vale para el empleo pagado, y lo mismo "
                    "para el estudio, la crianza, el cuidado de un padre o una madre y el sostén de un hogar.",
                ),
                "simple": L(
                    "God gave the first person a job: to take care of the garden. Helping and taking "
                    "care of things is something good that God made us to do.",
                    "Dios le dio un trabajo a la primera persona: cuidar el jardín. Ayudar y cuidar "
                    "las cosas es algo bueno para lo que Dios nos hizo.",
                ),
                "ask": L(
                    "What has been put in your care right now, at work, at school or at home? How "
                    "would you treat it if you saw it as given to you by God?",
                    "¿Qué se ha puesto a tu cuidado ahora, en el trabajo, la escuela o la casa? ¿Cómo "
                    "lo tratarías si lo vieras como algo que Dios te confió?",
                ),
                "kid_ask": L(
                    "What is something you take care of: a pet, a plant, your room?",
                    "¿Qué cosa cuidas tú: una mascota, una planta, tu cuarto?",
                ),
                "do": L(
                    "Choose one ordinary task today and do it as an act of care for something God has "
                    "entrusted to you. Notice whether that changes how it feels.",
                    "Elige hoy una tarea común y hazla como un acto de cuidado por algo que Dios te "
                    "confió. Fíjate si eso cambia cómo se siente.",
                ),
                "kid_do": L(
                    "Take care of one thing today without being asked: water a plant, feed a pet or "
                    "tidy a shelf.",
                    "Cuida hoy una cosa sin que te lo pidan: riega una planta, dale de comer a una "
                    "mascota u ordena un estante.",
                ),
                "pray": L(
                    "God, you made me to work and to take care of things. Help me see today's tasks as "
                    "something you have placed in my hands.",
                    "Dios, me hiciste para trabajar y cuidar. Ayúdame a ver las tareas de hoy como "
                    "algo que tú pusiste en mis manos.",
                ),
            },
            {
                "key": "work-2",
                "ref": "Genesis 3:17-19",
                "title": L("Why work is so hard", "Por qué el trabajo cuesta tanto"),
                "truth": L(
                    "After the first humans turn from God, the ground itself becomes difficult. Work "
                    "remains, but now it comes with thorns, sweat and frustration, and it ends in "
                    "dust. This is the Bible's honest account of why good work is so often exhausting, "
                    "unfair or fruitless. It means that a hard job is not proof you are in the wrong "
                    "place or that God is against you. Work is a good thing that has been damaged, "
                    "along with everything else. You can expect both in the same day: real meaning and "
                    "real thorns.",
                    "Después de que los primeros seres humanos se apartan de Dios, la tierra misma se "
                    "vuelve difícil. El trabajo sigue, pero ahora viene con espinas, sudor y "
                    "frustración, y termina en polvo. Así explica la Biblia, con honestidad, por qué "
                    "el buen trabajo tantas veces agota, es injusto o no da fruto. Significa que un "
                    "trabajo duro no prueba que estés en el lugar equivocado ni que Dios esté en tu "
                    "contra. El trabajo es algo bueno que quedó dañado, como todo lo demás. Puedes "
                    "esperar las dos cosas en un mismo día: sentido verdadero y espinas verdaderas.",
                ),
                "simple": L(
                    "Work is good, but sometimes it is hard and tiring, like pulling weeds. That is "
                    "normal. God is still with us when work is hard.",
                    "Trabajar es bueno, pero a veces cuesta y cansa, como arrancar hierbas malas. Eso "
                    "es normal. Dios sigue con nosotros cuando el trabajo es difícil.",
                ),
                "ask": L(
                    "What are the thorns in your work right now? Have you been reading them as a sign "
                    "that something is wrong with you?",
                    "¿Cuáles son las espinas de tu trabajo ahora? ¿Las has interpretado como señal de "
                    "que algo anda mal contigo?",
                ),
                "kid_ask": L(
                    "What job or schoolwork feels hard for you?",
                    "¿Qué tarea o trabajo de la escuela te parece difícil?",
                ),
                "do": L(
                    "Name one frustration at work or school that you cannot change and one that you "
                    "can. Hand the first to God in prayer; take one small action on the second.",
                    "Nombra una frustración del trabajo o la escuela que no puedes cambiar y una que "
                    "sí. Entrégale la primera a Dios en oración; da un paso pequeño con la segunda.",
                ),
                "kid_do": L(
                    "Finish one hard job today, even a small one, and tell a grown-up how it felt to finish.",
                    "Termina hoy una tarea difícil, aunque sea pequeña, y cuéntale a un adulto cómo se "
                    "sintió terminarla.",
                ),
                "pray": L(
                    "Lord, my work has thorns in it, and I am worn out. Help me not to be surprised or "
                    "bitter. Meet me in the sweat of today.",
                    "Señor, mi trabajo tiene espinas y me tiene sin fuerzas. Ayúdame a no sorprenderme "
                    "ni amargarme. Encuéntrame en el sudor de hoy.",
                ),
            },
            {
                "key": "work-3",
                "ref": "Colossians 3:23-24",
                "title": L("Who you are really working for", "Para quién trabajas en realidad"),
                "truth": L(
                    "Paul first wrote these words to household servants, people with little say over "
                    "their tasks and little recognition. He tells them to put their heart into "
                    "whatever they do, as work done for the Lord and not for human masters, because it "
                    "is Christ they are serving and he will not overlook it. That gives dignity to "
                    "work no one applauds: the night shift, the homework, the diapers, the "
                    "spreadsheet. It is not a reason to accept mistreatment. It is a reason to know "
                    "your work counts, even when no boss or teacher notices. Someone does.",
                    "Pablo escribió estas palabras primero a siervos de las casas, gente con poca voz "
                    "sobre sus tareas y poco reconocimiento. Les dice que pongan el corazón en todo lo "
                    "que hagan, como trabajo hecho para el Señor y no para amos humanos, porque es a "
                    "Cristo a quien sirven y él no lo pasará por alto. Eso dignifica el trabajo que "
                    "nadie aplaude: el turno de noche, la tarea escolar, los pañales, la hoja de "
                    "cálculo. No es razón para aceptar malos tratos. Es razón para saber que tu "
                    "trabajo cuenta, aunque ningún jefe o maestro lo note. Alguien sí lo nota.",
                ),
                "simple": L(
                    "When you do your work, you can do it for Jesus. He sees you even when no one else "
                    "does, and it makes him glad.",
                    "Cuando haces tu trabajo, puedes hacerlo para Jesús. Él te ve aunque nadie más te "
                    "vea, y eso lo alegra.",
                ),
                "ask": L(
                    "Which part of your work do you do only for the people watching? How would you do "
                    "it if Christ were the one receiving it?",
                    "¿Qué parte de tu trabajo haces solo para quienes te miran? ¿Cómo la harías si "
                    "fuera Cristo quien la recibe?",
                ),
                "kid_ask": L(
                    "What is a job you do that nobody sees?",
                    "¿Qué tarea haces tú que nadie ve?",
                ),
                "do": L(
                    "Pick the task you like least today. Before starting, say: Lord, this one is for "
                    "you. Then do it as well as you can.",
                    "Elige la tarea que menos te gusta hoy. Antes de empezar di: Señor, esta es para "
                    "ti. Luego hazla lo mejor que puedas.",
                ),
                "kid_do": L(
                    "Do your homework or a chore today as a gift for Jesus, as carefully as you can.",
                    "Haz hoy tu tarea o un quehacer como un regalo para Jesús, con todo el cuidado que puedas.",
                ),
                "pray": L(
                    "Lord Jesus, I work for you today, whoever else is watching or not watching. "
                    "Receive it, and help me do it well.",
                    "Señor Jesús, hoy trabajo para ti, me mire quien me mire o aunque nadie me mire. "
                    "Recíbelo y ayúdame a hacerlo bien.",
                ),
            },
            {
                "key": "work-4",
                "ref": "Luke 3:21-22",
                "title": L("Loved before the work begins", "Un amor que llega antes que el trabajo"),
                "truth": L(
                    "At his baptism, before his public work has begun, before any sermon, healing or "
                    "follower, Jesus hears the Father call him the beloved Son and say he is pleased "
                    "with him. The approval comes before the work. That order matters when you have no "
                    "work, or have lost it, or feel that what you do impresses no one. God's love for "
                    "you also comes first, as a gift, and is not earned by results. A job is something "
                    "you do. It was never meant to carry the weight of who you are.",
                    "En su bautismo, antes de comenzar su obra pública, antes de cualquier sermón, "
                    "sanidad o seguidor, Jesús oye al Padre llamarlo Hijo amado y decir que en él se "
                    "complace. La aprobación llega antes que el trabajo. Ese orden importa cuando no "
                    "tienes empleo, o lo perdiste, o sientes que lo que haces no impresiona a nadie. "
                    "El amor de Dios por ti también viene primero, como regalo, y no se gana con "
                    "resultados. Un empleo es algo que haces. Nunca fue hecho para cargar con el peso "
                    "de quién eres.",
                ),
                "simple": L(
                    "God told Jesus he loved him before Jesus started his big work. God loves you too, "
                    "not because of what you do, but because he made you.",
                    "Dios le dijo a Jesús que lo amaba antes de que Jesús empezara su gran trabajo. A "
                    "ti también te ama, no por lo que haces, sino porque él te hizo.",
                ),
                "ask": L(
                    "If your work or title were taken away tomorrow, what would you say you are? What "
                    "does God say?",
                    "Si mañana te quitaran tu trabajo o tu título, ¿qué dirías que eres? ¿Qué dice Dios?",
                ),
                "kid_ask": L(
                    "Does God love you more when you win or get a good grade? (No. He loves you all "
                    "the time.)",
                    "¿Dios te ama más cuando ganas o sacas buena nota? (No. Te ama todo el tiempo.)",
                ),
                "do": L(
                    "Tomorrow, before any work or job search, begin by saying: God loves me before I "
                    "do anything today. If you are out of work, tell one person honestly how you are "
                    "doing, and ask them to pray and to keep an ear open for you.",
                    "Mañana, antes de cualquier trabajo o búsqueda de empleo, empieza diciendo: Dios "
                    "me ama antes de que yo haga nada hoy. Si estás sin trabajo, dile a una persona "
                    "con honestidad cómo estás y pídele que ore y esté atenta por si sabe de algo.",
                ),
                "kid_do": L(
                    "Ask a grown-up to tell you three things they love about you that have nothing to "
                    "do with what you are good at.",
                    "Pídele a un adulto que te diga tres cosas que ama de ti que no tengan que ver con "
                    "lo que haces bien.",
                ),
                "pray": L(
                    "Father, I have measured myself by what I produce. Let me hear that I, too, am "
                    "loved by you. Let me work, or wait, from there.",
                    "Padre, me he medido por lo que produzco. Déjame oír que tú también me amas a mí. "
                    "Que desde ahí trabaje, o espere.",
                ),
            },
            {
                "key": "work-5",
                "ref": "Ephesians 2:8-10",
                "title": L("Calling is bigger than a job", "La vocación es más grande que un empleo"),
                "truth": L(
                    "Paul puts two things in careful order. First, we are saved by grace as a gift, "
                    "not by anything we have done, so no one can boast. Then: we are God's own "
                    "handiwork, made in Christ for good works that God prepared ahead of time for us "
                    "to walk in. Your calling, then, is not one perfect career you might miss. It is "
                    "the good that God has already placed along your path: in your job, but also in "
                    "your street, your family, your church and your interruptions. You can live your "
                    "calling in any honest work, and without paid work at all.",
                    "Pablo pone dos cosas en un orden cuidadoso. Primero: somos salvos por gracia, "
                    "como regalo, no por algo que hayamos hecho, así que nadie puede presumir. "
                    "Después: somos obra de las manos de Dios, creados en Cristo para buenas obras que "
                    "él preparó de antemano para que anduviéramos en ellas. Tu vocación, entonces, no "
                    "es una única carrera perfecta que podrías perderte. Es el bien que Dios ya puso a "
                    "lo largo de tu camino: en tu empleo, pero también en tu calle, tu familia, tu "
                    "iglesia y tus interrupciones. Puedes vivirla en cualquier trabajo honrado, y "
                    "también sin trabajo pagado.",
                ),
                "simple": L(
                    "God made you on purpose, and he has good things for you to do every day, like "
                    "helping, sharing and being kind.",
                    "Dios te hizo a propósito, y tiene cosas buenas para que hagas cada día, como "
                    "ayudar, compartir y tratar bien a los demás.",
                ),
                "ask": L(
                    "What good is sitting in your path this week, outside your job description, that "
                    "may have been prepared for you?",
                    "¿Qué bien está en tu camino esta semana, fuera de tus funciones, que quizá fue "
                    "preparado para ti?",
                ),
                "kid_ask": L(
                    "What good thing could you do today that would help someone?",
                    "¿Qué cosa buena podrías hacer hoy para ayudar a alguien?",
                ),
                "do": L(
                    "Each morning this week, ask God what good he has prepared for you that day. Each "
                    "evening, write down one thing that might have been the answer.",
                    "Cada mañana de esta semana pregúntale a Dios qué bien preparó para ti ese día. "
                    "Cada noche anota una cosa que pudo haber sido la respuesta.",
                ),
                "kid_do": L(
                    "Look for one good thing to do today that nobody asked you to do, and do it.",
                    "Busca hoy una cosa buena que nadie te haya pedido, y hazla.",
                ),
                "pray": L(
                    "God, you made me, and you have prepared good for me to do. Open my eyes to it "
                    "today, and keep me from thinking I must earn your love by doing it.",
                    "Dios, tú me hiciste y preparaste un bien para que yo lo haga. Ábreme los ojos "
                    "para verlo hoy, y líbrame de pensar que con eso tengo que ganarme tu amor.",
                ),
            },
        ],
    },
    {
        "key": "money",
        "category": "wisdom",
        "title": L("Money, debt and enough", "Dinero, deudas y lo suficiente"),
        "summary": L(
            "For when money is tight, when it is plentiful, or when it takes up more of your mind "
            "than you want. Five readings on where your heart is, what is enough, the weight of debt, "
            "and the freedom of giving.",
            "Para cuando el dinero escasea, cuando abunda o cuando ocupa más espacio en tu mente del "
            "que quisieras. Cinco lecturas sobre dónde está tu corazón, qué es suficiente, el peso de "
            "las deudas y la libertad de dar.",
        ),
        "keywords": [
            "money", "debt", "bills", "afford", "budget", "salary", "paycheck", "loan", "financ",
            "spending", "greed", "dinero", "deuda", "sueldo", "gasto", "presupuesto", "ahorr",
            "préstamo", "no me alcanza", "pagar la renta", "codicia",
        ],
        "situations": ["working", "job_seeking", "parent", "single_parent", "married", "retired", "student"],
        "traits": ["contentment", "generosity", "trust"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "Your first money, and the pull to have what others have. The habits you form now "
                "with small amounts will follow you.",
                "Tu primer dinero, y las ganas de tener lo que otros tienen. Los hábitos que formes "
                "ahora con cantidades pequeñas te acompañarán.",
            ),
            "young_adult": L(
                "Loans, rent, first salary, comparison. Here is a way to think about money before it "
                "starts thinking for you.",
                "Préstamos, renta, primer sueldo, comparación. Aquí hay una manera de pensar en el "
                "dinero antes de que él empiece a pensar por ti.",
            ),
            "adult": L(
                "For bills, debt, providing for others, and the question of how much is enough when "
                "there never seems to be quite enough.",
                "Para las cuentas, las deudas, el sostén de otros y la pregunta de cuánto es "
                "suficiente cuando nunca parece alcanzar.",
            ),
            "senior": L(
                "For living on a fixed income, fearing it will run out, and deciding what to give and "
                "what to leave behind.",
                "Para vivir con un ingreso fijo, temer que no alcance y decidir qué dar y qué dejar.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "money-1",
                "ref": "Matthew 6:19-21",
                "title": L("Where your heart follows", "A dónde va tu corazón"),
                "truth": L(
                    "Jesus does not say money is evil. He says that things stored up on earth do not "
                    "last: they wear out, lose value or get taken. And he states a law of the heart: "
                    "wherever you put your treasure, your heart goes after it. That works in both "
                    "directions. What you spend on shows what you love, and what you choose to invest "
                    "in, you will come to love. So he urges a kind of treasure that cannot be lost: "
                    "what is given to God and done for others.",
                    "Jesús no dice que el dinero sea malo. Dice que lo que se acumula en la tierra no "
                    "dura: se desgasta, pierde valor o se lo llevan. Y enuncia una ley del corazón: "
                    "donde pongas tu tesoro, allá irá tu corazón. Funciona en los dos sentidos. En qué "
                    "gastas muestra lo que amas, y aquello en lo que decides invertir, llegarás a "
                    "amarlo. Por eso anima a buscar un tesoro que no se puede perder: lo que se "
                    "entrega a Dios y se hace por los demás.",
                ),
                "simple": L(
                    "Toys and things can break or get lost. Love for God and for people lasts forever. "
                    "That is the best treasure.",
                    "Los juguetes y las cosas se rompen o se pierden. El amor a Dios y a las personas "
                    "dura para siempre. Ese es el mejor tesoro.",
                ),
                "ask": L(
                    "If someone read only your last month of spending, what would they say you "
                    "treasure? Is it what you would say?",
                    "Si alguien leyera solo tus gastos del último mes, ¿qué diría que atesoras? ¿Es lo "
                    "mismo que dirías tú?",
                ),
                "kid_ask": L(
                    "What is your favorite thing you own? What do you love that is not a thing?",
                    "¿Cuál es tu cosa favorita? ¿Qué amas que no sea una cosa?",
                ),
                "do": L(
                    "Look over your last month of spending. Mark one item that reflects what you love "
                    "and one you would like to change. Change that one this month.",
                    "Revisa tus gastos del último mes. Marca uno que refleje lo que amas y uno que te "
                    "gustaría cambiar. Cambia ese este mes.",
                ),
                "kid_do": L(
                    "Share one of your toys or treats with someone today.",
                    "Comparte hoy uno de tus juguetes o dulces con alguien.",
                ),
                "pray": L(
                    "Jesus, my heart goes where my money goes. Show me honestly where that is, and "
                    "teach me to treasure what lasts.",
                    "Jesús, mi corazón va a donde va mi dinero. Muéstrame con honestidad dónde está, y "
                    "enséñame a atesorar lo que perdura.",
                ),
            },
            {
                "key": "money-2",
                "ref": "1 Timothy 6:6-10",
                "title": L("The trap of wanting more", "La trampa de querer más"),
                "truth": L(
                    "Paul says that devotion to God together with contentment is great gain, and he "
                    "grounds it in a plain fact: we brought nothing into the world and will take "
                    "nothing out. With food and clothing, he says, we can be content. Then comes a "
                    "warning, not against having money but against the craving to be rich. That "
                    "craving is a trap that has pulled many people into ruin and left them full of "
                    "grief. Notice exactly what he says: it is the love of money, not money, that is a "
                    "root of all kinds of evil.",
                    "Pablo dice que la devoción a Dios acompañada de contentamiento es una gran "
                    "ganancia, y lo apoya en un hecho sencillo: nada trajimos al mundo y nada nos "
                    "llevaremos. Teniendo alimento y abrigo, dice, podemos estar contentos. Luego "
                    "viene una advertencia, no contra tener dinero sino contra el afán de hacerse "
                    "rico. Ese afán es una trampa que ha arrastrado a muchos a la ruina y los ha "
                    "llenado de dolores. Fíjate en lo que dice exactamente: es el amor al dinero, no "
                    "el dinero, la raíz de toda clase de males.",
                ),
                "simple": L(
                    "We came into the world with nothing, and everything we have is a gift. Always "
                    "wanting more makes us unhappy. Being thankful makes us glad.",
                    "Llegamos al mundo sin nada, y todo lo que tenemos es un regalo. Querer siempre "
                    "más nos hace infelices. Dar gracias nos alegra.",
                ),
                "ask": L(
                    "What is the thing you believe would finally make you feel you had enough? How "
                    "long has that target been moving?",
                    "¿Qué es eso que crees que por fin te haría sentir que tienes suficiente? ¿Desde "
                    "cuándo se viene moviendo esa meta?",
                ),
                "kid_ask": L(
                    "What is something you already have that you are thankful for?",
                    "¿Qué cosa que ya tienes agradeces?",
                ),
                "do": L(
                    "For one week, each time you want to buy something you had not planned, wait a day "
                    "first. Note how many of those wants are still there.",
                    "Durante una semana, cada vez que quieras comprar algo que no habías planeado, "
                    "espera un día. Anota cuántos de esos deseos siguen ahí.",
                ),
                "kid_do": L(
                    "Name five things you have, and say thank you to God for each one.",
                    "Nombra cinco cosas que tienes y dale gracias a Dios por cada una.",
                ),
                "pray": L(
                    "God, I came with nothing and I will leave with nothing. Free me from the craving "
                    "for more, and teach me to be content with what you have given today.",
                    "Dios, llegué sin nada y me iré sin nada. Líbrame del afán de tener más y enséñame "
                    "a contentarme con lo que me has dado hoy.",
                ),
            },
            {
                "key": "money-3",
                "ref": "Proverbs 30:7-9",
                "title": L("The prayer for enough", "La oración por lo suficiente"),
                "truth": L(
                    "This is one of the most honest prayers about money in the Bible. The writer asks "
                    "for two things: to be kept from lies, and to be given neither poverty nor riches, "
                    "only the food he needs. He knows himself. With too much, he might forget God and "
                    "feel he needs no one. With too little, he might steal and dishonor God. Scripture "
                    "does not pretend poverty is holy or harmless; it is a real danger, as wealth is. "
                    "The wise request is for enough, and for a heart that knows when it has it.",
                    "Esta es una de las oraciones más honestas sobre el dinero en la Biblia. El autor "
                    "pide dos cosas: que lo aleje de la mentira, y que no le dé pobreza ni riqueza, "
                    "solo el pan que necesita. Se conoce bien. Con demasiado, podría olvidarse de Dios "
                    "y sentir que no necesita a nadie. Con muy poco, podría robar y deshonrar a Dios. "
                    "La Escritura no finge que la pobreza sea santa o inofensiva; es un peligro real, "
                    "igual que la riqueza. La petición sabia es tener lo suficiente, y un corazón que "
                    "sepa reconocerlo.",
                ),
                "simple": L(
                    "A wise man prayed: God, please give me just what I need, not too much and not too "
                    "little. We can ask God for what we need each day.",
                    "Un hombre sabio oró: Dios, dame solo lo que necesito, ni demasiado ni muy poco. "
                    "Podemos pedirle a Dios lo que necesitamos cada día.",
                ),
                "ask": L(
                    "Have you ever defined enough for yourself, as a number or as a way of living? "
                    "What would it be?",
                    "¿Alguna vez has definido qué es suficiente para ti, en una cifra o en una forma "
                    "de vivir? ¿Cuál sería?",
                ),
                "kid_ask": L(
                    "What are things you really need? What are things you just want?",
                    "¿Qué cosas necesitas de verdad? ¿Qué cosas solo quieres?",
                ),
                "do": L(
                    "Write down what enough would look like for your household this year. If you do "
                    "not have enough right now, tell someone you trust, such as a pastor or a local "
                    "aid organization. Asking for help is not a failure.",
                    "Escribe cómo se vería lo suficiente para tu hogar este año. Si ahora mismo no te "
                    "alcanza, cuéntaselo a alguien de confianza, como un pastor o una organización de "
                    "ayuda local. Pedir ayuda no es un fracaso.",
                ),
                "kid_do": L(
                    "With a grown-up, make two short lists: things we need and things we want.",
                    "Con un adulto, haz dos listas cortas: cosas que necesitamos y cosas que queremos.",
                ),
                "pray": L(
                    "God, give me neither too much nor too little. Give me today's bread, and a heart "
                    "that recognizes enough.",
                    "Dios, no me des ni demasiado ni muy poco. Dame el pan de hoy y un corazón que "
                    "sepa reconocer lo suficiente.",
                ),
            },
            {
                "key": "money-4",
                "ref": "Proverbs 22:7",
                "title": L("The weight of debt", "El peso de las deudas"),
                "truth": L(
                    "This proverb does not scold; it describes. The one who borrows becomes a servant "
                    "to the one who lends. Anyone in debt knows the feeling: decisions made for you, a "
                    "future already spent, a weight that wakes you at night. Scripture names that "
                    "weight honestly, so you do not have to pretend it is not there. Debt has many "
                    "causes, and some are not your fault. It is a kind of bondage all the same, and it "
                    "is good to want out. The way out nearly always begins by looking at the whole "
                    "truth of it, with someone beside you.",
                    "Este proverbio no regaña; describe. Quien pide prestado se vuelve siervo de quien "
                    "le presta. Cualquiera con deudas conoce la sensación: decisiones que ya tomaron "
                    "por ti, un futuro ya gastado, un peso que te despierta de noche. La Escritura "
                    "nombra ese peso con honestidad, así que no tienes que fingir que no existe. Las "
                    "deudas tienen muchas causas, y algunas no son culpa tuya. Con todo, son una forma "
                    "de atadura, y es bueno querer salir. La salida casi siempre empieza por mirar "
                    "toda la verdad de frente, con alguien a tu lado.",
                ),
                "simple": L(
                    "When we borrow something, we have to give it back. It is wise to be careful about "
                    "borrowing and to return what we borrow.",
                    "Cuando pedimos algo prestado, hay que devolverlo. Es sabio tener cuidado al pedir "
                    "prestado y devolver lo que nos prestan.",
                ),
                "ask": L(
                    "Do you know the exact total of what you owe? What feeling has kept you from looking?",
                    "¿Sabes el total exacto de lo que debes? ¿Qué sentimiento te ha impedido mirarlo?",
                ),
                "kid_ask": L(
                    "Have you ever borrowed something? How did you take care of it?",
                    "¿Alguna vez pediste algo prestado? ¿Cómo lo cuidaste?",
                ),
                "do": L(
                    "Write every debt on one page: who, how much, what interest. Then show the page to "
                    "one trustworthy person, such as a wise friend or a nonprofit credit counselor, "
                    "and make a first plan together.",
                    "Escribe todas tus deudas en una hoja: a quién, cuánto, con qué interés. Luego "
                    "muéstrasela a una persona confiable, como un amigo sensato o un asesor financiero "
                    "sin fines de lucro, y hagan juntos un primer plan.",
                ),
                "kid_do": L(
                    "If you have borrowed something from someone, give it back today and say thank you.",
                    "Si le pediste algo prestado a alguien, devuélveselo hoy y dale las gracias.",
                ),
                "pray": L(
                    "Lord, this debt weighs on me, and I have been afraid to look at it. Give me "
                    "courage to face the numbers, help to make a plan, and peace while I work my way out.",
                    "Señor, esta deuda me pesa y he tenido miedo de mirarla. Dame valor para enfrentar "
                    "los números, ayuda para hacer un plan y paz mientras voy saliendo.",
                ),
            },
            {
                "key": "money-5",
                "ref": "Mark 12:41-44",
                "title": L("How Jesus counts a gift", "Cómo cuenta Jesús una ofrenda"),
                "truth": L(
                    "Jesus sits and watches people give at the temple. The wealthy put in large sums. "
                    "A poor widow puts in two tiny coins, worth almost nothing. Jesus calls his "
                    "disciples over to say that she gave more than all of them, because they gave out "
                    "of their surplus and she gave out of her need. He measures a gift by what it "
                    "costs the giver, not by its size. That means generosity is open to everyone. No "
                    "gift is too small to count, and none given in love goes unseen.",
                    "Jesús se sienta y observa a la gente dar en el templo. Los ricos echan grandes "
                    "sumas. Una viuda pobre echa dos moneditas que casi no valen nada. Jesús llama a "
                    "sus discípulos para decirles que ella dio más que todos, porque ellos dieron de "
                    "lo que les sobraba y ella dio desde su necesidad. Él mide un regalo por lo que le "
                    "cuesta a quien lo da, no por su tamaño. Eso significa que la generosidad está "
                    "abierta a todos. Ningún regalo es tan pequeño que no cuente, y ninguno dado con "
                    "amor pasa inadvertido.",
                ),
                "simple": L(
                    "A woman gave two tiny coins, and Jesus said it was a big gift, because it was all "
                    "she had. Even a small gift matters to God.",
                    "Una mujer dio dos moneditas, y Jesús dijo que era un regalo grande, porque era "
                    "todo lo que tenía. Hasta un regalo pequeño le importa a Dios.",
                ),
                "ask": L(
                    "When did you last give in a way you actually felt? What holds you back: fear of "
                    "not having enough, or something else?",
                    "¿Cuándo fue la última vez que diste de una manera que de verdad sentiste? ¿Qué te "
                    "frena: el miedo a que no te alcance, u otra cosa?",
                ),
                "kid_ask": L(
                    "What is something small you could give to make someone happy?",
                    "¿Qué cosa pequeña podrías dar para alegrar a alguien?",
                ),
                "do": L(
                    "Give something this week that you will notice: money, a meal, an afternoon. "
                    "Choose an amount that fits what you have, give it quietly, and do not mention it "
                    "to anyone.",
                    "Esta semana da algo que se note en tu bolsillo o en tu agenda: dinero, una "
                    "comida, una tarde. Elige una cantidad acorde con lo que tienes, dalo en silencio "
                    "y no se lo menciones a nadie.",
                ),
                "kid_do": L(
                    "Give something of yours away today: a coin, a toy, or a drawing you make for someone.",
                    "Regala hoy algo tuyo: una moneda, un juguete o un dibujo que hagas para alguien.",
                ),
                "pray": L(
                    "Jesus, you see what I give and what I hold back, and why. Loosen my grip. Give me "
                    "a generous heart with whatever I have.",
                    "Jesús, tú ves lo que doy y lo que me guardo, y por qué. Afloja mi puño. Dame un "
                    "corazón generoso con lo que tenga.",
                ),
            },
        ],
    },
    {
        "key": "words",
        "category": "wisdom",
        "title": L("Words: what we say and post", "Palabras: lo que decimos y publicamos"),
        "summary": L(
            "For anyone who has said something they regret, passed on what was not theirs to share, "
            "or wants their words to do more good. Four readings on where words come from and how to "
            "use them to heal.",
            "Para quien ha dicho algo de lo que se arrepiente, ha contado lo que no le tocaba contar, "
            "o quiere que sus palabras hagan más bien. Cuatro lecturas sobre de dónde salen las "
            "palabras y cómo usarlas para sanar.",
        ),
        "keywords": [
            "words", "gossip", "lied", "lying", "rumor", "insult", "complain", "posted", "tongue",
            "said something", "sarcas", "palabra", "chisme", "mentir", "mentira", "mentí", "quej",
            "grosería", "lengua", "publiqu", "dije algo",
        ],
        "situations": ["student", "parent", "married", "working", "leader"],
        "traits": ["honesty", "kindness", "self_control"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Words can help or hurt. God helps you use kind and true words, even when you are upset.",
                "Las palabras pueden ayudar o lastimar. Dios te ayuda a usar palabras amables y "
                "verdaderas, aun cuando algo te molesta.",
            ),
            "teen": L(
                "For group chats, comments, rumors and the things said at home in anger. Your words "
                "carry more weight than you think.",
                "Para los chats de grupo, los comentarios, los rumores y lo que se dice en casa con "
                "enojo. Tus palabras pesan más de lo que crees.",
            ),
            "young_adult": L(
                "For what you post, how you talk about people who are not in the room, and learning "
                "to tell the truth kindly.",
                "Para lo que publicas, cómo hablas de quienes no están presentes y aprender a decir "
                "la verdad con bondad.",
            ),
            "adult": L(
                "Your words shape your home and your workplace every day. Here is how to make them a "
                "source of life.",
                "Tus palabras dan forma a tu hogar y a tu trabajo cada día. Aquí verás cómo hacer de "
                "ellas una fuente de vida.",
            ),
            "senior": L(
                "A lifetime gives your words weight. Use them to bless, to tell the truth gently, and "
                "to say what should not be left unsaid.",
                "Toda una vida les da peso a tus palabras. Úsalas para bendecir, para decir la verdad "
                "con suavidad y para decir lo que no debe quedarse sin decir.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "words-1",
                "ref": "Luke 6:43-45",
                "title": L("Words come from somewhere", "Las palabras salen de algún lugar"),
                "truth": L(
                    "Jesus uses a picture anyone can check: a tree is known by its fruit. Then he "
                    "applies it to speech. What comes out of the mouth is the overflow of what fills "
                    "the heart. So when a harsh, false or belittling word slips out, the honest "
                    "response is not only to say you did not mean it. It is to ask what is stored up "
                    "inside: resentment, fear, envy, tiredness. This is hopeful. You cannot fix your "
                    "speech merely by biting your tongue, but God can change a heart, and new words follow.",
                    "Jesús usa una imagen que cualquiera puede comprobar: al árbol se le conoce por su "
                    "fruto. Luego la aplica al hablar. Lo que sale de la boca es lo que rebosa del "
                    "corazón. Así que cuando se te escapa una palabra dura, falsa o humillante, la "
                    "respuesta honesta no es solo decir que no fue tu intención. Es preguntarte qué "
                    "hay guardado adentro: resentimiento, miedo, envidia, cansancio. Esto da "
                    "esperanza. No arreglas tu manera de hablar solo mordiéndote la lengua, pero Dios "
                    "puede cambiar un corazón, y las palabras nuevas vienen después.",
                ),
                "simple": L(
                    "Good trees grow good fruit. When our hearts are full of love, kind words come "
                    "out. God helps fill our hearts with good things.",
                    "Los árboles buenos dan fruta buena. Cuando nuestro corazón está lleno de amor, "
                    "salen palabras amables. Dios ayuda a llenar nuestro corazón de cosas buenas.",
                ),
                "ask": L(
                    "Think of something you said recently that you regret. What was your heart full of "
                    "at that moment?",
                    "Piensa en algo que dijiste hace poco y lamentas. ¿De qué estaba lleno tu corazón "
                    "en ese momento?",
                ),
                "kid_ask": L(
                    "What kind words did you say today? Were there any words you wish you could take back?",
                    "¿Qué palabras amables dijiste hoy? ¿Hubo alguna que quisieras no haber dicho?",
                ),
                "do": L(
                    "For one day, notice your words without judging them: the tone of your messages, "
                    "your first words to the people you live with. At night, ask what they show about "
                    "your heart.",
                    "Durante un día, observa tus palabras sin juzgarlas: el tono de tus mensajes, lo "
                    "primero que les dices a quienes viven contigo. Por la noche, pregúntate qué "
                    "muestran de tu corazón.",
                ),
                "kid_do": L(
                    "Say three kind things to three different people today.",
                    "Dile hoy tres cosas amables a tres personas distintas.",
                ),
                "pray": L(
                    "Lord, my words show what is in me. Fill my heart with what is good, so that what "
                    "overflows gives life.",
                    "Señor, mis palabras muestran lo que hay en mí. Llena mi corazón de lo bueno, para "
                    "que lo que rebose dé vida.",
                ),
            },
            {
                "key": "words-2",
                "ref": "Proverbs 12:17-19",
                "title": L("True words, healing words", "Palabras verdaderas, palabras que sanan"),
                "truth": L(
                    "These three proverbs set two kinds of speech side by side. There are words that "
                    "tell the truth and words that deceive. There are reckless words that stab like a "
                    "sword, and wise words that bring healing. And there is a difference in how long "
                    "they last: truth endures, while a lie holds up only for a moment. Honesty and "
                    "kindness belong together here. Truth told without care can wound, and a kind word "
                    "that is false does not last. The aim is words that are both true and healing.",
                    "Estos tres proverbios ponen lado a lado dos clases de palabras. Hay palabras que "
                    "dicen la verdad y palabras que engañan. Hay palabras imprudentes que hieren como "
                    "espada, y palabras sabias que traen sanidad. Y hay una diferencia en cuánto "
                    "duran: la verdad permanece, mientras que la mentira se sostiene solo un instante. "
                    "Aquí la honestidad y la bondad van juntas. La verdad dicha sin cuidado puede "
                    "herir, y una palabra amable pero falsa no dura. La meta son palabras a la vez "
                    "verdaderas y sanadoras.",
                ),
                "simple": L(
                    "True words last. Lies fall apart. And kind words can help someone feel better, "
                    "like a bandage on a scrape.",
                    "Las palabras verdaderas duran. Las mentiras se deshacen. Y las palabras amables "
                    "ayudan a que alguien se sienta mejor, como una curita en un raspón.",
                ),
                "ask": L(
                    "Where are you tempted to shade the truth: to look better, to avoid conflict, to "
                    "spare yourself? What would the true and kind sentence be?",
                    "¿Dónde te tienta maquillar la verdad: para quedar mejor, evitar un conflicto o "
                    "ahorrarte un mal rato? ¿Cuál sería la frase verdadera y amable?",
                ),
                "kid_ask": L(
                    "Why is it sometimes hard to tell the truth?",
                    "¿Por qué a veces cuesta decir la verdad?",
                ),
                "do": L(
                    "This week, correct one thing you exaggerated, hid or left misleading. Go back to "
                    "the person and tell them the plain truth.",
                    "Esta semana corrige una cosa que exageraste, escondiste o dejaste a medias. "
                    "Vuelve con la persona y dile la verdad sencilla.",
                ),
                "kid_do": L(
                    "If you told a fib, tell the truth to a grown-up today. It is brave, and they will "
                    "be glad you did.",
                    "Si dijiste una mentirita, dile hoy la verdad a un adulto. Es de valientes, y le "
                    "va a dar gusto que lo hagas.",
                ),
                "pray": L(
                    "God of truth, I have bent the truth to protect myself. Make me honest, and make "
                    "my honesty gentle.",
                    "Dios de verdad, he torcido la verdad para protegerme. Dame honestidad, y que mi "
                    "honestidad sea amable.",
                ),
            },
            {
                "key": "words-3",
                "ref": "Proverbs 26:20-22",
                "title": L("The fire needs wood", "El fuego necesita leña"),
                "truth": L(
                    "A fire dies when no one adds wood, and a quarrel dies when no one passes it "
                    "along. That is how this proverb describes gossip: it is fuel. It also admits why "
                    "gossip is hard to resist. Whispered words about someone else are like tasty bites "
                    "that go down deep; they are enjoyable, they stay in us, and they change how we "
                    "see the person. The good news in the picture is how simple the remedy is. You do "
                    "not have to put out the fire. You only have to stop carrying wood, in person and "
                    "online.",
                    "El fuego se apaga cuando nadie le echa leña, y un pleito se apaga cuando nadie lo "
                    "sigue contando. Así describe este proverbio el chisme: es combustible. También "
                    "admite por qué cuesta resistirlo. Las palabras dichas en voz baja sobre otra "
                    "persona son como bocados sabrosos que llegan hasta lo más hondo; se disfrutan, se "
                    "nos quedan adentro y cambian cómo vemos a esa persona. Lo bueno de la imagen es "
                    "lo sencillo del remedio. No tienes que apagar el incendio. Solo tienes que dejar "
                    "de llevar leña, en persona y en línea.",
                ),
                "simple": L(
                    "Telling stories about other people is like putting wood on a fire. It makes "
                    "fights bigger. If we stop, the fire goes out.",
                    "Contar cosas de otras personas es como echarle leña al fuego. Hace más grandes "
                    "los pleitos. Si dejamos de hacerlo, el fuego se apaga.",
                ),
                "ask": L(
                    "What do you get from passing on a story about someone: belonging, importance, "
                    "relief? Where could you get that honestly instead?",
                    "¿Qué obtienes al contar algo de otra persona: pertenecer, sentirte importante, "
                    "desahogarte? ¿Dónde podrías obtenerlo de manera honesta?",
                ),
                "kid_ask": L(
                    "How would you feel if friends were whispering about you?",
                    "¿Cómo te sentirías si tus amigos hablaran de ti en secreto?",
                ),
                "do": L(
                    "This week, let one story end with you. When you are about to share, forward or "
                    "repost something about a person, ask: is it true, is it mine to tell, will it "
                    "help? If not, leave it.",
                    "Esta semana deja que un chisme termine contigo. Cuando estés por contar, reenviar "
                    "o compartir algo sobre una persona, pregúntate: ¿es verdad?, ¿me toca a mí "
                    "contarlo?, ¿va a ayudar? Si no, déjalo ahí.",
                ),
                "kid_do": L(
                    "If someone starts telling you something unkind about a friend today, say: I do "
                    "not want to talk about them. Let us play.",
                    "Si hoy alguien empieza a contarte algo feo de un amigo, di: no quiero hablar de "
                    "él. Mejor vamos a jugar.",
                ),
                "pray": L(
                    "Lord, I like the taste of a story about someone else. Forgive me. Make me the "
                    "place where the fire runs out of wood.",
                    "Señor, me gusta el sabor de un chisme. Perdóname. Hazme el lugar donde al fuego "
                    "se le acaba la leña.",
                ),
            },
            {
                "key": "words-4",
                "ref": "Ephesians 4:29",
                "title": L("Words that build", "Palabras que construyen"),
                "truth": L(
                    "Paul gives a filter with three parts. Let nothing rotten come out of your mouth, "
                    "only what is good for building others up, what fits the need of the moment, and "
                    "what gives grace to those who hear. The test is not only whether something is "
                    "true or whether you have the right to say it. It is what your words will do in "
                    "the person who receives them. This applies to every channel: the dinner table, "
                    "the meeting, the comment box, the message sent at midnight. Every one of them "
                    "reaches a real person.",
                    "Pablo da un filtro de tres partes. Que no salga de tu boca nada podrido, sino "
                    "solo lo que sirva para edificar a otros, lo que responda a la necesidad del "
                    "momento y lo que dé gracia a quienes escuchan. La prueba no es solo si algo es "
                    "verdad o si tienes derecho a decirlo. Es qué harán tus palabras en la persona que "
                    "las recibe. Vale para todos los canales: la mesa de la cena, la reunión, la caja "
                    "de comentarios, el mensaje enviado a medianoche. Cada uno llega a una persona real.",
                ),
                "simple": L(
                    "Our words can be like building blocks. God wants us to use words that build "
                    "people up, not knock them down.",
                    "Nuestras palabras pueden ser como bloques para construir. Dios quiere que usemos "
                    "palabras que levanten a las personas, no que las derriben.",
                ),
                "ask": L(
                    "Who in your life most needs a building-up word from you right now, and what "
                    "specifically could you say?",
                    "¿Quién en tu vida necesita más de ti una palabra de ánimo ahora mismo, y qué "
                    "podrías decirle exactamente?",
                ),
                "kid_ask": L(
                    "Who could you cheer up with kind words today?",
                    "¿A quién podrías animar hoy con palabras amables?",
                ),
                "do": L(
                    "Today, before you post, send or say anything sharp, run it through three "
                    "questions: does it build, does it fit, does it give grace? Then send one message "
                    "of specific encouragement to someone.",
                    "Hoy, antes de publicar, enviar o decir algo cortante, pásalo por tres preguntas: "
                    "¿edifica?, ¿viene al caso?, ¿da gracia? Luego envíale a alguien un mensaje de "
                    "ánimo concreto.",
                ),
                "kid_do": L(
                    "Write or draw a kind note for someone and give it to them.",
                    "Escribe o dibuja una notita amable para alguien y dásela.",
                ),
                "pray": L(
                    "God, watch over my mouth and my thumbs. Let what I say and send today build "
                    "someone up and give them grace.",
                    "Dios, cuida mi boca y mis pulgares. Que lo que hoy diga y envíe levante a alguien "
                    "y le dé gracia.",
                ),
            },
        ],
    },
    {
        "key": "priorities",
        "category": "wisdom",
        "title": L("Priorities: time and what matters", "Prioridades: el tiempo y lo que importa"),
        "summary": L(
            "For full calendars and the feeling that the important things keep getting pushed to "
            "later. Four readings on what matters most, how Jesus handled demands on his time, and "
            "how to count your days.",
            "Para agendas llenas y la sensación de que lo importante siempre queda para después. "
            "Cuatro lecturas sobre lo que más importa, cómo manejó Jesús las exigencias sobre su "
            "tiempo y cómo contar tus días.",
        ),
        "keywords": [
            "busy", "priorit", "schedule", "rushed", "hurry", "overcommit", "distract", "balance",
            "calendar", "no time", "too much to do", "ocupad", "prisa", "agenda", "distra",
            "ajetre", "equilibrio", "no tengo tiempo", "no me da tiempo", "pendientes",
        ],
        "situations": ["working", "parent", "single_parent", "student", "leader", "caregiver"],
        "traits": ["wisdom", "peace", "prayerfulness"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "School, activities, friends, your phone. Learning now what to say yes to will serve "
                "you for life.",
                "Escuela, actividades, amigos, el teléfono. Aprender desde ahora a qué decir que sí "
                "te servirá toda la vida.",
            ),
            "young_adult": L(
                "Everything seems possible and urgent at once. Here is help choosing what to build "
                "your days around.",
                "Todo parece posible y urgente a la vez. Aquí hay ayuda para elegir alrededor de qué "
                "construir tus días.",
            ),
            "adult": L(
                "For the years when everyone needs something from you, and the things you care about "
                "most get what is left over.",
                "Para los años en que todos necesitan algo de ti y lo que más te importa recibe lo "
                "que sobra.",
            ),
            "senior": L(
                "With more of life behind than ahead, the question sharpens: what is worth the days "
                "you have been given?",
                "Con más vida detrás que delante, la pregunta se afila: ¿qué merece los días que se "
                "te han dado?",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "priorities-1",
                "ref": "Mark 12:28-31",
                "title": L("What matters most", "Lo que más importa"),
                "truth": L(
                    "A teacher of the law asks Jesus which commandment is the most important of all. "
                    "Out of all the commandments, Jesus names two, and both are about love. Love God "
                    "with everything you are: heart, soul, mind and strength. And love your neighbor "
                    "as yourself. This is Jesus' own answer to the question of priorities. It does not "
                    "tell you exactly how to fill your week, but it gives the test for every week: did "
                    "the way I spent my time serve love for God and love for the people near me?",
                    "Un maestro de la ley le pregunta a Jesús cuál es el mandamiento más importante de "
                    "todos. De entre todos los mandamientos, Jesús nombra dos, y los dos tratan del "
                    "amor. Ama a Dios con todo lo que eres: corazón, alma, mente y fuerzas. Y ama a tu "
                    "prójimo como a ti mismo. Esta es la respuesta del propio Jesús a la pregunta de "
                    "las prioridades. No te dice exactamente cómo llenar tu semana, pero da la prueba "
                    "para cada semana: ¿la manera en que usé mi tiempo sirvió al amor a Dios y al amor "
                    "a las personas que tengo cerca?",
                ),
                "simple": L(
                    "Jesus said the two most important things are to love God and to love other "
                    "people. Everything else comes after that.",
                    "Jesús dijo que las dos cosas más importantes son amar a Dios y amar a las demás "
                    "personas. Todo lo demás viene después.",
                ),
                "ask": L(
                    "Looking at last week's calendar, where did love for God and love for people "
                    "actually get your time, and where were they crowded out?",
                    "Al mirar tu agenda de la semana pasada, ¿dónde recibieron tiempo de verdad el "
                    "amor a Dios y a las personas, y dónde quedaron desplazados?",
                ),
                "kid_ask": L(
                    "Who are the people you love most? How do you show them?",
                    "¿Quiénes son las personas que más quieres? ¿Cómo se lo demuestras?",
                ),
                "do": L(
                    "Write your three most important relationships, starting with God. Next to each, "
                    "put one specific time this week that belongs to it, and protect that time.",
                    "Escribe tus tres relaciones más importantes, empezando por Dios. Junto a cada una "
                    "anota un momento concreto de esta semana que le pertenezca, y protégelo.",
                ),
                "kid_do": L(
                    "Spend ten minutes today doing something with someone you love, with no screens.",
                    "Pasa hoy diez minutos haciendo algo con alguien que quieres, sin pantallas.",
                ),
                "pray": L(
                    "Lord, you have told me what matters most. My week does not always show it. "
                    "Reorder my days around loving you and the people you have given me.",
                    "Señor, tú me has dicho qué es lo que más importa. Mi semana no siempre lo "
                    "refleja. Reordena mis días en torno a amarte a ti y a las personas que me diste.",
                ),
            },
            {
                "key": "priorities-2",
                "ref": "Luke 10:38-42",
                "title": L("Distracted by good things", "La distracción de las cosas buenas"),
                "truth": L(
                    "Martha welcomes Jesus into her home and then gets pulled in many directions by "
                    "the work of hosting. What she is doing is good. But she ends up anxious, "
                    "resentful of her sister, and even annoyed with Jesus. He answers her gently, "
                    "saying her name twice. She is worried about many things; only one is needed, and "
                    "Mary has chosen it by sitting and listening to him. Jesus is not belittling work "
                    "or service. He is showing her that even good work, cut off from being with him, "
                    "turns into worry and complaint.",
                    "Marta recibe a Jesús en su casa y luego se dispersa en muchas direcciones por el "
                    "trabajo de atenderlo. Lo que hace es bueno. Pero termina ansiosa, resentida con "
                    "su hermana y hasta molesta con Jesús. Él le responde con ternura, diciendo su "
                    "nombre dos veces. Ella se preocupa por muchas cosas; solo una es necesaria, y "
                    "María la eligió al sentarse a escucharlo. Jesús no desprecia el trabajo ni el "
                    "servicio. Le muestra que hasta el trabajo bueno, separado de estar con él, se "
                    "convierte en preocupación y queja.",
                ),
                "simple": L(
                    "Martha was so busy that she got upset. Jesus told her kindly that the best thing "
                    "was to stop and be with him.",
                    "Marta estaba tan ocupada que se molestó. Jesús le dijo con cariño que lo mejor "
                    "era detenerse y estar con él.",
                ),
                "ask": L(
                    "What good work has been making you anxious or resentful lately? What might that "
                    "be telling you about what is missing?",
                    "¿Qué trabajo bueno te ha traído últimamente ansiedad o resentimiento? ¿Qué podría "
                    "estar diciéndote eso sobre lo que falta?",
                ),
                "kid_ask": L(
                    "When do you feel too busy? What helps you slow down?",
                    "¿Cuándo sientes que tienes demasiadas cosas? ¿Qué te ayuda a ir más despacio?",
                ),
                "do": L(
                    "Before the busiest part of tomorrow, sit still for ten minutes with this passage. "
                    "Do nothing useful. Let the work wait while you listen.",
                    "Mañana, antes de la parte más ocupada del día, siéntate en quietud diez minutos "
                    "con este pasaje. No hagas nada útil. Deja que el trabajo espere mientras escuchas.",
                ),
                "kid_do": L(
                    "Sit quietly for one minute with a grown-up and tell Jesus one thing about your day.",
                    "Siéntate en silencio un minuto con un adulto y cuéntale a Jesús una cosa de tu día.",
                ),
                "pray": L(
                    "Jesus, I am worried and upset about many things. Say my name. Teach me to sit "
                    "with you first, and to work from there.",
                    "Jesús, me preocupan y me alteran muchas cosas. Di mi nombre. Enséñame a sentarme "
                    "primero contigo y a trabajar desde ahí.",
                ),
            },
            {
                "key": "priorities-3",
                "ref": "Mark 1:35-38",
                "title": L("The freedom to say no", "La libertad de decir que no"),
                "truth": L(
                    "After a day of healing crowds, Jesus gets up while it is still dark and goes to a "
                    "deserted place to pray. His disciples track him down with news that sounds like "
                    "success: the whole town is asking for him. His answer is surprising. They will go "
                    "on to the other towns, because that is what he came to do. He leaves real needs "
                    "unmet in one place because he is clear about his purpose, and he had just been "
                    "praying. Not every demand on you is a call from God. Saying no to something good "
                    "is sometimes how you say yes to what you are here for.",
                    "Tras un día sanando multitudes, Jesús se levanta cuando aún está oscuro y va a un "
                    "lugar solitario a orar. Sus discípulos lo encuentran con una noticia que suena a "
                    "éxito: todo el pueblo pregunta por él. Su respuesta sorprende. Irán a los otros "
                    "pueblos, porque para eso vino. Deja necesidades reales sin atender en un lugar "
                    "porque tiene claro su propósito, y acababa de orar. No toda exigencia que recibes "
                    "es un llamado de Dios. A veces decir que no a algo bueno es la manera de decir "
                    "que sí a aquello para lo que estás aquí.",
                ),
                "simple": L(
                    "Jesus got up early to talk with God. Then he knew what to do that day. Talking "
                    "with God helps us choose the most important things.",
                    "Jesús se levantó temprano para hablar con Dios. Luego supo qué hacer ese día. "
                    "Hablar con Dios nos ayuda a elegir lo más importante.",
                ),
                "ask": L(
                    "What are you saying yes to mainly because people expect it? What would you need "
                    "to be clear about in order to say a kind no?",
                    "¿A qué le dices que sí sobre todo porque la gente lo espera? ¿Qué necesitarías "
                    "tener claro para decir un no amable?",
                ),
                "kid_ask": L(
                    "When is a good time for you to talk with God each day?",
                    "¿Cuál es un buen momento del día para que hables con Dios?",
                ),
                "do": L(
                    "Identify one commitment that is good but not yours to carry right now. This week, "
                    "decline it or hand it on, politely and without a long apology.",
                    "Identifica un compromiso que es bueno pero que no te toca cargar ahora. Esta "
                    "semana recházalo o pásalo a alguien más, con amabilidad y sin largas disculpas.",
                ),
                "kid_do": L(
                    "Tomorrow morning, before anything else, say: Good morning, God. Help me with today.",
                    "Mañana por la mañana, antes que nada, di: Buenos días, Dios. Ayúdame con este día.",
                ),
                "pray": L(
                    "Father, many people want something from me. Meet me before the day starts. Show "
                    "me what I am here for today, and what I can leave.",
                    "Padre, mucha gente quiere algo de mí. Encuéntrame antes de que empiece el día. "
                    "Muéstrame para qué estoy aquí hoy, y qué puedo dejar.",
                ),
            },
            {
                "key": "priorities-4",
                "ref": "Psalm 90:12",
                "title": L("Counting your days", "Contar tus días"),
                "truth": L(
                    "This prayer, handed down as a prayer of Moses, asks God for one skill: to number "
                    "our days, so that we gain a heart of wisdom. It is not meant to be gloomy. A "
                    "person who knows their time is limited stops assuming there will always be a "
                    "later, and starts treating today as something given and unrepeatable. Counting "
                    "your days does not mean cramming more in. It means choosing: this conversation, "
                    "this child's bedtime, this act of obedience, while it is still today. Wisdom "
                    "begins with accepting that you cannot do everything, and were never asked to.",
                    "Esta oración, transmitida como oración de Moisés, le pide a Dios una sola "
                    "habilidad: contar nuestros días, para adquirir un corazón sabio. No busca "
                    "entristecer. Quien sabe que su tiempo es limitado deja de suponer que siempre "
                    "habrá un después y empieza a tratar el día de hoy como algo regalado e "
                    "irrepetible. Contar tus días no es meterles más cosas. Es elegir: esta "
                    "conversación, la hora de dormir de este niño, este acto de obediencia, mientras "
                    "todavía es hoy. La sabiduría empieza por aceptar que no puedes hacerlo todo, y "
                    "que nunca se te pidió.",
                ),
                "simple": L(
                    "Every day is a gift from God. We can ask him to help us use each day for things "
                    "that really matter, like loving people.",
                    "Cada día es un regalo de Dios. Podemos pedirle que nos ayude a usar cada día en "
                    "lo que de verdad importa, como amar a las personas.",
                ),
                "ask": L(
                    "If you knew you had one year, what would you stop doing, and what would you "
                    "start? What keeps you from making one of those changes now?",
                    "Si supieras que te queda un año, ¿qué dejarías de hacer y qué empezarías? ¿Qué te "
                    "impide hacer ahora uno de esos cambios?",
                ),
                "kid_ask": L(
                    "What was the best part of your day today?",
                    "¿Cuál fue la mejor parte de tu día hoy?",
                ),
                "do": L(
                    "Tonight, look back over the day and name the one hour that mattered most. "
                    "Tomorrow, plan for one more like it.",
                    "Esta noche repasa el día y nombra la hora que más importó. Mañana, planea una más "
                    "como esa.",
                ),
                "kid_do": L(
                    "At bedtime, tell God thank you for one thing from today.",
                    "A la hora de dormir, dale gracias a Dios por una cosa de hoy.",
                ),
                "pray": L(
                    "Lord, teach me to count my days. I cannot do everything, and I do not have "
                    "forever. Give me a wise heart for the day in front of me.",
                    "Señor, enséñame a contar mis días. No puedo hacerlo todo ni tengo todo el tiempo. "
                    "Dame un corazón sabio para el día que tengo delante.",
                ),
            },
        ],
    },
    {
        "key": "humility",
        "category": "wisdom",
        "title": L("Humility: seeing yourself rightly", "Humildad: verte como eres"),
        "summary": L(
            "For pride, comparison, and the opposite trouble of thinking you are worth nothing. Four "
            "readings on seeing yourself truthfully before God, and the freedom of not having to be "
            "the greatest.",
            "Para el orgullo, la comparación y el problema contrario de pensar que no vales nada. "
            "Cuatro lecturas sobre verte con verdad delante de Dios y la libertad de no tener que "
            "estar por encima de nadie.",
        ),
        "keywords": [
            "pride", "proud", "humbl", "humility", "arrogan", "ego", "compare", "comparing",
            "comparison", "jealous", "envy", "envious", "show off", "orgull", "humild", "soberbi",
            "arrogan", "compara", "envidi", "presum", "celos",
        ],
        "situations": ["leader", "student", "working", "new_believer"],
        "traits": ["humility", "servanthood", "contentment"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "You do not have to be the best at everything. God loves you, and he loves the other "
                "kids too.",
                "No tienes que ganar en todo ni ser quien más sabe. Dios te ama, y también ama a los "
                "demás niños.",
            ),
            "teen": L(
                "For the constant measuring: looks, grades, followers, who is in and who is out. "
                "There is a way off that scale.",
                "Para la medición constante: apariencia, notas, seguidores, quién está dentro y quién "
                "fuera. Hay una manera de bajarte de esa báscula.",
            ),
            "young_adult": L(
                "For proving yourself, and for the fear that you are behind everyone else. A true "
                "view of yourself is steadier than either.",
                "Para el afán de demostrar lo que vales y el temor de ir detrás de todos. Una visión "
                "verdadera de ti es más firme que cualquiera de los dos.",
            ),
            "adult": L(
                "For success that has gone to your head, or failure that has gone to your heart. "
                "Humility deals with both.",
                "Para el éxito que se te subió a la cabeza o el fracaso que se te metió en el "
                "corazón. La humildad atiende los dos.",
            ),
            "senior": L(
                "For receiving help gracefully, letting others lead, and holding a lifetime of "
                "experience without needing to be right.",
                "Para recibir ayuda con gracia, dejar que otros dirijan y llevar toda una vida de "
                "experiencia sin necesidad de tener la razón.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "humility-1",
                "ref": "Luke 18:9-14",
                "title": L("The trouble with comparing", "El problema de compararse"),
                "truth": L(
                    "Jesus tells this story to people who were sure of their own goodness and looked "
                    "down on everyone else. Two men pray. One thanks God that he is not like other "
                    "people and lists his achievements. The other stands at a distance, cannot even "
                    "look up, and asks only for mercy as a sinner. Jesus says it was the second man "
                    "who went home right with God. Pride works by comparison; it always needs someone "
                    "to be above. Humility stops looking sideways and looks at God, and finds mercy there.",
                    "Jesús cuenta esta historia a personas que estaban seguras de su propia bondad y "
                    "miraban a los demás por encima del hombro. Dos hombres oran. Uno da gracias a "
                    "Dios por no ser como los demás y enumera sus logros. El otro se queda a "
                    "distancia, no se atreve ni a levantar la vista y solo pide misericordia como "
                    "pecador. Jesús dice que fue el segundo quien volvió a casa en paz con Dios. El "
                    "orgullo funciona comparando; siempre necesita a alguien por debajo. La humildad "
                    "deja de mirar a los lados, mira a Dios y allí encuentra misericordia.",
                ),
                "simple": L(
                    "One man bragged to God about how good he was. Another man said: God, I have done "
                    "wrong; please be kind to me. God was pleased with the second man.",
                    "Un hombre presumió ante Dios de lo bueno que era. Otro dijo: Dios, hice cosas "
                    "malas; ten compasión de mí. A Dios le agradó el segundo hombre.",
                ),
                "ask": L(
                    "Who do you compare yourself with to feel better, or to feel worse? What happens "
                    "to that comparison when you stand before God instead?",
                    "¿Con quién te comparas para sentirte mejor, o para sentirte peor? ¿Qué pasa con "
                    "esa comparación cuando te pones delante de Dios?",
                ),
                "kid_ask": L(
                    "Do you ever feel like you have to be better than someone else? When?",
                    "¿Alguna vez sientes que tienes que ser mejor que alguien? ¿Cuándo?",
                ),
                "do": L(
                    "Catch one comparison today, in person or on a screen. When you notice it, pray "
                    "the second man's prayer in your own words, and then ask a blessing on the person "
                    "you compared yourself with.",
                    "Atrapa hoy una comparación, en persona o en una pantalla. Cuando la notes, haz "
                    "con tus palabras la oración del segundo hombre, y luego pide una bendición para "
                    "la persona con quien te comparaste.",
                ),
                "kid_do": L(
                    "Tell someone today: you are really good at that. Mean it.",
                    "Dile hoy a alguien: eso te sale muy bien. Y dilo de corazón.",
                ),
                "pray": L(
                    "God, have mercy on me. I keep measuring myself against other people. Turn my eyes "
                    "to you, where I do not need to win.",
                    "Dios, ten misericordia de mí. Vivo midiéndome con los demás. Vuelve mis ojos "
                    "hacia ti, donde no necesito ganar.",
                ),
            },
            {
                "key": "humility-2",
                "ref": "Romans 12:3-5",
                "title": L("Neither too high nor too low", "Ni muy alto ni muy bajo"),
                "truth": L(
                    "Paul's instruction is precise: do not think of yourself more highly than you "
                    "should, but think with sober judgment. Sober means accurate. Humility is not "
                    "pretending to be worthless or denying what you do well; that is just another way "
                    "of being absorbed in yourself. It is seeing yourself truthfully. Then he gives "
                    "the picture that makes it possible: one body with many parts, each different, "
                    "each belonging to the others. You are not everything, and you are not nothing. "
                    "You are a part, with something real to give and a real need of the rest.",
                    "La indicación de Pablo es precisa: no pienses de ti más alto de lo que debes, "
                    "sino con juicio sobrio. Sobrio quiere decir exacto. La humildad no es fingir que "
                    "no vales nada ni negar lo que haces bien; esa es solo otra forma de vivir "
                    "pendiente de ti. Es verte con verdad. Luego da la imagen que lo hace posible: un "
                    "solo cuerpo con muchas partes, cada una distinta, cada una perteneciente a las "
                    "demás. No lo eres todo, pero tampoco eres poca cosa. Eres una parte, con algo "
                    "real que dar y una necesidad real de los demás.",
                ),
                "simple": L(
                    "You are not the most important person, and you are not unimportant either. You "
                    "are one special part of God's big family, and so is everyone else.",
                    "No eres la persona más importante, y tampoco eres poco importante. Eres una parte "
                    "especial de la gran familia de Dios, y los demás también.",
                ),
                "ask": L(
                    "Do you tend to think too highly of yourself, or too little? What would a sober, "
                    "accurate sentence about your gifts and limits sound like?",
                    "¿Tiendes a pensar demasiado alto de ti, o demasiado poco? ¿Cómo sonaría una frase "
                    "sobria y exacta sobre tus dones y tus límites?",
                ),
                "kid_ask": L(
                    "What is something you are good at? What is something a friend is good at?",
                    "¿Qué cosa te sale bien a ti? ¿Qué cosa le sale bien a un amigo tuyo?",
                ),
                "do": L(
                    "Write two honest lists of three: things you do well, and things you need others "
                    "for. Thank God for the first, and thank one person from the second.",
                    "Escribe dos listas honestas de tres: cosas que haces bien y cosas para las que "
                    "necesitas a otros. Da gracias a Dios por la primera, y dale las gracias a una "
                    "persona de la segunda.",
                ),
                "kid_do": L(
                    "Ask a friend or family member to teach you something they are good at.",
                    "Pídele a un amigo o familiar que te enseñe algo que le sale bien.",
                ),
                "pray": L(
                    "Lord, give me a true view of myself: no bigger and no smaller than I am. Thank "
                    "you for what you have given me and for the people I need.",
                    "Señor, dame una visión verdadera de mí: ni más grande ni más pequeña de lo que "
                    "soy. Gracias por lo que me diste y por las personas que necesito.",
                ),
            },
            {
                "key": "humility-3",
                "ref": "Philippians 2:3-8",
                "title": L("The mind of Christ", "La manera de pensar de Cristo"),
                "truth": L(
                    "Paul asks for something hard: do nothing out of rivalry or vanity, treat others "
                    "as more important than yourself, and look out for their interests as well as your "
                    "own. Then he shows where that comes from. Christ Jesus, who was equal with God, "
                    "did not cling to his position. He emptied himself, took the form of a servant, "
                    "became human, and went down as far as death on a cross. Humility, then, is not a "
                    "small person staying small. It is someone with everything choosing to go lower "
                    "for the sake of others. That is the pattern we are invited into.",
                    "Pablo pide algo difícil: no hagas nada por rivalidad ni por vanidad, trata a los "
                    "demás como más importantes que tú, y cuida sus intereses además de los tuyos. "
                    "Luego muestra de dónde sale eso. Cristo Jesús, siendo igual a Dios, no se aferró "
                    "a su posición. Se despojó a sí mismo, tomó forma de siervo, se hizo humano y "
                    "descendió hasta la muerte en una cruz. La humildad, entonces, no es una persona "
                    "pequeña que se queda pequeña. Es alguien que lo tiene todo y elige bajar por amor "
                    "a otros. Ese es el modelo al que se nos invita.",
                ),
                "simple": L(
                    "Jesus is the King of everything, but he came to help and serve us. Being humble "
                    "means caring about what other people need, like Jesus did.",
                    "Jesús es el Rey de todo, pero vino a ayudarnos y servirnos. Ser humilde es "
                    "interesarse por lo que otros necesitan, como hizo Jesús.",
                ),
                "ask": L(
                    "Where are you holding on to a position, a right or being seen? What would it look "
                    "like to go one step lower there for someone else's good?",
                    "¿Dónde te aferras a una posición, a un derecho o a que te vean? ¿Cómo sería bajar "
                    "un escalón ahí por el bien de otra persona?",
                ),
                "kid_ask": L(
                    "How could you let someone else go first today?",
                    "¿Cómo podrías dejar que otra persona vaya primero hoy?",
                ),
                "do": L(
                    "Today, in one conversation, ask about the other person's concerns before "
                    "mentioning yours. Then do one task that is beneath your role without pointing it out.",
                    "Hoy, en una conversación, pregunta por las preocupaciones de la otra persona "
                    "antes de mencionar las tuyas. Luego haz una tarea que esté por debajo de tu "
                    "puesto sin hacerlo notar.",
                ),
                "kid_do": L(
                    "Let someone else choose the game or go first today, and do it with a smile.",
                    "Deja hoy que otra persona elija el juego o vaya primero, y hazlo con una sonrisa.",
                ),
                "pray": L(
                    "Lord Jesus, you had every right and laid it down for me. Give me your way of "
                    "thinking. Show me where to go lower today.",
                    "Señor Jesús, tenías todo el derecho y lo dejaste por mí. Dame tu manera de "
                    "pensar. Muéstrame dónde bajar hoy.",
                ),
            },
            {
                "key": "humility-4",
                "ref": "1 Peter 5:5-7",
                "title": L("Humility is a relief", "La humildad es un descanso"),
                "truth": L(
                    "Peter tells everyone to put on humility toward one another like a piece of "
                    "clothing, because God resists the proud and gives grace to the humble. Then he "
                    "connects humility with something unexpected: handing over your worries. To humble "
                    "yourself under God's strong hand is to stop acting as if everything depends on "
                    "you, and to throw your anxieties onto him, because he cares for you. Pride is "
                    "exhausting. It has to manage every impression and control every outcome. Humility "
                    "lets God be God, and lets you rest in being cared for.",
                    "Pedro les dice a todos que se vistan de humildad unos con otros, como quien se "
                    "pone una prenda, porque Dios se opone a los orgullosos y da gracia a los "
                    "humildes. Luego une la humildad con algo inesperado: entregar tus preocupaciones. "
                    "Hacerte humilde bajo la mano poderosa de Dios es dejar de actuar como si todo "
                    "dependiera de ti y echar sobre él tus ansiedades, porque él cuida de ti. El "
                    "orgullo agota. Tiene que manejar cada impresión y controlar cada resultado. La "
                    "humildad deja que Dios sea Dios y te deja descansar en que alguien te cuida.",
                ),
                "simple": L(
                    "You do not have to be the boss of everything. God is big and strong, and he takes "
                    "care of you. You can give your worries to him.",
                    "No tienes que mandar en todo. Dios es grande y fuerte, y te cuida. Puedes darle "
                    "tus preocupaciones.",
                ),
                "ask": L(
                    "What are you trying to control that is not yours to control? What would it feel "
                    "like to put it in stronger hands?",
                    "¿Qué estás tratando de controlar que no te toca controlar? ¿Cómo se sentiría "
                    "ponerlo en manos más fuertes?",
                ),
                "kid_ask": L(
                    "What is something you worry about that you could give to God?",
                    "¿Qué cosa te preocupa que podrías darle a Dios?",
                ),
                "do": L(
                    "Name one outcome you have been straining to control. Open your hands and tell God "
                    "it is his. Then ask one person for help with something you usually insist on "
                    "doing alone.",
                    "Nombra un resultado que has estado esforzándote por controlar. Abre las manos y "
                    "dile a Dios que es suyo. Luego pídele ayuda a una persona con algo que sueles "
                    "insistir en hacer por tu cuenta.",
                ),
                "kid_do": L(
                    "Ask for help with one thing today instead of saying: I can do it all by myself.",
                    "Pide ayuda hoy con una cosa, en vez de decir: yo puedo sin ayuda de nadie.",
                ),
                "pray": L(
                    "God, I am tired of holding everything together. You are strong, and you care for "
                    "me. I put myself, and this worry, under your hand.",
                    "Dios, me cansé de sostenerlo todo. Tú eres fuerte y cuidas de mí. Me pongo, con "
                    "esta preocupación, bajo tu mano.",
                ),
            },
        ],
    },
]
