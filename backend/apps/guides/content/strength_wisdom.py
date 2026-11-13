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
    # @@NEXT@@
]
