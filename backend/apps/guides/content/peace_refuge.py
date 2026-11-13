from apps.guides.catalog import L

TOPICS = [
    # ======================================================================
    # PEACE
    # ======================================================================
    {
        "key": "anxiety",
        "category": "peace",
        "title": L("Anxiety and worry", "Ansiedad y preocupación"),
        "summary": L(
            "For when your mind keeps circling the same fears. Five short readings on handing worry "
            "to God and receiving a peace that does not depend on things being fixed.",
            "Para cuando tu mente da vueltas a los mismos temores. Cinco lecturas breves sobre entregar "
            "la preocupación a Dios y recibir una paz que no depende de que todo se arregle.",
        ),
        "keywords": [
            "anxi", "worr", "stress", "overwhelm", "panic", "nervous", "restless",
            "ansie", "preocup", "estrés", "agobi", "nervios", "angusti", "inquiet",
        ],
        "situations": ["working", "parent", "single_parent", "caregiver", "student", "job_seeking", "moving"],
        "traits": ["peace", "trust", "prayerfulness"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Everyone feels worried sometimes. God wants to hear about it.",
                "Todos nos preocupamos a veces. Dios quiere que se lo cuentes.",
            ),
            "teen": L(
                "Grades, friends, the future, what people think: this is for the nights it all gets loud.",
                "Notas, amigos, el futuro, lo que piensan los demás: esto es para las noches en que todo hace ruido.",
            ),
            "young_adult": L(
                "When every decision feels like it could ruin everything, here is somewhere to stand.",
                "Cuando cada decisión parece que puede arruinarlo todo, aquí hay dónde pararte.",
            ),
            "adult": L(
                "For carrying work, money and the people who depend on you without being crushed by them.",
                "Para cargar el trabajo, el dinero y a quienes dependen de ti sin que te aplasten.",
            ),
            "senior": L(
                "Health, family, what comes next: the worries change with the years, the invitation does not.",
                "La salud, la familia, lo que viene: las preocupaciones cambian con los años, la invitación no.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "anxiety-1",
                "ref": "Philippians 4:6-7",
                "title": L("What to do with a worry", "Qué hacer con una preocupación"),
                "truth": L(
                    "Paul writes this from prison, so it is not advice from someone whose life is easy. He does "
                    "not say worries are silly. He says what to do with them: turn each one into a request, "
                    "with thanks, and bring it to God. What follows is not a fix but a guard: a peace that "
                    "stands watch over heart and mind even while the problem is still there.",
                    "Pablo escribe esto desde la cárcel, así que no es el consejo de alguien con una vida fácil. "
                    "No dice que las preocupaciones sean tonterías. Dice qué hacer con ellas: convertir cada una "
                    "en una petición, con gratitud, y llevarla a Dios. Lo que sigue no es una solución sino una "
                    "guardia: una paz que vigila el corazón y la mente aunque el problema siga ahí.",
                ),
                "simple": L(
                    "When you feel worried, you can tell God about it, just like telling someone who loves you. "
                    "God listens, and God can help your heart feel calm.",
                    "Cuando te sientes preocupado, puedes contárselo a Dios, como a alguien que te quiere. "
                    "Dios escucha y puede ayudar a que tu corazón se calme.",
                ),
                "ask": L(
                    "Which worry have you been carrying alone that you have not actually put into words to God?",
                    "¿Qué preocupación has cargado a solas sin haberla puesto en palabras delante de Dios?",
                ),
                "kid_ask": L(
                    "What is one thing that makes you feel worried?",
                    "¿Qué es algo que te hace sentir preocupado?",
                ),
                "do": L(
                    "Tonight, write your three biggest worries as three one-sentence requests, and add one "
                    "thing you are thankful for beside each.",
                    "Esta noche escribe tus tres mayores preocupaciones como tres peticiones de una frase, y "
                    "junto a cada una algo por lo que das gracias.",
                ),
                "kid_do": L(
                    "Tell God your worry in one sentence, then tell a grown-up too.",
                    "Cuéntale a Dios tu preocupación en una frase y luego cuéntasela también a un adulto.",
                ),
                "pray": L(
                    "God, here is what I keep turning over: … I cannot fix it tonight. Guard my heart and my "
                    "mind while I wait.",
                    "Dios, esto es lo que no dejo de darle vueltas: … No puedo arreglarlo esta noche. Guarda mi "
                    "corazón y mi mente mientras espero.",
                ),
            },
            {
                "key": "anxiety-2",
                "ref": "Matthew 6:25-34",
                "title": L("What the birds know", "Lo que saben los pájaros"),
                "truth": L(
                    "Jesus is speaking to people who had real reasons to worry about food and clothing. He does "
                    "not scold them. He points to birds and wildflowers: the Father feeds and dresses them, and "
                    "you matter more to him than they do. Worry, he says, cannot add a single hour to your life. "
                    "Then he gets practical: tomorrow will bring its own trouble, so you are only asked to live "
                    "today, with a Father who already knows what you need.",
                    "Jesús habla a personas que tenían motivos reales para preocuparse por la comida y la ropa. "
                    "No las regaña. Señala a los pájaros y a las flores del campo: el Padre los alimenta y los "
                    "viste, y tú le importas más que ellos. La preocupación, dice, no puede añadir ni una hora a "
                    "tu vida. Luego se vuelve práctico: mañana traerá sus propios problemas, así que solo se te "
                    "pide vivir hoy, con un Padre que ya sabe lo que necesitas.",
                ),
                "simple": L(
                    "God takes care of the birds and the flowers. You matter even more to God than they do, "
                    "and he knows what you need.",
                    "Dios cuida a los pájaros y a las flores. Tú le importas todavía más que ellos, y él sabe "
                    "lo que necesitas.",
                ),
                "ask": L(
                    "Which of tomorrow's troubles are you trying to carry today? What would it look like to "
                    "deal only with today's?",
                    "¿Cuál de los problemas de mañana estás tratando de cargar hoy? ¿Cómo sería ocuparte solo "
                    "de los de hoy?",
                ),
                "kid_ask": L(
                    "What is something God has given you today that you needed?",
                    "¿Qué te ha dado Dios hoy que necesitabas?",
                ),
                "do": L(
                    "Step outside for five minutes today. Watch one bird or look at one growing thing, and "
                    "tell God the one thing you need for today, and only today.",
                    "Sal cinco minutos hoy. Observa un pájaro o algo que esté creciendo, y dile a Dios lo "
                    "único que necesitas para hoy, solo para hoy.",
                ),
                "kid_do": L(
                    "Look out the window for a bird or a flower. Tell God thank you for taking care of it, "
                    "and of you.",
                    "Busca por la ventana un pájaro o una flor. Dale gracias a Dios por cuidarlo, y por "
                    "cuidarte a ti.",
                ),
                "pray": L(
                    "Father, you know what I need before I ask. Help me to live this one day with you and to "
                    "leave tomorrow where it belongs.",
                    "Padre, tú sabes lo que necesito antes de que te lo pida. Ayúdame a vivir este único día "
                    "contigo y a dejar el mañana en su lugar.",
                ),
            },
            {
                "key": "anxiety-3",
                "ref": "1 Peter 5:6-7",
                "title": L("It does not all depend on you", "No todo depende de ti"),
                "truth": L(
                    "Peter joins two things we rarely connect: humility and worry. Part of anxiety is the "
                    "feeling that everything rests on you. To humble yourself under God's hand is to admit "
                    "that it does not. Then comes the invitation to throw the whole load onto him. The reason "
                    "Peter gives is not that your problems are small. It is that God cares about you.",
                    "Pedro une dos cosas que casi nunca relacionamos: la humildad y la preocupación. Parte de "
                    "la ansiedad es sentir que todo descansa sobre ti. Humillarte bajo la mano de Dios es "
                    "reconocer que no es así. Después viene la invitación a echar toda la carga sobre él. La "
                    "razón que da Pedro no es que tus problemas sean pequeños. Es que Dios se interesa por ti.",
                ),
                "simple": L(
                    "You do not have to carry heavy worries by yourself. You can give them to God, because "
                    "God cares about you.",
                    "No tienes que cargar las preocupaciones pesadas por tu cuenta. Puedes dárselas a Dios, "
                    "porque a Dios le importas.",
                ),
                "ask": L(
                    "What are you carrying as if it all depended on you? What would change if you admitted "
                    "it is too heavy for one person?",
                    "¿Qué estás cargando como si todo dependiera de ti? ¿Qué cambiaría si reconocieras que "
                    "es demasiado peso para una sola persona?",
                ),
                "kid_ask": L(
                    "Who helps you when something is too heavy to carry?",
                    "¿Quién te ayuda cuando algo pesa demasiado para cargarlo?",
                ),
                "do": L(
                    "Pick up something heavy, like a full bag. Name your worry out loud, set the bag down, "
                    "and leave it there as a sign that you have handed the worry to God. When it comes back, "
                    "hand it over again. That is not failing; that is the practice.",
                    "Levanta algo pesado, como una bolsa llena. Di tu preocupación en voz alta, deja la bolsa "
                    "en el suelo y déjala ahí como señal de que se la entregaste a Dios. Cuando vuelva, "
                    "entrégala otra vez. Eso no es fallar; esa es la práctica.",
                ),
                "kid_do": L(
                    "Hold a heavy book, tell God your worry, and then put the book down. Giving God a worry "
                    "is a little like that.",
                    "Sostén un libro pesado, cuéntale a Dios tu preocupación y luego suelta el libro. Darle "
                    "una preocupación a Dios se parece un poco a eso.",
                ),
                "pray": L(
                    "God, I have been living as if everything depended on me. It does not. I put … into "
                    "your hands, because you care about me.",
                    "Dios, he vivido como si todo dependiera de mí. No es así. Pongo … en tus manos, porque "
                    "yo te importo.",
                ),
            },
            {
                "key": "anxiety-4",
                "ref": "Psalm 94:18-19",
                "title": L("When the worries multiply", "Cuando las preocupaciones se multiplican"),
                "truth": L(
                    "The writer hides nothing: his foot was slipping and his anxious thoughts were many. He "
                    "does not say the thoughts stopped. He says that in the middle of them God's faithful love "
                    "held him up and God's comfort brought him joy. Anxiety and comfort can live in the same "
                    "person in the same hour. Having anxious thoughts does not mean your faith has failed.",
                    "El autor no esconde nada: su pie resbalaba y sus pensamientos ansiosos eran muchos. No "
                    "dice que los pensamientos se detuvieron. Dice que en medio de ellos el amor fiel de Dios "
                    "lo sostuvo y el consuelo de Dios le dio alegría. La ansiedad y el consuelo pueden vivir "
                    "en la misma persona a la misma hora. Tener pensamientos ansiosos no significa que tu fe "
                    "haya fallado.",
                ),
                "simple": L(
                    "Sometimes many worried thoughts come all at once. God holds on to you, like a hand that "
                    "catches you when you slip.",
                    "A veces llegan muchos pensamientos de preocupación al mismo tiempo. Dios te sostiene, "
                    "como una mano que te agarra cuando resbalas.",
                ),
                "ask": L(
                    "When did you think you were slipping, and something held? What comforted you then?",
                    "¿Cuándo pensaste que resbalabas y algo te sostuvo? ¿Qué te consoló en ese momento?",
                ),
                "kid_ask": L(
                    "Who holds your hand so that you do not fall?",
                    "¿Quién te da la mano para que no te caigas?",
                ),
                "do": L(
                    "Write down one time you were held when you thought you would fall, and keep it where "
                    "you will see it. And if anxiety is keeping you from sleeping, eating or getting through "
                    "your days, tell a doctor or counselor. Asking for help is one of the ways people are "
                    "held up.",
                    "Escribe una ocasión en que algo te sostuvo cuando creías que ibas a caer, y guárdala "
                    "donde la veas. Y si la ansiedad no te deja dormir, comer o sacar adelante tus días, "
                    "cuéntaselo a un médico o consejero. Pedir ayuda es una de las formas en que Dios "
                    "sostiene a las personas.",
                ),
                "kid_do": L(
                    "Draw a big hand holding you. Then hold a grown-up's hand and tell them one worried "
                    "thought.",
                    "Dibuja una mano grande que te sostiene. Luego toma la mano de un adulto y cuéntale un "
                    "pensamiento que te preocupa.",
                ),
                "pray": L(
                    "Lord, my thoughts are many tonight and I feel my foot slipping. Hold me up with your "
                    "love, and let your comfort reach me here.",
                    "Señor, esta noche mis pensamientos son muchos y siento que mi pie resbala. Sostenme con "
                    "tu amor y haz que tu consuelo me alcance aquí.",
                ),
            },
            {
                "key": "anxiety-5",
                "ref": "John 14:25-27",
                "title": L("A different kind of peace", "Una paz de otra clase"),
                "truth": L(
                    "Jesus says this the night before his arrest, when his friends' world is about to come "
                    "apart. He does not promise them calm circumstances. He gives them his own peace and says "
                    "it is unlike the kind the world gives. The world's peace arrives when problems leave. "
                    "His comes with his presence, through the Spirit who will stay with them and remind them "
                    "of his words. Troubled hearts are told not to be afraid because they will not be left alone.",
                    "Jesús dice esto la noche antes de su arresto, cuando el mundo de sus amigos está por "
                    "derrumbarse. No les promete circunstancias tranquilas. Les da su propia paz y dice que no "
                    "se parece a la que da el mundo. La paz del mundo llega cuando los problemas se van. La "
                    "suya llega con su presencia, por medio del Espíritu que se quedará con ellos y les "
                    "recordará sus palabras. Al corazón angustiado se le dice que no tema porque no lo "
                    "dejarán solo.",
                ),
                "simple": L(
                    "Jesus gives his friends a special peace. It is a calm feeling inside that comes from "
                    "knowing Jesus is with you.",
                    "Jesús les da a sus amigos una paz especial. Es una calma por dentro que viene de saber "
                    "que Jesús está contigo.",
                ),
                "ask": L(
                    "Where are you waiting for circumstances to change before you allow yourself peace? What "
                    "would it mean to receive it as a gift now?",
                    "¿Dónde estás esperando que cambien las circunstancias para permitirte la paz? ¿Qué "
                    "significaría recibirla como un regalo ahora?",
                ),
                "kid_ask": L(
                    "When do you feel calm and safe?",
                    "¿Cuándo sientes calma y seguridad?",
                ),
                "do": L(
                    "Three times today, morning, midday and night, stop for one minute. Breathe in slowly "
                    "remembering that Jesus is with you; breathe out one thing you are afraid of.",
                    "Tres veces hoy, mañana, mediodía y noche, detente un minuto. Inhala despacio recordando "
                    "que Jesús está contigo; exhala una cosa que te da miedo.",
                ),
                "kid_do": L(
                    "Take three slow breaths and say: Jesus, thank you for being with me.",
                    "Respira despacio tres veces y di: Jesús, gracias por estar conmigo.",
                ),
                "pray": L(
                    "Jesus, I have been looking for peace in getting everything settled. Give me your peace, "
                    "the kind that stays when things are not settled.",
                    "Jesús, he buscado la paz en dejar todo resuelto. Dame tu paz, la que permanece cuando "
                    "las cosas no están resueltas.",
                ),
            },
        ],
    },
    {
        "key": "fear",
        "category": "peace",
        "title": L("Fear", "Miedo"),
        "summary": L(
            "For when you are afraid of what is happening or of what might. Five readings about a God "
            "who does not shame frightened people but stays with them.",
            "Para cuando tienes miedo de lo que pasa o de lo que podría pasar. Cinco lecturas sobre un "
            "Dios que no avergüenza a quien tiene miedo, sino que se queda a su lado.",
        ),
        "keywords": [
            "fear", "afraid", "scared", "terrif", "dread", "frighten", "nightmare",
            "miedo", "temor", "asust", "pánico", "pesadilla", "terror", "atemoriz",
        ],
        "situations": ["parent", "single_parent", "ill", "military", "moving", "job_seeking", "caregiver"],
        "traits": ["courage", "trust", "peace"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Everybody gets scared sometimes, even grown-ups. God stays close when you are afraid.",
                "Todos sentimos miedo a veces, también los adultos. Dios se queda cerca cuando tienes miedo.",
            ),
            "teen": L(
                "Fear of failing, of being left out, of what is happening in the world: you can say it out loud here.",
                "Miedo a fallar, a quedarte fuera, a lo que pasa en el mundo: aquí puedes decirlo en voz alta.",
            ),
            "young_adult": L(
                "For the fear that you will choose wrong, end up alone or never get started. You are not walking in alone.",
                "Para el miedo a elegir mal, a terminar a solas o a no arrancar nunca. No entras sin compañía.",
            ),
            "adult": L(
                "For fears about your children, your health, your work and the news, the kind that wake you at three in the morning.",
                "Para los miedos por tus hijos, tu salud, tu trabajo y las noticias, los que te despiertan a las tres de la mañana.",
            ),
            "senior": L(
                "For fears about your body, about being a burden, about what lies ahead. The one who held you this far still holds you.",
                "Para los miedos por tu cuerpo, por ser una carga, por lo que viene. Quien te sostuvo hasta aquí te sigue sosteniendo.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "fear-1",
                "ref": "Psalm 56:3-4",
                "title": L("When, not if", "Cuando, no si acaso"),
                "truth": L(
                    "David wrote this while he was in real danger, and he does not claim he is never afraid. "
                    "He says what he does when he is: he turns his trust toward God. Fear and trust appear in "
                    "the same sentence. Courage here is not a feeling you must produce. It is a direction: "
                    "where you turn while you are still afraid.",
                    "David escribió esto estando en verdadero peligro, y no afirma que nunca tiene miedo. Dice "
                    "lo que hace cuando lo tiene: vuelve su confianza hacia Dios. El miedo y la confianza "
                    "aparecen en la misma frase. Aquí la valentía no es un sentimiento que debes fabricar. Es "
                    "una dirección: hacia dónde te vuelves mientras todavía tienes miedo.",
                ),
                "simple": L(
                    "Even brave people feel afraid. When you are scared, you can tell God that you trust him.",
                    "Hasta las personas valientes sienten miedo. Cuando tengas miedo, puedes decirle a Dios "
                    "que confías en él.",
                ),
                "ask": L(
                    "What are you afraid of right now, said plainly? What would turning toward God with it "
                    "look like in one sentence?",
                    "¿De qué tienes miedo ahora mismo, dicho con sencillez? ¿Cómo sería volverte hacia Dios "
                    "con eso, en una sola frase?",
                ),
                "kid_ask": L(
                    "What is something that scares you?",
                    "¿Qué es algo que te da miedo?",
                ),
                "do": L(
                    "Finish this sentence on paper: When I am afraid of …, I will … End it with one concrete "
                    "way of turning to God, such as a line to pray or a person to call.",
                    "Completa esta frase en un papel: Cuando tenga miedo de …, voy a … Termínala con una "
                    "forma concreta de volverte a Dios, como una frase para orar o una persona a quien llamar.",
                ),
                "kid_do": L(
                    "Next time you feel scared, whisper to God that you trust him, and go tell a grown-up.",
                    "La próxima vez que sientas miedo, dile a Dios en voz bajita que confías en él y ve a "
                    "contárselo a un adulto.",
                ),
                "pray": L(
                    "God, I am afraid of … I am not going to pretend otherwise. Right here, still afraid, I "
                    "choose to trust you.",
                    "Dios, tengo miedo de … No voy a fingir otra cosa. Aquí mismo, todavía con miedo, decido "
                    "confiar en ti.",
                ),
            },
            {
                "key": "fear-2",
                "ref": "Mark 4:35-41",
                "title": L("In the boat with you", "En la barca contigo"),
                "truth": L(
                    "The storm was real. Several of these men were fishermen, and they believed they were "
                    "about to drown. Their cry is the one frightened people still pray: do you not care? "
                    "Jesus had been in the boat the whole time. He calms the wind and the sea, and then asks "
                    "about their fear, not to send them away but so they will learn who is with them. They "
                    "end the night with a bigger question than the storm: who is this?",
                    "La tormenta era real. Varios de estos hombres eran pescadores y creyeron que se iban a "
                    "ahogar. Su grito es el que todavía ora la gente con miedo: ¿no te importa? Jesús había "
                    "estado en la barca todo el tiempo. Calma el viento y el mar, y luego les pregunta por su "
                    "miedo, no para apartarlos sino para que aprendan quién está con ellos. Terminan la noche "
                    "con una pregunta más grande que la tormenta: ¿quién es este?",
                ),
                "simple": L(
                    "Jesus's friends were scared in a big storm. Jesus was right there in the boat with them, "
                    "and he made the storm stop. Jesus is with you when you are scared too.",
                    "Los amigos de Jesús tuvieron miedo en una gran tormenta. Jesús estaba ahí mismo, en la "
                    "barca con ellos, e hizo que la tormenta se detuviera. Jesús también está contigo cuando "
                    "tienes miedo.",
                ),
                "ask": L(
                    "Where does it feel as if Jesus is asleep in your situation? What changes if he is in "
                    "the boat with you?",
                    "¿En qué parte de tu situación sientes como si Jesús estuviera dormido? ¿Qué cambia si "
                    "él está en la barca contigo?",
                ),
                "kid_ask": L(
                    "What would you have said to Jesus in the boat?",
                    "¿Qué le habrías dicho tú a Jesús en la barca?",
                ),
                "do": L(
                    "Name your storm. Then pray the disciples' honest prayer in your own words: tell Jesus "
                    "you are afraid and ask him whether he cares. Sit quietly for two minutes afterward.",
                    "Ponle nombre a tu tormenta. Luego haz con tus palabras la oración sincera de los "
                    "discípulos: dile a Jesús que tienes miedo y pregúntale si le importa. Después quédate "
                    "dos minutos en silencio.",
                ),
                "kid_do": L(
                    "Draw the boat in the storm with Jesus in it. Draw yourself in the boat too.",
                    "Dibuja la barca en la tormenta con Jesús adentro. Dibújate a ti también en la barca.",
                ),
                "pray": L(
                    "Jesus, the waves look bigger than I am. Thank you that you have not left the boat. "
                    "Speak your calm into this storm, and into me.",
                    "Jesús, las olas se ven más grandes que yo. Gracias porque no te has bajado de la barca. "
                    "Pon tu calma en esta tormenta, y en mí.",
                ),
            },
            {
                "key": "fear-3",
                "ref": "Isaiah 41:10",
                "title": L("The reason not to fear", "La razón para no temer"),
                "truth": L(
                    "God says this to a small, threatened people far from home. He tells them not to be "
                    "afraid, and he gives a reason. The reason is not that the danger is imaginary. It is "
                    "who is with them: their God, who promises to strengthen them, help them and hold them "
                    "up with his own hand. In the Bible, the answer to fear is rarely an explanation. It is "
                    "almost always a presence.",
                    "Dios le dice esto a un pueblo pequeño y amenazado, lejos de su tierra. Les dice que no "
                    "teman y les da una razón. La razón no es que el peligro sea imaginario. Es quién está "
                    "con ellos: su Dios, que promete fortalecerlos, ayudarlos y sostenerlos con su propia "
                    "mano. En la Biblia, la respuesta al miedo rara vez es una explicación. Casi siempre es "
                    "una presencia.",
                ),
                "simple": L(
                    "God tells his people not to be afraid, because he is with them. He makes them strong "
                    "and holds them up with his hand.",
                    "Dios le dice a su pueblo que no tenga miedo, porque él está con ellos. Les da fuerza y "
                    "los sostiene con su mano.",
                ),
                "ask": L(
                    "Of the three things God promises here, strength, help, or being held up, which do you "
                    "need most this week, and for what?",
                    "De las tres cosas que Dios promete aquí, fuerza, ayuda o ser sostenido, ¿cuál necesitas "
                    "más esta semana, y para qué?",
                ),
                "kid_ask": L(
                    "When has someone holding your hand helped you feel brave?",
                    "¿Cuándo te ayudó a ser valiente que alguien te tomara de la mano?",
                ),
                "do": L(
                    "Before the thing you dread this week, open your hand, palm up, for a moment and ask God "
                    "for the strength for that one hour.",
                    "Antes de eso que temes esta semana, abre la mano con la palma hacia arriba un momento y "
                    "pídele a Dios la fuerza para esa sola hora.",
                ),
                "kid_do": L(
                    "Hold a grown-up's hand on a walk today. Remember that God holds on to you like that.",
                    "Toma la mano de un adulto en un paseo hoy. Recuerda que Dios te sostiene así.",
                ),
                "pray": L(
                    "God, you say you are with me. I need your strength for … Hold me up, because I cannot "
                    "hold myself up today.",
                    "Dios, tú dices que estás conmigo. Necesito tu fuerza para … Sostenme, porque hoy no "
                    "puedo sostenerme por mi cuenta.",
                ),
            },
            {
                "key": "fear-4",
                "ref": "Psalm 4:8",
                "title": L("Afraid at night", "Miedo por la noche"),
                "truth": L(
                    "Fears grow in the dark. David ends a day full of trouble by lying down and sleeping, "
                    "not because the trouble is gone but because the Lord is the one who keeps him safe. "
                    "Sleep is a quiet act of trust. For hours you stop standing guard, and God does not.",
                    "Los miedos crecen en la oscuridad. David termina un día lleno de problemas acostándose "
                    "a dormir, no porque los problemas se hayan ido, sino porque el Señor es quien lo "
                    "mantiene a salvo. Dormir es un acto callado de confianza. Durante horas dejas de montar "
                    "guardia, y Dios no.",
                ),
                "simple": L(
                    "At night God is still awake, taking care of you. You can lie down and sleep in peace.",
                    "De noche Dios sigue despierto, cuidándote. Puedes acostarte y dormir en paz.",
                ),
                "ask": L(
                    "Which fears get louder for you at night? What would it mean to let God keep watch "
                    "while you sleep?",
                    "¿Qué miedos se vuelven más fuertes para ti por la noche? ¿Qué significaría dejar que "
                    "Dios vigile mientras duermes?",
                ),
                "kid_ask": L(
                    "What helps you feel safe at bedtime?",
                    "¿Qué te ayuda a sentirte a salvo a la hora de dormir?",
                ),
                "do": L(
                    "Tonight, put your phone out of reach before bed. Name the fear that usually visits at "
                    "night, and hand the night watch to God in one sentence.",
                    "Esta noche deja el teléfono fuera de tu alcance antes de acostarte. Nombra el miedo que "
                    "suele visitarte de noche y entrégale a Dios la guardia nocturna en una frase.",
                ),
                "kid_do": L(
                    "At bedtime tonight, thank God for taking care of you while you sleep.",
                    "Esta noche, al acostarte, dale gracias a Dios por cuidarte mientras duermes.",
                ),
                "pray": L(
                    "Lord, I cannot guard myself or the people I love through the night. You can. I am "
                    "going to lie down now and leave the watch with you.",
                    "Señor, no puedo cuidarme ni cuidar a los que amo durante la noche. Tú sí. Ahora me voy "
                    "a acostar y te dejo la guardia a ti.",
                ),
            },
            {
                "key": "fear-5",
                "ref": "Romans 8:38-39",
                "title": L("What fear cannot take", "Lo que el miedo no puede quitar"),
                "truth": L(
                    "Fear always asks: what if? Paul does not answer that the bad thing will never happen; he "
                    "had lived through most of what people dread. He makes a list of the largest things there "
                    "are, death and life, present and future, every power, and says that none of them can "
                    "separate us from the love of God in Christ Jesus. Whatever happens, one thing remains "
                    "out of fear's reach.",
                    "El miedo siempre pregunta: ¿y si…? Pablo no responde que lo malo nunca pasará; él había "
                    "vivido casi todo lo que la gente teme. Hace una lista de las cosas más grandes que "
                    "existen, la muerte y la vida, lo presente y lo por venir, todo poder, y dice que ninguna "
                    "puede separarnos del amor de Dios en Cristo Jesús. Pase lo que pase, hay algo que queda "
                    "fuera del alcance del miedo.",
                ),
                "simple": L(
                    "Nothing in the whole world can take God's love away from you. Nothing at all.",
                    "Nada en todo el mundo puede quitarte el amor de Dios. Nada de nada.",
                ),
                "ask": L(
                    "Follow your fear to the end: what are you most afraid of losing? Is God's love on "
                    "Paul's list of things that can be taken?",
                    "Sigue tu miedo hasta el final: ¿qué es lo que más temes perder? ¿Está el amor de Dios "
                    "en la lista de Pablo de cosas que se pueden quitar?",
                ),
                "kid_ask": L(
                    "Can you think of anything bigger than God's love?",
                    "¿Se te ocurre algo más grande que el amor de Dios?",
                ),
                "do": L(
                    "Write your worst what-if on a piece of paper. Under it write: even then, I would still "
                    "be loved by God. Read both lines out loud.",
                    "Escribe en un papel tu peor ¿y si…? Debajo escribe: aun así, Dios me seguiría amando. "
                    "Lee las dos líneas en voz alta.",
                ),
                "kid_do": L(
                    "Draw a big heart and write your name inside it. That is you, inside God's love.",
                    "Dibuja un corazón grande y escribe tu nombre adentro. Ese eres tú, dentro del amor de Dios.",
                ),
                "pray": L(
                    "God, I am afraid of losing … Thank you that whatever comes, nothing can pull me out of "
                    "your love.",
                    "Dios, tengo miedo de perder … Gracias porque, venga lo que venga, nada puede sacarme "
                    "de tu amor.",
                ),
            },
        ],
    },
    {
        "key": "rest",
        "category": "peace",
        "title": L("Rest for the weary", "Descanso para quien está cansado"),
        "summary": L(
            "For when you are worn out, running on empty or close to burning out. Four readings on rest "
            "as a gift from God, not a prize for finishing everything.",
            "Para cuando ya no das más, andas sin fuerzas o al borde del agotamiento. Cuatro lecturas "
            "sobre el descanso como regalo de Dios, no como premio por terminarlo todo.",
        ),
        "keywords": [
            "tired", "exhaust", "weary", "burnout", "burned out", "worn out", "overwork", "drained",
            "insomni", "sabbath", "cansa", "agota", "descans", "fatiga", "rendid", "sin fuerzas",
        ],
        "situations": ["working", "parent", "single_parent", "caregiver", "leader", "student", "military"],
        "traits": ["peace", "trust", "humility"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "School, activities, a phone that never sleeps: you are allowed to stop, and God says so.",
                "Escuela, actividades, un teléfono que nunca duerme: tienes permiso para parar, y lo dice Dios.",
            ),
            "young_adult": L(
                "For years when resting feels like falling behind. Your worth was never your output.",
                "Para años en que descansar se siente como quedarse atrás. Tu valor nunca fue lo que produces.",
            ),
            "adult": L(
                "For people who hold up a job, a home and other people's needs, and cannot remember their last real day off.",
                "Para quienes sostienen un trabajo, un hogar y las necesidades de otros, y no recuerdan su último día libre de verdad.",
            ),
            "senior": L(
                "For a tiredness that sleep does not always fix, and for learning to rest without feeling useless.",
                "Para un cansancio que el sueño no siempre arregla, y para aprender a descansar sin sentirte inútil.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "rest-1",
                "ref": "Matthew 11:28-30",
                "title": L("Come as tired as you are", "Ven con todo tu cansancio"),
                "truth": L(
                    "Jesus invites everyone who is worn out and weighed down, with no conditions, and "
                    "promises them rest. Then he offers a yoke, the wooden frame that joins two animals so "
                    "they pull together. He does not say there will be nothing to carry. He says you will not "
                    "pull alone, and that the one beside you is gentle and humble. The rest he gives reaches "
                    "deeper than the body, down to the soul.",
                    "Jesús invita a todos los que están rendidos y cargados, sin condiciones, y les promete "
                    "descanso. Luego ofrece un yugo, el madero que une a dos animales para que tiren juntos. "
                    "No dice que no habrá nada que cargar. Dice que no vas a tirar por tu cuenta, y que quien "
                    "va a tu lado es manso y humilde. El descanso que da llega más hondo que el cuerpo: llega "
                    "al alma.",
                ),
                "simple": L(
                    "When you are very tired, Jesus says to come to him. He is gentle, and he helps you rest.",
                    "Cuando sientes mucho cansancio, Jesús te dice que vayas a él. Él es tierno y te ayuda a "
                    "descansar.",
                ),
                "ask": L(
                    "What is wearing you out that Jesus never asked you to carry alone, or never asked you "
                    "to carry at all?",
                    "¿Qué te está agotando que Jesús nunca te pidió cargar a solas, o que nunca te pidió "
                    "cargar?",
                ),
                "kid_ask": L(
                    "What makes you feel really tired?",
                    "¿Qué te cansa mucho?",
                ),
                "do": L(
                    "List everything you are carrying this week. Mark what is truly yours, what could be "
                    "shared, and what could be put down. Put one thing down today.",
                    "Haz una lista de todo lo que cargas esta semana. Marca lo que de verdad es tuyo, lo que "
                    "podrías compartir y lo que podrías soltar. Suelta una cosa hoy.",
                ),
                "kid_do": L(
                    "Sit quietly for one minute with a grown-up and tell Jesus one thing that made you "
                    "tired today.",
                    "Siéntate un minuto en silencio con un adulto y cuéntale a Jesús una cosa que te cansó hoy.",
                ),
                "pray": L(
                    "Jesus, I am tired in a way that sleep has not fixed. I am coming to you as I am. Teach "
                    "me to walk at your pace.",
                    "Jesús, tengo un cansancio que el sueño no ha quitado. Vengo a ti así como estoy. "
                    "Enséñame a caminar a tu paso.",
                ),
            },
            {
                "key": "rest-2",
                "ref": "Genesis 2:1-3",
                "title": L("Rest was there from the beginning", "El descanso estuvo desde el principio"),
                "truth": L(
                    "When the work of creation was finished, God rested, and he blessed that day and set it "
                    "apart. God was not exhausted. He was building rest into the shape of the world, as "
                    "something good and holy. So rest is not a reward for people who have finished "
                    "everything, and it is not laziness. It is part of how life was made to work, from the "
                    "first week.",
                    "Cuando terminó la obra de la creación, Dios descansó, y bendijo ese día y lo apartó. "
                    "Dios no estaba agotado. Estaba poniendo el descanso en la forma misma del mundo, como "
                    "algo bueno y santo. Así que el descanso no es un premio para quienes ya lo terminaron "
                    "todo, y tampoco es pereza. Es parte de cómo fue hecha la vida para funcionar, desde la "
                    "primera semana.",
                ),
                "simple": L(
                    "God made the whole world, and then God rested. He made rest a good thing for us too.",
                    "Dios hizo el mundo entero, y después descansó. También hizo que el descanso fuera algo "
                    "bueno para nosotros.",
                ),
                "ask": L(
                    "Do you treat rest as something you have to earn? Where did you learn that?",
                    "¿Tratas el descanso como algo que tienes que ganarte? ¿Dónde aprendiste eso?",
                ),
                "kid_ask": L(
                    "What is your favorite restful thing to do?",
                    "¿Cuál es tu manera favorita de descansar?",
                ),
                "do": L(
                    "Choose a block of time this week, even two hours, with no work, no errands and no "
                    "catching up. Put it on your calendar like any other appointment, and keep it.",
                    "Elige un bloque de tiempo esta semana, aunque sean dos horas, sin trabajo, sin "
                    "pendientes y sin ponerte al día. Anótalo en tu calendario como cualquier otra cita, y "
                    "cúmplelo.",
                ),
                "kid_do": L(
                    "Pick one quiet thing to do today, like reading, drawing or lying on the grass, and "
                    "thank God for rest.",
                    "Elige hoy algo tranquilo para hacer, como leer, dibujar o acostarte en el pasto, y dale "
                    "gracias a Dios por el descanso.",
                ),
                "pray": L(
                    "God, you rested and called it good. Free me from the idea that I must earn my rest. "
                    "Help me to stop, and to enjoy what you have made.",
                    "Dios, tú descansaste y lo llamaste bueno. Líbrame de la idea de que debo ganarme el "
                    "descanso. Ayúdame a parar y a disfrutar lo que has hecho.",
                ),
            },
            {
                "key": "rest-3",
                "ref": "Psalm 127:1-2",
                "title": L("You are not holding it all up", "No lo estás sosteniendo todo tú"),
                "truth": L(
                    "This psalm is not against hard work. It is against working as though everything "
                    "depended on you: getting up early, staying up late, eating your bread with anxiety. "
                    "That, it says, is wasted effort, because it is the Lord who builds the house and guards "
                    "the city. And to those he loves he gives sleep. Going to sleep is a small confession "
                    "that the world keeps running without you, because it is in other hands.",
                    "Este salmo no está en contra del trabajo duro. Está en contra de trabajar como si todo "
                    "dependiera de ti: madrugar, desvelarte, comer tu pan con ansiedad. Eso, dice, es "
                    "esfuerzo perdido, porque es el Señor quien edifica la casa y guarda la ciudad. Y a "
                    "quienes ama les da el sueño. Irte a dormir es una pequeña confesión de que el mundo "
                    "sigue andando sin ti, porque está en otras manos.",
                ),
                "simple": L(
                    "God takes care of the world even while you are asleep. Sleep is a gift from God.",
                    "Dios cuida el mundo incluso mientras duermes. El sueño es un regalo de Dios.",
                ),
                "ask": L(
                    "What are you afraid will happen if you stop?",
                    "¿Qué temes que pase si te detienes?",
                ),
                "kid_ask": L(
                    "Who takes care of everything while you are asleep?",
                    "¿Quién cuida de todo mientras tú duermes?",
                ),
                "do": L(
                    "Set a time to stop tonight and keep it. When you stop, say out loud what is unfinished "
                    "and leave it with God until morning.",
                    "Fija una hora para parar esta noche y respétala. Cuando pares, di en voz alta lo que "
                    "quedó sin terminar y déjalo con Dios hasta la mañana.",
                ),
                "kid_do": L(
                    "At bedtime, thank God for your bed and tell him goodnight.",
                    "A la hora de dormir, dale gracias a Dios por tu cama y dile buenas noches.",
                ),
                "pray": L(
                    "Lord, unless you build this, my long hours will not be enough. I leave what is "
                    "unfinished with you. Give me the sleep you give to those you love.",
                    "Señor, si tú no edificas esto, mis largas horas no alcanzarán. Dejo contigo lo que "
                    "quedó sin terminar. Dame el sueño que das a quienes amas.",
                ),
            },
            {
                "key": "rest-4",
                "ref": "Mark 6:30-32",
                "title": L("Jesus notices when you are spent", "Jesús nota cuando ya no puedes más"),
                "truth": L(
                    "The disciples come back from serving people and report everything they have done. So "
                    "many are coming and going that they have not even had a chance to eat. Jesus does not "
                    "hand them a new assignment. He tells them to come away with him to a quiet place and "
                    "rest a while. Burnout often finds people who are doing good things for others. Jesus "
                    "treats their tiredness as a real need, not as a weakness to push through.",
                    "Los discípulos regresan de servir a la gente y cuentan todo lo que han hecho. Es tanta "
                    "la gente que va y viene que ni siquiera han podido comer. Jesús no les da una nueva "
                    "tarea. Les dice que vayan con él a un lugar tranquilo y descansen un poco. El "
                    "agotamiento suele alcanzar a quienes hacen cosas buenas por otros. Jesús trata su "
                    "cansancio como una necesidad real, no como una debilidad que hay que aguantar.",
                ),
                "simple": L(
                    "Jesus's friends worked so hard that they had no time to eat. Jesus told them to come "
                    "and rest with him. Jesus cares when you are tired.",
                    "Los amigos de Jesús trabajaron tanto que no tuvieron tiempo de comer. Jesús les dijo "
                    "que fueran a descansar con él. A Jesús le importa cuando te cansas.",
                ),
                "ask": L(
                    "Which good thing that you do for others has left you empty? What would coming away "
                    "for a while look like in your real life?",
                    "¿Qué cosa buena que haces por otros te ha dejado sin nada? ¿Cómo sería apartarte un "
                    "rato en tu vida real?",
                ),
                "kid_ask": L(
                    "How can you tell when someone in your family is very tired?",
                    "¿Cómo te das cuenta cuando alguien de tu familia tiene mucho cansancio?",
                ),
                "do": L(
                    "Tell one person honestly how tired you are, and ask them to help you find one thing to "
                    "step back from this month. If weeks of rest do not lift the exhaustion, see a doctor; "
                    "that is taking your tiredness as seriously as Jesus does.",
                    "Dile a una persona con sinceridad cuánto cansancio tienes, y pídele que te ayude a "
                    "encontrar una cosa de la que puedas apartarte este mes. Si semanas de descanso no "
                    "quitan el agotamiento, consulta a un médico; eso es tomar tu cansancio tan en serio "
                    "como lo toma Jesús.",
                ),
                "kid_do": L(
                    "Help a tired grown-up rest today: do one small job for them without being asked.",
                    "Ayuda hoy a descansar a un adulto que tenga cansancio: haz por él o ella una tarea "
                    "pequeña sin que te la pida.",
                ),
                "pray": L(
                    "Jesus, you saw that your friends had not even eaten. You see me too. Show me the quiet "
                    "place, and give me the courage to go there with you.",
                    "Jesús, tú viste que tus amigos ni siquiera habían comido. A mí también me ves. "
                    "Muéstrame el lugar tranquilo y dame el valor de ir allí contigo.",
                ),
            },
        ],
    },
    {
        "key": "contentment",
        "category": "peace",
        "title": L("Contentment", "Contentamiento"),
        "summary": L(
            "For when what you have never feels like enough, or everyone else seems to have more. Four "
            "readings on a peace that does not wait for more.",
            "Para cuando lo que tienes nunca parece suficiente, o parece que los demás tienen más. "
            "Cuatro lecturas sobre una paz que no espera a tener más.",
        ),
        "keywords": [
            "content", "envy", "envious", "jealous", "compare", "comparison", "enough", "discontent",
            "dissatisf", "covet", "envidi", "celos", "insatisf", "suficiente", "comparar", "codici",
        ],
        "situations": ["single", "working", "job_seeking", "student", "retired", "parent"],
        "traits": ["contentment", "gratitude", "trust"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "When everyone online seems to have a better body, better friends and a better life, this is another way to see yours.",
                "Cuando en las redes todos parecen tener mejor cuerpo, mejores amigos y mejor vida, esta es otra forma de mirar la tuya.",
            ),
            "young_adult": L(
                "For the years when friends' careers, weddings and homes become a scoreboard. You were given your own road.",
                "Para los años en que las carreras, bodas y casas de tus amigos se vuelven un marcador. A ti se te dio tu propio camino.",
            ),
            "adult": L(
                "For the quiet ache of the life you thought you would have by now, and the pull of always needing a little more.",
                "Para el dolor callado por la vida que creías tener a estas alturas, y el tirón de necesitar siempre un poco más.",
            ),
            "senior": L(
                "For making peace with what was and was not, and finding that what you cannot lose is still yours.",
                "Para hacer las paces con lo que fue y lo que no fue, y descubrir que lo que no puedes perder sigue siendo tuyo.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "contentment-1",
                "ref": "Philippians 4:10-13",
                "title": L("A secret that is learned", "Un secreto que se aprende"),
                "truth": L(
                    "Paul says twice that he learned to be content. It did not come naturally to him, and "
                    "it will not to you. He learned it in both directions: with plenty and with hunger. He "
                    "writes from prison. The strength Christ gives him here is not power to achieve "
                    "whatever he wants. It is strength to be at peace in whatever situation he is in.",
                    "Pablo dice dos veces que aprendió a estar contento. No le salía de manera natural, y a "
                    "ti tampoco te saldrá. Lo aprendió en las dos direcciones: con abundancia y con hambre. "
                    "Escribe desde la cárcel. La fuerza que Cristo le da aquí no es poder para lograr lo que "
                    "quiera. Es fuerza para estar en paz en cualquier situación en que se encuentre.",
                ),
                "simple": L(
                    "Paul learned to be glad inside whether he had a lot or a little, because Jesus made "
                    "him strong.",
                    "Pablo aprendió a tener alegría por dentro tuviera mucho o poco, porque Jesús le daba "
                    "fuerzas.",
                ),
                "ask": L(
                    "When is contentment harder for you: when you have little, or when you have plenty and "
                    "still want more?",
                    "¿Cuándo te cuesta más el contentamiento: cuando tienes poco, o cuando tienes bastante "
                    "y aun así quieres más?",
                ),
                "kid_ask": L(
                    "Can you remember a time you were happy with something small?",
                    "¿Recuerdas alguna vez en que algo pequeño te hizo feliz?",
                ),
                "do": L(
                    "Each evening this week, finish this sentence in writing: Today I had enough of … "
                    "Learning contentment starts with noticing it.",
                    "Cada noche de esta semana completa por escrito esta frase: Hoy tuve suficiente de … "
                    "Aprender el contentamiento empieza por notarlo.",
                ),
                "kid_do": L(
                    "Find three things you already have that you are glad about, and tell a grown-up.",
                    "Busca tres cosas que ya tienes y que te alegran, y cuéntaselas a un adulto.",
                ),
                "pray": L(
                    "Lord, I have not learned this yet. Teach me to be at peace with what today holds, and "
                    "give me your strength for it.",
                    "Señor, todavía no he aprendido esto. Enséñame a estar en paz con lo que trae el día de "
                    "hoy, y dame tu fuerza para ello.",
                ),
            },
            {
                "key": "contentment-2",
                "ref": "Luke 12:15-21",
                "title": L("More is not the same as life", "Tener más no es lo mismo que vivir"),
                "truth": L(
                    "Jesus warns that a person's life is not made of how much they own, and tells of a "
                    "farmer with a harvest too big for his barns. The harvest is not the problem. The "
                    "problem is that the man talks only to himself, plans only for himself and believes "
                    "that once enough is stored he will finally be able to relax. His life ends before that "
                    "day comes. Jesus calls this being rich in things but poor toward God.",
                    "Jesús advierte que la vida de una persona no consiste en cuánto posee, y cuenta de un "
                    "agricultor con una cosecha demasiado grande para sus graneros. La cosecha no es el "
                    "problema. El problema es que el hombre solo habla consigo mismo, solo planea para sí "
                    "mismo y cree que cuando tenga suficiente guardado por fin podrá descansar. Su vida "
                    "termina antes de que llegue ese día. Jesús llama a esto ser rico en cosas pero pobre "
                    "delante de Dios.",
                ),
                "simple": L(
                    "Jesus says that having lots and lots of things is not what makes a good life. Loving "
                    "God and sharing are worth more.",
                    "Jesús dice que tener muchísimas cosas no es lo que hace buena la vida. Amar a Dios y "
                    "compartir valen más.",
                ),
                "ask": L(
                    "What are you storing up or chasing in the belief that then, at last, you will be able "
                    "to relax?",
                    "¿Qué estás acumulando o persiguiendo con la idea de que entonces, por fin, podrás "
                    "estar en paz?",
                ),
                "kid_ask": L(
                    "What matters more to you than toys or things?",
                    "¿Qué te importa más que los juguetes o las cosas?",
                ),
                "do": L(
                    "Give away one thing this week that you have been keeping just in case, and notice "
                    "what it stirs in you.",
                    "Regala esta semana una cosa que has guardado por si acaso, y fíjate en lo que eso "
                    "despierta en ti.",
                ),
                "kid_do": L(
                    "Choose one toy or book to share with someone today.",
                    "Elige un juguete o un libro para compartir con alguien hoy.",
                ),
                "pray": L(
                    "God, I keep thinking that a little more will be enough. Make me rich toward you, and "
                    "open my hands.",
                    "Dios, sigo pensando que con un poco más será suficiente. Hazme rico delante de ti, y "
                    "abre mis manos.",
                ),
            },
            {
                "key": "contentment-3",
                "ref": "John 21:20-22",
                "title": L("What about them?", "¿Y ellos qué?"),
                "truth": L(
                    "Peter has just been forgiven and given his own calling. Almost at once he turns "
                    "around, sees another disciple, and asks what will happen to him. Jesus answers that "
                    "the other man's path is not Peter's business; Peter's part is to follow. Comparison "
                    "is one of the quickest ways to lose contentment. You were not given someone else's "
                    "life to live, and they were not given yours.",
                    "Pedro acaba de ser perdonado y de recibir su propio llamado. Casi enseguida se da "
                    "vuelta, ve a otro discípulo y pregunta qué va a pasar con él. Jesús responde que el "
                    "camino del otro no es asunto de Pedro; lo que le toca a Pedro es seguirlo. Compararse "
                    "es una de las formas más rápidas de perder el contentamiento. No se te dio la vida de "
                    "otra persona para vivirla, ni a ella la tuya.",
                ),
                "simple": L(
                    "Peter looked at his friend and asked Jesus, what about him? Jesus told Peter to just "
                    "follow him. You do not have to be like anyone else.",
                    "Pedro miró a su amigo y le preguntó a Jesús: ¿y él qué? Jesús le dijo a Pedro que "
                    "simplemente lo siguiera. No tienes que ser como nadie más.",
                ),
                "ask": L(
                    "Whose life do you measure yours against? What has Jesus actually asked of you?",
                    "¿Con la vida de quién mides la tuya? ¿Qué te ha pedido Jesús a ti en realidad?",
                ),
                "kid_ask": L(
                    "Do you ever wish you had what a friend has? What was it?",
                    "¿A veces deseas tener lo que tiene un amigo? ¿Qué era?",
                ),
                "do": L(
                    "For three days, step away from the place where you compare most, whether a feed, a "
                    "group or a conversation. Each time you feel the pull, thank God for one thing on your "
                    "own road.",
                    "Durante tres días, aléjate del lugar donde más te comparas, sea una red social, un "
                    "grupo o una conversación. Cada vez que sientas el tirón, dale gracias a Dios por una "
                    "cosa de tu propio camino.",
                ),
                "kid_do": L(
                    "Tell a friend or a brother or sister one thing you like about them. Then thank God "
                    "for one thing about being you.",
                    "Dile a un amigo o a un hermano o hermana algo que te gusta de él o ella. Luego dale "
                    "gracias a Dios por algo de ser tú.",
                ),
                "pray": L(
                    "Jesus, I keep looking sideways at … Turn my eyes back to you. Show me the next step "
                    "on the road you gave me.",
                    "Jesús, sigo mirando de reojo a … Vuelve mis ojos hacia ti. Muéstrame el siguiente paso "
                    "en el camino que me diste.",
                ),
            },
            {
                "key": "contentment-4",
                "ref": "Hebrews 13:5-6",
                "title": L("Enough, because of who stays", "Suficiente, por quien se queda"),
                "truth": L(
                    "The writer says to keep free from the love of money and to be content with what you "
                    "have, and then gives the reason: God has promised never to leave you or abandon you. "
                    "Contentment is not pretending you need nothing. It is knowing that the one thing you "
                    "most need cannot be taken away. That is why the passage ends with courage: the Lord "
                    "is my helper, so I do not have to be afraid.",
                    "El autor dice que vivamos libres del amor al dinero y contentos con lo que tenemos, y "
                    "luego da la razón: Dios ha prometido que nunca te dejará ni te abandonará. El "
                    "contentamiento no es fingir que no necesitas nada. Es saber que lo que más necesitas "
                    "no te lo pueden quitar. Por eso el pasaje termina con valentía: el Señor es quien me "
                    "ayuda, así que no tengo por qué temer.",
                ),
                "simple": L(
                    "God promises never to leave you. That is better than having any thing.",
                    "Dios promete que nunca te va a dejar. Eso es mejor que tener cualquier cosa.",
                ),
                "ask": L(
                    "If you lost the thing you are most afraid of losing, what would you still have?",
                    "Si perdieras aquello que más temes perder, ¿qué seguirías teniendo?",
                ),
                "kid_ask": L(
                    "Who is always with you, even when you do not get what you want?",
                    "¿Quién está siempre contigo, aunque no consigas lo que quieres?",
                ),
                "do": L(
                    "This week, before you buy or wish for something, pause for ten seconds and ask: what "
                    "am I hoping this will give me?",
                    "Esta semana, antes de comprar o desear algo, detente diez segundos y pregúntate: ¿qué "
                    "espero que esto me dé?",
                ),
                "kid_do": L(
                    "Say this prayer in your own words: God, thank you that you never leave me.",
                    "Haz esta oración con tus palabras: Dios, gracias porque nunca me dejas.",
                ),
                "pray": L(
                    "God, you have said you will never leave me. Let that be enough for me today, more "
                    "than anything I could add to my life.",
                    "Dios, tú has dicho que nunca me dejarás. Que eso me baste hoy, más que cualquier cosa "
                    "que pudiera añadir a mi vida.",
                ),
            },
        ],
    },
    {
        "key": "gratitude",
        "category": "peace",
        "title": L("Gratitude", "Gratitud"),
        "summary": L(
            "For anyone who wants to notice the good they have been given, in easy seasons and hard "
            "ones. Four readings on thankfulness as a habit of the heart, not a forced smile.",
            "Para quien quiere notar lo bueno que ha recibido, en tiempos fáciles y difíciles. Cuatro "
            "lecturas sobre el agradecimiento como hábito del corazón, no como sonrisa forzada.",
        ),
        "keywords": [
            "thank", "grateful", "gratitud", "bless", "appreciat", "ungrateful", "complain",
            "gracias", "agradec", "bendic", "ingrat", "quej", "valorar",
        ],
        "situations": [],
        "traits": ["gratitude", "joy", "contentment"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "God gives us so many good things. Saying thank you helps us see them.",
                "Dios nos da muchísimas cosas buenas. Dar gracias nos ayuda a verlas.",
            ),
            "teen": L(
                "It is easy to see only what is missing. This trains your eyes to catch what is already there.",
                "Es fácil ver solo lo que falta. Esto entrena tus ojos para descubrir lo que ya está ahí.",
            ),
            "young_adult": L(
                "While you chase what is next, here is a way to receive what is now.",
                "Mientras persigues lo que sigue, aquí hay una forma de recibir lo que hay ahora.",
            ),
            "adult": L(
                "In full, hurried days, gratitude slows you down long enough to see who has been providing all along.",
                "En días llenos y apurados, la gratitud te frena lo suficiente para ver quién ha estado proveyendo todo el tiempo.",
            ),
            "senior": L(
                "A long life holds a long list of mercies. This is a chance to count them and to tell them.",
                "Una vida larga guarda una larga lista de misericordias. Esta es una ocasión para contarlas y para contárselas a otros.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "gratitude-1",
                "ref": "Luke 17:11-19",
                "title": L("The one who came back", "El que regresó"),
                "truth": L(
                    "Ten men with a skin disease that kept them away from everyone cry out to Jesus, and "
                    "all ten are healed on their way. Only one turns around, a Samaritan, a foreigner "
                    "nobody expected much from. He comes back praising God and thanks Jesus face to face. "
                    "All ten received the gift. Only one returned to the giver. Gratitude is that turning "
                    "back: noticing where the good came from, and saying so.",
                    "Diez hombres con una enfermedad de la piel que los mantenía lejos de todos claman a "
                    "Jesús, y los diez quedan sanos por el camino. Solo uno se da vuelta, un samaritano, "
                    "un extranjero del que nadie esperaba mucho. Regresa alabando a Dios y le da las "
                    "gracias a Jesús cara a cara. Los diez recibieron el regalo. Solo uno volvió a quien "
                    "se lo dio. La gratitud es ese volver: notar de dónde vino lo bueno, y decirlo.",
                ),
                "simple": L(
                    "Jesus helped ten men, and only one came back to say thank you. Jesus was glad he did. "
                    "We can be like the one who came back.",
                    "Jesús ayudó a diez hombres, y solo uno regresó a dar las gracias. A Jesús le alegró "
                    "que volviera. Nosotros podemos ser como el que regresó.",
                ),
                "ask": L(
                    "What good thing have you received lately and simply walked on from? Who do you need "
                    "to go back and thank?",
                    "¿Qué cosa buena recibiste hace poco y simplemente seguiste de largo? ¿A quién "
                    "necesitas volver para darle las gracias?",
                ),
                "kid_ask": L(
                    "Who did something kind for you this week?",
                    "¿Quién hizo algo bueno por ti esta semana?",
                ),
                "do": L(
                    "Go back to one person today, by message, call or visit, and thank them for something "
                    "specific they did. Then thank God for that person.",
                    "Vuelve hoy a una persona, por mensaje, llamada o visita, y dale las gracias por algo "
                    "concreto que hizo. Luego dale gracias a Dios por esa persona.",
                ),
                "kid_do": L(
                    "Say thank you to one person today for something they did for you. Then say thank you "
                    "to God too.",
                    "Dale las gracias hoy a una persona por algo que hizo por ti. Luego dale las gracias "
                    "también a Dios.",
                ),
                "pray": L(
                    "Jesus, I have taken so much and kept walking. Today I turn around. Thank you for …",
                    "Jesús, he recibido tanto y he seguido de largo. Hoy me doy vuelta. Gracias por …",
                ),
            },
            {
                "key": "gratitude-2",
                "ref": "Psalm 103:1-5",
                "title": L("Telling your soul to remember", "Decirle a tu alma que recuerde"),
                "truth": L(
                    "David is not talking to God here. He is talking to himself. He tells his own soul to "
                    "praise the Lord and not to forget what God has done, and then he begins a list: "
                    "forgiveness, healing, rescue, love and mercy, good things that renew his strength. "
                    "We forget kindness quickly and remember hurts for years. Gratitude is practiced "
                    "memory: choosing, on purpose, to call the good back to mind.",
                    "Aquí David no le habla a Dios. Se habla a sí mismo. Le dice a su propia alma que alabe "
                    "al Señor y que no olvide lo que Dios ha hecho, y entonces empieza una lista: perdón, "
                    "sanidad, rescate, amor y misericordia, cosas buenas que renuevan sus fuerzas. "
                    "Olvidamos pronto la bondad y recordamos las heridas por años. La gratitud es memoria "
                    "ejercitada: decidir, a propósito, traer lo bueno de vuelta a la mente.",
                ),
                "simple": L(
                    "It is easy to forget the good things God does. We can stop and remember them, one by one.",
                    "Es fácil olvidar las cosas buenas que hace Dios. Podemos detenernos y recordarlas, "
                    "una por una.",
                ),
                "ask": L(
                    "If you made your own list of what God has done for you, what are the first three "
                    "things on it?",
                    "Si hicieras tu propia lista de lo que Dios ha hecho por ti, ¿cuáles serían las "
                    "primeras tres cosas?",
                ),
                "kid_ask": L(
                    "What are three good things God has given you?",
                    "¿Cuáles son tres cosas buenas que Dios te ha dado?",
                ),
                "do": L(
                    "Start a list titled Do not forget. Write five things today and add one each day this "
                    "week. Read the whole list aloud on the seventh day.",
                    "Empieza una lista titulada No olvides. Escribe cinco cosas hoy y añade una cada día "
                    "de esta semana. Lee toda la lista en voz alta el séptimo día.",
                ),
                "kid_do": L(
                    "Draw three good things God has given you and put the drawing where you can see it.",
                    "Dibuja tres cosas buenas que Dios te ha dado y pon el dibujo donde lo puedas ver.",
                ),
                "pray": L(
                    "Lord, my soul forgets so fast. Today I remember: you gave me …, you forgave me, you "
                    "carried me through … Thank you.",
                    "Señor, mi alma olvida muy rápido. Hoy recuerdo: me diste …, me perdonaste, me "
                    "sostuviste en … Gracias.",
                ),
            },
            {
                "key": "gratitude-3",
                "ref": "Deuteronomy 8:10-14",
                "title": L("The danger of a full table", "El peligro de una mesa llena"),
                "truth": L(
                    "Moses is preparing people who have known hunger to enter a good land. His warning is "
                    "surprising: the risky moment is not the hard time but the comfortable one. When you "
                    "have eaten your fill, built good houses and watched everything you own grow, the "
                    "heart becomes proud and forgets the God who brought you out. So he tells them that "
                    "when they are full, they are to bless the Lord. Thanks keeps a full life from "
                    "becoming a forgetful one.",
                    "Moisés prepara a un pueblo que ha conocido el hambre para entrar a una buena tierra. "
                    "Su advertencia sorprende: el momento de riesgo no es el tiempo difícil sino el cómodo. "
                    "Cuando has comido hasta saciarte, has construido buenas casas y has visto crecer todo "
                    "lo que tienes, el corazón se vuelve orgulloso y olvida al Dios que te sacó adelante. "
                    "Por eso les dice que, cuando estén satisfechos, bendigan al Señor. Dar gracias evita "
                    "que una vida llena se vuelva una vida olvidadiza.",
                ),
                "simple": L(
                    "When we have plenty of food and a nice home, it is easy to forget who gave them to "
                    "us. Saying thank you to God helps us remember.",
                    "Cuando tenemos suficiente comida y una casa bonita, es fácil olvidar quién nos las "
                    "dio. Darle gracias a Dios nos ayuda a recordar.",
                ),
                "ask": L(
                    "What do you now take for granted that you once prayed for or could only hope for?",
                    "¿Qué das hoy por sentado que alguna vez pediste en oración o apenas te atrevías a esperar?",
                ),
                "kid_ask": L(
                    "What is your favorite food? Who helped it get to your table?",
                    "¿Cuál es tu comida favorita? ¿Quién ayudó a que llegara a tu mesa?",
                ),
                "do": L(
                    "At one meal each day this week, before you eat, stop and name where the food came "
                    "from: the hands, the work, the God who gave it.",
                    "En una comida de cada día de esta semana, antes de comer, detente y nombra de dónde "
                    "vino el alimento: las manos, el trabajo, el Dios que lo dio.",
                ),
                "kid_do": L(
                    "Before you eat today, thank God for your food and thank the person who made it.",
                    "Hoy, antes de comer, dale gracias a Dios por tu comida y dale las gracias a quien la "
                    "preparó.",
                ),
                "pray": L(
                    "God, I have eaten and I am full, and I had forgotten to say so. All of this came from "
                    "your hand. Thank you.",
                    "Dios, he comido y tengo de sobra, y había olvidado decirlo. Todo esto vino de tu "
                    "mano. Gracias.",
                ),
            },
            {
                "key": "gratitude-4",
                "ref": "1 Thessalonians 5:16-18",
                "title": L("In everything, not for everything", "En todo, no por todo"),
                "truth": L(
                    "Paul writes to a young church that was being mistreated for its faith. He tells them "
                    "to give thanks in every circumstance. He does not say to give thanks for every "
                    "circumstance. You are not asked to call a bad thing good, or to hide your tears "
                    "behind a cheerful face. You are asked to look, even on the worst day, for what is "
                    "still given and for the God who is still there.",
                    "Pablo escribe a una iglesia joven que sufría maltrato por su fe. Les dice que den "
                    "gracias en toda circunstancia. No dice que den gracias por toda circunstancia. No se "
                    "te pide llamar bueno a lo malo, ni esconder tus lágrimas detrás de una cara alegre. "
                    "Se te pide buscar, incluso en el peor día, lo que todavía se te da y al Dios que "
                    "todavía está ahí.",
                ),
                "simple": L(
                    "Even on a hard day there is something to thank God for. God is with you on good days "
                    "and on bad days.",
                    "Hasta en un día difícil hay algo por lo que dar gracias a Dios. Dios está contigo en "
                    "los días buenos y en los malos.",
                ),
                "ask": L(
                    "Think of the hardest part of your life right now. Without calling it good, what is "
                    "one thing you can honestly thank God for in the middle of it?",
                    "Piensa en la parte más difícil de tu vida ahora. Sin llamarla buena, ¿qué cosa puedes "
                    "agradecerle sinceramente a Dios en medio de ella?",
                ),
                "kid_ask": L(
                    "Think of a day that was hard. Was there one good thing in that day?",
                    "Piensa en un día que fue difícil. ¿Hubo alguna cosa buena en ese día?",
                ),
                "do": L(
                    "Tonight, write two honest lines: the hardest thing about today, and one thing in "
                    "today you are thankful for. Both lines are allowed to be true.",
                    "Esta noche escribe dos líneas sinceras: lo más difícil de hoy, y una cosa de hoy por "
                    "la que das gracias. Las dos líneas pueden ser verdad a la vez.",
                ),
                "kid_do": L(
                    "At bedtime, tell a grown-up one hard thing and one good thing from today. Thank God "
                    "for the good one.",
                    "A la hora de dormir, cuéntale a un adulto una cosa difícil y una cosa buena de hoy. "
                    "Dale gracias a Dios por la buena.",
                ),
                "pray": L(
                    "God, I will not pretend today was easy. And still, in it, I thank you for … Stay with "
                    "me tomorrow as well.",
                    "Dios, no voy a fingir que hoy fue fácil. Y aun así, dentro de este día, te doy "
                    "gracias por … Quédate conmigo mañana también.",
                ),
            },
        ],
    },
    {
        "key": "waiting",
        "category": "peace",
        "title": L("Waiting on God", "Esperar en Dios"),
        "summary": L(
            "For when you have prayed and nothing seems to change. Five readings for long waits and "
            "unanswered prayers, honest about the silence and about the God who is still there in it.",
            "Para cuando has orado y nada parece cambiar. Cinco lecturas para esperas largas y "
            "oraciones sin respuesta, sinceras sobre el silencio y sobre el Dios que sigue ahí.",
        ),
        "keywords": [
            "wait", "unanswered", "delay", "stuck", "how long", "impatien", "silence", "nothing changes",
            "esper", "sin respuesta", "demora", "estanc", "hasta cuándo", "impacien", "silencio", "nada cambia",
        ],
        "situations": ["single", "job_seeking", "ill", "caregiver", "moving", "exploring", "parent"],
        "traits": ["patience", "trust", "perseverance"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "When you have asked God for something again and again and heard nothing back, you are allowed to say so.",
                "Cuando le has pedido algo a Dios una y otra vez y no has oído nada, tienes permiso de decirlo.",
            ),
            "young_adult": L(
                "For waiting on a job, a person, a direction or a door that will not open, while others seem to move ahead.",
                "Para esperar un trabajo, una persona, un rumbo o una puerta que no se abre, mientras otros parecen avanzar.",
            ),
            "adult": L(
                "For prayers you have prayed for years: a child, a marriage, a diagnosis, a change that has not come.",
                "Para oraciones que llevas años haciendo: un hijo, un matrimonio, un diagnóstico, un cambio que no llega.",
            ),
            "senior": L(
                "For prayers still open after a lifetime, and for trusting God with what you may not see finished.",
                "Para oraciones que siguen abiertas después de toda una vida, y para confiarle a Dios lo que quizá no veas terminado.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "waiting-1",
                "ref": "Psalm 13:1-6",
                "title": L("How long?", "¿Hasta cuándo?"),
                "truth": L(
                    "David asks God how long four times in two verses. He feels forgotten, and he says so "
                    "to God's face. This prayer is in the Bible, which means you are permitted to pray it. "
                    "Then, with nothing changed around him, David decides to lean on God's faithful love "
                    "and remembers that God has been good to him. The waiting has not ended by the last "
                    "line. The trust has begun again.",
                    "David le pregunta a Dios hasta cuándo cuatro veces en dos versículos. Siente que lo "
                    "han olvidado, y se lo dice a Dios de frente. Esta oración está en la Biblia, lo cual "
                    "significa que tienes permiso de hacerla. Luego, sin que nada haya cambiado a su "
                    "alrededor, David decide apoyarse en el amor fiel de Dios y recuerda que Dios ha sido "
                    "bueno con él. La espera no ha terminado en la última línea. La confianza ha vuelto a "
                    "empezar.",
                ),
                "simple": L(
                    "Sometimes waiting feels very long. You can tell God that it is hard to wait. God "
                    "has not forgotten you.",
                    "A veces esperar se siente larguísimo. Puedes decirle a Dios que te cuesta esperar. "
                    "Dios no se ha olvidado de ti.",
                ),
                "ask": L(
                    "What is your own how long? Have you said it to God as bluntly as David does?",
                    "¿Cuál es tu propio hasta cuándo? ¿Se lo has dicho a Dios tan de frente como David?",
                ),
                "kid_ask": L(
                    "What is something you are waiting for that feels like it is taking forever?",
                    "¿Qué estás esperando que parece tardar una eternidad?",
                ),
                "do": L(
                    "Write your own four-line prayer: two lines that begin How long, one line that asks, "
                    "and one line that begins But I trust.",
                    "Escribe tu propia oración de cuatro líneas: dos que empiecen con Hasta cuándo, una "
                    "que pida, y una que empiece con Pero yo confío.",
                ),
                "kid_do": L(
                    "Tell God one thing that is hard to wait for, and ask him to help you wait.",
                    "Cuéntale a Dios algo que te cuesta esperar, y pídele que te ayude a esperar.",
                ),
                "pray": L(
                    "Lord, how long? I have waited for … and I feel forgotten. Look at me and answer. I am "
                    "choosing to lean on your love while I wait.",
                    "Señor, ¿hasta cuándo? He esperado … y siento que me olvidaste. Mírame y respóndeme. "
                    "Decido apoyarme en tu amor mientras espero.",
                ),
            },
            {
                "key": "waiting-2",
                "ref": "Luke 18:1-8",
                "title": L("Keep asking", "Sigue pidiendo"),
                "truth": L(
                    "Luke tells us why Jesus told this story: so that his followers would keep praying and "
                    "not give up. A widow with no power keeps coming to a judge who cares about no one, "
                    "until he finally acts. The point is the contrast. God is not that judge. If even he "
                    "listened in the end, how much more will a God who loves his people. Jesus admits "
                    "there will be waiting. What he is concerned about is that we might stop asking.",
                    "Lucas nos dice por qué Jesús contó esta historia: para que sus seguidores siguieran "
                    "orando y no se dieran por vencidos. Una viuda sin ningún poder insiste ante un juez a "
                    "quien nadie le importa, hasta que por fin actúa. La clave es el contraste. Dios no es "
                    "ese juez. Si hasta él terminó escuchando, cuánto más lo hará un Dios que ama a su "
                    "pueblo. Jesús reconoce que habrá espera. Lo que le preocupa es que dejemos de pedir.",
                ),
                "simple": L(
                    "Jesus says to keep praying and not give up. God loves you and always listens.",
                    "Jesús dice que sigas orando y no te rindas. Dios te ama y siempre escucha.",
                ),
                "ask": L(
                    "Is there a prayer you have quietly stopped praying? What made you stop?",
                    "¿Hay alguna oración que dejaste de hacer sin decirlo? ¿Qué te hizo dejarla?",
                ),
                "kid_ask": L(
                    "What is something you would like to keep asking God about?",
                    "¿Qué es algo que te gustaría seguir pidiéndole a Dios?",
                ),
                "do": L(
                    "Pick up one prayer you had given up on. Pray it once a day this week, in one sentence, "
                    "at the same time each day.",
                    "Retoma una oración que habías abandonado. Hazla una vez al día esta semana, en una "
                    "frase, a la misma hora cada día.",
                ),
                "kid_do": L(
                    "Choose one thing to pray about every night this week, in one sentence.",
                    "Elige una cosa por la que orar cada noche de esta semana, en una frase.",
                ),
                "pray": L(
                    "God, I had stopped asking about … because it hurt to keep hoping. I am asking again. "
                    "Keep my faith alive while I wait.",
                    "Dios, había dejado de pedirte por … porque dolía seguir esperando. Te lo pido otra "
                    "vez. Mantén viva mi fe mientras espero.",
                ),
            },
            {
                "key": "waiting-3",
                "ref": "Mark 14:32-36",
                "title": L("When the answer is not what you asked", "Cuando la respuesta no es lo que pediste"),
                "truth": L(
                    "The night before the cross, Jesus is overwhelmed with sorrow. He calls God by the "
                    "close family word for father and asks that the suffering ahead be taken away. Then he "
                    "gives himself to what the Father wants. The cup was not removed. So a prayer that is "
                    "not granted is no proof that your faith is weak or that God does not love you. It "
                    "happened to Jesus. He knows this kind of praying from the inside.",
                    "La noche antes de la cruz, Jesús está abrumado de tristeza. Llama a Dios con la "
                    "palabra cercana y familiar para decir padre, y le pide que aparte el sufrimiento que "
                    "viene. Luego se entrega a lo que el Padre quiere. La copa no fue apartada. Así que "
                    "una oración no concedida no prueba que tu fe sea débil ni que Dios no te ame. Le pasó "
                    "a Jesús. Él conoce esta manera de orar desde adentro.",
                ),
                "simple": L(
                    "Jesus asked his Father for something very hard, and he trusted his Father's answer. "
                    "When God's answer is not what we hoped, Jesus understands how that feels.",
                    "Jesús le pidió a su Padre algo muy difícil, y confió en la respuesta de su Padre. "
                    "Cuando la respuesta de Dios no es la que esperábamos, Jesús entiende cómo se siente.",
                ),
                "ask": L(
                    "Which prayer of yours has been answered with a no, or not yet? Can you pray both "
                    "halves of Jesus's prayer about it: what you want, and your trust?",
                    "¿Qué oración tuya ha recibido un no, o un todavía no? ¿Puedes orar por eso las dos "
                    "mitades de la oración de Jesús: lo que deseas, y tu confianza?",
                ),
                "kid_ask": L(
                    "Have you ever asked for something and the answer was no? How did it feel?",
                    "¿Alguna vez pediste algo y te dijeron que no? ¿Cómo te sentiste?",
                ),
                "do": L(
                    "Write the prayer that was not granted. Under it, write honestly how that has felt. "
                    "Then, only if you can mean it, add a line of trust. If you cannot yet, tell God that "
                    "instead.",
                    "Escribe la oración que no fue concedida. Debajo escribe con sinceridad cómo se ha "
                    "sentido eso. Luego, solo si puedes decirlo de verdad, añade una línea de confianza. "
                    "Si todavía no puedes, dile eso a Dios.",
                ),
                "kid_do": L(
                    "Tell God about a time you felt sad because the answer was no. Then ask a grown-up "
                    "for a hug.",
                    "Cuéntale a Dios de una vez en que te dio tristeza porque la respuesta fue no. Luego "
                    "pídele un abrazo a un adulto.",
                ),
                "pray": L(
                    "Father, you know what I asked for, and you know what it cost me when it did not come. "
                    "Jesus has prayed here before me. Help me to trust you with this.",
                    "Padre, tú sabes lo que pedí, y sabes lo que me costó que no llegara. Jesús ya oró "
                    "aquí antes que yo. Ayúdame a confiarte esto.",
                ),
            },
            {
                "key": "waiting-4",
                "ref": "Lamentations 3:22-26",
                "title": L("Enough mercy for this morning", "Misericordia suficiente para esta mañana"),
                "truth": L(
                    "These lines were written in the ruins of a destroyed city, in the middle of a book of "
                    "grief. Right there, the writer calls something to mind: the Lord's faithful love has "
                    "not run out, and his mercies arrive new every morning. He says it is good to wait "
                    "quietly for God's help. A long wait cannot be lived a year at a time. It is lived a "
                    "morning at a time, on that morning's mercy.",
                    "Estas líneas se escribieron entre las ruinas de una ciudad destruida, en medio de un "
                    "libro de dolor. Ahí mismo, el autor trae algo a la memoria: el amor fiel del Señor no "
                    "se ha agotado, y sus misericordias llegan nuevas cada mañana. Dice que es bueno "
                    "esperar en silencio la ayuda de Dios. Una espera larga no se puede vivir de año en "
                    "año. Se vive de mañana en mañana, con la misericordia de esa mañana.",
                ),
                "simple": L(
                    "Every single morning, God's love is brand new. He has enough love and help for you today.",
                    "Cada mañana, el amor de Dios está nuevecito. Él tiene suficiente amor y ayuda para ti hoy.",
                ),
                "ask": L(
                    "What mercy arrived this morning that you nearly missed because you were looking at "
                    "the thing that has not changed?",
                    "¿Qué misericordia llegó esta mañana que casi no viste por estar mirando lo que no ha "
                    "cambiado?",
                ),
                "kid_ask": L(
                    "What is one good thing about this morning?",
                    "¿Qué cosa buena tuvo esta mañana?",
                ),
                "do": L(
                    "For the next seven mornings, before you check anything else, name one mercy that is "
                    "new today. Ask only for what you need to wait well until tonight.",
                    "Durante las próximas siete mañanas, antes de revisar cualquier otra cosa, nombra una "
                    "misericordia que sea nueva hoy. Pide solo lo que necesitas para esperar bien hasta "
                    "la noche.",
                ),
                "kid_do": L(
                    "Tomorrow morning when you wake up, say: Thank you, God, for a new day.",
                    "Mañana, cuando despiertes, di: Gracias, Dios, por un día nuevo.",
                ),
                "pray": L(
                    "Lord, I cannot wait a whole year today. I can only wait until tonight. Give me this "
                    "morning's mercy, and let it be enough.",
                    "Señor, hoy no puedo esperar un año entero. Solo puedo esperar hasta esta noche. Dame "
                    "la misericordia de esta mañana, y que me baste.",
                ),
            },
            {
                "key": "waiting-5",
                "ref": "Habakkuk 3:17-19",
                "title": L("Even if nothing changes", "Aunque nada cambie"),
                "truth": L(
                    "Habakkuk pictures the worst for a farming people: no figs, no grapes, no olives, empty "
                    "fields and empty stalls. Then he says that even so he will rejoice in the Lord, "
                    "because God himself is his strength. He is not pretending; a verse earlier he is "
                    "trembling. He is deciding where his joy will be rooted: not in the outcome he is "
                    "waiting for, but in the God he is waiting on.",
                    "Habacuc imagina lo peor para un pueblo de agricultores: sin higos, sin uvas, sin "
                    "aceitunas, con los campos y los corrales vacíos. Y entonces dice que aun así se "
                    "alegrará en el Señor, porque Dios mismo es su fuerza. No está fingiendo; un versículo "
                    "antes está temblando. Está decidiendo dónde echará raíces su alegría: no en el "
                    "resultado que espera, sino en el Dios en quien espera.",
                ),
                "simple": L(
                    "Even when things do not go the way we want, God is still good and still makes us strong.",
                    "Aunque las cosas no salgan como queremos, Dios sigue siendo bueno y nos sigue dando fuerzas.",
                ),
                "ask": L(
                    "What is your even if? If the thing you are waiting for never came, what would you "
                    "still have in God?",
                    "¿Cuál es tu aunque? Si lo que esperas nunca llegara, ¿qué seguirías teniendo en Dios?",
                ),
                "kid_ask": L(
                    "When something does not go your way, what helps you feel better?",
                    "Cuando algo no sale como querías, ¿qué te ayuda a sentirte mejor?",
                ),
                "do": L(
                    "Write your own version of Habakkuk's prayer: three lines beginning Even if, naming "
                    "what might not come, and one line beginning Yet I will.",
                    "Escribe tu propia versión de la oración de Habacuc: tres líneas que empiecen con "
                    "Aunque, nombrando lo que tal vez no llegue, y una que empiece con Aun así yo.",
                ),
                "kid_do": L(
                    "Think of one thing that did not go your way today. Then thank God for one thing that "
                    "is still good.",
                    "Piensa en algo que hoy no salió como querías. Luego dale gracias a Dios por algo que "
                    "sigue siendo bueno.",
                ),
                "pray": L(
                    "God, even if … never comes, I want my joy to rest in you. I am not there yet. Be my "
                    "strength, and steady my feet.",
                    "Dios, aunque … nunca llegue, quiero que mi alegría descanse en ti. Todavía no llego "
                    "ahí. Sé mi fuerza y afirma mis pies.",
                ),
            },
        ],
    },
    # ======================================================================
    # REFUGE
    # ======================================================================
    {
        "key": "refuge",
        "category": "refuge",
        "title": L("God, a safe place", "Dios, un lugar seguro"),
        "summary": L(
            "For when life feels frightening or the ground keeps shifting under you. Four readings "
            "about God as a shelter you can run to, as you are, at any hour.",
            "Para cuando la vida asusta o el suelo no deja de moverse bajo tus pies. Cuatro lecturas "
            "sobre Dios como un refugio al que puedes correr, tal como estás, a cualquier hora.",
        ),
        "keywords": [
            "refuge", "safe", "shelter", "unstable", "chaos", "protect", "insecur", "crisis", "unsafe",
            "refugi", "seguridad", "a salvo", "protec", "proteg", "inestab", "caos", "amparo", "insegur",
        ],
        "situations": ["moving", "single_parent", "divorced", "military", "job_seeking", "caregiver", "ill"],
        "traits": ["trust", "peace", "courage"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "When things feel scary or keep changing, God is a safe place you can always go to.",
                "Cuando las cosas dan miedo o cambian mucho, Dios es un lugar seguro al que siempre puedes ir.",
            ),
            "teen": L(
                "When home, school or your own head does not feel safe, there is somewhere you can go that will not move.",
                "Cuando la casa, la escuela o tu propia cabeza no se sienten seguras, hay un lugar al que puedes ir que no se mueve.",
            ),
            "young_adult": L(
                "New city, new job, plans that fell through: when nothing around you is settled, here is solid ground.",
                "Ciudad nueva, trabajo nuevo, planes que se cayeron: cuando nada a tu alrededor está firme, aquí hay suelo firme.",
            ),
            "adult": L(
                "For the seasons when what you built starts to shake: a job, a marriage, a diagnosis, the news.",
                "Para las épocas en que lo que construiste empieza a temblar: un trabajo, un matrimonio, un diagnóstico, las noticias.",
            ),
            "senior": L(
                "As familiar things and people slip away, the one who has been your shelter all these years remains.",
                "Mientras cosas y personas conocidas se van, permanece quien ha sido tu refugio todos estos años.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "refuge-1",
                "ref": "Psalm 46:1-3",
                "title": L("When the ground moves", "Cuando el suelo se mueve"),
                "truth": L(
                    "This psalm does not say the ground will hold still. It imagines the worst, the earth "
                    "giving way and mountains falling into the sea, and says that even then there is "
                    "somewhere to go. God is a refuge and a source of strength, a help close at hand when "
                    "trouble comes. A refuge is a place you run to. Here it is not a place but a person, "
                    "and he is already near.",
                    "Este salmo no dice que el suelo se quedará quieto. Imagina lo peor, la tierra que cede "
                    "y los montes que caen al mar, y dice que aun entonces hay adónde ir. Dios es refugio y "
                    "fuente de fuerza, una ayuda que está a la mano cuando llega la angustia. Un refugio es "
                    "un lugar al que corres. Aquí no es un lugar sino una persona, y ya está cerca.",
                ),
                "simple": L(
                    "God is like a strong, safe place you can run to when things feel scary. He is always "
                    "close by to help.",
                    "Dios es como un lugar fuerte y seguro al que puedes correr cuando algo da miedo. "
                    "Siempre está cerca para ayudar.",
                ),
                "ask": L(
                    "What in your life is shaking right now? Where do you usually run first when you are "
                    "frightened?",
                    "¿Qué está temblando en tu vida ahora? ¿Adónde sueles correr primero cuando algo te "
                    "asusta?",
                ),
                "kid_ask": L(
                    "Where is a place you feel safe?",
                    "¿En qué lugar sientes que nada malo te va a pasar?",
                ),
                "do": L(
                    "Notice the first thing you reach for when you are afraid this week: your phone, food, "
                    "work, a person. Before you reach for it, take thirty seconds to run to God first, in "
                    "one sentence.",
                    "Fíjate esta semana en lo primero que buscas cuando tienes miedo: el teléfono, la "
                    "comida, el trabajo, una persona. Antes de buscarlo, toma treinta segundos para correr "
                    "primero a Dios, con una frase.",
                ),
                "kid_do": L(
                    "Draw your safe place. Then draw God's big hands around it.",
                    "Dibuja tu lugar seguro. Luego dibuja las manos grandes de Dios alrededor.",
                ),
                "pray": L(
                    "God, things I thought were solid are shaking. Be my refuge today. I am running to "
                    "you with …",
                    "Dios, cosas que yo creía firmes están temblando. Sé hoy mi refugio. Corro hacia ti "
                    "con …",
                ),
            },
            {
                "key": "refuge-2",
                "ref": "Psalm 62:5-8",
                "title": L("A place to pour it all out", "Un lugar para vaciar el corazón"),
                "truth": L(
                    "David tells his own soul to find its rest in God alone, his rock and his fortress. "
                    "Then he turns to everyone else with an invitation: trust God at all times, and pour "
                    "out your hearts before him. A refuge is not a place where you have to hold yourself "
                    "together. It is the place where you can finally stop. Nothing you pour out there, "
                    "fear, anger, confusion, will be too much for him.",
                    "David le dice a su propia alma que halle su descanso solo en Dios, su roca y su "
                    "fortaleza. Luego se vuelve hacia todos los demás con una invitación: confíen en Dios "
                    "en todo momento y derramen su corazón delante de él. Un refugio no es un lugar donde "
                    "tengas que mantenerte entero. Es el lugar donde por fin puedes dejar de hacerlo. Nada "
                    "de lo que derrames allí, miedo, enojo, confusión, será demasiado para él.",
                ),
                "simple": L(
                    "You can tell God everything in your heart: happy, sad, mad or scared. God is a safe "
                    "place for all of it.",
                    "Puedes contarle a Dios todo lo que hay en tu corazón: alegría, tristeza, enojo o "
                    "miedo. Dios es un lugar seguro para todo eso.",
                ),
                "ask": L(
                    "What have you been holding in because you think it is too much, or not proper to say "
                    "to God?",
                    "¿Qué te has guardado porque crees que es demasiado, o que no es correcto decírselo a "
                    "Dios?",
                ),
                "kid_ask": L(
                    "What is something in your heart you would like to tell God?",
                    "¿Qué hay en tu corazón que te gustaría contarle a Dios?",
                ),
                "do": L(
                    "Set a timer for ten minutes. Write or speak to God without editing anything, "
                    "everything that is in you. When the timer ends, sit in silence for one minute.",
                    "Pon un temporizador de diez minutos. Escríbele o háblale a Dios sin corregir nada, "
                    "todo lo que llevas dentro. Cuando suene, quédate un minuto en silencio.",
                ),
                "kid_do": L(
                    "Tell God three things: one happy thing, one sad thing and one thing you need help with.",
                    "Cuéntale a Dios tres cosas: una alegre, una triste y una en la que necesitas ayuda.",
                ),
                "pray": L(
                    "God, I have been holding myself together for everyone. With you I do not have to. "
                    "Here is all of it: …",
                    "Dios, he estado aguantando delante de todos. Contigo no tengo que hacerlo. Aquí está "
                    "todo: …",
                ),
            },
            {
                "key": "refuge-3",
                "ref": "Matthew 7:24-27",
                "title": L("The storm comes to both houses", "La tormenta llega a las dos casas"),
                "truth": L(
                    "Jesus describes two builders. Rain, floods and wind hit both of their houses; following "
                    "Jesus does not keep the storm away. The difference is underneath. One house rests on "
                    "rock: that is the person who hears what Jesus says and puts it into practice. A "
                    "foundation is laid in ordinary days, one small act of trust and obedience at a time, "
                    "long before the weather turns.",
                    "Jesús describe a dos constructores. La lluvia, los ríos y el viento golpean las dos "
                    "casas; seguir a Jesús no aleja la tormenta. La diferencia está debajo. Una casa "
                    "descansa sobre roca: esa es la persona que oye lo que Jesús dice y lo pone en "
                    "práctica. Un cimiento se pone en los días comunes, un pequeño acto de confianza y "
                    "obediencia a la vez, mucho antes de que cambie el clima.",
                ),
                "simple": L(
                    "A house built on rock stays standing in a storm. Listening to Jesus and doing what "
                    "he says is like building on rock.",
                    "Una casa construida sobre roca sigue en pie en la tormenta. Escuchar a Jesús y hacer "
                    "lo que él dice es como construir sobre roca.",
                ),
                "ask": L(
                    "What is one thing Jesus said that you have heard many times but not yet put into "
                    "practice?",
                    "¿Qué cosa dijo Jesús que has oído muchas veces pero todavía no has puesto en práctica?",
                ),
                "kid_ask": L(
                    "What happens to a sandcastle when the water comes? What about a big rock?",
                    "¿Qué le pasa a un castillo de arena cuando llega el agua? ¿Y a una roca grande?",
                ),
                "do": L(
                    "Choose one plain teaching of Jesus, such as forgiving someone, telling the truth or "
                    "giving quietly, and do it once today. That is one stone laid.",
                    "Elige una enseñanza sencilla de Jesús, como perdonar a alguien, decir la verdad o dar "
                    "sin que nadie lo vea, y hazla una vez hoy. Esa es una piedra puesta.",
                ),
                "kid_do": L(
                    "Build two block towers, one on a pillow and one on the floor. See which one stands "
                    "better, and talk about why.",
                    "Construye dos torres de bloques, una sobre una almohada y otra sobre el piso. Mira "
                    "cuál se sostiene mejor, y conversa sobre por qué.",
                ),
                "pray": L(
                    "Jesus, I have heard more of your words than I have lived. Help me do one of them "
                    "today, so that when the storm comes I am standing on you.",
                    "Jesús, he oído más palabras tuyas de las que he vivido. Ayúdame a practicar una hoy, "
                    "para que cuando llegue la tormenta yo esté firme sobre ti.",
                ),
            },
            {
                "key": "refuge-4",
                "ref": "Psalm 121:1-8",
                "title": L("The one who watches does not sleep", "Quien te cuida no duerme"),
                "truth": L(
                    "A traveler looks up at the hills ahead and asks where help will come from. The answer "
                    "is not the hills but the Lord who made them. Six times the psalm says that God keeps "
                    "or watches over his people, and it adds that he never dozes off. Every refuge people "
                    "build has gaps. This keeper has none: by day and by night, in your going out and "
                    "your coming home, now and always.",
                    "Un viajero levanta la vista hacia los montes que tiene por delante y pregunta de dónde "
                    "vendrá su ayuda. La respuesta no son los montes, sino el Señor que los hizo. Seis "
                    "veces el salmo dice que Dios guarda o cuida a su pueblo, y añade que nunca se queda "
                    "dormido. Todo refugio que la gente construye tiene huecos. Este guardián no tiene "
                    "ninguno: de día y de noche, cuando sales y cuando vuelves a casa, ahora y siempre.",
                ),
                "simple": L(
                    "God never falls asleep. He watches over you in the day and at night, wherever you go.",
                    "Dios nunca se queda dormido. Te cuida de día y de noche, adondequiera que vayas.",
                ),
                "ask": L(
                    "Where have you been looking for help lately? In which part of your day do you most "
                    "need to remember that you are watched over?",
                    "¿Dónde has buscado ayuda últimamente? ¿En qué parte de tu día necesitas más recordar "
                    "que alguien te cuida?",
                ),
                "kid_ask": L(
                    "When would you like to remember that God is watching over you?",
                    "¿En qué momento te gustaría recordar que Dios te está cuidando?",
                ),
                "do": L(
                    "Each time you go out your door and come back in this week, pause on the threshold "
                    "and remember that God keeps your going and your coming.",
                    "Cada vez que salgas por tu puerta y vuelvas a entrar esta semana, detente en el "
                    "umbral y recuerda que Dios cuida tu salida y tu regreso.",
                ),
                "kid_do": L(
                    "When you leave home and when you come back today, say: God is with me.",
                    "Hoy, cuando salgas de casa y cuando regreses, di: Dios está conmigo.",
                ),
                "pray": L(
                    "Lord, maker of heaven and earth, my help comes from you. Watch over me and those I "
                    "love today, in every coming and going.",
                    "Señor, creador del cielo y de la tierra, mi ayuda viene de ti. Cuídame hoy, y cuida "
                    "a los que amo, en cada salida y cada regreso.",
                ),
            },
        ],
    },
    {
        "key": "suffering",
        "category": "refuge",
        "title": L("Suffering and hardship", "Sufrimiento y adversidad"),
        "summary": L(
            "For when life hurts and you are asking why. Five readings that do not explain your pain "
            "away, but show a God who refuses to blame you, hears your questions and stays with you in it.",
            "Para cuando la vida duele y preguntas por qué. Cinco lecturas que no pretenden explicar tu "
            "dolor, sino mostrar a un Dios que no te culpa, escucha tus preguntas y se queda contigo.",
        ),
        "keywords": [
            "suffer", "hardship", "hurting", "painful", "trial", "afflict", "tragedy", "why god", "unfair",
            "sufr", "dolor", "prueba", "duele", "aflic", "tragedia", "adversi", "injust", "por qué dios",
        ],
        "situations": ["ill", "grieving", "caregiver", "divorced", "widowed", "job_seeking", "single_parent"],
        "traits": ["perseverance", "hope", "trust"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "When something painful has happened and the easy answers do not help, you can bring your real questions here.",
                "Cuando ha pasado algo doloroso y las respuestas fáciles no ayudan, aquí puedes traer tus preguntas de verdad.",
            ),
            "young_adult": L(
                "For the first time life breaks in a way you cannot fix, and for a faith that can be honest about it.",
                "Para la primera vez que la vida se rompe de un modo que no puedes arreglar, y para una fe que puede ser sincera al respecto.",
            ),
            "adult": L(
                "For the hard things that came anyway, in your body, your family or your work, and the question of where God is in them.",
                "Para las cosas duras que llegaron de todos modos, en tu cuerpo, tu familia o tu trabajo, y la pregunta de dónde está Dios en ellas.",
            ),
            "senior": L(
                "For old sorrows and new ones, and for the company of a God who has carried you through more than you can count.",
                "Para penas viejas y nuevas, y para la compañía de un Dios que te ha sostenido en más de lo que puedes contar.",
            ),
        },
        "sensitive": True,
        "lessons": [
            {
                "key": "suffering-1",
                "ref": "John 9:1-3",
                "title": L("Whose fault is it?", "¿De quién es la culpa?"),
                "truth": L(
                    "The disciples see a man born blind and assume someone must be to blame: he sinned, or "
                    "his parents did. Jesus rejects both options. He will not join the search for someone "
                    "to blame, and he turns their eyes to what God is about to do for the man. Jesus does "
                    "not explain all suffering here. But he shuts the door on the cruelest explanation: "
                    "that your pain is proof God is punishing you.",
                    "Los discípulos ven a un hombre ciego de nacimiento y dan por hecho que alguien tiene "
                    "la culpa: pecó él, o pecaron sus padres. Jesús rechaza las dos opciones. No se suma a "
                    "la búsqueda de un culpable, y dirige la mirada de ellos a lo que Dios está por hacer "
                    "en ese hombre. Jesús no explica aquí todo el sufrimiento. Pero cierra la puerta a la "
                    "explicación más cruel: que tu dolor es prueba de que Dios te está castigando.",
                ),
                "simple": L(
                    "When something sad or hard happens, it does not mean God is angry with you. Jesus "
                    "said so.",
                    "Cuando pasa algo triste o difícil, no significa que Dios esté enojado contigo. Jesús "
                    "lo dijo.",
                ),
                "ask": L(
                    "Have you been asking what you did to deserve this? What does Jesus's answer to his "
                    "disciples say to that question?",
                    "¿Te has preguntado qué hiciste para merecer esto? ¿Qué le dice a esa pregunta la "
                    "respuesta de Jesús a sus discípulos?",
                ),
                "kid_ask": L(
                    "Have you ever thought something sad happened because of you? You can tell a grown-up "
                    "about it.",
                    "¿Alguna vez pensaste que algo triste pasó por tu culpa? Puedes contárselo a un adulto.",
                ),
                "do": L(
                    "Write down the blaming thought you come back to most. Beneath it, write Jesus's answer "
                    "in your own words. Then say both out loud to one person you trust this week; blame "
                    "grows when it is kept secret.",
                    "Escribe el pensamiento de culpa al que más vuelves. Debajo, escribe con tus palabras "
                    "la respuesta de Jesús. Luego di las dos cosas en voz alta a una persona de confianza "
                    "esta semana; la culpa crece cuando se guarda en secreto.",
                ),
                "kid_do": L(
                    "Tell a grown-up about one hard thing, and ask for a hug.",
                    "Cuéntale a un adulto una cosa difícil, y pídele un abrazo.",
                ),
                "pray": L(
                    "Jesus, I have been asking whose fault this is, and often I blame myself. You did not "
                    "play that game. Free me from it, and show me where you are at work.",
                    "Jesús, me he preguntado de quién es la culpa, y muchas veces me culpo a mí. Tú no "
                    "entraste en ese juego. Líbrame de él y muéstrame dónde estás obrando.",
                ),
            },
            {
                "key": "suffering-2",
                "ref": "Psalm 22:1-5",
                "title": L("You are allowed to ask why", "Tienes permiso de preguntar por qué"),
                "truth": L(
                    "David cries out that God has abandoned him. He prays day and night and hears nothing. "
                    "Even so he still says my God, and he reminds himself that those who came before him "
                    "trusted and were not let down. Jesus prayed the first line of this psalm from the "
                    "cross. So asking God why is not unbelief. The Son of God did it. A cry of pain "
                    "addressed to God is still a prayer.",
                    "David clama que Dios lo ha abandonado. Ora de día y de noche y no oye nada. Aun así "
                    "sigue diciendo Dios mío, y se recuerda a sí mismo que quienes vinieron antes que él "
                    "confiaron y no quedaron defraudados. Jesús oró la primera línea de este salmo desde "
                    "la cruz. Así que preguntarle a Dios por qué no es incredulidad. Lo hizo el Hijo de "
                    "Dios. Un grito de dolor dirigido a Dios sigue siendo una oración.",
                ),
                "simple": L(
                    "When you are very sad, you can ask God why. Your questions do not upset God. He listens.",
                    "Cuando tienes mucha tristeza, puedes preguntarle a Dios por qué. Tus preguntas no "
                    "molestan a Dios. Él escucha.",
                ),
                "ask": L(
                    "What is the why you have been afraid to say to God? What would it be like to say it "
                    "and still call him my God?",
                    "¿Cuál es el porqué que has tenido miedo de decirle a Dios? ¿Cómo sería decírselo y "
                    "seguir llamándolo Dios mío?",
                ),
                "kid_ask": L(
                    "What is one question you would like to ask God?",
                    "¿Qué pregunta te gustaría hacerle a Dios?",
                ),
                "do": L(
                    "Pray your why out loud today, in the plainest words you have. Do not tidy it up. Then "
                    "add one true thing you still know about God, however small.",
                    "Ora hoy tu porqué en voz alta, con las palabras más sencillas que tengas. No lo "
                    "arregles. Luego añade una cosa verdadera que todavía sabes de Dios, por pequeña que sea.",
                ),
                "kid_do": L(
                    "Tell God one question you have for him. Then tell a grown-up the same question.",
                    "Dile a Dios una pregunta que tengas para él. Luego hazle la misma pregunta a un adulto.",
                ),
                "pray": L(
                    "My God, why? I have called and I do not hear you. I am still calling you mine. Do "
                    "not be far from me.",
                    "Dios mío, ¿por qué? Te he llamado y no te oigo. Sigo llamándote mío. No te alejes "
                    "de mí.",
                ),
            },
            {
                "key": "suffering-3",
                "ref": "Isaiah 43:1-2",
                "title": L("Through, not around", "A través, no alrededor"),
                "truth": L(
                    "God speaks to a people far from home and begins with who they are: made by him, "
                    "called by name, his own. Then he speaks of deep water, rivers and fire, and the word "
                    "he uses is when, not if. He does not promise a way around. He promises his company on "
                    "the way through, and that the flood and the fire will not have the last word over "
                    "someone who belongs to him.",
                    "Dios le habla a un pueblo lejos de su tierra y empieza por decirles quiénes son: "
                    "hechos por él, llamados por su nombre, suyos. Luego habla de aguas profundas, ríos y "
                    "fuego, y la palabra que usa es cuando, no si acaso. No promete un camino alrededor. "
                    "Promete su compañía al atravesarlos, y que la inundación y el fuego no tendrán la "
                    "última palabra sobre alguien que le pertenece.",
                ),
                "simple": L(
                    "God knows your name, and you belong to him. When hard things come, God goes through "
                    "them with you.",
                    "Dios sabe tu nombre, y tú eres suyo. Cuando llegan cosas difíciles, Dios las "
                    "atraviesa contigo.",
                ),
                "ask": L(
                    "What water are you passing through right now? Where, even faintly, have you noticed "
                    "that you were not alone in it?",
                    "¿Qué aguas estás atravesando ahora? ¿Dónde has notado, aunque sea apenas, que no "
                    "estabas sin compañía en ellas?",
                ),
                "kid_ask": L(
                    "Who stays with you when something is hard?",
                    "¿Quién se queda contigo cuando algo es difícil?",
                ),
                "do": L(
                    "You were not meant to go through this without people either. This week tell one "
                    "trusted person what you are really facing: a friend, a pastor, or a doctor or "
                    "counselor if the strain is affecting your health or your sleep.",
                    "Tampoco fuiste hecho para atravesar esto sin gente a tu lado. Esta semana cuéntale a "
                    "una persona de confianza lo que de verdad enfrentas: un amigo, un pastor, o un médico "
                    "o consejero si la carga está afectando tu salud o tu sueño.",
                ),
                "kid_do": L(
                    "Write your name on a piece of paper and decorate it. Remember: God knows your name.",
                    "Escribe tu nombre en un papel y decóralo. Recuerda: Dios sabe tu nombre.",
                ),
                "pray": L(
                    "God, you call me by name and say I am yours. The water is deep. Do not let it sweep "
                    "me away. Walk through it with me.",
                    "Dios, tú me llamas por mi nombre y dices que soy tuyo. El agua está honda. No dejes "
                    "que me arrastre. Atraviésala conmigo.",
                ),
            },
            {
                "key": "suffering-4",
                "ref": "Hebrews 4:14-16",
                "title": L("A God who knows from the inside", "Un Dios que lo sabe desde adentro"),
                "truth": L(
                    "A high priest was the person who stood before God on behalf of the people. This "
                    "passage says Jesus is that for us, and that he is not out of touch with what we go "
                    "through: he was tested in every way we are, and he understands weakness. The "
                    "Christian claim is not that God explains suffering from a distance. It is that he "
                    "entered it. So you can come to him with confidence, and find mercy and help when you "
                    "need them.",
                    "Un sumo sacerdote era la persona que se presentaba ante Dios en nombre del pueblo. "
                    "Este pasaje dice que Jesús es eso para nosotros, y que no es ajeno a lo que vivimos: "
                    "fue puesto a prueba en todo igual que nosotros, y entiende la debilidad. Lo que "
                    "afirman los cristianos no es que Dios explique el sufrimiento desde lejos. Es que "
                    "entró en él. Por eso puedes acercarte a él con confianza, y hallar misericordia y "
                    "ayuda cuando las necesitas.",
                ),
                "simple": L(
                    "Jesus knows what it feels like to be sad, tired and hurt. He understands you, and "
                    "you can always ask him for help.",
                    "Jesús sabe lo que se siente tener tristeza, cansancio y dolor. Él te entiende, y "
                    "siempre puedes pedirle ayuda.",
                ),
                "ask": L(
                    "What part of your pain do you assume nobody could understand? What changes if Jesus "
                    "understands it?",
                    "¿Qué parte de tu dolor das por hecho que nadie podría entender? ¿Qué cambia si Jesús "
                    "la entiende?",
                ),
                "kid_ask": L(
                    "How does it feel when someone really understands you?",
                    "¿Cómo te sientes cuando alguien te entiende de verdad?",
                ),
                "do": L(
                    "Today, tell Jesus about the hardest part as you would tell someone who has been "
                    "through it, with no explaining and no apologizing. Then ask for one specific help for "
                    "this day.",
                    "Hoy cuéntale a Jesús la parte más difícil como se la contarías a alguien que ya pasó "
                    "por eso, sin explicar ni disculparte. Luego pídele una ayuda concreta para este día.",
                ),
                "kid_do": L(
                    "Tell Jesus one thing that hurt today. He understands.",
                    "Cuéntale a Jesús una cosa que te dolió hoy. Él entiende.",
                ),
                "pray": L(
                    "Jesus, you know weakness and pain from the inside. I do not have to explain this to "
                    "you. I need mercy, and I need help with … today.",
                    "Jesús, tú conoces la debilidad y el dolor desde adentro. No tengo que explicarte "
                    "esto. Necesito misericordia, y necesito ayuda con … hoy.",
                ),
            },
            {
                "key": "suffering-5",
                "ref": "2 Corinthians 1:3-7",
                "title": L("Comfort that gets passed on", "Un consuelo que se comparte"),
                "truth": L(
                    "Paul calls God the Father of compassion and the God of all comfort, who comes "
                    "alongside us in every trouble. Then he notices what comfort does: once received, it "
                    "can be given to someone else in trouble. Paul does not say God sends pain to make us "
                    "useful. He says the comfort you receive is never wasted. It also means that others "
                    "who have suffered are carrying something that could help you now.",
                    "Pablo llama a Dios Padre de compasión y Dios de todo consuelo, el que se pone a "
                    "nuestro lado en cada dificultad. Luego observa lo que hace el consuelo: una vez "
                    "recibido, puede darse a otra persona que sufre. Pablo no dice que Dios mande el dolor "
                    "para hacernos útiles. Dice que el consuelo que recibes nunca se desperdicia. También "
                    "significa que otros que han sufrido llevan consigo algo que podría ayudarte ahora.",
                ),
                "simple": L(
                    "God comforts us when we are sad. Then we can comfort other people when they are sad.",
                    "Dios nos consuela cuando sentimos tristeza. Después nosotros podemos consolar a "
                    "otras personas cuando ellas la sienten.",
                ),
                "ask": L(
                    "Who has comforted you well, and what did they actually do? Is there someone whose "
                    "experience you could lean on now?",
                    "¿Quién te ha consolado bien, y qué fue lo que hizo? ¿Hay alguien en cuya experiencia "
                    "podrías apoyarte ahora?",
                ),
                "kid_ask": L(
                    "Who comforts you when you are sad? What do they do?",
                    "¿Quién te consuela cuando tienes tristeza? ¿Qué hace esa persona?",
                ),
                "do": L(
                    "Reach out to one person who has been through something like yours and ask how they "
                    "got through. Or, if you are further along, send a note to someone who is where you "
                    "once were. If your pain feels too heavy to carry, tell a pastor, doctor or counselor "
                    "as well.",
                    "Busca a una persona que haya pasado por algo parecido a lo tuyo y pregúntale cómo "
                    "salió adelante. O, si ya vas más adelante, escríbele a alguien que está donde tú "
                    "estuviste. Si tu dolor pesa demasiado para cargarlo, cuéntaselo también a un pastor, "
                    "médico o consejero.",
                ),
                "kid_do": L(
                    "Comfort someone today: give a hug, draw them a picture or sit beside them.",
                    "Consuela a alguien hoy: dale un abrazo, hazle un dibujo o siéntate a su lado.",
                ),
                "pray": L(
                    "God of all comfort, come alongside me in this. Send me someone who understands, and "
                    "one day let what I receive from you reach someone else.",
                    "Dios de todo consuelo, ponte a mi lado en esto. Envíame a alguien que entienda, y "
                    "que un día lo que recibo de ti alcance a otra persona.",
                ),
            },
        ],
    },
    # @@NEXT@@
]
