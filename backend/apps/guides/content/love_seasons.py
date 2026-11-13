from apps.guides.catalog import L

TOPICS = [
    # ======================================================================
    # LOVE
    # ======================================================================
    {
        "key": "loving_god",
        "category": "love",
        "title": L("Loving God", "Amar a Dios"),
        "summary": L(
            "For anyone who wonders what it really means to love a God you cannot see. Five short readings "
            "on loving God with heart, soul, mind and strength, starting from the fact that he loved you first.",
            "Para quien se pregunta qué significa de verdad amar a un Dios que no se ve. Cinco lecturas breves "
            "sobre amar a Dios con el corazón, el alma, la mente y las fuerzas, sabiendo que él te amó primero.",
        ),
        "keywords": [
            "love god",
            "worship",
            "devot",
            "close to god",
            "far from god",
            "obey",
            "lukewarm",
            "amar a dios",
            "ador",
            "devoc",
            "cerca de dios",
            "lejos de dios",
            "obedec",
            "tibi",
        ],
        "situations": ["new_believer", "returning"],
        "traits": ["love", "faithfulness", "prayerfulness"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "God loves you very much. You can love God back with your words, your thoughts and what you do.",
                "Dios te ama muchísimo. Tú también puedes amarlo con tus palabras, tus pensamientos y lo que haces.",
            ),
            "teen": L(
                "Loving God is not a feeling you have to fake. It is something you can learn, honestly, "
                "from wherever you are.",
                "Amar a Dios no es un sentimiento que tengas que fingir. Es algo que se aprende, con honestidad, "
                "desde donde estés.",
            ),
            "young_adult": L(
                "So much is competing for your heart. This is about what you love most, and how that shapes "
                "everything else.",
                "Muchas cosas compiten por tu corazón. Esto trata de lo que más amas y de cómo eso le da forma "
                "a todo lo demás.",
            ),
            "adult": L(
                "For when faith has become one more duty on the list, and you want to love God again and not "
                "only work for him.",
                "Para cuando la fe se volvió un deber más en la lista y quieres volver a amar a Dios, no solo "
                "trabajar para él.",
            ),
            "senior": L(
                "Over many years love can deepen or go quiet. These readings are an invitation back to the "
                "first thing.",
                "Con los años el amor puede hacerse más hondo o apagarse. Estas lecturas son una invitación a "
                "volver a lo primero.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "loving_god-1",
                "ref": "Mark 12:28-31",
                "title": L("All of you", "Todo lo que eres"),
                "truth": L(
                    "A teacher of the law asks Jesus which commandment matters most. Jesus does not answer with "
                    "a rule about behavior. He names a relationship: love God with heart, soul, mind and "
                    "strength, and love your neighbor as yourself. Those four words are not four separate "
                    "tasks. Together they mean all of you: what you feel, who you are, how you think and where "
                    "your energy goes. God is not asking for a slice of your week. He is asking for you.",
                    "Un maestro de la ley le pregunta a Jesús cuál es el mandamiento más importante. Jesús no "
                    "responde con una regla de conducta. Nombra una relación: amar a Dios con el corazón, el "
                    "alma, la mente y las fuerzas, y amar al prójimo como a ti mismo. Esas cuatro palabras no "
                    "son cuatro tareas distintas. Juntas quieren decir todo lo que eres: lo que sientes, quién "
                    "eres, cómo piensas y en qué gastas tu energía. Dios no pide un pedazo de tu semana. Te "
                    "pide a ti.",
                ),
                "simple": L(
                    "Jesus said the most important thing is to love God with everything you are, and to love "
                    "other people too.",
                    "Jesús dijo que lo más importante es amar a Dios con todo lo que eres, y amar también a "
                    "las demás personas.",
                ),
                "ask": L(
                    "Of heart, soul, mind and strength, which one do you most easily leave out when it comes "
                    "to God?",
                    "De corazón, alma, mente y fuerzas, ¿cuál es la que más fácilmente dejas fuera cuando se "
                    "trata de Dios?",
                ),
                "kid_ask": L(
                    "What is one way you can show God that you love him?",
                    "¿De qué manera puedes mostrarle a Dios que lo amas?",
                ),
                "do": L(
                    "Take the one you named and give God ten minutes of it today: ten minutes of honest "
                    "feeling, of quiet, of thinking over one verse, or of doing something for someone.",
                    "Toma la que nombraste y dale a Dios diez minutos de ella hoy: diez minutos de sentir con "
                    "honestidad, de silencio, de pensar en un versículo o de hacer algo por alguien.",
                ),
                "kid_do": L(
                    "Tell God, in your own words, one thing you love about him.",
                    "Dile a Dios, con tus propias palabras, una cosa que te encanta de él.",
                ),
                "pray": L(
                    "God, I want to love you with all of me, not only the tidy parts. Show me where I have "
                    "been holding back.",
                    "Dios, quiero amarte con todo lo que soy, no solo con las partes ordenadas. Muéstrame "
                    "dónde me he estado guardando.",
                ),
            },
            {
                "key": "loving_god-2",
                "ref": "1 John 4:16-19",
                "title": L("He loved first", "Él amó primero"),
                "truth": L(
                    "John does not begin with your love for God. He begins with God's love for you, and says "
                    "that God is love. Our love is an answer, not an opening offer. That changes how the "
                    "great commandment sounds. You are not being told to work up a feeling in order to win "
                    "God over. You are being invited to respond to someone who already loves you, and whose "
                    "love pushes the dread of punishment out of the room.",
                    "Juan no empieza por tu amor a Dios. Empieza por el amor de Dios hacia ti, y dice que Dios "
                    "es amor. Nuestro amor es una respuesta, no la primera oferta. Eso cambia cómo suena el "
                    "gran mandamiento. No se te pide fabricar un sentimiento para ganarte a Dios. Se te invita "
                    "a responder a alguien que ya te ama, y cuyo amor saca de la habitación el miedo al "
                    "castigo.",
                ),
                "simple": L(
                    "God loved you before you ever loved him. When we love God, we are answering, "
                    '"I love you too."',
                    "Dios te amó antes de que tú lo amaras. Cuando amamos a Dios, le estamos respondiendo: "
                    '"Yo también te amo".',
                ),
                "ask": L(
                    "When you think of God, do you mostly feel loved or mostly feel watched? Where did that "
                    "picture come from?",
                    "Cuando piensas en Dios, ¿sientes sobre todo que te ama o sobre todo que te vigila? ¿De "
                    "dónde salió esa imagen?",
                ),
                "kid_ask": L(
                    "How do you know when someone loves you?",
                    "¿Cómo sabes cuando alguien te quiere?",
                ),
                "do": L(
                    "Before you ask God for anything today, sit for two minutes and say only this: you loved "
                    "me first. Let that be the whole prayer.",
                    "Hoy, antes de pedirle algo a Dios, quédate dos minutos en silencio y dile solo esto: tú "
                    "me amaste primero. Que esa sea toda la oración.",
                ),
                "kid_do": L(
                    "Draw one good thing God has given you because he loves you.",
                    "Dibuja una cosa buena que Dios te ha dado porque te ama.",
                ),
                "pray": L(
                    "God, you loved me before I did anything for you. Help me believe that today, and let my "
                    "love for you grow out of it.",
                    "Dios, me amaste antes de que yo hiciera algo por ti. Ayúdame a creerlo hoy, y que de ahí "
                    "crezca mi amor por ti.",
                ),
            },
            {
                "key": "loving_god-3",
                "ref": "Deuteronomy 6:4-9",
                "title": L("Love in an ordinary day", "Amor en un día cualquiera"),
                "truth": L(
                    "These are the words Jesus was quoting. Israel was to keep them close every day. Notice "
                    "where Moses places love for God: not only in holy places, but at home, on the road, at "
                    "bedtime and on waking. Loving God with your mind means letting his words stay in your "
                    "thoughts as the day goes on. It is less about one intense moment and more about many "
                    "small turnings of attention toward him.",
                    "Estas son las palabras que Jesús estaba citando. Israel debía tenerlas cerca todos los "
                    "días. Fíjate dónde pone Moisés el amor a Dios: no solo en lugares sagrados, sino en casa, "
                    "en el camino, al acostarse y al levantarse. Amar a Dios con la mente es dejar que sus "
                    "palabras se queden en tus pensamientos a lo largo del día. No se trata tanto de un "
                    "momento intenso como de muchas pequeñas veces en que vuelves la atención hacia él.",
                ),
                "simple": L(
                    "You can think about God anywhere: at home, on the way to school, and when you go to bed.",
                    "Puedes pensar en Dios en cualquier lugar: en casa, camino a la escuela y cuando te vas "
                    "a dormir.",
                ),
                "ask": L(
                    "At what ordinary point in your day (the commute, the dishes, the last minutes before "
                    "sleep) could you turn your thoughts toward God?",
                    "¿En qué momento común de tu día (el trayecto, los platos, los últimos minutos antes de "
                    "dormir) podrías volver tus pensamientos hacia Dios?",
                ),
                "kid_ask": L(
                    "When during your day could you talk to God?",
                    "¿En qué momento de tu día podrías hablar con Dios?",
                ),
                "do": L(
                    "Choose one short phrase from today's passage, put it where you will see it (a mirror, a "
                    "door, your phone screen), and say it to God each time you pass.",
                    "Elige una frase corta del pasaje de hoy, ponla donde la veas (un espejo, una puerta, la "
                    "pantalla del teléfono) y dísela a Dios cada vez que pases.",
                ),
                "kid_do": L(
                    "Say good morning to God when you wake up tomorrow.",
                    "Mañana, al despertar, dile buenos días a Dios.",
                ),
                "pray": L(
                    "Lord, be in my thoughts when I get up and when I lie down. Teach me to remember you in "
                    "the middle of ordinary things.",
                    "Señor, quédate en mis pensamientos cuando me levanto y cuando me acuesto. Enséñame a "
                    "recordarte en medio de las cosas de todos los días.",
                ),
            },
            {
                "key": "loving_god-4",
                "ref": "John 14:21-24",
                "title": L("Love that does something", "Un amor que hace algo"),
                "truth": L(
                    "Jesus ties love to action. The person who loves him is the one who holds on to what he "
                    "said and does it. This is not a way of earning his love, which came first. It is what "
                    "love looks like when it has hands, the way love for a friend shows in keeping your word "
                    "to them. And Jesus adds a promise: he and the Father will come and make their home with "
                    "the one who loves him. Obedience is not cold duty. It is how the friendship grows close.",
                    "Jesús une el amor con la acción. Quien lo ama es quien guarda lo que él dijo y lo pone "
                    "en práctica. No es una manera de ganarse su amor, que llegó primero. Es el aspecto que "
                    "tiene el amor cuando tiene manos, igual que el cariño por un amigo se nota en cumplirle "
                    "la palabra. Y Jesús añade una promesa: él y el Padre vendrán a hacer su hogar con quien "
                    "lo ama. Obedecer no es un deber frío. Es la forma en que la amistad se vuelve cercana.",
                ),
                "simple": L(
                    "When we love Jesus, we want to do what he says, like being kind and telling the truth.",
                    "Cuando amamos a Jesús, queremos hacer lo que él dice, como ser amables y decir la verdad.",
                ),
                "ask": L(
                    "Is there one thing Jesus clearly taught that you have been agreeing with but not doing?",
                    "¿Hay algo que Jesús enseñó con claridad y con lo que estás de acuerdo, pero que no estás "
                    "haciendo?",
                ),
                "kid_ask": L(
                    "What is one thing Jesus asks us to do?",
                    "¿Qué es una cosa que Jesús nos pide hacer?",
                ),
                "do": L(
                    "Take that one teaching and act on it in a single concrete step before the day ends: the "
                    "apology, the gift, the truth told, the habit dropped.",
                    "Toma esa enseñanza y da un solo paso concreto antes de que termine el día: la disculpa, "
                    "el regalo, la verdad dicha, la costumbre que dejas.",
                ),
                "kid_do": L(
                    "Think of one thing Jesus would do today, like sharing or telling the truth, and do it.",
                    "Piensa en algo que Jesús haría hoy, como compartir o decir la verdad, y hazlo.",
                ),
                "pray": L(
                    "Jesus, I do not want to love you only in words. Give me strength to do the one thing I "
                    "already know you are asking.",
                    "Jesús, no quiero amarte solo de palabra. Dame fuerzas para hacer eso que ya sé que me "
                    "estás pidiendo.",
                ),
            },
            {
                "key": "loving_god-5",
                "ref": "John 21:15-17",
                "title": L("When your love has failed", "Cuando tu amor ha fallado"),
                "truth": L(
                    "Peter had sworn he would never leave Jesus, and then denied knowing him three times. "
                    "After the resurrection Jesus does not lecture him. He asks one question, three times: do "
                    "you love me? Each answer is met with trust, a task of caring for his people. If you have "
                    "loved God badly, this is how he comes back to you. Not with a list of your failures, but "
                    "with a question and a way forward.",
                    "Pedro había jurado que nunca dejaría a Jesús, y luego negó tres veces conocerlo. Después "
                    "de la resurrección, Jesús no lo regaña. Le hace una sola pregunta, tres veces: ¿me amas? "
                    "A cada respuesta le sigue un gesto de confianza: el encargo de cuidar a los suyos. Si has "
                    "amado mal a Dios, así es como él vuelve a buscarte. No con la lista de tus fallas, sino "
                    "con una pregunta y un camino por delante.",
                ),
                "simple": L(
                    "Peter made a big mistake, but Jesus still loved him and gave him a new start. Jesus does "
                    "that for you too.",
                    "Pedro cometió un error grande, pero Jesús lo siguió amando y le dio un nuevo comienzo. "
                    "Jesús hace lo mismo contigo.",
                ),
                "ask": L(
                    "If Jesus asked you today whether you love him, what would your honest answer be, and "
                    "what would you want to add?",
                    "Si Jesús te preguntara hoy si lo amas, ¿cuál sería tu respuesta honesta, y qué querrías "
                    "agregar?",
                ),
                "kid_ask": L(
                    "How do you think Peter felt when Jesus gave him a new start?",
                    "¿Cómo crees que se sintió Pedro cuando Jesús le dio un nuevo comienzo?",
                ),
                "do": L(
                    "Write your honest answer to Jesus' question in two or three sentences. Do not tidy it "
                    "up. Then read it to him as a prayer.",
                    "Escribe en dos o tres frases tu respuesta honesta a la pregunta de Jesús. No la "
                    "arregles. Luego léesela como oración.",
                ),
                "kid_do": L(
                    "If you did something wrong today, tell Jesus you are sorry, and remember he still "
                    "loves you.",
                    "Si hoy hiciste algo mal, dile a Jesús que lo sientes, y recuerda que él te sigue amando.",
                ),
                "pray": L(
                    "Lord, you know everything. You know where I have failed, and you know that I love you. "
                    "Take me back, and show me who you want me to care for.",
                    "Señor, tú lo sabes todo. Sabes dónde he fallado y sabes que te amo. Recíbeme de nuevo y "
                    "muéstrame a quién quieres que cuide.",
                ),
            },
        ],
    },
    {
        "key": "loving_others",
        "category": "love",
        "title": L("Loving other people", "Amar a los demás"),
        "summary": L(
            "For anyone trying to love real people: the stranger, the one who wears you out, the one who "
            "hurt you. Five readings on kindness, the neighbor, the difficult person and the enemy.",
            "Para quien intenta amar a personas reales: el desconocido, quien te agota, quien te lastimó. "
            "Cinco lecturas sobre la bondad, el prójimo, la persona difícil y el enemigo.",
        ),
        "keywords": [
            "neighbor",
            "kindness",
            "unkind",
            "difficult person",
            "annoy",
            "enemy",
            "selfish",
            "compassion",
            "prójimo",
            "vecin",
            "amab",
            "bondad",
            "enemig",
            "egoís",
            "compasi",
            "me cae mal",
        ],
        "situations": [],
        "traits": ["love", "kindness", "compassion"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Being kind to people, even when it is hard, is one of the ways we show God's love.",
                "Ser amable con las personas, aun cuando cuesta, es una de las formas de mostrar el amor "
                "de Dios.",
            ),
            "teen": L(
                "The kid nobody sits with, the person who mocks you, the sibling who drives you up the wall: "
                "this is where love gets tested.",
                "El chico con quien nadie se sienta, quien se burla de ti, el hermano que te saca de quicio: "
                "ahí es donde el amor se pone a prueba.",
            ),
            "young_adult": L(
                "Roommates, coworkers, strangers online. This is about love as something you practice, not "
                "only something you feel.",
                "Compañeros de casa, de trabajo, desconocidos en internet. Esto trata del amor como algo que "
                "se practica, no solo que se siente.",
            ),
            "adult": L(
                "For loving the people already in your days when you are tired and they are not easy.",
                "Para amar a las personas que ya están en tus días cuando el cansancio pesa y ellas no son "
                "fáciles.",
            ),
            "senior": L(
                "Old neighbors, old grudges, new strangers. There is still someone near you who needs a "
                "neighbor.",
                "Viejos vecinos, viejos rencores, nuevos desconocidos. Todavía hay alguien cerca de ti que "
                "necesita un prójimo.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "loving_others-1",
                "ref": "Luke 10:29-37",
                "title": L("Who is my neighbor?", "¿Quién es mi prójimo?"),
                "truth": L(
                    "A man asks Jesus where the duty to love stops. Jesus answers with a story. Two religious "
                    "men see a beaten traveler and cross to the other side. A Samaritan, an outsider his "
                    "listeners looked down on, stops, bandages him and pays for his care. Then Jesus turns "
                    "the question around. The issue is not who counts as your neighbor. It is whether you "
                    "will be one to the person in front of you, even when it costs you time and money.",
                    "Un hombre le pregunta a Jesús hasta dónde llega el deber de amar. Jesús responde con una "
                    "historia. Dos hombres religiosos ven a un viajero golpeado y pasan de largo. Un "
                    "samaritano, un extranjero al que sus oyentes despreciaban, se detiene, lo venda y paga "
                    "por su cuidado. Entonces Jesús le da vuelta a la pregunta. El asunto no es quién cuenta "
                    "como tu prójimo. Es si tú vas a ser prójimo de quien tienes delante, aunque te cueste "
                    "tiempo y dinero.",
                ),
                "simple": L(
                    "A man was hurt on the road. Two people walked past, but one stopped to help. Jesus says: "
                    "be like the one who stopped.",
                    "Un hombre estaba herido en el camino. Dos personas pasaron de largo, pero una se detuvo "
                    "a ayudar. Jesús dice: sé como el que se detuvo.",
                ),
                "ask": L(
                    "Who have you been walking past lately, and what is the real reason you keep crossing "
                    "the road?",
                    "¿Junto a quién has estado pasando de largo últimamente, y cuál es la verdadera razón?",
                ),
                "kid_ask": L(
                    "Who do you know that might need help or a friend?",
                    "¿A quién conoces que tal vez necesite ayuda o un amigo?",
                ),
                "do": L(
                    "This week, stop once. When you notice someone in need (a neighbor, a coworker, a "
                    "stranger), give them unhurried time and one practical help.",
                    "Esta semana, detente una vez. Cuando notes a alguien con una necesidad (un vecino, un "
                    "compañero, un desconocido), dale tiempo sin prisa y una ayuda práctica.",
                ),
                "kid_do": L(
                    "Look for someone who needs help today, and help them.",
                    "Busca hoy a alguien que necesite ayuda, y ayúdale.",
                ),
                "pray": L(
                    "Lord, slow me down enough to see the person at the side of my road. Make me willing "
                    "to stop.",
                    "Señor, hazme ir más despacio para ver a quien está a la orilla de mi camino. Dame la "
                    "disposición de detenerme.",
                ),
            },
            {
                "key": "loving_others-2",
                "ref": "Colossians 3:12-14",
                "title": L("Put on kindness", "Vístete de bondad"),
                "truth": L(
                    "Paul describes love as clothing you put on. Compassion, kindness, humility, gentleness "
                    "and patience are not moods that arrive by themselves. They are chosen each morning, like "
                    "getting dressed. And he starts from who you already are: chosen and dearly loved by God. "
                    "You do not practice kindness to become loved. You practice it because you are, and love "
                    "is what holds all the rest together.",
                    "Pablo describe el amor como ropa que uno se pone. La compasión, la bondad, la humildad, "
                    "la mansedumbre y la paciencia no son estados de ánimo que llegan solos. Se eligen cada "
                    "mañana, como al vestirse. Y él parte de lo que ya eres: una persona escogida y muy amada "
                    "por Dios. No practicas la bondad para ganarte ese amor. La practicas porque ya lo "
                    "tienes, y el amor es lo que mantiene unido todo lo demás.",
                ),
                "simple": L(
                    "Each morning you put on clothes. You can also choose to put on kindness and patience, "
                    "because God loves you.",
                    "Cada mañana te pones ropa. También puedes elegir ponerte la bondad y la paciencia, "
                    "porque Dios te ama.",
                ),
                "ask": L(
                    "Which of the five (compassion, kindness, humility, gentleness, patience) would the "
                    "people you live or work with say you leave off most often?",
                    "De las cinco (compasión, bondad, humildad, mansedumbre, paciencia), ¿cuál dirían quienes "
                    "viven o trabajan contigo que más seguido te falta?",
                ),
                "kid_ask": L(
                    "What does being kind look like at home?",
                    "¿Cómo se ve ser amable en casa?",
                ),
                "do": L(
                    "Tomorrow morning as you get dressed, name the one quality you will put on deliberately, "
                    "and the person who will most need it from you.",
                    "Mañana, mientras te vistes, nombra la cualidad que vas a ponerte a propósito y la "
                    "persona que más la va a necesitar de ti.",
                ),
                "kid_do": L(
                    "When you get dressed tomorrow, choose one kind thing you will do that day.",
                    "Mañana, cuando te vistas, elige una cosa amable que harás ese día.",
                ),
                "pray": L(
                    "God, you have loved me dearly. Dress me today in kindness, especially toward …",
                    "Dios, tú me has amado mucho. Vísteme hoy de bondad, sobre todo con …",
                ),
            },
            {
                "key": "loving_others-3",
                "ref": "1 Corinthians 13:4-7",
                "title": L(
                    "Love for the difficult person", "Amor para la persona difícil"
                ),
                "truth": L(
                    "This is often read at weddings, but Paul wrote it to a church whose members were "
                    "getting on each other's nerves. Read it as a description of how to treat someone who is "
                    "hard to be around. Love is patient when they are slow. It does not need to win. It does "
                    "not keep a running list of their wrongs. None of this is a feeling. It is a set of "
                    "choices you can make toward a person you may not even like yet.",
                    "Esto se lee mucho en las bodas, pero Pablo lo escribió a una iglesia cuyos miembros no "
                    "se soportaban. Léelo como una descripción de cómo tratar a alguien con quien cuesta "
                    "estar. El amor tiene paciencia cuando el otro es lento. No necesita ganar. No lleva la "
                    "cuenta de sus faltas. Nada de esto es un sentimiento. Son decisiones que puedes tomar "
                    "hacia una persona que quizá todavía ni te cae bien.",
                ),
                "simple": L(
                    "Love is patient and kind. It does not brag or stay angry. We can love people even when "
                    "they are hard to be with.",
                    "El amor es paciente y bondadoso. No presume ni se queda enojado. Podemos amar a las "
                    "personas aun cuando es difícil estar con ellas.",
                ),
                "ask": L(
                    "Think of one difficult person. Which line of this passage is hardest for you to live "
                    "out toward them, and why?",
                    "Piensa en una persona difícil. ¿Qué línea de este pasaje te cuesta más vivir con ella, "
                    "y por qué?",
                ),
                "kid_ask": L(
                    "Who is someone that is hard for you to be nice to?",
                    "¿Con quién te cuesta ser amable?",
                ),
                "do": L(
                    "The next time that person irritates you, wait five seconds before you answer, and then "
                    "say one thing that is both true and kind.",
                    "La próxima vez que esa persona te irrite, espera cinco segundos antes de responder, y "
                    "luego di una cosa que sea a la vez verdadera y amable.",
                ),
                "kid_do": L(
                    "Say one kind thing today to someone who is hard to be nice to.",
                    "Dile hoy algo amable a alguien con quien te cuesta ser amable.",
                ),
                "pray": L(
                    "Lord, you are patient with me. Give me patience with …, and help me stop keeping score.",
                    "Señor, tú me tienes paciencia. Dame paciencia con …, y ayúdame a dejar de llevar la "
                    "cuenta.",
                ),
            },
            {
                "key": "loving_others-4",
                "ref": "Matthew 5:43-48",
                "title": L("Even your enemy", "Incluso a tu enemigo"),
                "truth": L(
                    "Jesus goes further than anyone expected. Loving people who love you back is ordinary. "
                    "He asks his followers to love their enemies and pray for those who mistreat them, "
                    "because that is how the Father treats the world: sun and rain fall on good and bad "
                    "alike. Loving an enemy does not mean calling wrong right, trusting them, or staying "
                    "where they can keep harming you. It means refusing to hate, and wanting their good "
                    "before God. Praying for them is usually where it starts.",
                    "Jesús va más lejos de lo que nadie esperaba. Amar a quien te ama es lo normal. Él les "
                    "pide a sus seguidores amar a sus enemigos y orar por quienes los maltratan, porque así "
                    "trata el Padre al mundo: el sol y la lluvia caen sobre buenos y malos por igual. Amar a "
                    "un enemigo no significa llamar bueno a lo malo, confiar en esa persona ni quedarte donde "
                    "pueda seguir haciéndote daño. Significa negarte a odiar y desear su bien delante de "
                    "Dios. Casi siempre se empieza orando por ella.",
                ),
                "simple": L(
                    "Jesus asks us to love even people who are mean to us. A good way to start is to pray "
                    "for them. And if someone keeps hurting you, tell a grown-up.",
                    "Jesús nos pide amar incluso a quienes nos tratan mal. Una buena forma de empezar es orar "
                    "por ellos. Y si alguien te sigue lastimando, cuéntaselo a un adulto.",
                ),
                "ask": L(
                    "Who comes to mind when you hear the word enemy, and what would it mean to want good for "
                    "them without pretending they did no wrong?",
                    "¿Quién te viene a la mente al oír la palabra enemigo, y qué significaría desearle el "
                    "bien sin fingir que no hizo nada malo?",
                ),
                "kid_ask": L(
                    "Has someone been unkind to you? How did it feel?",
                    "¿Alguien te ha tratado mal? ¿Cómo te sentiste?",
                ),
                "do": L(
                    "Pray for that person by name once a day for a week. Keep it short and honest: ask God "
                    "to do them good, and to deal with what is wrong.",
                    "Ora por esa persona, por su nombre, una vez al día durante una semana. Que sea breve y "
                    "honesto: pídele a Dios que le haga bien y que se ocupe de lo que está mal.",
                ),
                "kid_do": L(
                    "Pray one sentence for someone who was unkind to you.",
                    "Ora una frase por alguien que te trató mal.",
                ),
                "pray": L(
                    "Father, your sun rises on people like me. I do not feel love for …, but I bring them "
                    "to you. Do them good, and keep hatred from growing in me.",
                    "Padre, tu sol sale sobre gente como yo. No siento amor por …, pero te traigo a esa "
                    "persona. Hazle bien, y no dejes que el odio crezca en mí.",
                ),
            },
            {
                "key": "loving_others-5",
                "ref": "1 John 3:16-18",
                "title": L("Love with hands", "Amor con manos"),
                "truth": L(
                    "John gives love a definition and a test. The definition is Jesus, who laid down his life "
                    "for us. The test is plain: if you have what someone needs and close your heart to them, "
                    "the love you talk about is not doing its work. Love is not finished when you feel warmly "
                    "or say the right thing. It is finished when the other person has actually been helped. "
                    "Most days, laying down your life looks small: your time, your money, your evening.",
                    "Juan le da al amor una definición y una prueba. La definición es Jesús, que entregó su "
                    "vida por nosotros. La prueba es sencilla: si tienes lo que alguien necesita y le cierras "
                    "el corazón, el amor del que hablas no está haciendo su trabajo. El amor no termina "
                    "cuando sientes cariño o dices lo correcto. Termina cuando la otra persona de verdad "
                    "recibió ayuda. Casi todos los días, entregar la vida se ve pequeño: tu tiempo, tu "
                    "dinero, tu tarde.",
                ),
                "simple": L(
                    "Love is more than nice words. Love helps. Jesus showed us how by giving everything "
                    "for us.",
                    "El amor es más que palabras bonitas. El amor ayuda. Jesús nos lo mostró al darlo todo "
                    "por nosotros.",
                ),
                "ask": L(
                    "Where have you said you care about someone without yet doing anything that costs you?",
                    "¿Dónde has dicho que alguien te importa sin haber hecho todavía nada que te cueste?",
                ),
                "kid_ask": L(
                    "What is something you have that you could share?",
                    "¿Qué tienes tú que podrías compartir?",
                ),
                "do": L(
                    "Turn one caring sentence into an action this week: bring the meal, send the money, make "
                    "the visit, give the ride.",
                    "Esta semana convierte una frase de cariño en una acción: lleva la comida, manda el "
                    "dinero, haz la visita, ofrece llevar a alguien adonde necesita ir.",
                ),
                "kid_do": L(
                    "Share something of yours with someone today.",
                    "Comparte hoy algo tuyo con alguien.",
                ),
                "pray": L(
                    "Jesus, you loved me with your whole life, not with words alone. Show me one need I can "
                    "meet this week, and make me willing.",
                    "Jesús, me amaste con toda tu vida, no solo con palabras. Muéstrame una necesidad que "
                    "pueda atender esta semana, y dame la disposición.",
                ),
            },
        ],
    },
    {
        "key": "forgiveness",
        "category": "love",
        "title": L("Forgiveness", "El perdón"),
        "summary": L(
            "For anyone carrying a wrong: one done to you, or one you did. Five readings on being forgiven by "
            "God and forgiving others. Forgiving is not pretending it did not hurt, and it never means "
            "staying where you are being harmed.",
            "Para quien carga con una ofensa: una que te hicieron o una que cometiste. Cinco lecturas sobre "
            "recibir el perdón de Dios y perdonar a otros. Perdonar no es fingir que no dolió, ni significa "
            "quedarte donde te hacen daño.",
        ),
        "keywords": [
            "forgiv",
            "grudge",
            "resent",
            "bitter",
            "betray",
            "guilt",
            "apolog",
            "hurt me",
            "perdon",
            "rencor",
            "resenti",
            "amarg",
            "traici",
            "culpa",
            "disculp",
            "me lastim",
        ],
        "situations": ["divorced", "recovery", "returning"],
        "traits": ["forgiveness", "compassion", "honesty"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Everyone does wrong things sometimes, and everyone gets hurt sometimes. God forgives us and "
                "helps us forgive.",
                "Todos hacemos cosas malas a veces, y a todos nos lastiman a veces. Dios nos perdona y nos "
                "ayuda a perdonar.",
            ),
            "teen": L(
                "A friend who turned on you, a parent who let you down, something you did and cannot undo. "
                "Start here.",
                "Un amigo que te dio la espalda, un padre o una madre que te falló, algo que hiciste y no "
                "puedes deshacer. Empieza aquí.",
            ),
            "young_adult": L(
                "Before old hurts harden into who you are, here is a way to set them down without pretending "
                "they were small.",
                "Antes de que las viejas heridas se endurezcan y te definan, aquí hay una forma de soltarlas "
                "sin fingir que fueron pequeñas.",
            ),
            "adult": L(
                "For wounds with years on them: a marriage, a parent, a church, yourself. Honest about how "
                "long this can take.",
                "Para heridas que ya tienen años: las de un matrimonio, un padre, una iglesia, o las que te "
                "hiciste tú. Con honestidad sobre lo que esto puede tardar.",
            ),
            "senior": L(
                "Some things have been carried for decades. It is not too late to be forgiven, or to let a "
                "debt go.",
                "Hay cosas que se han cargado por décadas. No es tarde para recibir perdón ni para soltar "
                "una deuda.",
            ),
        },
        "sensitive": True,
        "lessons": [
            {
                "key": "forgiveness-1",
                "ref": "Psalm 103:8-12",
                "title": L("How God forgives", "Cómo perdona Dios"),
                "truth": L(
                    "Forgiveness starts with God's character, not ours. David describes him as "
                    "compassionate, slow to anger and overflowing with love. He does not treat us the way "
                    "our sins deserve. Then David reaches for the largest distances he knows: as high as "
                    "the sky is above the earth, as far as east is from west. That is how far God removes "
                    "the wrongs of those who turn to him. He does not keep them close at hand to bring up "
                    "later.",
                    "El perdón empieza por cómo es Dios, no por cómo somos nosotros. David lo describe como "
                    "compasivo, lento para enojarse y desbordante de amor. No nos trata como merecen "
                    "nuestros pecados. Luego David busca las distancias más grandes que conoce: tan alto "
                    "como está el cielo sobre la tierra, tan lejos como el oriente del occidente. Así de "
                    "lejos aparta Dios las faltas de quienes se vuelven a él. No las guarda a la mano para "
                    "sacarlas después.",
                ),
                "simple": L(
                    "God is kind and slow to get angry. When we tell him we are sorry, he takes our wrong "
                    "things far, far away.",
                    "Dios es bueno y tarda en enojarse. Cuando le decimos que lo sentimos, él se lleva "
                    "nuestras faltas muy, muy lejos.",
                ),
                "ask": L(
                    "Is there something you have asked God to forgive, yet keep bringing back up as if he "
                    "had not?",
                    "¿Hay algo que le pediste a Dios que perdonara y que sigues trayendo de vuelta como si "
                    "no lo hubiera hecho?",
                ),
                "kid_ask": L(
                    "What is the farthest-away place you can think of?",
                    "¿Cuál es el lugar más lejano que puedes imaginar?",
                ),
                "do": L(
                    "Write that one thing on a slip of paper. Read the last two verses of today's passage "
                    "over it. Then throw the paper away, as a picture of what God has done with it.",
                    "Escribe eso en un papelito. Lee sobre él los dos últimos versículos del pasaje de hoy. "
                    "Luego tira el papel, como imagen de lo que Dios ha hecho con eso.",
                ),
                "kid_do": L(
                    "Tell God sorry for one thing. Then stretch your arms as wide as you can, to remember "
                    "how far away he takes it.",
                    "Pídele perdón a Dios por una cosa. Luego abre los brazos todo lo que puedas, para "
                    "recordar qué tan lejos se la lleva.",
                ),
                "pray": L(
                    "Lord, you are slow to anger and full of love. Thank you for not treating me as I "
                    "deserve. Help me believe that what you have removed is truly gone.",
                    "Señor, tú eres lento para el enojo y lleno de amor. Gracias por no tratarme como "
                    "merezco. Ayúdame a creer que lo que tú apartaste de verdad ya no está.",
                ),
            },
            {
                "key": "forgiveness-2",
                "ref": "Psalm 32:1-5",
                "title": L("Stop hiding", "Deja de esconderte"),
                "truth": L(
                    "David knows this from both sides. While he kept quiet about what he had done, it wore "
                    "him down from the inside; his strength dried up as in summer heat. Then he stopped "
                    "covering it, told God plainly, and God forgave. Confession is not groveling or "
                    "punishing yourself. It is agreeing with God about what is true, so that the hiding can "
                    "end. And when you have wronged a person, telling them the truth is usually part of it.",
                    "David conoce esto desde los dos lados. Mientras calló lo que había hecho, se fue "
                    "desgastando por dentro; sus fuerzas se secaron como en el calor del verano. Entonces "
                    "dejó de encubrirlo, se lo dijo a Dios sin rodeos, y Dios lo perdonó. Confesar no es "
                    "humillarte ni castigarte. Es ponerte de acuerdo con Dios sobre lo que es verdad, para "
                    "que se acabe el esconderse. Y cuando le has fallado a una persona, decirle la verdad "
                    "casi siempre es parte de ello.",
                ),
                "simple": L(
                    "When we do something wrong and hide it, we feel heavy inside. When we tell the truth "
                    "and say sorry, God forgives us and the heavy feeling can go.",
                    "Cuando hacemos algo malo y lo escondemos, sentimos un peso por dentro. Cuando decimos "
                    "la verdad y pedimos perdón, Dios nos perdona y ese peso se puede ir.",
                ),
                "ask": L(
                    "What are you tired of hiding, from God or from someone you have wronged?",
                    "¿Qué te has cansado de esconder, de Dios o de alguien a quien le fallaste?",
                ),
                "kid_ask": L(
                    "How does it feel inside when you hide something you did wrong?",
                    "¿Cómo te sientes por dentro cuando escondes algo malo que hiciste?",
                ),
                "do": L(
                    "Name the thing to God in one plain sentence, with no excuses attached. If a person was "
                    "hurt by it, decide today when and how you will tell them you were wrong.",
                    "Dile eso a Dios en una frase sencilla, sin excusas. Si alguien salió lastimado, decide "
                    "hoy cuándo y cómo le vas a decir que hiciste mal.",
                ),
                "kid_do": L(
                    "If there is something you have been hiding, tell a grown-up you trust, and tell "
                    "God too.",
                    "Si hay algo que has estado escondiendo, cuéntaselo a un adulto de confianza, y "
                    "cuéntaselo también a Dios.",
                ),
                "pray": L(
                    "God, I have kept quiet about …, and it has been heavy. I am not covering it any longer. "
                    "Forgive me, and give me courage to make it right.",
                    "Dios, he callado …, y me ha pesado. Ya no lo voy a encubrir. Perdóname, y dame valor "
                    "para reparar lo que pueda.",
                ),
            },
            {
                "key": "forgiveness-3",
                "ref": "Matthew 18:23-33",
                "title": L(
                    "Forgiven people forgive", "Quien ha sido perdonado, perdona"
                ),
                "truth": L(
                    "Peter had just asked how many times he must forgive. Jesus tells of a servant whose "
                    "king cancels a debt too large to repay in many lifetimes. That same servant then seizes "
                    "a fellow worker over a small sum. Jesus is not saying the wrong done to you is small. "
                    "He sets it beside something larger: what God has let go for you. To forgive is to "
                    "release the debt and give up the right to make the person pay. It is a decision before "
                    "it is a feeling, and it often has to be made more than once.",
                    "Pedro acababa de preguntar cuántas veces debía perdonar. Jesús cuenta de un siervo a "
                    "quien su rey le cancela una deuda imposible de pagar ni en muchas vidas. Ese mismo "
                    "siervo agarra después a un compañero por una suma pequeña. Jesús no dice que el mal que "
                    "te hicieron sea pequeño. Lo pone junto a algo más grande: lo que Dios te ha perdonado "
                    "a ti. Perdonar es soltar la deuda y renunciar al derecho de cobrársela a la persona. Es "
                    "una decisión antes que un sentimiento, y muchas veces hay que tomarla más de una vez.",
                ),
                "simple": L(
                    "A king forgave a man who owed him a huge amount. But that man would not forgive a "
                    "friend who owed him a little. God has forgiven us a lot, so we can forgive others.",
                    "Un rey le perdonó a un hombre una deuda enorme. Pero ese hombre no quiso perdonar a un "
                    "amigo que le debía poquito. Dios nos ha perdonado mucho, y por eso podemos perdonar a "
                    "otros.",
                ),
                "ask": L(
                    "What do you feel a particular person still owes you: an apology, an explanation, years "
                    "of your life? What would it mean to stop collecting?",
                    "¿Qué sientes que cierta persona todavía te debe: una disculpa, una explicación, años de "
                    "tu vida? ¿Qué significaría dejar de cobrar?",
                ),
                "kid_ask": L(
                    "Is there someone you are still upset with?",
                    "¿Hay alguien con quien todavía sientes enojo?",
                ),
                "do": L(
                    "On paper, finish this sentence about one person: what they owe me is … Then pray, as a "
                    "decision and not a feeling: God, I hand this debt to you.",
                    "En un papel, completa esta frase sobre una persona: lo que me debe es … Luego ora, como "
                    "decisión y no como sentimiento: Dios, te entrego esta deuda.",
                ),
                "kid_do": L(
                    'Think of someone who said sorry to you. Tell them, "I forgive you."',
                    'Piensa en alguien que te pidió perdón. Dile: "Te perdono".',
                ),
                "pray": L(
                    "Father, you have forgiven me more than I can count. I choose to release … from what "
                    "they owe me. When the anger comes back, help me choose it again.",
                    "Padre, me has perdonado más de lo que puedo contar. Decido soltar a … de lo que me "
                    "debe. Cuando vuelva el enojo, ayúdame a decidirlo otra vez.",
                ),
            },
            {
                "key": "forgiveness-4",
                "ref": "Genesis 50:15-21",
                "title": L("It did hurt", "Sí dolió"),
                "truth": L(
                    "Joseph's brothers sold him as a slave. Years later, afraid, they beg for mercy. Joseph "
                    "weeps, and what he says matters. He does not say it was nothing. He says plainly that "
                    "they meant to harm him. Then he says God turned it toward good, and he refuses to take "
                    "God's place as their judge. Notice that Joseph says this about his own story, many "
                    "years on; no one else can say it for you. Forgiveness does not ask you to shrink the "
                    "wrong or to stop feeling it. You can call evil what it was, grieve it, and still let "
                    "go of revenge.",
                    "Los hermanos de José lo vendieron como esclavo. Años después, con miedo, le suplican "
                    "misericordia. José llora, y lo que dice importa. No dice que no fue nada. Dice con "
                    "claridad que ellos quisieron hacerle daño. Luego dice que Dios lo encaminó para bien, y "
                    "se niega a ocupar el lugar de Dios como juez. Fíjate que José dice esto de su propia "
                    "historia, muchos años después; nadie más puede decirlo por ti. El perdón no te pide "
                    "achicar la ofensa ni dejar de sentirla. Puedes llamar mal a lo que fue malo, llorarlo, "
                    "y aun así soltar la venganza.",
                ),
                "simple": L(
                    "Joseph's brothers were very unkind to him, and it really hurt. Joseph did not pretend "
                    "it was okay. But he forgave them and took care of them.",
                    "Los hermanos de José lo trataron muy mal, y de verdad le dolió. José no fingió que "
                    "estaba bien. Pero los perdonó y cuidó de ellos.",
                ),
                "ask": L(
                    "What happened to you that you have been told, or have told yourself, was not that bad? "
                    "What would you call it if you were honest?",
                    "¿Qué te pasó que te han dicho, o te has dicho, que no fue para tanto? ¿Cómo lo "
                    "llamarías si hablaras con honestidad?",
                ),
                "kid_ask": L(
                    "Can you forgive someone and still say that what they did hurt?",
                    "¿Puedes perdonar a alguien y aun así decir que lo que hizo te dolió?",
                ),
                "do": L(
                    "Write down what was done to you in plain words, the way Joseph named it. Do not soften "
                    "it. Then tell God what it cost you.",
                    "Escribe con palabras claras lo que te hicieron, como José lo nombró. No lo suavices. "
                    "Luego dile a Dios lo que te costó.",
                ),
                "kid_do": L(
                    "If someone hurt your feelings, tell a grown-up what happened and how it felt.",
                    "Si alguien hirió tus sentimientos, cuéntale a un adulto qué pasó y cómo te sentiste.",
                ),
                "pray": L(
                    "God, what happened was wrong, and it hurt. I will not pretend otherwise with you. I am "
                    "not the judge. Help me leave that place to you.",
                    "Dios, lo que pasó estuvo mal, y dolió. Contigo no voy a fingir otra cosa. Yo no soy el "
                    "juez. Ayúdame a dejarte ese lugar a ti.",
                ),
            },
            {
                "key": "forgiveness-5",
                "ref": "Romans 12:17-21",
                "title": L(
                    "Forgiving is not staying in harm's way",
                    "Perdonar no es quedarte donde te hacen daño",
                ),
                "truth": L(
                    "Paul says not to repay evil with evil and to leave justice in God's hands. He also "
                    "says to live at peace as far as it depends on you, which admits that sometimes it does "
                    "not. Forgiving someone is not the same as trusting them again, and it is not the same "
                    "as going back. Trust is rebuilt only by real change over time. You can forgive from a "
                    "safe distance. If someone is hurting you, getting safe and telling someone is not a "
                    "failure to forgive. And leaving revenge to God is never a reason to stay silent about "
                    "harm.",
                    "Pablo dice que no devolvamos mal por mal y que dejemos la justicia en manos de Dios. "
                    "También dice que vivamos en paz en cuanto dependa de nosotros, y con eso reconoce que a "
                    "veces no depende. Perdonar a alguien no es lo mismo que volver a confiar, ni es lo "
                    "mismo que regresar. La confianza solo se reconstruye con un cambio real a lo largo del "
                    "tiempo. Puedes perdonar desde una distancia segura. Si alguien te está lastimando, "
                    "ponerte a salvo y contarlo no es falta de perdón. Y dejarle la venganza a Dios nunca "
                    "es motivo para callar el daño.",
                ),
                "simple": L(
                    "Forgiving someone does not mean letting them keep hurting you. If someone hurts you, "
                    "it is right to get away and tell a grown-up you trust.",
                    "Perdonar a alguien no significa dejar que te siga lastimando. Si alguien te lastima, "
                    "está bien alejarte y contárselo a un adulto de confianza.",
                ),
                "ask": L(
                    "Have you ever confused forgiving someone with having to trust them or stay close to "
                    "them? What would forgiveness with a wise boundary look like?",
                    "¿Has confundido alguna vez perdonar a alguien con tener que confiar en esa persona o "
                    "seguir cerca? ¿Cómo sería un perdón con un límite sabio?",
                ),
                "kid_ask": L(
                    "Which grown-ups could you tell if someone was hurting you?",
                    "¿A qué adultos les podrías contar si alguien te estuviera lastimando?",
                ),
                "do": L(
                    "If anyone is harming or frightening you now, tell a trusted person today and reach out "
                    "to a pastor, counselor, doctor or local helpline; in immediate danger, call your local "
                    "emergency number. If you are safe, write down one boundary that would let you forgive "
                    "without being hurt again.",
                    "Si alguien te está haciendo daño o te da miedo ahora, cuéntaselo hoy a una persona de "
                    "confianza y busca a un pastor, consejero, médico o línea de ayuda de tu zona; si hay "
                    "peligro inmediato, llama al número de emergencias. Si estás a salvo, escribe un límite "
                    "que te permita perdonar sin que te vuelvan a lastimar.",
                ),
                "kid_do": L(
                    "Name two grown-ups you trust. If anyone ever hurts you or scares you, tell one of them "
                    "right away.",
                    "Nombra a dos adultos en quienes confías. Si alguna vez alguien te lastima o te asusta, "
                    "cuéntaselo enseguida a uno de ellos.",
                ),
                "pray": L(
                    "Lord, I leave justice with you. Show me how to be free of hatred and also safe. Give "
                    "me courage to tell someone what I need to tell.",
                    "Señor, dejo la justicia contigo. Muéstrame cómo vivir libre de odio y también a salvo. "
                    "Dame valor para contarle a alguien lo que necesito contar.",
                ),
            },
        ],
    },
    {
        "key": "marriage",
        "category": "love",
        "title": L("Marriage", "El matrimonio"),
        "summary": L(
            "For married people, in good seasons and hard ones. Five readings on covenant love, serving "
            "each other and holding on. If you are not safe at home, your safety and outside help come "
            "first.",
            "Para personas casadas, en épocas buenas y difíciles. Cinco lecturas sobre el amor de pacto, "
            "servirse el uno al otro y perseverar. Si no estás a salvo en tu casa, tu seguridad y la ayuda "
            "de afuera van primero.",
        ),
        "keywords": [
            "marriage",
            "husband",
            "wife",
            "spouse",
            "wedding",
            "anniversar",
            "married",
            "matrimonio",
            "espos",
            "marido",
            "casad",
            "pareja",
            "boda",
            "aniversario",
        ],
        "situations": ["married"],
        "traits": ["love", "faithfulness", "servanthood"],
        "stages": ["young_adult", "adult", "senior"],
        "stage_notes": {
            "young_adult": L(
                "For the early years, when you are learning that love is something you build on "
                "ordinary days.",
                "Para los primeros años, cuando vas aprendiendo que el amor se construye en los días "
                "comunes.",
            ),
            "adult": L(
                "For the crowded years of work, children and tiredness, when it is easy to become "
                "co-managers instead of companions.",
                "Para los años llenos de trabajo, hijos y cansancio, cuando es fácil volverse socios que "
                "administran una casa en vez de compañeros.",
            ),
            "senior": L(
                "For long marriages: illness, retirement, the house gone quiet. Love still has things "
                "to learn.",
                "Para matrimonios largos: la enfermedad, la jubilación, la casa en silencio. El amor todavía "
                "tiene cosas que aprender.",
            ),
        },
        "sensitive": True,
        "lessons": [
            {
                "key": "marriage-1",
                "ref": "Genesis 2:18-24",
                "title": L("Made for companionship", "Hechos para acompañarse"),
                "truth": L(
                    "Before anything had gone wrong in the world, God named one thing as not good: for the "
                    "human being to be alone. Marriage is one of the gifts he gave in answer, a companion "
                    "who truly matches you. The passage ends with a leaving and a joining: two people "
                    "become one new family, one flesh. That is what a covenant is, a binding promise that "
                    "makes two lives into one shared life. It is more than an arrangement that lasts while "
                    "it suits both sides.",
                    "Antes de que algo saliera mal en el mundo, Dios señaló una cosa como no buena: que el "
                    "ser humano estuviera solo. El matrimonio es uno de los regalos que dio en respuesta: "
                    "una compañía que de verdad te corresponde. El pasaje termina con un dejar y un unirse: "
                    "dos personas llegan a ser una familia nueva, una sola carne. Eso es un pacto: una "
                    "promesa que ata y hace de dos vidas una vida compartida. Es más que un arreglo que dura "
                    "mientras les convenga a los dos.",
                ),
                "simple": L(
                    "God made people to love and help each other. A husband and wife promise to be a team "
                    "for life.",
                    "Dios hizo a las personas para amarse y ayudarse. Un esposo y una esposa prometen ser "
                    "un equipo para toda la vida.",
                ),
                "ask": L(
                    "When did you last treat your husband or wife as a gift, rather than a problem to "
                    "manage or a role to fill?",
                    "¿Cuándo fue la última vez que trataste a tu esposo o esposa como un regalo, y no como "
                    "un problema que resolver o un papel que cumplir?",
                ),
                "kid_ask": L(
                    "Who are the people God has given you so that you are not alone?",
                    "¿Quiénes son las personas que Dios te ha dado para que no estés solo?",
                ),
                "do": L(
                    "Today, tell your spouse one specific way your life is better because they are in it. "
                    "Say it out loud, not by text.",
                    "Hoy dile a tu cónyuge una forma concreta en que tu vida es mejor porque está en ella. "
                    "Díselo en voz alta, no por mensaje.",
                ),
                "kid_do": L(
                    "Say thank you to someone in your family for being with you.",
                    "Dale las gracias a alguien de tu familia por estar contigo.",
                ),
                "pray": L(
                    "God, thank you for … Forgive me for the days I take this gift for granted. Make us one "
                    "in more than name.",
                    "Dios, gracias por … Perdóname por los días en que doy por hecho este regalo. Haznos "
                    "uno, y no solo de nombre.",
                ),
            },
            {
                "key": "marriage-2",
                "ref": "Philippians 2:3-8",
                "title": L("Serving each other", "Servirse el uno al otro"),
                "truth": L(
                    "Paul wrote this to a whole church, and it fits a marriage closely. Do nothing out of "
                    "rivalry or pride. Look to the other's interests and not only your own. Then he points "
                    "to Jesus, who had every right to be served and instead took the place of a servant, "
                    "all the way to the cross. This is asked of both of you, not of one. A marriage changes "
                    "when each person stops counting who did more and starts asking what the other needs "
                    "today.",
                    "Pablo escribió esto a toda una iglesia, y le queda muy bien a un matrimonio. No hagan "
                    "nada por rivalidad ni por orgullo. Miren por el bien del otro y no solo por el propio. "
                    "Luego señala a Jesús, que tenía todo el derecho de ser servido y prefirió tomar el "
                    "lugar de un siervo, hasta la cruz. Esto se les pide a los dos, no a uno solo. Un "
                    "matrimonio cambia cuando cada quien deja de contar quién hizo más y empieza a "
                    "preguntarse qué necesita el otro hoy.",
                ),
                "simple": L(
                    "Jesus did not think only about himself. He served others. In a family, love means "
                    "caring about what the other person needs.",
                    "Jesús no pensó solo en sí mismo. Sirvió a los demás. En una familia, amar es fijarte "
                    "en lo que la otra persona necesita.",
                ),
                "ask": L(
                    "Where have you been keeping score in your marriage, and what does the tally do to the "
                    "way you speak to each other?",
                    "¿En qué has estado llevando la cuenta en tu matrimonio, y qué le hace esa cuenta a la "
                    "forma en que se hablan?",
                ),
                "kid_ask": L(
                    "What is one way you can help someone in your family today?",
                    "¿De qué manera puedes ayudar hoy a alguien de tu familia?",
                ),
                "do": L(
                    "This week, quietly take over one task your spouse dislikes, and do not mention it.",
                    "Esta semana, hazte cargo en silencio de una tarea que a tu cónyuge no le gusta, y no "
                    "lo menciones.",
                ),
                "kid_do": L(
                    "Do one helpful thing at home today without being asked.",
                    "Haz hoy algo útil en casa sin que te lo pidan.",
                ),
                "pray": L(
                    "Jesus, you took the lowest place for me. Take the scorekeeping out of me. Show me what "
                    "… needs from me today.",
                    "Jesús, tú tomaste el último lugar por mí. Quítame la costumbre de llevar la cuenta. "
                    "Muéstrame qué necesita … de mí hoy.",
                ),
            },
            {
                "key": "marriage-3",
                "ref": "Ephesians 4:25-32",
                "title": L(
                    "How you speak when you are angry", "Cómo hablas cuando hay enojo"
                ),
                "truth": L(
                    "This is practical counsel for people who live close together. Tell each other the "
                    "truth. Anger will come, but do not let it lead you into sin or leave it to harden "
                    "overnight. Use words that build up and fit the need of the moment. Put away "
                    "bitterness, shouting and insults. Be kind and forgive, the way God forgave you in "
                    "Christ. Most marriages are not worn down by one great blow but by many small "
                    "sentences. They are mended the same way.",
                    "Este es un consejo práctico para gente que vive muy cerca. Díganse la verdad. El enojo "
                    "va a llegar, pero no dejes que te lleve a pecar ni que se endurezca de un día para "
                    "otro. Usa palabras que edifiquen y respondan a lo que el momento necesita. Deja la "
                    "amargura, los gritos y los insultos. Sé amable y perdona, como Dios te perdonó en "
                    "Cristo. A la mayoría de los matrimonios no los desgasta un gran golpe, sino muchas "
                    "frases pequeñas. Y así también se reparan.",
                ),
                "simple": L(
                    "Our words can hurt or help. God asks us to tell the truth, not to stay angry, and to "
                    "use kind words.",
                    "Nuestras palabras pueden lastimar o ayudar. Dios nos pide decir la verdad, no "
                    "quedarnos enojados y usar palabras amables.",
                ),
                "ask": L(
                    "What is your habit when you are angry at home: going silent, raising your voice, "
                    "bringing up the past? What does it cost the two of you?",
                    "¿Cuál es tu costumbre cuando te enojas en casa: callarte, levantar la voz, sacar el "
                    "pasado? ¿Qué les cuesta eso a los dos?",
                ),
                "kid_ask": L(
                    "What kind words could you use when you feel angry?",
                    "¿Qué palabras amables podrías usar cuando sientes enojo?",
                ),
                "do": L(
                    "The next time you disagree, say one true thing about what you feel, beginning with "
                    '"I" rather than "you always," and say it before the day ends.',
                    "La próxima vez que no estén de acuerdo, di una cosa verdadera sobre lo que sientes, "
                    'empezando con "yo" y no con "tú siempre", y dila antes de que termine el día.',
                ),
                "kid_do": L(
                    "If you feel angry with someone today, take three slow breaths, then use kind words to "
                    "say why.",
                    "Si hoy te enojas con alguien, respira despacio tres veces y luego explica por qué con "
                    "palabras amables.",
                ),
                "pray": L(
                    "Lord, set a guard over my mouth at home. Where I have wounded … with words, give me "
                    "the humility to say so and to ask forgiveness.",
                    "Señor, pon un guardia en mi boca cuando estoy en casa. Donde he herido a … con "
                    "palabras, dame humildad para reconocerlo y pedir perdón.",
                ),
            },
            {
                "key": "marriage-4",
                "ref": "Ecclesiastes 4:9-12",
                "title": L(
                    "Hard seasons, and help from outside",
                    "Épocas difíciles y ayuda de afuera",
                ),
                "truth": L(
                    "The Teacher observes that two are better than one: when one falls, the other lifts. "
                    "Then he adds a third strand, and a cord of three is not quickly broken. Every marriage "
                    "meets seasons of illness, money trouble, grief or distance, and most couples then need "
                    "a third strand: God, and wise people outside the two of you. Asking for help is not "
                    "failure. But a hard season is different from being unsafe. If your spouse hits you, "
                    "threatens you, controls you or makes you afraid, that is abuse. God does not ask you "
                    "to endure it. Your safety, and your children's, comes first.",
                    "El Maestro observa que dos valen más que uno: cuando uno cae, el otro lo levanta. Luego "
                    "añade un tercer hilo, y una cuerda de tres no se rompe fácilmente. Todo matrimonio pasa "
                    "por épocas de enfermedad, apuros de dinero, duelo o distancia, y entonces la mayoría "
                    "necesita ese tercer hilo: Dios, y personas sabias fuera de ustedes dos. Pedir ayuda no "
                    "es fracasar. Pero una época difícil no es lo mismo que estar en peligro. Si tu cónyuge "
                    "te golpea, te amenaza, te controla o te da miedo, eso es maltrato. Dios no te pide que "
                    "lo aguantes. Tu seguridad, y la de tus hijos, va primero.",
                ),
                "simple": L(
                    "Two people can help each other up when one falls down. And when things are hard, it "
                    "is good to ask for help.",
                    "Dos personas pueden ayudarse a levantarse cuando una se cae. Y cuando las cosas se "
                    "ponen difíciles, es bueno pedir ayuda.",
                ),
                "ask": L(
                    "What are the two of you carrying alone that a pastor, a counselor or a trusted older "
                    "couple could help you carry?",
                    "¿Qué están cargando ustedes dos a solas que un pastor, un consejero o un matrimonio "
                    "mayor de confianza podría ayudarles a cargar?",
                ),
                "kid_ask": L(
                    "Who helps you when something is too hard to do by yourself?",
                    "¿Quién te ayuda cuando algo es demasiado difícil para hacerlo tú solo?",
                ),
                "do": L(
                    "Name one struggle in your marriage and ask a trusted person or a counselor for help "
                    "with it this week. If you are afraid of your spouse, do not wait: tell someone you "
                    "trust, contact a domestic violence helpline, and in an emergency call your local "
                    "emergency number.",
                    "Nombra una dificultad de tu matrimonio y esta semana pídele ayuda a una persona de "
                    "confianza o a un consejero. Si le tienes miedo a tu cónyuge, no esperes: cuéntaselo a "
                    "alguien de confianza, comunícate con una línea de ayuda contra la violencia doméstica "
                    "y, en una emergencia, llama al número de emergencias.",
                ),
                "kid_do": L(
                    "The next time something is too hard, ask a grown-up for help instead of struggling "
                    "alone.",
                    "La próxima vez que algo sea muy difícil, pídele ayuda a un adulto en vez de batallar "
                    "sin ayuda.",
                ),
                "pray": L(
                    "God, we cannot hold this together by ourselves. Be the third strand. Lead us to the "
                    "right people, and give me courage to ask.",
                    "Dios, no podemos sostener esto por nuestra cuenta. Sé tú el tercer hilo. Llévanos a "
                    "las personas indicadas, y dame valor para pedir ayuda.",
                ),
            },
            {
                "key": "marriage-5",
                "ref": "Song of Solomon 8:6-7",
                "title": L("A love worth guarding", "Un amor que vale la pena cuidar"),
                "truth": L(
                    "The Bible holds a whole book of love poetry between a bride and a groom, and near its "
                    "end comes this. Love is like a seal pressed on the heart, strong as death, a flame "
                    "that floods cannot put out and money cannot buy. Scripture is not embarrassed by the "
                    "delight of married love. It treats it as a fire worth tending. Faithfulness is more "
                    "than not leaving. It is choosing, again and again, to turn your attention and "
                    "affection toward this one person.",
                    "La Biblia guarda un libro entero de poesía de amor entre una novia y un novio, y cerca "
                    "del final aparece esto. El amor es como un sello puesto sobre el corazón, fuerte como "
                    "la muerte, una llama que las inundaciones no apagan y que el dinero no compra. La "
                    "Escritura no se avergüenza del deleite del amor conyugal. Lo trata como un fuego que "
                    "vale la pena cuidar. La fidelidad es más que no irse. Es elegir, una y otra vez, "
                    "volver tu atención y tu cariño hacia esta persona.",
                ),
                "simple": L(
                    "Real love is strong and it lasts. It is worth more than all the money in the world.",
                    "El amor verdadero es fuerte y dura. Vale más que todo el dinero del mundo.",
                ),
                "ask": L(
                    "What used to keep the flame alive between you that has slipped out of your weeks?",
                    "¿Qué mantenía viva la llama entre ustedes y se les ha ido perdiendo en la rutina?",
                ),
                "kid_ask": L(
                    "What is something that money cannot buy?",
                    "¿Qué es algo que el dinero no puede comprar?",
                ),
                "do": L(
                    "Set aside one unhurried hour with your spouse this week, phones away, and do something "
                    "you both used to enjoy.",
                    "Aparta esta semana una hora sin prisa con tu cónyuge, sin teléfonos, y hagan algo que "
                    "antes disfrutaban juntos.",
                ),
                "kid_do": L(
                    "Give someone you love a hug and tell them you love them.",
                    "Dale un abrazo a alguien que quieres y dile que lo quieres.",
                ),
                "pray": L(
                    "Lord, thank you for the love between us. Guard it from neglect and from anything that "
                    "would draw my heart away. Teach me to choose … again today.",
                    "Señor, gracias por el amor que hay entre nosotros. Cuídalo del descuido y de todo lo "
                    "que quiera llevarse mi corazón a otra parte. Enséñame a elegir a … otra vez hoy.",
                ),
            },
        ],
    },
    {
        "key": "parenting",
        "category": "love",
        "title": L("Parenting", "Criar a los hijos"),
        "summary": L(
            "For parents, grandparents and anyone raising a child. Five readings on receiving children as a "
            "gift, living your faith where they can see it, patience on long days, and loving a child who "
            "has walked away.",
            "Para padres, madres, abuelos y quien esté criando a un niño. Cinco lecturas sobre recibir a los "
            "hijos como un regalo, vivir la fe donde ellos la vean, la paciencia en los días largos y amar "
            "al hijo que se alejó.",
        ),
        "keywords": [
            "parent",
            "my son",
            "my daughter",
            "my kids",
            "my child",
            "toddler",
            "teenager",
            "prodigal",
            "mi hijo",
            "mi hija",
            "mis hijos",
            "crianza",
            "criar",
            "adolescente",
            "pródig",
            "berrinche",
        ],
        "situations": ["parent", "single_parent", "grandparent", "caregiver"],
        "traits": ["patience", "love", "trust"],
        "stages": ["young_adult", "adult", "senior"],
        "stage_notes": {
            "young_adult": L(
                "For new parents, short on sleep and unsure they are doing it right. You are not doing "
                "this alone.",
                "Para quienes empiezan a ser padres, con poco sueño y sin saber si lo están haciendo bien. "
                "No estás haciendo esto sin ayuda.",
            ),
            "adult": L(
                "For the long middle: school runs, slammed doors, a child who is pulling away. Grace for "
                "you as well as for them.",
                "Para el largo trecho de en medio: idas a la escuela, portazos, un hijo que se va alejando. "
                "Gracia para ti y también para ellos.",
            ),
            "senior": L(
                "For parents of grown children and for grandparents: still loving, still praying, learning "
                "to hold with an open hand.",
                "Para padres de hijos adultos y para abuelos: siguen amando, siguen orando, y aprenden a "
                "sostener con la mano abierta.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "parenting-1",
                "ref": "Psalm 127:1-3",
                "title": L(
                    "A gift, and not yours alone to build",
                    "Un regalo, y no lo construyes a solas",
                ),
                "truth": L(
                    "The psalm begins with a house: unless the Lord builds it, the builders work for "
                    "nothing. Parents know the anxious toil it describes, rising early and going to bed "
                    "late. It does not tell you to stop working. It tells you that you are not the only one "
                    "at work, and that God gives rest to those he loves. Then it calls children a gift from "
                    "him. A gift is received, not manufactured. Your child is not your project or your "
                    "proof. They are entrusted to you by a God who loves them more than you do.",
                    "El salmo empieza con una casa: si el Señor no la construye, en vano trabajan los "
                    "albañiles. Los padres conocen ese afán del que habla: madrugar y acostarse tarde. No "
                    "te dice que dejes de trabajar. Te dice que no eres la única persona trabajando, y que "
                    "Dios da descanso a quienes ama. Luego llama a los hijos un regalo suyo. Un regalo se "
                    "recibe, no se fabrica. Tu hijo no es tu proyecto ni tu prueba. Te lo confió un Dios "
                    "que lo ama más que tú.",
                ),
                "simple": L(
                    "Children are a gift from God. God helps grown-ups take care of their families.",
                    "Los niños son un regalo de Dios. Dios ayuda a los adultos a cuidar de sus familias.",
                ),
                "ask": L(
                    "Where are you parenting as though everything depends on you, and what would change if "
                    "you believed God is also at work in your child?",
                    "¿En qué estás criando como si todo dependiera de ti, y qué cambiaría si creyeras que "
                    "Dios también está obrando en tu hijo?",
                ),
                "kid_ask": L(
                    "What do you like best about your family?",
                    "¿Qué es lo que más te gusta de tu familia?",
                ),
                "do": L(
                    "Tonight, when your child is asleep or out of the house, name one worry about them to "
                    "God, and then go to bed on purpose, as an act of trust.",
                    "Esta noche, cuando tu hijo duerma o no esté en casa, dile a Dios una preocupación que "
                    "tienes por él, y luego vete a dormir a propósito, como acto de confianza.",
                ),
                "kid_do": L(
                    "Thank God for the people who take care of you.",
                    "Dale gracias a Dios por las personas que te cuidan.",
                ),
                "pray": L(
                    "Lord, … is your gift before being my responsibility. Build what I cannot. Let me rest "
                    "tonight knowing that you are still at work.",
                    "Señor, … es tu regalo antes que mi responsabilidad. Construye lo que yo no puedo. "
                    "Déjame descansar esta noche sabiendo que tú sigues obrando.",
                ),
            },
            {
                "key": "parenting-2",
                "ref": "Deuteronomy 11:18-21",
                "title": L("Faith they can see", "Una fe que puedan ver"),
                "truth": L(
                    "Moses tells parents to keep God's words in their own hearts first, and then to talk "
                    "about them with their children in the plain places of life: sitting at home, walking "
                    "along the road, lying down, getting up. Faith is passed on less by lectures than by a "
                    "life lived within sight. Children notice what you do when you are worried, how you "
                    "speak about people, whether you say sorry. You cannot give what you do not have, and "
                    "you do not need to be perfect. You need to be real.",
                    "Moisés les dice a los padres que primero guarden las palabras de Dios en su propio "
                    "corazón, y luego hablen de ellas con sus hijos en los lugares comunes de la vida: "
                    "sentados en casa, andando por el camino, al acostarse, al levantarse. La fe se "
                    "transmite menos con sermones que con una vida vivida a la vista. Los hijos notan qué "
                    "haces cuando algo te preocupa, cómo hablas de la gente, si pides perdón. No puedes dar "
                    "lo que no tienes, y no necesitas una vida perfecta. Necesitas una vida auténtica.",
                ),
                "simple": L(
                    "Families can talk about God anywhere: at the table, in the car and at bedtime.",
                    "Las familias pueden hablar de Dios en cualquier lugar: en la mesa, en el carro y a la "
                    "hora de dormir.",
                ),
                "ask": L(
                    "If your children described your faith only from what they see at home, what would "
                    "they say?",
                    "Si tus hijos describieran tu fe solo por lo que ven en casa, ¿qué dirían?",
                ),
                "kid_ask": L(
                    "What would you like to ask a grown-up about God?",
                    "¿Qué te gustaría preguntarle a un adulto sobre Dios?",
                ),
                "do": L(
                    "Choose one ordinary moment this week (a meal, a drive, bedtime) and tell your child "
                    "one true thing about how God has helped you. Keep it under two minutes.",
                    "Elige un momento común de esta semana (una comida, un trayecto, la hora de dormir) y "
                    "cuéntale a tu hijo algo verdadero sobre cómo Dios te ha ayudado. Que dure menos de dos "
                    "minutos.",
                ),
                "kid_do": L(
                    "At dinner or bedtime, ask a grown-up to tell you about a time God helped them.",
                    "En la cena o antes de dormir, pídele a un adulto que te cuente de una vez en que Dios "
                    "le ayudó.",
                ),
                "pray": L(
                    "God, put your words deep in me before I try to put them in my children. Let them see "
                    "something true of you in the way I live.",
                    "Dios, pon tus palabras bien dentro de mí antes de que yo intente ponerlas en mis "
                    "hijos. Que vean algo verdadero de ti en mi manera de vivir.",
                ),
            },
            {
                "key": "parenting-3",
                "ref": "Psalm 103:13-14",
                "title": L("Patience on the long days", "Paciencia en los días largos"),
                "truth": L(
                    "David says God's compassion is like that of a good father toward his children, and he "
                    "gives the reason: God knows how we are made and remembers that we are dust. He does "
                    "not expect from us what we cannot yet do. This is how God parents you, and it is a "
                    "pattern for the long days. A tired four-year-old and a moody fourteen-year-old are not "
                    "yet what they will be. Patience begins by remembering how they are made, and how "
                    "patient God has been with you.",
                    "David dice que la compasión de Dios es como la de un buen padre con sus hijos, y da la "
                    "razón: Dios sabe de qué estamos hechos y recuerda que somos polvo. No espera de "
                    "nosotros lo que todavía no podemos hacer. Así te cría Dios a ti, y es un modelo para "
                    "los días largos. Una niña de cuatro años cansada y un muchacho de catorce de mal humor "
                    "todavía no son lo que llegarán a ser. La paciencia empieza por recordar de qué están "
                    "hechos, y cuánta paciencia te ha tenido Dios.",
                ),
                "simple": L(
                    "God is gentle with us because he knows we are still growing. Grown-ups and kids can be "
                    "patient with each other too.",
                    "Dios es tierno con nosotros porque sabe que todavía estamos creciendo. Los adultos y "
                    "los niños también pueden tenerse paciencia.",
                ),
                "ask": L(
                    "When do you most often lose patience with your child, and what is usually going on in "
                    "you at that moment: tiredness, fear, embarrassment?",
                    "¿Cuándo pierdes más seguido la paciencia con tu hijo, y qué suele estar pasando en ti "
                    "en ese momento: cansancio, miedo, vergüenza?",
                ),
                "kid_ask": L(
                    "What is something you are still learning to do?",
                    "¿Qué es algo que todavía estás aprendiendo a hacer?",
                ),
                "do": L(
                    "Pick your hardest hour of the day. Before it comes tomorrow, pray one sentence. When "
                    "your patience runs thin, lower your voice instead of raising it. If you fail, tell "
                    "your child you are sorry.",
                    "Elige tu hora más difícil del día. Mañana, antes de que llegue, ora una frase. Cuando "
                    "se te acabe la paciencia, baja la voz en vez de subirla. Si fallas, pídele perdón a "
                    "tu hijo.",
                ),
                "kid_do": L(
                    "Say thank you to a grown-up who has been patient with you.",
                    "Dale las gracias a un adulto que te ha tenido paciencia.",
                ),
                "pray": L(
                    "Father, you remember that I am dust. Help me remember it about … today. Give me a "
                    "gentle voice in the hard hour.",
                    "Padre, tú recuerdas que soy polvo. Ayúdame a recordarlo hoy de … Dame una voz suave "
                    "en la hora difícil.",
                ),
            },
            {
                "key": "parenting-4",
                "ref": "Mark 10:13-16",
                "title": L("Bring them to Jesus", "Llévalos a Jesús"),
                "truth": L(
                    "People were bringing children to Jesus, and the disciples tried to send them away, as "
                    "if he had more important business. Jesus was indignant. He took the children in his "
                    "arms and blessed them, and said the kingdom of God belongs to such as these. Your "
                    "child matters to Jesus now, not only for who they may become. Your part is the part "
                    "those parents played: to bring them. You cannot make a child believe. You can keep "
                    "bringing them, in prayer and in person, to the one who welcomes them.",
                    "La gente le llevaba niños a Jesús, y los discípulos trataron de alejarlos, como si él "
                    "tuviera asuntos más importantes. Jesús se indignó. Tomó a los niños en sus brazos y "
                    "los bendijo, y dijo que el reino de Dios es de quienes son como ellos. Tu hijo le "
                    "importa a Jesús ahora, no solo por lo que pueda llegar a ser. Tu parte es la que "
                    "hicieron aquellos padres: llevarlo. No puedes hacer que un hijo crea. Puedes seguir "
                    "llevándolo, en oración y en persona, a quien lo recibe.",
                ),
                "simple": L(
                    "Jesus loves children. He wanted them close and he blessed them. You are welcome with "
                    "Jesus too.",
                    "Jesús ama a los niños. Quiso tenerlos cerca y los bendijo. Tú también tienes un lugar "
                    "junto a Jesús.",
                ),
                "ask": L(
                    "In what simple ways are you bringing your child to Jesus right now, and what tends to "
                    "crowd them out?",
                    "¿De qué maneras sencillas estás llevando a tu hijo a Jesús ahora, y qué es lo que "
                    "suele quitarles el lugar?",
                ),
                "kid_ask": L(
                    "What would you tell Jesus if you were sitting next to him?",
                    "¿Qué le dirías a Jesús si estuvieras sentado junto a él?",
                ),
                "do": L(
                    "Pray a short blessing over your child tonight, by name, with a hand on their head or "
                    "shoulder if they will let you. If they are grown or far away, pray it for them where "
                    "you are.",
                    "Esta noche ora una bendición breve por tu hijo, por su nombre, con una mano sobre su "
                    "cabeza o su hombro si te deja. Si ya es adulto o está lejos, órala por él desde donde "
                    "estés.",
                ),
                "kid_do": L(
                    "Ask a grown-up to pray for you tonight, and thank Jesus for loving you.",
                    "Pídele a un adulto que ore por ti esta noche, y dale gracias a Jesús por amarte.",
                ),
                "pray": L(
                    "Jesus, you welcomed the children. I bring … to you today. Take them in your arms and "
                    "bless them, and do not let me stand in the way.",
                    "Jesús, tú recibiste a los niños. Hoy te traigo a … Dale tu abrazo y tu bendición, y no "
                    "permitas que yo sea un estorbo.",
                ),
            },
            {
                "key": "parenting-5",
                "ref": "Luke 15:17-24",
                "title": L("The child who has walked away", "El hijo que se fue"),
                "truth": L(
                    "Jesus told this story to show what God is like. A son takes his inheritance, leaves "
                    "and wastes it. The father does not chase him or drag him home. He lets him go, and he "
                    "keeps watching the road. When the son turns back, the father sees him from far off, "
                    "runs, and embraces him before the apology is finished. If your child has walked away "
                    "from you or from faith, their choices are not the measure of your parenting; even this "
                    "father had a child who left. Your part is to keep loving, keep praying and keep the "
                    "door open.",
                    "Jesús contó esta historia para mostrar cómo es Dios. Un hijo toma su herencia, se va y "
                    "la malgasta. El padre no lo persigue ni lo trae a rastras. Lo deja ir, y sigue mirando "
                    "el camino. Cuando el hijo emprende el regreso, el padre lo ve desde lejos, corre y lo "
                    "abraza antes de que termine de disculparse. Si tu hijo se alejó de ti o de la fe, sus "
                    "decisiones no son la medida de tu crianza; hasta este padre tuvo un hijo que se fue. "
                    "Tu parte es seguir amando, seguir orando y dejar la puerta abierta.",
                ),
                "simple": L(
                    "A son left home and made bad choices. When he came back, his father ran to hug him. "
                    "God loves us like that, always ready to welcome us home.",
                    "Un hijo se fue de casa y tomó malas decisiones. Cuando regresó, su papá corrió a "
                    "abrazarlo. Así nos ama Dios: siempre listo para recibirnos en casa.",
                ),
                "ask": L(
                    "What would it look like to keep the door open for your child without pretending all "
                    "is well, and without trying to control them?",
                    "¿Cómo sería dejarle la puerta abierta a tu hijo sin fingir que todo está bien y sin "
                    "tratar de controlarlo?",
                ),
                "kid_ask": L(
                    "How do you think the son felt when his father ran to hug him?",
                    "¿Cómo crees que se sintió el hijo cuando su papá corrió a abrazarlo?",
                ),
                "do": L(
                    "Send your child one short message this week with no advice and no question in it: "
                    "only that you love them and are glad they are yours. Then tell one trusted friend how "
                    "you are really doing.",
                    "Esta semana mándale a tu hijo un mensaje corto, sin consejos ni preguntas: solo que lo "
                    "amas y que te alegra que sea tuyo. Luego cuéntale a una amistad de confianza cómo "
                    "estás de verdad.",
                ),
                "kid_do": L(
                    "Give someone in your family a big hug today.",
                    "Dale hoy un abrazo grande a alguien de tu familia.",
                ),
                "pray": L(
                    "Father, you know what it is to watch the road. … is yours even more than mine. Go "
                    "where I cannot go. Keep my heart soft and my door open.",
                    "Padre, tú sabes lo que es quedarse mirando el camino. … te pertenece a ti aún más que a "
                    "mí. Ve adonde yo no puedo ir. Mantén tierno mi corazón y abierta mi puerta.",
                ),
            },
        ],
    },
    {
        "key": "family",
        "category": "love",
        "title": L("Family", "La familia"),
        "summary": L(
            "For children, teens and adults who belong to a family that is not perfect, which is every "
            "family. Five readings on honoring parents, getting along with brothers and sisters, and "
            "finding God at work in the family you have.",
            "Para niños, adolescentes y adultos que son parte de una familia imperfecta, es decir, de "
            "cualquier familia. Cinco lecturas sobre honrar a los padres, llevarse bien entre hermanos y "
            "ver a Dios obrar en la familia que tienes.",
        ),
        "keywords": [
            "family",
            "my parents",
            "my mom",
            "my dad",
            "brother",
            "sister",
            "sibling",
            "relatives",
            "in-law",
            "familia",
            "mis padres",
            "mi mamá",
            "mi papá",
            "herman",
            "parientes",
            "suegr",
            "abuel",
        ],
        "situations": [],
        "traits": ["love", "patience", "forgiveness"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Your family is a gift from God, even on the days when it is hard to get along.",
                "Tu familia es un regalo de Dios, aun en los días en que cuesta llevarse bien.",
            ),
            "teen": L(
                "You did not choose your family, and some days it shows. This is about honor, honesty and "
                "room to grow.",
                "Tú no elegiste a tu familia, y hay días en que se nota. Esto trata de la honra, la "
                "honestidad y el espacio para crecer.",
            ),
            "young_adult": L(
                "Leaving home changes how you belong to your family. Here is help working out what you owe "
                "and what you can let go.",
                "Salir de casa cambia tu manera de pertenecer a tu familia. Aquí hay ayuda para distinguir "
                "lo que debes y lo que puedes soltar.",
            ),
            "adult": L(
                "Aging parents, old sibling roles, holidays that reopen things. For loving the family you "
                "actually have.",
                "Padres que envejecen, viejos papeles entre hermanos, fiestas que reabren heridas. Para "
                "amar a la familia que de verdad tienes.",
            ),
            "senior": L(
                "For the one many now look to: mending what can be mended, and blessing the generations "
                "that come after you.",
                "Para quien ahora es referencia de muchos: reparar lo que se pueda reparar y bendecir a las "
                "generaciones que vienen detrás.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "family-1",
                "ref": "Ephesians 6:1-4",
                "title": L(
                    "Honor goes both ways", "La honra va en las dos direcciones"
                ),
                "truth": L(
                    "Paul speaks to children directly: obey your parents, and honor your father and mother. "
                    "Then he speaks to parents: do not provoke your children to anger, but bring them up "
                    "with the Lord's training and care. To honor someone is to treat them as a person who "
                    "matters. For a child that mostly means listening and obeying. For an adult it means "
                    "respect, gratitude and care, not lifelong obedience. And honoring a parent never means "
                    "hiding it when someone is harming you. Telling the truth to a safe person is right.",
                    "Pablo les habla directamente a los hijos: obedezcan a sus padres, y honren a su padre "
                    "y a su madre. Luego les habla a los padres: no hagan enojar a sus hijos, sino críenlos "
                    "con la enseñanza y el cuidado del Señor. Honrar a alguien es tratarlo como una persona "
                    "que importa. Para un niño, eso es sobre todo escuchar y obedecer. Para un adulto es "
                    "respeto, gratitud y cuidado, no obediencia de por vida. Y honrar a un padre o a una "
                    "madre nunca significa callar cuando alguien te hace daño. Decirle la verdad a una "
                    "persona segura es lo correcto.",
                ),
                "simple": L(
                    "God asks children to listen to their parents and honor them. He asks parents to be "
                    "gentle and to teach their children about him.",
                    "Dios les pide a los hijos que escuchen a sus padres y los honren. A los padres les "
                    "pide que sean tiernos y que les enseñen a sus hijos acerca de él.",
                ),
                "ask": L(
                    "What would honoring your parents look like at your age and in your real situation, "
                    "without pretending the past was different from what it was?",
                    "¿Cómo sería honrar a tus padres a tu edad y en tu situación real, sin fingir que el "
                    "pasado fue distinto de lo que fue?",
                ),
                "kid_ask": L(
                    "How can you show the grown-ups who take care of you that they matter to you?",
                    "¿Cómo puedes mostrarles a los adultos que te cuidan que son importantes para ti?",
                ),
                "do": L(
                    "Do one concrete act of honor this week: thanks for something specific, a call, help "
                    "with a chore, or patience in a conversation that usually goes badly.",
                    "Haz esta semana un acto concreto de honra: dar gracias por algo específico, una "
                    "llamada, ayuda con una tarea, o paciencia en una conversación que casi siempre sale "
                    "mal.",
                ),
                "kid_do": L(
                    "The next time a grown-up at home asks you to do something, do it the first time they "
                    "ask.",
                    "La próxima vez que un adulto en casa te pida algo, hazlo a la primera.",
                ),
                "pray": L(
                    "Father, thank you for the people who raised me, for what they got right and in spite "
                    "of what they got wrong. Show me how to honor them truthfully.",
                    "Padre, gracias por quienes me criaron, por lo que hicieron bien y a pesar de lo que "
                    "hicieron mal. Muéstrame cómo honrarlos con verdad.",
                ),
            },
            {
                "key": "family-2",
                "ref": "Genesis 33:4-11",
                "title": L("Brothers and sisters", "Hermanos y hermanas"),
                "truth": L(
                    "Jacob had cheated his brother Esau out of their father's blessing, and Esau had wanted "
                    "him dead. They spent some twenty years apart. Now Jacob comes home afraid, bowing, "
                    "with gifts. Esau runs to him and embraces him, and they both weep. Rivalry between "
                    "brothers and sisters is as old as families: who was favored, who got more, who was "
                    "wronged. This meeting shows that the old story does not have to be the last one. "
                    "Someone has to come toward the other, and someone has to put the grudge down.",
                    "Jacob le había quitado con engaños a su hermano Esaú la bendición de su padre, y Esaú "
                    "había querido matarlo. Pasaron unos veinte años separados. Ahora Jacob vuelve a casa "
                    "con miedo, inclinándose, con regalos. Esaú corre hacia él y lo abraza, y los dos "
                    "lloran. La rivalidad entre hermanos es tan vieja como las familias: a quién "
                    "prefirieron, quién recibió más, a quién le hicieron mal. Este encuentro muestra que la "
                    "vieja historia no tiene que ser la última. Alguien tiene que acercarse, y alguien "
                    "tiene que soltar el rencor.",
                ),
                "simple": L(
                    "Jacob and Esau were brothers who had a big fight. After a long time, they hugged and "
                    "became friends again.",
                    "Jacob y Esaú eran hermanos y tuvieron un pleito muy grande. Después de mucho tiempo, "
                    "se abrazaron y volvieron a ser amigos.",
                ),
                "ask": L(
                    "Is there a brother, sister or relative you share an old story with? Which part is "
                    "yours to do: come toward them, or put the grudge down?",
                    "¿Hay un hermano, una hermana o un pariente con quien tienes una vieja historia? ¿Qué "
                    "parte te toca a ti: acercarte o soltar el rencor?",
                ),
                "kid_ask": L(
                    "What do you and your brother, sister or cousin argue about most?",
                    "¿Por qué se pelean más tú y tu hermano, hermana o primo?",
                ),
                "do": L(
                    "Reach out to one sibling or relative this week with something small and warm: a "
                    "message, an old photo, a thank-you. Do not reopen the argument.",
                    "Esta semana busca a un hermano o pariente con algo pequeño y cálido: un mensaje, una "
                    "foto vieja, un gracias. No reabras la discusión.",
                ),
                "kid_do": L(
                    "Do one kind thing today for your brother, sister or cousin, like sharing or letting "
                    "them go first.",
                    "Haz hoy algo amable por tu hermano, hermana o primo, como compartir o dejar que pase "
                    "primero.",
                ),
                "pray": L(
                    "God, you know the history between me and … Soften what has hardened in me. Show me "
                    "the first step toward them.",
                    "Dios, tú conoces la historia entre … y yo. Ablanda lo que se endureció en mí. "
                    "Muéstrame el primer paso para acercarme.",
                ),
            },
            {
                "key": "family-3",
                "ref": "Matthew 1:1-6",
                "title": L("No perfect families", "No hay familias perfectas"),
                "truth": L(
                    "The New Testament opens with a family tree, and it is not a tidy one. In these few "
                    "lines are Jacob the deceiver, Judah and Tamar with their painful story, Rahab with a "
                    "past she would not have chosen to advertise, Ruth the foreigner, and David, whose "
                    "son's mother is named only as the wife of a man David wronged. Matthew could have left "
                    "them out. He did not. This is the family God chose for his Son. If your family carries "
                    "secrets, failures and people who do not fit, you are in familiar company. God does "
                    "not wait for a family to be respectable before he works in it.",
                    "El Nuevo Testamento empieza con un árbol familiar, y no es uno ordenado. En estas "
                    "pocas líneas están Jacob el tramposo, Judá y Tamar con su historia dolorosa, Rahab con "
                    "un pasado que no habría querido anunciar, Rut la extranjera, y David, cuyo hijo tiene "
                    "por madre a una mujer nombrada solo como la esposa de un hombre al que David le hizo "
                    "mal. Mateo pudo haberlos omitido. No lo hizo. Esta es la familia que Dios eligió para "
                    "su Hijo. Si tu familia carga secretos, fracasos y personas que no encajan, estás en "
                    "buena compañía. Dios no espera a que una familia sea respetable para obrar en ella.",
                ),
                "simple": L(
                    "Jesus' family had all kinds of people in it, and some made big mistakes. God loved "
                    "that family and worked through it anyway.",
                    "En la familia de Jesús hubo toda clase de personas, y algunas cometieron errores "
                    "grandes. Dios amó a esa familia y obró por medio de ella de todos modos.",
                ),
                "ask": L(
                    "What part of your family's story are you ashamed of, and where might God be at work "
                    "in it?",
                    "¿Qué parte de la historia de tu familia te avergüenza, y dónde podría estar Dios "
                    "obrando en ella?",
                ),
                "kid_ask": L(
                    "Who are the people in your family? Can you name them all?",
                    "¿Quiénes son las personas de tu familia? ¿Puedes nombrarlas a todas?",
                ),
                "do": L(
                    "Sketch your family tree for three generations. Beside each name write one thing you "
                    "are grateful for, or one thing you are praying for.",
                    "Dibuja tu árbol familiar de tres generaciones. Junto a cada nombre escribe algo que "
                    "agradeces o algo por lo que estás orando.",
                ),
                "kid_do": L(
                    "Draw a picture of your family and thank God for each person in it.",
                    "Haz un dibujo de tu familia y dale gracias a Dios por cada persona.",
                ),
                "pray": L(
                    "Lord, you were not ashamed to be born into a real family. Come into mine as it is. "
                    "Redeem what I cannot fix.",
                    "Señor, no te avergonzaste de nacer en una familia real. Entra en la mía tal como es. "
                    "Redime lo que yo no puedo arreglar.",
                ),
            },
            {
                "key": "family-4",
                "ref": "John 19:25-27",
                "title": L(
                    "Caring for those who cared for you", "Cuidar a quienes te cuidaron"
                ),
                "truth": L(
                    "Jesus is dying, and he sees his mother standing near the cross. Among his last words "
                    "he makes sure she will be cared for, placing her in the keeping of the disciple he "
                    "loved. From that hour the disciple takes her into his home. Honoring parents does not "
                    "end when you grow up; it turns into practical care. Notice also that Jesus makes a "
                    "family here that is not based on blood. Sometimes the people God gives you to care "
                    "for, and to be cared for by, are family by love.",
                    "Jesús está muriendo y ve a su madre de pie junto a la cruz. Entre sus últimas palabras "
                    "se asegura de que alguien la cuide, y la confía al discípulo a quien amaba. Desde esa "
                    "hora el discípulo la recibe en su casa. Honrar a los padres no termina cuando creces; "
                    "se convierte en cuidado práctico. Fíjate también en que Jesús forma aquí una familia "
                    "que no depende de la sangre. A veces las personas que Dios te da para cuidar, y para "
                    "que te cuiden, son familia por amor.",
                ),
                "simple": L(
                    "Even when Jesus was hurting, he made sure his mother would be taken care of. Families "
                    "take care of each other.",
                    "Aun cuando Jesús estaba sufriendo, se aseguró de que alguien cuidara a su mamá. Las "
                    "familias se cuidan unas a otras.",
                ),
                "ask": L(
                    "Who in your family, or among those who have been family to you, needs your practical "
                    "care in this season?",
                    "¿Quién en tu familia, o entre quienes han sido familia para ti, necesita tu cuidado "
                    "práctico en esta etapa?",
                ),
                "kid_ask": L(
                    "Who takes care of you? Who can you help take care of?",
                    "¿Quién te cuida a ti? ¿A quién puedes ayudar a cuidar tú?",
                ),
                "do": L(
                    "Do one practical thing this week for an older relative or someone who has been like "
                    "family: a visit, a meal, a ride to an appointment, an unhurried phone call.",
                    "Haz esta semana algo práctico por un familiar mayor o por alguien que ha sido como de "
                    "tu familia: una visita, una comida, llevarlo a una cita, una llamada sin prisa.",
                ),
                "kid_do": L(
                    "Call or visit a grandparent or an older person you love, or make them a card.",
                    "Llama o visita a un abuelo o a una persona mayor que quieres, o hazle una tarjeta.",
                ),
                "pray": L(
                    "Jesus, you thought of your mother even from the cross. Show me who needs my care, and "
                    "give me the time and tenderness to give it.",
                    "Jesús, pensaste en tu madre aun desde la cruz. Muéstrame quién necesita mi cuidado, y "
                    "dame el tiempo y la ternura para darlo.",
                ),
            },
            {
                "key": "family-5",
                "ref": "Psalm 68:5-6",
                "title": L(
                    "When family has let you down", "Cuando la familia te ha fallado"
                ),
                "truth": L(
                    "Not everyone has a family that is safe, or even present. David sings of a God who is "
                    "father to the fatherless and defender of widows, and who gives lonely people a home to "
                    "belong to. If your family has been a place of absence or harm, God does not ask you to "
                    "pretend. He takes the side of the one left without protection, and he gives a wider "
                    "family, his people, where those who are alone can belong. It is not disloyal to need "
                    "that, or to keep a safe distance from relatives who harm you.",
                    "No todo el mundo tiene una familia segura, ni siquiera presente. David canta de un "
                    "Dios que es padre de los huérfanos y defensor de las viudas, y que les da un hogar a "
                    "quienes están solos. Si tu familia ha sido un lugar de ausencia o de daño, Dios no te "
                    "pide que finjas. Él se pone del lado de quien quedó sin protección, y da una familia "
                    "más amplia, su pueblo, donde quienes están solos pueden pertenecer. No es deslealtad "
                    "necesitar eso, ni mantener una distancia segura de parientes que te hacen daño.",
                ),
                "simple": L(
                    "God is like a loving father to anyone who needs one. He gives people who feel alone a "
                    "family to belong to.",
                    "Dios es como un papá amoroso para quien lo necesita. A las personas que se sienten "
                    "solas les da una familia a la cual pertenecer.",
                ),
                "ask": L(
                    "Where has your family left a gap, and whom has God placed in your life who has been "
                    "family to you?",
                    "¿Dónde dejó tu familia un vacío, y a quién ha puesto Dios en tu vida que ha sido "
                    "familia para ti?",
                ),
                "kid_ask": L(
                    "Who outside your home feels like family to you?",
                    "¿Quién, fuera de tu casa, es como de tu familia?",
                ),
                "do": L(
                    "Thank one person who has been like family to you. Then look around your church or "
                    "neighborhood for someone who is alone, and invite them to a meal.",
                    "Dale las gracias a una persona que ha sido como familia para ti. Luego busca en tu "
                    "iglesia o en tu barrio a alguien que esté solo, e invítalo a comer.",
                ),
                "kid_do": L(
                    "Think of someone who might feel lonely, and invite them to play or sit with you.",
                    "Piensa en alguien que quizá se sienta solo, e invítalo a jugar o a sentarse contigo.",
                ),
                "pray": L(
                    "God, you are a father to those who have none. Fill the gaps my family has left. Set me "
                    "in a family, and make me family for someone else.",
                    "Dios, tú eres padre de quienes no tienen padre. Llena los vacíos que dejó mi familia. "
                    "Ponme en una familia, y hazme familia para alguien más.",
                ),
            },
        ],
    },
    {
        "key": "friendship",
        "category": "love",
        "title": L("Friendship", "La amistad"),
        "summary": L(
            "For anyone who wants better friends, or wants to be one. Five readings on loyalty, honesty, "
            "choosing your company wisely, carrying each other, and the friend who will not leave.",
            "Para quien quiere mejores amigos, o quiere ser uno. Cinco lecturas sobre la lealtad, la "
            "honestidad, elegir bien tus compañías, cargarse unos a otros y el amigo que no se va.",
        ),
        "keywords": [
            "friend",
            "left out",
            "peer pressure",
            "clique",
            "bad influence",
            "loyal",
            "amig",
            "amistad",
            "compañer",
            "me dejaron fuera",
            "mala influencia",
            "leal",
        ],
        "situations": ["student", "moving"],
        "traits": ["faithfulness", "honesty", "kindness"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Friends are a gift. God can help you be a good friend and find good friends.",
                "Los amigos son un regalo. Dios puede ayudarte a ser un buen amigo y a encontrar buenos "
                "amigos.",
            ),
            "teen": L(
                "Who you spend time with shapes who you become. This is about loyalty, honesty, and friends "
                "who are good for you.",
                "Las personas con quienes pasas el tiempo le dan forma a quien llegas a ser. Esto trata de "
                "lealtad, honestidad y amigos que te hacen bien.",
            ),
            "young_adult": L(
                "Friendships take effort once school ends. Here is what is worth looking for, and worth "
                "being.",
                "Cuando termina la escuela, las amistades requieren esfuerzo. Aquí está lo que vale la pena "
                "buscar, y lo que vale la pena ser.",
            ),
            "adult": L(
                "Busy years quietly thin out friendships. For rebuilding the kind that tells you the truth.",
                "Los años ocupados van adelgazando las amistades sin hacer ruido. Para reconstruir las que "
                "te dicen la verdad.",
            ),
            "senior": L(
                "Old friends are fewer and precious, and new ones are still possible. It is not too late "
                "to be a friend.",
                "Los viejos amigos son menos y valen mucho, y todavía es posible hacer nuevos. No es tarde "
                "para ser amigo de alguien.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "friendship-1",
                "ref": "1 Samuel 18:1-4",
                "title": L("A friend who gives", "Un amigo que da"),
                "truth": L(
                    "Jonathan was the king's son and heir. David was the young shepherd everyone was "
                    "suddenly praising. Jonathan had every reason to see a rival. Instead he loved David as "
                    "himself, made a covenant with him, and handed over his own robe and weapons. Real "
                    "friendship is not built on what you can get, or on staying ahead. It is glad when the "
                    "other does well, and it gives without keeping a tally. That kind of friend is rare. "
                    "The surest way to find one is to become one.",
                    "Jonatán era hijo y heredero del rey. David era el joven pastor al que de pronto todos "
                    "elogiaban. Jonatán tenía todos los motivos para ver en él a un rival. En cambio, lo "
                    "amó como a sí mismo, hizo un pacto con él y le entregó su propio manto y sus armas. La "
                    "amistad verdadera no se construye sobre lo que puedes sacar ni sobre ir adelante del "
                    "otro. Se alegra cuando al otro le va bien, y da sin llevar la cuenta. Un amigo así es "
                    "raro. La manera más segura de encontrarlo es llegar a serlo.",
                ),
                "simple": L(
                    "Jonathan was a prince, and David was his friend. Jonathan gave David his own robe. "
                    "Good friends share, and they are glad when good things happen to each other.",
                    "Jonatán era un príncipe, y David era su amigo. Jonatán le dio a David su propio manto. "
                    "Los buenos amigos comparten y se alegran cuando al otro le pasan cosas buenas.",
                ),
                "ask": L(
                    "Is there a friend whose success you find hard to celebrate? What would it look like "
                    "to be glad for them out loud?",
                    "¿Hay un amigo cuyo éxito te cuesta celebrar? ¿Cómo sería alegrarte por él en voz alta?",
                ),
                "kid_ask": L(
                    "What makes someone a good friend?",
                    "¿Qué hace que alguien sea un buen amigo?",
                ),
                "do": L(
                    "Congratulate one friend today on something good in their life. Be specific, and do "
                    "not mention yourself.",
                    "Felicita hoy a un amigo por algo bueno en su vida. Sé específico, y no hables de ti.",
                ),
                "kid_do": L(
                    "Share something you like with a friend today.",
                    "Comparte hoy con un amigo algo que te gusta.",
                ),
                "pray": L(
                    "Lord, take envy out of my friendships. Make me the kind of friend who gives freely and "
                    "is glad when … does well.",
                    "Señor, saca la envidia de mis amistades. Hazme la clase de amigo que da con libertad y "
                    "se alegra cuando a … le va bien.",
                ),
            },
            {
                "key": "friendship-2",
                "ref": "Proverbs 27:5-6",
                "title": L(
                    "A friend who tells the truth", "Un amigo que dice la verdad"
                ),
                "truth": L(
                    "These two sayings turn our instincts around. Honest correction, spoken openly, is "
                    "better than love that stays hidden and silent. The wounds a friend gives can be "
                    "trusted, while an enemy's kisses are many and worth nothing. A friend who only ever "
                    "agrees with you is pleasant company and little help. The one who cares enough to say "
                    "a hard thing, gently and to your face, is giving you something costly. It takes "
                    "humility to receive it and love to give it.",
                    "Estos dos dichos le dan vuelta a nuestro instinto. Una corrección sincera, dicha de "
                    "frente, vale más que un amor que se queda escondido y callado. Las heridas que causa "
                    "un amigo son de fiar, mientras que los besos de un enemigo son muchos y no valen nada. "
                    "Un amigo que siempre te da la razón es buena compañía y poca ayuda. Quien te quiere lo "
                    "bastante para decirte algo difícil, con suavidad y de frente, te está dando algo que "
                    "le cuesta. Hace falta humildad para recibirlo y amor para darlo.",
                ),
                "simple": L(
                    "A real friend tells you the truth in a kind way, even when it is hard to hear.",
                    "Un amigo de verdad te dice la verdad con cariño, aun cuando cuesta escucharla.",
                ),
                "ask": L(
                    "Who has permission to tell you the truth about yourself, and when did you last thank "
                    "them instead of defending yourself?",
                    "¿Quién tiene permiso de decirte la verdad sobre ti, y cuándo fue la última vez que se "
                    "lo agradeciste en vez de defenderte?",
                ),
                "kid_ask": L(
                    "Has a friend ever told you something true that was hard to hear?",
                    "¿Alguna vez un amigo te dijo algo verdadero que te costó escuchar?",
                ),
                "do": L(
                    "Ask one trusted friend this week: is there anything you see in me that I am not "
                    "seeing? Listen without arguing, and say thank you.",
                    "Pregúntale esta semana a un amigo de confianza: ¿hay algo que ves en mí que yo no "
                    "estoy viendo? Escucha sin discutir, y da las gracias.",
                ),
                "kid_do": L(
                    "Tell a friend the truth today in a kind way, even about something small.",
                    "Dile hoy la verdad a un amigo con cariño, aunque sea sobre algo pequeño.",
                ),
                "pray": L(
                    "God, give me friends honest enough to tell me the truth, and make me humble enough to "
                    "listen. Help me speak truth with love to …",
                    "Dios, dame amigos tan sinceros que me digan la verdad, y hazme tan humilde que la "
                    "escuche. Ayúdame a hablarle con verdad y amor a …",
                ),
            },
            {
                "key": "friendship-3",
                "ref": "Psalm 1:1-3",
                "title": L("Choosing your company", "Elegir tus compañías"),
                "truth": L(
                    "The first psalm begins with whom you walk with, stand with and sit with. It pictures "
                    "a slow slide: first listening to bad advice, then lingering, then settling in among "
                    "people who mock what is good. Against that it sets a tree planted by water, fed by "
                    "God's teaching and fruitful in its season. This is not about refusing kindness to "
                    "anyone; Jesus ate with all kinds of people. It is about whose voice shapes you. You "
                    "become like the people whose counsel you take.",
                    "El primer salmo empieza por con quién caminas, con quién te detienes y con quién te "
                    "sientas. Describe un deslizarse lento: primero escuchar malos consejos, luego "
                    "quedarse, luego acomodarse entre quienes se burlan de lo bueno. Frente a eso pone un "
                    "árbol plantado junto al agua, alimentado por la enseñanza de Dios y que da fruto a su "
                    "tiempo. No se trata de negarle la bondad a nadie; Jesús comió con toda clase de "
                    "personas. Se trata de qué voz te va formando. Uno termina pareciéndose a aquellos "
                    "cuyos consejos sigue.",
                ),
                "simple": L(
                    "The friends we spend the most time with change us. Choose friends who help you do "
                    "what is good.",
                    "Los amigos con quienes pasamos más tiempo nos cambian. Elige amigos que te ayuden a "
                    "hacer lo bueno.",
                ),
                "ask": L(
                    "Whose influence are you under most right now, and is it making you more or less like "
                    "the person you want to be?",
                    "¿Bajo la influencia de quién estás más ahora, y te está haciendo parecerte más o "
                    "menos a la persona que quieres ser?",
                ),
                "kid_ask": L(
                    "Which friends help you make good choices?",
                    "¿Qué amigos te ayudan a tomar buenas decisiones?",
                ),
                "do": L(
                    "List the five people you spend the most time with, in person or on a screen. Beside "
                    "each, write a word for what they bring out in you. Choose one good friendship to "
                    "invest in more.",
                    "Haz una lista de las cinco personas con quienes pasas más tiempo, en persona o en "
                    "pantalla. Junto a cada una escribe una palabra sobre lo que saca de ti. Elige una "
                    "buena amistad a la que le vas a dedicar más.",
                ),
                "kid_do": L(
                    "Spend time today with a friend who helps you be kind.",
                    "Pasa tiempo hoy con un amigo que te ayuda a ser amable.",
                ),
                "pray": L(
                    "Lord, plant me by good water. Show me which voices to draw near to and which to step "
                    "back from, without looking down on anyone.",
                    "Señor, plántame junto a buenas aguas. Muéstrame a qué voces acercarme y de cuáles "
                    "tomar distancia, sin despreciar a nadie.",
                ),
            },
            {
                "key": "friendship-4",
                "ref": "Mark 2:1-5",
                "title": L("Friends who carry you", "Amigos que te cargan"),
                "truth": L(
                    "A paralyzed man could not get to Jesus by himself, and the house was too crowded to "
                    "enter. His four friends carried him up to the roof, opened it, and lowered him down. "
                    "Mark says Jesus saw their faith, the friends' faith, and spoke to the man. There are "
                    "days when you cannot pray or hope or move for yourself, and friends carry you. There "
                    "are days when it is your turn to pick up a corner of someone else's mat. Friendship "
                    "at its best brings each other to Jesus.",
                    "Un hombre paralítico no podía llegar a Jesús por sí mismo, y la casa estaba tan llena "
                    "que no se podía entrar. Sus cuatro amigos lo subieron al techo, lo abrieron y lo "
                    "bajaron. Marcos dice que Jesús vio la fe de ellos, la de los amigos, y le habló al "
                    "hombre. Hay días en que no puedes orar, ni esperar, ni moverte por tu cuenta, y los "
                    "amigos te cargan. Hay días en que te toca a ti tomar una esquina de la camilla de "
                    "otro. La mejor amistad es la que nos lleva unos a otros a Jesús.",
                ),
                "simple": L(
                    "Four friends carried a man who could not walk all the way to Jesus. Good friends help "
                    "each other, especially when things are hard.",
                    "Cuatro amigos cargaron hasta Jesús a un hombre que no podía caminar. Los buenos "
                    "amigos se ayudan, sobre todo cuando las cosas se ponen difíciles.",
                ),
                "ask": L(
                    "Who has carried you when you could not carry yourself? And whose mat is God asking "
                    "you to help lift now?",
                    "¿Quién te ha cargado cuando no podías contigo? ¿Y la camilla de quién te está "
                    "pidiendo Dios que ayudes a levantar ahora?",
                ),
                "kid_ask": L(
                    "How could you help a friend who is having a hard day?",
                    "¿Cómo podrías ayudar a un amigo que está teniendo un día difícil?",
                ),
                "do": L(
                    "Pray by name for one friend who is struggling, then do one thing that takes weight "
                    "off them: a meal, a ride, an hour of company.",
                    "Ora por su nombre por un amigo que la está pasando mal, y luego haz algo que le "
                    "aligere la carga: una comida, llevarlo a algún lado, una hora de compañía.",
                ),
                "kid_do": L(
                    "Pray for a friend today, and do one thing to help them.",
                    "Ora hoy por un amigo, y haz una cosa para ayudarlo.",
                ),
                "pray": L(
                    "Jesus, thank you for the people who have carried me to you. Today I bring you my "
                    "friend … Show me which corner of the mat is mine.",
                    "Jesús, gracias por las personas que me han cargado hasta ti. Hoy te traigo a mi amigo "
                    "… Muéstrame qué esquina de la camilla me toca.",
                ),
            },
            {
                "key": "friendship-5",
                "ref": "John 15:12-15",
                "title": L("The friend who will not leave", "El amigo que no se va"),
                "truth": L(
                    "On the night before he died, Jesus gave his followers a new name: no longer servants, "
                    "but friends. A servant is told what to do. A friend is told why, and Jesus says he "
                    "has shared with them everything he heard from the Father. Then he defines friendship "
                    "by its highest act, laying down your life for your friends, which he was about to do. "
                    "Every human friendship will at some point disappoint you. Beneath them all is this "
                    "one, offered to you. It is also the pattern for how to love the friends you have.",
                    "La noche antes de morir, Jesús les dio a sus seguidores un nombre nuevo: ya no "
                    "siervos, sino amigos. A un siervo se le dice qué hacer. A un amigo se le dice por "
                    "qué, y Jesús dice que les ha contado todo lo que oyó del Padre. Luego define la "
                    "amistad por su acto más alto, dar la vida por los amigos, que era lo que estaba por "
                    "hacer. Toda amistad humana te va a decepcionar en algún momento. Debajo de todas está "
                    "esta, que se te ofrece a ti. Y es también el modelo para amar a los amigos que tienes.",
                ),
                "simple": L(
                    "Jesus calls us his friends. He loved his friends so much that he gave his life for "
                    "them. He is a friend who never leaves.",
                    "Jesús nos llama sus amigos. Amó tanto a sus amigos que dio su vida por ellos. Es un "
                    "amigo que nunca se va.",
                ),
                "ask": L(
                    "What changes in the way you pray if you think of Jesus as a friend who has told you "
                    "his heart, and not only as a master?",
                    "¿Qué cambia en tu manera de orar si piensas en Jesús como un amigo que te ha abierto "
                    "su corazón, y no solo como un amo?",
                ),
                "kid_ask": L(
                    "What does it mean to you that Jesus wants to be your friend?",
                    "¿Qué significa para ti que Jesús quiera ser tu amigo?",
                ),
                "do": L(
                    "Talk to Jesus for five minutes today as you would to a close friend: what happened, "
                    "what you are glad about, and what you are dreading.",
                    "Habla hoy cinco minutos con Jesús como hablarías con un amigo cercano: qué pasó, qué "
                    "te alegra y qué te da miedo.",
                ),
                "kid_do": L(
                    "Tell Jesus about your day, just as you would tell a friend.",
                    "Cuéntale a Jesús cómo te fue hoy, como se lo contarías a un amigo.",
                ),
                "pray": L(
                    "Jesus, you call me friend, and you proved it with your life. Thank you. Teach me to "
                    "love my friends the way you have loved me.",
                    "Jesús, me llamas amigo, y lo demostraste con tu vida. Gracias. Enséñame a amar a mis "
                    "amigos como tú me has amado.",
                ),
            },
        ],
    },
    {
        "key": "conflict",
        "category": "love",
        "title": L("Conflict and making peace", "Conflictos y cómo hacer las paces"),
        "summary": L(
            "For when you are at odds with someone at home, at work or at church. Five readings on "
            "listening, owning your part, speaking gently, going first, and what to do when you still "
            "cannot agree.",
            "Para cuando estás en conflicto con alguien en casa, en el trabajo o en la iglesia. Cinco "
            "lecturas sobre escuchar, reconocer tu parte, hablar con suavidad, dar el primer paso y qué "
            "hacer cuando siguen sin estar de acuerdo.",
        ),
        "keywords": [
            "conflict",
            "argu",
            "fight",
            "disagree",
            "reconcil",
            "tension",
            "quarrel",
            "conflicto",
            "discut",
            "discusi",
            "pelea",
            "pleito",
            "desacuerdo",
            "tensión",
        ],
        "situations": ["married", "parent", "working", "leader"],
        "traits": ["peace", "gentleness", "humility"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Everybody argues sometimes. God can help you listen, say sorry and make friends again.",
                "Todos discutimos a veces. Dios puede ayudarte a escuchar, pedir perdón y volver a ser "
                "amigos.",
            ),
            "teen": L(
                "Fights with parents, friends, group chats that blow up. Here is how to disagree without "
                "burning everything down.",
                "Peleas con tus padres, con amigos, chats de grupo que explotan. Aquí hay una forma de "
                "estar en desacuerdo sin quemarlo todo.",
            ),
            "young_adult": L(
                "Roommates, partners, coworkers: you cannot avoid conflict, but you can learn to handle "
                "it well.",
                "Compañeros de casa, pareja, compañeros de trabajo: no puedes evitar el conflicto, pero sí "
                "aprender a manejarlo bien.",
            ),
            "adult": L(
                "For the standoff at home or at work that has gone on too long, and the conversation you "
                "keep putting off.",
                "Para ese conflicto en casa o en el trabajo que ya se alargó demasiado, y la conversación "
                "que sigues posponiendo.",
            ),
            "senior": L(
                "Long family disputes and old estrangements. As far as it depends on you, there may still "
                "be a step to take.",
                "Largos pleitos de familia y viejos distanciamientos. En lo que dependa de ti, quizá "
                "todavía haya un paso que dar.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "conflict-1",
                "ref": "James 1:19-20",
                "title": L("Listen first", "Primero escucha"),
                "truth": L(
                    "James gives three instructions in an order that matters: be quick to listen, slow to "
                    "speak, slow to become angry. In most arguments we do the reverse, preparing our reply "
                    "while the other person is still talking. He adds a reason: human anger does not "
                    "produce the upright life God wants. Anger feels as though it is setting things right, "
                    "and it almost never does. Listening is not agreeing. It is making sure you have "
                    "understood before you answer.",
                    "Santiago da tres instrucciones en un orden que importa: sé pronto para escuchar, "
                    "lento para hablar, lento para enojarte. En casi todas las discusiones hacemos lo "
                    "contrario: preparamos la respuesta mientras la otra persona todavía habla. Y da una "
                    "razón: el enojo humano no produce la vida recta que Dios quiere. El enojo se siente "
                    "como si estuviera arreglando las cosas, y casi nunca lo hace. Escuchar no es estar de "
                    "acuerdo. Es asegurarte de haber entendido antes de responder.",
                ),
                "simple": L(
                    "God wants us to be quick to listen and slow to get angry. Listening can stop a fight "
                    "before it grows.",
                    "Dios quiere que seamos rápidos para escuchar y lentos para enojarnos. Escuchar puede "
                    "detener una pelea antes de que crezca.",
                ),
                "ask": L(
                    "In your last argument, what was the other person really trying to say? Could you put "
                    "it in words they would agree with?",
                    "En tu última discusión, ¿qué estaba tratando de decir en realidad la otra persona? "
                    "¿Podrías ponerlo en palabras con las que ella estaría de acuerdo?",
                ),
                "kid_ask": L(
                    "Is it hard for you to listen when you are upset? Why?",
                    "¿Te cuesta escuchar cuando sientes enojo? ¿Por qué?",
                ),
                "do": L(
                    "In your next disagreement, before you give your side, say back what you heard (what I "
                    "hear you saying is …) and ask whether you got it right.",
                    "En tu próximo desacuerdo, antes de dar tu versión, repite lo que oíste (lo que te "
                    "escucho decir es …) y pregunta si entendiste bien.",
                ),
                "kid_do": L(
                    "The next time someone is upset with you, let them finish talking before you say "
                    "anything.",
                    "La próxima vez que alguien esté molesto contigo, déjalo terminar de hablar antes de "
                    "decir algo.",
                ),
                "pray": L(
                    "Lord, make me quick to listen and slow to speak. When anger rises in me today, slow "
                    "me down.",
                    "Señor, hazme pronto para escuchar y lento para hablar. Cuando hoy me suba el enojo, "
                    "frena mi paso.",
                ),
            },
            {
                "key": "conflict-2",
                "ref": "Matthew 7:3-5",
                "title": L("Your part first", "Primero tu parte"),
                "truth": L(
                    "Jesus uses a picture meant to raise a smile: someone with a wooden beam in their own "
                    "eye, fussing over a speck of sawdust in another's. He does not say the speck is "
                    "imaginary, or that you may never help with it. He says to deal with your own first, "
                    "and then you will see clearly. In most ordinary quarrels some part is yours, even if "
                    "it is the smaller part. Owning it first, without adding a but, changes the whole "
                    "conversation. This is about quarrels between equals; being mistreated is not your "
                    "fault.",
                    "Jesús usa una imagen pensada para hacer sonreír: alguien con una viga de madera en su "
                    "propio ojo, preocupado por una astilla en el ojo de otro. No dice que la astilla sea "
                    "imaginaria, ni que nunca puedas ayudar con ella. Dice que primero te ocupes de lo "
                    "tuyo, y entonces verás con claridad. En la mayoría de los pleitos comunes hay una "
                    "parte que es tuya, aunque sea la menor. Reconocerla primero, sin agregar un pero, "
                    "cambia toda la conversación. Esto se refiere a pleitos entre iguales; que te "
                    "maltraten no es tu culpa.",
                ),
                "simple": L(
                    "Before we point at what someone else did wrong, Jesus asks us to look at what we did "
                    "wrong first.",
                    "Antes de señalar lo que otro hizo mal, Jesús nos pide mirar primero lo que hicimos "
                    "mal nosotros.",
                ),
                "ask": L(
                    "In the conflict on your mind, what is your part, however small? Can you name it "
                    "without the word but?",
                    "En el conflicto que tienes en mente, ¿cuál es tu parte, por pequeña que sea? ¿Puedes "
                    "nombrarla sin usar la palabra pero?",
                ),
                "kid_ask": L(
                    "When you have a fight, is it easy or hard to say what you did wrong?",
                    "Cuando tienes una pelea, ¿te resulta fácil o difícil decir lo que tú hiciste mal?",
                ),
                "do": L(
                    "Write one sentence that owns your part and nothing else: I was wrong to … Say it to "
                    "the person this week.",
                    "Escribe una frase que reconozca tu parte y nada más: hice mal al … Dísela a la "
                    "persona esta semana.",
                ),
                "kid_do": L(
                    "If you had a fight today, say sorry for your part first.",
                    "Si hoy tuviste una pelea, pide perdón primero por tu parte.",
                ),
                "pray": L(
                    "Jesus, show me the beam in my own eye. Give me the honesty to name my part before I "
                    "name theirs.",
                    "Jesús, muéstrame la viga en mi propio ojo. Dame honestidad para nombrar mi parte "
                    "antes de nombrar la del otro.",
                ),
            },
            {
                "key": "conflict-3",
                "ref": "Proverbs 15:1-4",
                "title": L("A gentle answer", "Una respuesta suave"),
                "truth": L(
                    "A gentle answer turns anger away, and a harsh word stirs it up. The proverb treats a "
                    "quarrel like a fire: every reply either feeds it or cools it. Gentleness here is not "
                    "weakness or giving in. You can say something firm, even unwelcome, in a tone that "
                    "leaves the other person their dignity. These sayings add that a soothing tongue is "
                    "like a tree of life, while a twisted one crushes the spirit. How you say a thing "
                    "decides whether it can be heard.",
                    "Una respuesta suave aparta el enojo, y una palabra áspera lo enciende. El proverbio "
                    "trata un pleito como un fuego: cada respuesta lo alimenta o lo enfría. Aquí la "
                    "suavidad no es debilidad ni ceder. Puedes decir algo firme, incluso algo que no se "
                    "quiere oír, en un tono que le deje a la otra persona su dignidad. Estos dichos añaden "
                    "que una lengua que calma es como un árbol de vida, mientras que una lengua torcida "
                    "aplasta el ánimo. La manera de decir algo decide si se puede escuchar.",
                ),
                "simple": L(
                    "Gentle words can calm an angry person. Mean words make a fight bigger.",
                    "Las palabras suaves pueden calmar a una persona enojada. Las palabras feas hacen más "
                    "grande la pelea.",
                ),
                "ask": L(
                    "What happens to your tone when you feel attacked, and where did you learn to answer "
                    "that way?",
                    "¿Qué le pasa a tu tono cuando sientes que te atacan, y dónde aprendiste a responder "
                    "así?",
                ),
                "kid_ask": L(
                    "What does a gentle voice sound like?",
                    "¿Cómo suena una voz suave?",
                ),
                "do": L(
                    "The next time someone speaks sharply to you, answer more quietly and more slowly than "
                    "they did, and watch what happens.",
                    "La próxima vez que alguien te hable con dureza, responde más bajo y más despacio que "
                    "esa persona, y observa qué pasa.",
                ),
                "kid_do": L(
                    'Practice saying in a calm voice, "I feel upset because…"',
                    'Practica decir con voz tranquila: "Me siento mal porque…"',
                ),
                "pray": L(
                    "God, put gentleness in my mouth. When I am provoked, help me answer in a way that "
                    "cools the fire.",
                    "Dios, pon suavidad en mi boca. Cuando me provoquen, ayúdame a responder de una manera "
                    "que enfríe el fuego.",
                ),
            },
            {
                "key": "conflict-4",
                "ref": "Matthew 5:23-24",
                "title": L("Go first", "Da el primer paso"),
                "truth": L(
                    "Jesus pictures someone in the middle of worship who remembers that a brother or "
                    "sister has something against them. He says to leave the gift at the altar, go and be "
                    "reconciled, and then come back. Making things right with a person matters so much to "
                    "God that it can interrupt worship. And notice who goes: the one who remembers. Jesus "
                    "does not say to wait until the other apologizes, or until you are sure who was more "
                    "wrong. Someone has to move first. He asks that it be you.",
                    "Jesús imagina a alguien en plena adoración que se acuerda de que un hermano o una "
                    "hermana tiene algo contra él. Dice que deje la ofrenda en el altar, vaya a "
                    "reconciliarse y luego regrese. Arreglar las cosas con una persona le importa tanto a "
                    "Dios que puede interrumpir la adoración. Y fíjate quién va: el que se acuerda. Jesús "
                    "no dice que esperes a que el otro se disculpe, ni a estar seguro de quién tuvo más "
                    "culpa. Alguien tiene que moverse primero. Él pide que seas tú.",
                ),
                "simple": L(
                    "If you know someone is upset with you, Jesus says to go and make things right "
                    "without waiting.",
                    "Si sabes que alguien está molesto contigo, Jesús dice que vayas a arreglar las cosas "
                    "sin esperar.",
                ),
                "ask": L(
                    "Who has something against you right now? What has kept you from going to them?",
                    "¿Quién tiene algo contra ti en este momento? ¿Qué te ha detenido de ir a buscarlo?",
                ),
                "kid_ask": L(
                    "Is there someone you need to make up with?",
                    "¿Hay alguien con quien necesitas hacer las paces?",
                ),
                "do": L(
                    "Contact that person within the next two days. Talk to them, not about them. Begin "
                    "with your part and your wish to make things right, and let them answer in their own "
                    "time.",
                    "Busca a esa persona en los próximos dos días. Habla con ella, no de ella. Empieza por "
                    "tu parte y tu deseo de arreglar las cosas, y deja que responda a su tiempo.",
                ),
                "kid_do": L(
                    'If a friend or someone at home is upset with you, go to them today and ask, "Can we '
                    'make up?"',
                    'Si un amigo o alguien de tu casa está molesto contigo, ve hoy y pregúntale: "¿Hacemos '
                    'las paces?"',
                ),
                "pray": L(
                    "Lord, I have been waiting for … to move first. Give me the humility to go. Prepare "
                    "their heart and mine.",
                    "Señor, he estado esperando a que … dé el primer paso. Dame humildad para ir yo. "
                    "Prepara su corazón y el mío.",
                ),
            },
            {
                "key": "conflict-5",
                "ref": "Acts 15:36-41",
                "title": L(
                    "When you still cannot agree", "Cuando siguen sin estar de acuerdo"
                ),
                "truth": L(
                    "Paul and Barnabas were friends and partners who had risked their lives together. They "
                    "disagreed so sharply over whether to take John Mark along that they parted ways. The "
                    "Bible reports it without tidying it up or naming a winner. Both went on serving God, "
                    "and years later Paul writes warmly of Mark. Sometimes faithful people cannot agree, "
                    "and peace means parting without contempt and leaving the door open. And making peace "
                    "never requires you to go back to someone who is harming you. Peace is not the same as "
                    "pretending.",
                    "Pablo y Bernabé eran amigos y compañeros que habían arriesgado la vida juntos. "
                    "Discutieron tan fuerte sobre si llevar o no a Juan Marcos que se separaron. La Biblia "
                    "lo cuenta sin maquillarlo y sin declarar un ganador. Los dos siguieron sirviendo a "
                    "Dios, y años después Pablo escribe de Marcos con aprecio. A veces personas fieles no "
                    "logran ponerse de acuerdo, y la paz consiste en separarse sin desprecio y dejar la "
                    "puerta abierta. Y hacer las paces nunca te obliga a volver con alguien que te hace "
                    "daño. La paz no es lo mismo que fingir.",
                ),
                "simple": L(
                    "Sometimes people try hard and still do not agree. They can still be kind and wish "
                    "each other well.",
                    "A veces las personas se esfuerzan y aun así no se ponen de acuerdo. De todos modos "
                    "pueden ser amables y desearse el bien.",
                ),
                "ask": L(
                    "Is there a disagreement you may need to stop trying to win? What would it mean to "
                    "part, or to stay, without contempt?",
                    "¿Hay un desacuerdo que quizá necesitas dejar de querer ganar? ¿Qué significaría "
                    "separarte, o quedarte, sin desprecio?",
                ),
                "kid_ask": L(
                    "Can you still be kind to someone you disagree with? How?",
                    "¿Puedes seguir siendo amable con alguien con quien no estás de acuerdo? ¿Cómo?",
                ),
                "do": L(
                    "For one unresolved conflict, write down what you can still honestly respect in the "
                    "other person, and pray good for them. If the conflict involves being threatened or "
                    "mistreated, tell a trusted person about it this week.",
                    "Sobre un conflicto sin resolver, escribe lo que todavía puedes respetar con "
                    "honestidad en la otra persona, y ora pidiendo su bien. Si en el conflicto hay "
                    "amenazas o maltrato, cuéntaselo esta semana a una persona de confianza.",
                ),
                "kid_do": L(
                    "Say something kind today to someone you disagreed with.",
                    "Dile hoy algo amable a alguien con quien no estuviste de acuerdo.",
                ),
                "pray": L(
                    "God, we see this differently, and I cannot fix that. Keep me from bitterness. Bless "
                    "…, and keep the door open if there is a way back.",
                    "Dios, vemos esto de manera distinta, y no puedo arreglarlo. Líbrame de la amargura. "
                    "Bendice a …, y deja la puerta abierta si hay un camino de regreso.",
                ),
            },
        ],
    },
    {
        "key": "service",
        "category": "love",
        "title": L("Serving others", "Servir a los demás"),
        "summary": L(
            "For anyone who wants their ordinary days to count for someone else. Five readings on Jesus "
            "the servant, using what you have, work no one sees, and serving without sliding into "
            "resentment.",
            "Para quien quiere que sus días comunes le sirvan a alguien más. Cinco lecturas sobre Jesús "
            "el siervo, usar lo que tienes, el trabajo que nadie ve y servir sin caer en el resentimiento.",
        ),
        "keywords": [
            "serv",
            "volunteer",
            "helping",
            "ministry",
            "unappreciated",
            "taken for granted",
            "voluntari",
            "ayudar",
            "ministerio",
            "nadie agradece",
            "no me valoran",
            "útil",
        ],
        "situations": ["leader", "caregiver", "working", "retired"],
        "traits": ["servanthood", "humility", "generosity"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "You are not too small to help. God is glad when you help at home, at school and with "
                "your friends.",
                "No eres demasiado pequeño para ayudar. Dios se alegra cuando ayudas en casa, en la escuela "
                "y con tus amigos.",
            ),
            "teen": L(
                "You have more to give than you think. This is about noticing a need and doing something, "
                "even when nobody posts about it.",
                "Tienes más para dar de lo que crees. Esto trata de notar una necesidad y hacer algo, "
                "aunque nadie lo publique.",
            ),
            "young_adult": L(
                "Before life fills up, learn the habit of serving. It will shape the kind of person you "
                "become.",
                "Antes de que la vida se llene, aprende el hábito de servir. Va a darle forma a la clase "
                "de persona que llegarás a ser.",
            ),
            "adult": L(
                "Much of your life is already service nobody thanks you for. Here is how God sees it, and "
                "how to keep going.",
                "Gran parte de tu vida ya es un servicio que nadie agradece. Aquí está cómo lo ve Dios, y "
                "cómo seguir adelante.",
            ),
            "senior": L(
                "You may have less strength and more time. There is work only you can do: presence, "
                "prayer, encouragement.",
                "Quizá tengas menos fuerzas y más tiempo. Hay un trabajo que solo tú puedes hacer: estar "
                "presente, orar, animar.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "service-1",
                "ref": "John 13:12-17",
                "title": L("The Lord with a towel", "El Señor con una toalla"),
                "truth": L(
                    "Jesus has just knelt and washed his disciples' feet, the job of the lowest servant in "
                    "a house. Then he sits down and explains. He is their Lord and Teacher, he says, and "
                    "that is exactly why they should do the same for one another. He did not serve because "
                    "he lacked standing. He served knowing fully who he was. No task is beneath a follower "
                    "of Jesus, because none was beneath him. And he ends with a promise: the blessing is "
                    "in the doing, not only in the knowing.",
                    "Jesús acaba de arrodillarse y lavarles los pies a sus discípulos, el trabajo del "
                    "sirviente más bajo de una casa. Luego se sienta y lo explica. Él es su Señor y "
                    "Maestro, dice, y justo por eso ellos deben hacer lo mismo unos por otros. No sirvió "
                    "porque le faltara posición. Sirvió sabiendo muy bien quién era. Ninguna tarea está por "
                    "debajo de un seguidor de Jesús, porque ninguna estuvo por debajo de él. Y termina con "
                    "una promesa: la bendición está en hacerlo, no solo en saberlo.",
                ),
                "simple": L(
                    "Jesus washed his friends' dirty feet to show them how to love. He asks us to help "
                    "each other the same way.",
                    "Jesús les lavó los pies sucios a sus amigos para enseñarles cómo amar. Nos pide "
                    "ayudarnos unos a otros de la misma manera.",
                ),
                "ask": L(
                    "What task do you quietly consider beneath you, at home, at work or at church?",
                    "¿Qué tarea consideras, sin decirlo, que está por debajo de ti, en casa, en el trabajo "
                    "o en la iglesia?",
                ),
                "kid_ask": L(
                    "What is a job at home that nobody likes to do?",
                    "¿Cuál es un trabajo de la casa que a nadie le gusta hacer?",
                ),
                "do": L(
                    "Do that task once this week, cheerfully and without announcing it.",
                    "Haz esa tarea una vez esta semana, con buen ánimo y sin anunciarlo.",
                ),
                "kid_do": L(
                    "Do one job at home today that is not your favorite, like clearing the table, and do "
                    "it with a smile.",
                    "Haz hoy en casa un trabajo que no sea tu favorito, como recoger la mesa, y hazlo con "
                    "una sonrisa.",
                ),
                "pray": L(
                    "Jesus, you knelt with a towel. Nothing is beneath me if it was not beneath you. Show "
                    "me whose feet to wash this week.",
                    "Jesús, tú te arrodillaste con una toalla. Nada está por debajo de mí si no lo estuvo "
                    "de ti. Muéstrame a quién debo lavarle los pies esta semana.",
                ),
            },
            {
                "key": "service-2",
                "ref": "John 6:5-13",
                "title": L("Bring what you have", "Trae lo que tienes"),
                "truth": L(
                    "There is a hungry crowd of thousands, and the disciples can only count what they "
                    "lack. Andrew finds a boy with five small barley loaves and two fish, and almost "
                    "apologizes for mentioning it. Jesus takes that lunch, gives thanks, and feeds "
                    "everyone, with baskets left over. The boy did not have enough. He had something, and "
                    "it ended up in Jesus' hands. Serving does not start with being gifted, well off or "
                    "free of your own troubles. It starts with offering what you actually have.",
                    "Hay una multitud hambrienta de miles, y los discípulos solo saben contar lo que les "
                    "falta. Andrés encuentra a un muchacho con cinco panes pequeños de cebada y dos "
                    "pescados, y casi se disculpa por mencionarlo. Jesús toma ese almuerzo, da gracias y "
                    "alimenta a todos, y sobran canastas. El muchacho no tenía suficiente. Tenía algo, y "
                    "ese algo llegó a las manos de Jesús. Servir no empieza por tener talento, dinero o "
                    "una vida sin problemas. Empieza por ofrecer lo que de verdad tienes.",
                ),
                "simple": L(
                    "A boy shared his small lunch with Jesus, and Jesus used it to feed a huge crowd. "
                    "Jesus can use what you share, even if it is little.",
                    "Un niño compartió su pequeño almuerzo con Jesús, y Jesús lo usó para dar de comer a "
                    "muchísima gente. Jesús puede usar lo que compartes, aunque sea poquito.",
                ),
                "ask": L(
                    "What do you have (a skill, a spare hour, a room, a car, a listening ear) that you "
                    "have dismissed as too small to matter?",
                    "¿Qué tienes (una habilidad, una hora libre, un cuarto, un carro, un oído que escucha) "
                    "que has descartado por parecerte demasiado poco?",
                ),
                "kid_ask": L(
                    "What do you have that you could share with someone?",
                    "¿Qué tienes tú que podrías compartir con alguien?",
                ),
                "do": L(
                    "Write down three things you have, however ordinary. Pick one and offer it to a "
                    "specific person or need this week.",
                    "Escribe tres cosas que tienes, por comunes que sean. Elige una y ofrécela esta semana "
                    "a una persona o necesidad concreta.",
                ),
                "kid_do": L(
                    "Share part of your snack or one of your toys with someone today.",
                    "Comparte hoy con alguien parte de tu merienda o uno de tus juguetes.",
                ),
                "pray": L(
                    "Lord, here is what I have: … It is not much. Take it, give thanks over it, and use it "
                    "for someone.",
                    "Señor, esto es lo que tengo: … No es mucho. Tómalo, da gracias por ello y úsalo para "
                    "alguien.",
                ),
            },
            {
                "key": "service-3",
                "ref": "Matthew 6:1-4",
                "title": L("Work nobody sees", "El trabajo que nadie ve"),
                "truth": L(
                    "Jesus warns against doing good in order to be seen doing it. If applause is what you "
                    "are after, he says, applause is all you will get. Then he describes another way: "
                    "giving so quietly that one hand hardly knows what the other is doing. The Father sees "
                    "what is done in secret. This is good news for everyone whose service is hidden: the "
                    "night feedings, the cleaning, the care of a parent, the task no one will ever thank "
                    "you for. It is not lost. It is seen by the one whose notice matters most.",
                    "Jesús advierte contra hacer el bien para que te vean hacerlo. Si lo que buscas es el "
                    "aplauso, dice, el aplauso es todo lo que vas a recibir. Luego describe otro camino: "
                    "dar tan calladamente que una mano casi no sepa lo que hace la otra. El Padre ve lo "
                    "que se hace en secreto. Es una buena noticia para todos los que sirven a escondidas: "
                    "las desveladas con el bebé, la limpieza, el cuidado de un padre, la tarea que nadie "
                    "va a agradecer jamás. No se pierde. La ve aquel cuya mirada más importa.",
                ),
                "simple": L(
                    "You do not need everyone to see the good things you do. God sees, even when nobody "
                    "else does.",
                    "No necesitas que todos vean las cosas buenas que haces. Dios las ve, aunque nadie más "
                    "las vea.",
                ),
                "ask": L(
                    "How much of your serving depends on being noticed or thanked? What happens in you "
                    "when the thanks do not come?",
                    "¿Cuánto de tu servicio depende de que lo noten o lo agradezcan? ¿Qué pasa en ti "
                    "cuando el agradecimiento no llega?",
                ),
                "kid_ask": L(
                    "Could you do something kind in secret? What would it be?",
                    "¿Podrías hacer algo amable en secreto? ¿Qué sería?",
                ),
                "do": L(
                    "Do one good thing this week that no one can trace back to you, and tell nobody.",
                    "Haz esta semana algo bueno que nadie pueda saber que fuiste tú, y no se lo cuentes "
                    "a nadie.",
                ),
                "kid_do": L(
                    "Do a secret kind thing for someone at home today, and do not say it was you.",
                    "Haz hoy algo amable en secreto por alguien de tu casa, y no digas que fuiste tú.",
                ),
                "pray": L(
                    "Father, you see in secret. Free me from needing to be noticed. Let it be enough that "
                    "you know.",
                    "Padre, tú ves en lo secreto. Líbrame de necesitar que me noten. Que me baste con que "
                    "tú lo sepas.",
                ),
            },
            {
                "key": "service-4",
                "ref": "Matthew 25:34-40",
                "title": L(
                    "The face behind the need", "El rostro detrás de la necesidad"
                ),
                "truth": L(
                    "Jesus describes a day when the King welcomes people and tells them that they fed him, "
                    "took him in, clothed him and visited him when he was sick and in prison. They are "
                    "puzzled; they do not remember doing any of it. He answers that whatever they did for "
                    "the least of "
                    "his brothers and sisters, they did for him. The acts he lists are small and within "
                    "anyone's reach: a meal, a drink, a visit. Jesus identifies so closely with people in "
                    "need that serving them is serving him.",
                    "Jesús describe un día en que el Rey recibe a unas personas y les dice que le dieron de "
                    "comer, lo hospedaron, lo vistieron y lo visitaron cuando estuvo enfermo y en la "
                    "cárcel. Ellas se "
                    "extrañan; no recuerdan haber hecho nada de eso. Él responde que todo lo que hicieron "
                    "por el más pequeño de sus hermanos, lo hicieron por él. Los actos que menciona son "
                    "pequeños y están al alcance de cualquiera: una comida, un vaso de agua, una visita. "
                    "Jesús se identifica tanto con quienes pasan necesidad que servirles a ellos es "
                    "servirle a él.",
                ),
                "simple": L(
                    "When we help someone who is hungry, sick or lonely, Jesus says it is like helping "
                    "him.",
                    "Cuando ayudamos a alguien que tiene hambre, está enfermo o se siente solo, Jesús dice "
                    "que es como ayudarlo a él.",
                ),
                "ask": L(
                    "Who near you is hungry, sick, new in town or locked away, and when did you last come "
                    "close to one of them?",
                    "¿Quién cerca de ti tiene hambre, está enfermo, acaba de llegar o está encerrado, y "
                    "cuándo fue la última vez que te acercaste a alguno?",
                ),
                "kid_ask": L(
                    "Who do you know that is sick, sad or new and might need a friend?",
                    "¿A quién conoces que esté enfermo, triste o sea nuevo y quizá necesite un amigo?",
                ),
                "do": L(
                    "Choose one from the list (food, welcome, clothing, a visit to someone sick or "
                    "confined) and do it for one person this month. Put the date in your calendar today.",
                    "Elige una cosa de la lista (comida, hospitalidad, ropa, una visita a alguien enfermo "
                    "o encerrado) y hazla por una persona este mes. Anota hoy la fecha en tu calendario.",
                ),
                "kid_do": L(
                    "Make a card or a drawing for someone who is sick or lonely.",
                    "Haz una tarjeta o un dibujo para alguien que esté enfermo o se sienta solo.",
                ),
                "pray": L(
                    "Lord Jesus, I have walked past you without knowing it. Open my eyes to see you in "
                    "the person who needs something from me this week.",
                    "Señor Jesús, he pasado junto a ti sin saberlo. Ábreme los ojos para verte en la "
                    "persona que necesita algo de mí esta semana.",
                ),
            },
            {
                "key": "service-5",
                "ref": "Luke 10:38-42",
                "title": L(
                    "Serving without losing heart", "Servir sin perder el corazón"
                ),
                "truth": L(
                    "Martha welcomes Jesus into her home and works hard to serve him. That is good. But "
                    "the work turns into worry, and the worry into resentment: at her sister, and even at "
                    "Jesus, whom she accuses of not caring. Jesus answers her gently, saying her name "
                    "twice. He does not scold her for serving. He tells her she is anxious about many "
                    "things, and that Mary, sitting and listening, has chosen something that will not be "
                    "taken from her. Service that never sits at his feet runs dry. You are allowed to "
                    "stop, and you need to.",
                    "Marta recibe a Jesús en su casa y trabaja mucho para atenderlo. Eso es bueno. Pero el "
                    "trabajo se vuelve preocupación, y la preocupación resentimiento: contra su hermana, y "
                    "hasta contra Jesús, a quien le reclama que no le importa. Jesús le responde con "
                    "ternura, diciendo su nombre dos veces. No la regaña por servir. Le dice que está "
                    "inquieta por muchas cosas, y que María, sentada escuchando, eligió algo que nadie le "
                    "va a quitar. El servicio que nunca se sienta a sus pies termina por secarse. Tienes "
                    "permiso de parar, y lo necesitas.",
                ),
                "simple": L(
                    "Martha was so busy helping that she got upset. Jesus reminded her that being with "
                    "him matters most.",
                    "Marta estaba tan ocupada ayudando que se molestó. Jesús le recordó que lo más "
                    "importante es estar con él.",
                ),
                "ask": L(
                    "Where has your serving turned into resentment, and what might that be telling you "
                    "about your need to stop and receive?",
                    "¿Dónde se ha convertido tu servicio en resentimiento, y qué te estará diciendo eso "
                    "sobre tu necesidad de parar y recibir?",
                ),
                "kid_ask": L(
                    "What is your favorite way to spend quiet time with Jesus?",
                    "¿Cuál es tu manera favorita de pasar un rato tranquilo con Jesús?",
                ),
                "do": L(
                    "Tomorrow, before you do anything for anyone, sit for ten minutes with today's "
                    "passage and do nothing useful. If you are worn out from serving, tell someone and "
                    "ask for help with one thing.",
                    "Mañana, antes de hacer algo por alguien, siéntate diez minutos con el pasaje de hoy "
                    "y no hagas nada útil. Si servir te tiene sin fuerzas, cuéntaselo a alguien y pide "
                    "ayuda con una cosa.",
                ),
                "kid_do": L(
                    "Sit quietly for one minute today and tell Jesus you are glad to be with him.",
                    "Siéntate hoy un minuto en silencio y dile a Jesús que te alegra estar con él.",
                ),
                "pray": L(
                    "Lord, my mind is pulled in many directions: … Let me sit with you first. Then show me "
                    "what is mine to do, and what is not.",
                    "Señor, mi mente va en muchas direcciones a la vez: … Déjame sentarme contigo primero. "
                    "Luego muéstrame qué me toca hacer, y qué no.",
                ),
            },
        ],
    },
    # ======================================================================
    # SEASONS OF LIFE
    # ======================================================================
    {
        "key": "singleness",
        "category": "seasons",
        "title": L("Singleness: a whole life", "La soltería: una vida completa"),
        "summary": L(
            "For those who have never married, are divorced or are widowed. Five readings on a life that "
            "is whole now, not a waiting room: honest about longing, and clear that in Christ you are "
            "not half of anything.",
            "Para quienes nunca se casaron, se divorciaron o enviudaron. Cinco lecturas sobre una vida que "
            "ya es completa, no una sala de espera: con honestidad sobre el anhelo, y con la certeza de "
            "que en Cristo no eres la mitad de nada.",
        ),
        "keywords": [
            "singleness",
            "being single",
            "still single",
            "unmarried",
            "never married",
            "divorc",
            "widow",
            "solter",
            "sin pareja",
            "no me he casado",
            "divorci",
            "viud",
            "soledad",
        ],
        "situations": ["single", "divorced", "widowed", "single_parent"],
        "traits": ["contentment", "trust", "hope"],
        "stages": ["young_adult", "adult", "senior"],
        "stage_notes": {
            "young_adult": L(
                "When everyone around you seems to be pairing off, this is about a life that has already "
                "begun, not one on hold.",
                "Cuando parece que todos a tu alrededor forman pareja, esto trata de una vida que ya "
                "empezó, no de una vida en pausa.",
            ),
            "adult": L(
                "Never married, divorced, or raising children alone: your life is not a rough draft. "
                "Honest about the ache, clear about your worth.",
                "Sin haberte casado, después de un divorcio o criando hijos sin pareja: tu vida no es un "
                "borrador. Con honestidad sobre lo que duele y claridad sobre lo que vales.",
            ),
            "senior": L(
                "Widowed after many years, or single for a lifetime. Your days still hold purpose, company "
                "and God's full attention.",
                "Con muchos años de viudez o toda una vida de soltería. Tus días todavía tienen propósito, "
                "compañía y toda la atención de Dios.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "singleness-1",
                "ref": "1 Corinthians 7:32-35",
                "title": L("Not second best", "No es un segundo lugar"),
                "truth": L(
                    "In a world where nearly everyone was expected to marry, Paul, who was unmarried "
                    "himself, says something surprising: there is a real advantage in being single. An "
                    "unmarried person, he says, can give undivided attention to the Lord. He is careful to "
                    "add that he is not "
                    "laying down a restriction, and elsewhere he honors marriage too. But singleness is "
                    "not the lesser path or a problem to be solved. Jesus lived a full human life without "
                    "marrying. Whether this season is chosen, unwanted or temporary, it is a real life, "
                    "with its own freedom to give.",
                    "En un mundo donde se esperaba que casi todos se casaran, Pablo, que no estaba casado, "
                    "dice algo sorprendente: la soltería tiene una ventaja real. Una persona sin casarse, "
                    "dice, puede darle al Señor una atención sin divisiones. Tiene cuidado de aclarar que no "
                    "está imponiendo una restricción, y en otros lugares también honra el matrimonio. Pero "
                    "la soltería no es el camino menor ni un problema por resolver. Jesús vivió una vida "
                    "humana plena sin casarse. Sea esta etapa elegida, no deseada o pasajera, es una vida "
                    "real, con su propia libertad para dar.",
                ),
                "simple": L(
                    "Some grown-ups are married and some are not. Both are good ways to live and to "
                    "love God.",
                    "Algunos adultos están casados y otros no. Las dos son buenas maneras de vivir y de "
                    "amar a Dios.",
                ),
                "ask": L(
                    "Where have you taken in the idea that your life starts when you find someone? What "
                    "is already here to be lived?",
                    "¿Dónde aprendiste la idea de que tu vida empieza cuando encuentres a alguien? ¿Qué "
                    "hay ya aquí para vivir?",
                ),
                "kid_ask": L(
                    "Which grown-ups who are not your parents are kind to you?",
                    "¿Qué adultos, además de tus padres, son buenos contigo?",
                ),
                "do": L(
                    "List three things your present life makes possible (time, flexibility, attention for "
                    "certain people). Give one of them on purpose to God or to someone else this week.",
                    "Haz una lista de tres cosas que tu vida actual hace posibles (tiempo, flexibilidad, "
                    "atención para ciertas personas). Esta semana dale una de ellas, a propósito, a Dios "
                    "o a alguien más.",
                ),
                "kid_do": L(
                    "Say thank you to a grown-up who cares about you, like an aunt, an uncle, a teacher "
                    "or a neighbor.",
                    "Dale las gracias a un adulto que te quiere, como una tía, un tío, una maestra o "
                    "un vecino.",
                ),
                "pray": L(
                    "Lord, this is the life I have today. I do not want to wait to live it. Show me what "
                    "my undivided attention could be given to.",
                    "Señor, esta es la vida que tengo hoy. No quiero esperar para vivirla. Muéstrame a "
                    "qué podría darle mi atención entera.",
                ),
            },
            {
                "key": "singleness-2",
                "ref": "Colossians 2:9-10",
                "title": L("Already whole", "Ya tienes plenitud"),
                "truth": L(
                    "Paul says that all the fullness of God lives in Christ, and that those who belong to "
                    "Christ have been brought to fullness in him. Notice the tense: have been. Not will be "
                    "once you marry, or once the loneliness lifts. Films and songs, and sometimes "
                    "churches, suggest a person is half of something until the other half arrives. "
                    "Scripture never says that. A spouse is a gift, not a completion. You are a whole "
                    "person now, and a whole person is what you would bring into any relationship.",
                    "Pablo dice que toda la plenitud de Dios habita en Cristo, y que quienes son de Cristo "
                    "han recibido esa plenitud en él. Fíjate en el tiempo del verbo: han recibido. No dice "
                    "que la recibirán cuando se casen, o cuando se vaya la soledad. Las películas y las "
                    "canciones, y a veces las iglesias, dan a entender que una persona es la mitad de algo "
                    "hasta que llega la otra mitad. La Escritura nunca dice eso. Un cónyuge es un regalo, "
                    "no lo que te completa. Ya eres una persona entera, y una persona entera es lo que "
                    "llevarías a cualquier relación.",
                ),
                "simple": L(
                    "You are a whole person, and Jesus loves you just as you are. You do not need someone "
                    "else to make you complete.",
                    "Tú eres una persona completa, y Jesús te ama tal como eres. No necesitas a nadie más "
                    "para serlo.",
                ),
                "ask": L(
                    "What have you been expecting another person to supply that this passage says you "
                    "already have in Christ?",
                    "¿Qué has estado esperando que otra persona te dé y que, según este pasaje, ya tienes "
                    "en Cristo?",
                ),
                "kid_ask": L(
                    "What is something special about the way God made you?",
                    "¿Qué tiene de especial la manera en que Dios te hizo?",
                ),
                "do": L(
                    "Each morning this week, before you look at your phone, say once: in Christ I am not "
                    "missing anything I need to be whole.",
                    "Cada mañana de esta semana, antes de mirar el teléfono, di una vez: en Cristo no me "
                    "falta nada para ser una persona completa.",
                ),
                "kid_do": L(
                    'Look in the mirror and say, "God made me, and God loves me."',
                    'Mírate al espejo y di: "Dios me hizo, y Dios me ama".',
                ),
                "pray": L(
                    "Jesus, in you I have been made whole. On the days I feel like half of something, "
                    "remind me whose I am.",
                    "Jesús, en ti he recibido plenitud. Los días en que me siento la mitad de algo, "
                    "recuérdame de quién soy.",
                ),
            },
            {
                "key": "singleness-3",
                "ref": "Psalm 62:5-8",
                "title": L(
                    "Honest about the ache", "Con honestidad sobre lo que duele"
                ),
                "truth": L(
                    "Being whole in Christ does not mean you feel no longing. David tells his own soul to "
                    "wait quietly for God, his rock and refuge, and then tells everyone to pour out their "
                    "hearts before him. Not to tidy them first. If you want to be married and are not, if "
                    "you miss the one who died, if the divorce still aches, God wants to hear exactly "
                    "that. Longing is not a lack of faith, and contentment is not pretending. You can "
                    "trust God and grieve what you do not have in the same prayer.",
                    "Tener plenitud en Cristo no significa que no sientas anhelo. David le dice a su "
                    "propia alma que espere en silencio a Dios, su roca y su refugio, y luego les dice a "
                    "todos que derramen el corazón delante de él. No que lo ordenen primero. Si quieres "
                    "casarte y no ha pasado, si extrañas a quien murió, si el divorcio todavía duele, Dios "
                    "quiere oír exactamente eso. Anhelar no es falta de fe, y el contentamiento no es "
                    "fingir. Puedes confiar en Dios y llorar lo que no tienes en la misma oración.",
                ),
                "simple": L(
                    "You can tell God everything you feel, the happy things and the sad things. He is a "
                    "safe place.",
                    "Puedes contarle a Dios todo lo que sientes, lo alegre y lo triste. Él es un lugar "
                    "seguro.",
                ),
                "ask": L(
                    "What would you say to God about being single if you were not trying to sound "
                    "content?",
                    "¿Qué le dirías a Dios sobre tu soltería si no estuvieras tratando de sonar conforme?",
                ),
                "kid_ask": L(
                    "What do you do when you feel lonely?",
                    "¿Qué haces cuando te sientes solo?",
                ),
                "do": L(
                    "Set a timer for ten minutes and pour it out to God, spoken or written, with no "
                    "editing. End with one sentence: you are my refuge. This week, also tell one trusted "
                    "friend how you really are.",
                    "Pon una alarma de diez minutos y derrama todo delante de Dios, hablado o escrito, sin "
                    "corregir nada. Termina con una frase: tú eres mi refugio. Esta semana cuéntale "
                    "también a una amistad de confianza cómo estás de verdad.",
                ),
                "kid_do": L(
                    "Tell God one thing that makes you sad and one thing that makes you glad.",
                    "Cuéntale a Dios una cosa que te pone triste y una cosa que te alegra.",
                ),
                "pray": L(
                    "God, here is the truth: … I am not going to dress it up. Be my rock on the nights "
                    "the house is too quiet.",
                    "Dios, esta es la verdad: … No la voy a adornar. Sé mi roca en las noches en que la "
                    "casa está demasiado callada.",
                ),
            },
            {
                "key": "singleness-4",
                "ref": "Isaiah 56:3-5",
                "title": L("A place and a name", "Un lugar y un nombre"),
                "truth": L(
                    "In Isaiah's day a foreigner, or a eunuch (a man who could not have children), would "
                    "assume he had no future among God's people. No family line meant no name. God "
                    "answers them directly: do not call yourself a dry tree. To those who hold fast to "
                    "him he promises a place within his house and a name better than sons and daughters, "
                    "one that will never be cut off. Your place in God's family does not come through a "
                    "spouse or through children. It is given to you directly, and it lasts.",
                    "En tiempos de Isaías, un extranjero o un eunuco (un hombre que no podía tener hijos) "
                    "daba por hecho que no tenía futuro en el pueblo de Dios. Sin descendencia no había "
                    "nombre. Dios les responde directamente: no te llames árbol seco. A quienes se aferran "
                    "a él les promete un lugar dentro de su casa y un nombre mejor que el de hijos e "
                    "hijas, un nombre que nunca será borrado. Tu lugar en la familia de Dios no llega por "
                    "medio de un cónyuge ni de los hijos. Se te da directamente, y permanece.",
                ),
                "simple": L(
                    "Everyone who loves God has a place in his family. Nobody is left out.",
                    "Todos los que aman a Dios tienen un lugar en su familia. Nadie se queda fuera.",
                ),
                "ask": L(
                    "Where do you feel like an outsider at church or in your family because you are single "
                    "or without children? What does God say here about your place?",
                    "¿Dónde te sientes de afuera, en la iglesia o en tu familia, por no tener pareja o "
                    "hijos? ¿Qué dice Dios aquí sobre tu lugar?",
                ),
                "kid_ask": L(
                    "How can you help someone feel that they belong?",
                    "¿Cómo puedes ayudar a que alguien sienta que tiene un lugar?",
                ),
                "do": L(
                    "Take one step into God's family this week: invite someone to your table, accept an "
                    "invitation you would usually decline, or ask a household at church if you may join "
                    "them for a meal.",
                    "Da esta semana un paso hacia la familia de Dios: invita a alguien a tu mesa, acepta "
                    "una invitación que normalmente rechazarías, o pregúntale a una familia de la iglesia "
                    "si puedes acompañarlos a comer.",
                ),
                "kid_do": L(
                    "Invite someone who is sitting alone to join you.",
                    "Invita a alguien que esté sentado sin compañía a estar contigo.",
                ),
                "pray": L(
                    "Lord, you give a place and a name that cannot be taken away. When I feel like a dry "
                    "tree, say this to me again. Show me where I belong, and whom I can welcome.",
                    "Señor, tú das un lugar y un nombre que nadie puede quitar. Cuando me sienta árbol "
                    "seco, dímelo otra vez. Muéstrame dónde pertenezco, y a quién puedo recibir.",
                ),
            },
            {
                "key": "singleness-5",
                "ref": "Luke 2:36-38",
                "title": L("Anna's long faithfulness", "La larga fidelidad de Ana"),
                "truth": L(
                    "Anna was married for seven years and then widowed. When we meet her she is very old, "
                    "and she has spent the long years since in worship, fasting and prayer. Luke does not "
                    "present her as a sad footnote. He calls her a prophet. She is among the first to "
                    "recognize the child Jesus, and she speaks about him to everyone who was waiting for "
                    "God's rescue. Her life after loss was not a waiting room. It had a purpose, a place "
                    "and a voice. So does yours.",
                    "Ana estuvo casada siete años y luego enviudó. Cuando la conocemos ya es muy anciana, "
                    "y ha pasado los largos años desde entonces en adoración, ayuno y oración. Lucas no la "
                    "presenta como una nota triste al pie de la página. La llama profetisa. Es de las "
                    "primeras en reconocer al niño Jesús, y habla de él a todos los que esperaban el "
                    "rescate de Dios. Su vida después de la pérdida no fue una sala de espera. Tuvo un "
                    "propósito, un lugar y una voz. La tuya también.",
                ),
                "simple": L(
                    "Anna was a very old woman who had lived without a husband for many years. She loved "
                    "God, and she got to see baby Jesus and tell others about him.",
                    "Ana era una mujer muy anciana que había vivido muchos años sin esposo. Amaba a Dios, "
                    "y pudo ver al niño Jesús y contarles a otros acerca de él.",
                ),
                "ask": L(
                    "What might God want to do through you in this season precisely because of the way "
                    "your life is arranged now?",
                    "¿Qué podría querer hacer Dios por medio de ti en esta etapa, justamente por la forma "
                    "en que está organizada tu vida ahora?",
                ),
                "kid_ask": L(
                    "Who is an older person you know who loves God?",
                    "¿Qué persona mayor conoces que ama a Dios?",
                ),
                "do": L(
                    "Name one person or one piece of work that could be your steady faithfulness (praying "
                    "daily for someone, mentoring, serving at church) and begin it this week.",
                    "Nombra a una persona o una tarea que podría ser tu fidelidad constante (orar a diario "
                    "por alguien, acompañar a alguien más joven, servir en la iglesia) y empieza esta "
                    "semana.",
                ),
                "kid_do": L(
                    "Ask an older person you know to tell you a story about God.",
                    "Pídele a una persona mayor que conoces que te cuente una historia sobre Dios.",
                ),
                "pray": L(
                    "God, you saw Anna through all those years, and you see me. Give my days a purpose. "
                    "Let me recognize Jesus and speak of him to someone.",
                    "Dios, tú viste a Ana durante todos esos años, y me ves a mí. Dales un propósito a mis "
                    "días. Permíteme reconocer a Jesús y hablarle de él a alguien.",
                ),
            },
        ],
    },
    {
        "key": "aging",
        "category": "seasons",
        "title": L("Growing older", "Envejecer"),
        "summary": L(
            "For anyone feeling the years: a slower body, a shorter list of what you can do, questions "
            "about what you are still for. Five readings on being carried, still bearing fruit, and "
            "passing faith on.",
            "Para quien siente el paso de los años: un cuerpo más lento, una lista más corta de lo que "
            "puedes hacer, preguntas sobre para qué sigues aquí. Cinco lecturas sobre ser sostenido, "
            "seguir dando fruto y transmitir la fe.",
        ),
        "keywords": [
            "aging",
            "getting older",
            "growing old",
            "retire",
            "grandchild",
            "legacy",
            "frail",
            "envejec",
            "vejez",
            "jubil",
            "niet",
            "legado",
            "achaque",
            "ya no puedo",
        ],
        "situations": ["retired", "grandparent", "widowed", "ill"],
        "traits": ["hope", "faithfulness", "gratitude"],
        "stages": ["adult", "senior"],
        "stage_notes": {
            "adult": L(
                "The first gray hairs, a slower body, parents growing frail. A way to meet the years ahead "
                "without dread.",
                "Las primeras canas, un cuerpo más lento, padres que se van debilitando. Una forma de "
                "recibir los años que vienen sin temor.",
            ),
            "senior": L(
                "For a season of limits and of freedom: what you can no longer do, what only you can give, "
                "and who carries you.",
                "Para una etapa de límites y de libertad: lo que ya no puedes hacer, lo que solo tú puedes "
                "dar, y quién te sostiene.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "aging-1",
                "ref": "Isaiah 46:3-4",
                "title": L("Carried all the way", "Dios te sostiene hasta el final"),
                "truth": L(
                    "God speaks to his people as one who has carried them since before they were born. "
                    "Then he looks ahead: even to your old age, even when your hair is gray, he is the "
                    "same, and he will carry you. Just before this, Isaiah describes the idols of Babylon "
                    "being loaded onto weary animals; those gods have to be carried. The living God "
                    "carries his people. As strength lessens and you need more help, you are not becoming "
                    "a burden to him. He made you, and he has promised to sustain you to the end.",
                    "Dios le habla a su pueblo como quien lo ha cargado desde antes de nacer. Luego mira "
                    "hacia adelante: hasta tu vejez, hasta cuando tengas canas, él es el mismo, y te va a "
                    "sostener. Justo antes, Isaías describe a los ídolos de Babilonia cargados sobre "
                    "animales cansados; a esos dioses hay que llevarlos. El Dios vivo es quien lleva a su "
                    "pueblo. Cuando las fuerzas disminuyen y necesitas más ayuda, no te estás volviendo "
                    "una carga para él. Él te hizo, y prometió sostenerte hasta el final.",
                ),
                "simple": L(
                    "God takes care of people when they are babies, when they are grown, and when they "
                    "are very old. He never stops.",
                    "Dios cuida a las personas cuando son bebés, cuando son grandes y cuando son muy "
                    "ancianas. Nunca deja de hacerlo.",
                ),
                "ask": L(
                    "What frightens you most about growing older, and what does this promise say to that "
                    "particular fear?",
                    "¿Qué es lo que más te asusta de envejecer, y qué le dice esta promesa a ese temor "
                    "en particular?",
                ),
                "kid_ask": L(
                    "Who is the oldest person you know? What do you like about them?",
                    "¿Quién es la persona de más edad que conoces? ¿Qué te gusta de ella?",
                ),
                "do": L(
                    "Write down the one fear about aging that visits you most. Under it, write in your "
                    "own words what God promises in this passage. Keep it where you will see it.",
                    "Escribe el temor sobre la vejez que más te visita. Debajo, escribe con tus propias "
                    "palabras lo que Dios promete en este pasaje. Guárdalo donde lo veas.",
                ),
                "kid_do": L(
                    "Give a hug or a kind word to an older person today.",
                    "Dale hoy un abrazo o una palabra amable a una persona mayor.",
                ),
                "pray": L(
                    "Lord, you carried me before I knew you, and you say you will carry me still. When I "
                    "am afraid of what is coming, hold me.",
                    "Señor, me llevaste en brazos antes de que yo te conociera, y dices que me seguirás "
                    "llevando. Cuando tenga miedo de lo que viene, sostenme.",
                ),
            },
            {
                "key": "aging-2",
                "ref": "2 Corinthians 4:16-18",
                "title": L("When the body slows", "Cuando el cuerpo va más lento"),
                "truth": L(
                    "Paul does not pretend. Outwardly, he says, we are wearing away. Bodies slow, ache and "
                    "fail, and it is right to grieve what you can no longer do. But he sets a second truth "
                    "beside it: inwardly we are being renewed day by day. The person you are before God "
                    "can keep growing while the body declines. He calls present troubles light and brief "
                    "only by comparison with what is coming, a glory that outweighs them, and he fixes "
                    "his eyes on what is unseen and lasting.",
                    "Pablo no finge. Por fuera, dice, nos vamos desgastando. El cuerpo se vuelve lento, "
                    "duele y falla, y está bien llorar lo que ya no puedes hacer. Pero al lado pone una "
                    "segunda verdad: por dentro nos vamos renovando día tras día. La persona que eres "
                    "delante de Dios puede seguir creciendo mientras el cuerpo decae. Llama ligeras y "
                    "breves a las aflicciones de ahora solo en comparación con lo que viene, una gloria "
                    "que pesa mucho más, y fija la mirada en lo que no se ve y permanece.",
                ),
                "simple": L(
                    "Our bodies get older and slower, but God keeps making our hearts new and strong on "
                    "the inside.",
                    "Nuestro cuerpo se hace más viejo y más lento, pero Dios sigue haciendo nuevo y fuerte "
                    "nuestro corazón por dentro.",
                ),
                "ask": L(
                    "What have you had to give up as your body has changed? And where are you more alive "
                    "inside than you were at thirty?",
                    "¿A qué has tenido que renunciar con los cambios de tu cuerpo? ¿Y en qué tienes más "
                    "vida por dentro que a los treinta?",
                ),
                "kid_ask": L(
                    "What matters more about a person than how strong or fast they are?",
                    "¿Qué importa más de una persona que lo fuerte o lo rápida que es?",
                ),
                "do": L(
                    "Name one loss honestly to God today. Then name one way you have grown inwardly in "
                    "recent years, and thank him. If a change in your health is worrying you, tell your "
                    "doctor and someone close to you.",
                    "Dile hoy a Dios, con honestidad, una pérdida. Luego nombra una forma en que has "
                    "crecido por dentro en los últimos años, y dale gracias. Si te preocupa un cambio en "
                    "tu salud, díselo a tu médico y a alguien cercano.",
                ),
                "kid_do": L(
                    "Ask a grandparent or an older friend what they know now that they did not know at "
                    "your age.",
                    "Pregúntale a un abuelo o a un amigo mayor qué sabe ahora que no sabía a tu edad.",
                ),
                "pray": L(
                    "God, my body is not what it was, and I miss what I could do. Renew me inside today. "
                    "Fix my eyes on what does not wear out.",
                    "Dios, mi cuerpo ya no es el que era, y extraño lo que podía hacer. Renuévame hoy por "
                    "dentro. Fija mis ojos en lo que no se desgasta.",
                ),
            },
            {
                "key": "aging-3",
                "ref": "Psalm 92:12-15",
                "title": L("Still bearing fruit", "Todavía das fruto"),
                "truth": L(
                    "The psalm pictures people rooted in God as palms and cedars, trees that live long and "
                    "stay green. Planted in the Lord's house, they still bear fruit in old age. The fruit "
                    "named here is not productivity. It is a life that declares that God is upright and "
                    "dependable, a rock. Age makes that more possible, not less: you have decades of "
                    "evidence. You may do less than you once did. Your worth to God was never measured in "
                    "output. A long life that still trusts him says something no young life can.",
                    "El salmo describe a quienes están arraigados en Dios como palmeras y cedros, árboles "
                    "que viven mucho y se mantienen verdes. Plantados en la casa del Señor, todavía dan "
                    "fruto en la vejez. El fruto que aquí se nombra no es productividad. Es una vida que "
                    "declara que Dios es recto y digno de confianza, una roca. La edad hace eso más "
                    "posible, no menos: tienes décadas de evidencia. Quizá hagas menos que antes. Tu valor "
                    "para Dios nunca se midió por tu rendimiento. Una vida larga que sigue confiando en él "
                    "dice algo que ninguna vida joven puede decir.",
                ),
                "simple": L(
                    "People who love God are like strong trees. Even when they are very old, they still "
                    "give good fruit.",
                    "Las personas que aman a Dios son como árboles fuertes. Aun cuando son muy ancianas, "
                    "siguen dando buen fruto.",
                ),
                "ask": L(
                    "If your worth is not measured by how much you can do, what fruit could your life "
                    "bear in this season?",
                    "Si tu valor no se mide por cuánto puedes hacer, ¿qué fruto podría dar tu vida en "
                    "esta etapa?",
                ),
                "kid_ask": L(
                    "What good things do older people give you?",
                    "¿Qué cosas buenas te dan las personas mayores?",
                ),
                "do": L(
                    "This week, tell one younger person a specific story of how God proved dependable in "
                    "your life. Keep it short and true.",
                    "Esta semana cuéntale a una persona más joven una historia concreta de cómo Dios "
                    "demostró ser digno de confianza en tu vida. Que sea breve y verdadera.",
                ),
                "kid_do": L(
                    'Ask an older person, "What is a good thing God has done for you?" and listen to '
                    "the answer.",
                    'Pregúntale a una persona mayor: "¿Qué cosa buena ha hecho Dios por ti?", y escucha '
                    "su respuesta.",
                ),
                "pray": L(
                    "Lord, keep me green. I can do less, but let my life still say that you are my rock "
                    "and that you can be trusted.",
                    "Señor, mantenme verde. Puedo hacer menos, pero que mi vida siga diciendo que tú eres "
                    "mi roca y que se puede confiar en ti.",
                ),
            },
            {
                "key": "aging-4",
                "ref": "Psalm 71:17-18",
                "title": L("Pass it on", "Pásalo a los que vienen"),
                "truth": L(
                    "The writer has known God since youth and has spent a lifetime telling what God has "
                    "done. Now, old and gray, he asks one thing: do not leave me until I have told the "
                    "next generation about your power. He sees his remaining years as having a purpose. "
                    "Those who come after need to hear, from someone who has lived it, that God is real "
                    "and faithful. You do not need to preach. You need to tell what you have seen, to a "
                    "grandchild, a neighbor, a young person at church.",
                    "Quien escribe ha conocido a Dios desde joven y ha pasado la vida contando lo que Dios "
                    "ha hecho. Ahora, viejo y con canas, pide una cosa: no me dejes hasta que le haya "
                    "contado de tu poder a la generación que viene. Ve los años que le quedan como años "
                    "con propósito. Los que vienen detrás necesitan oír, de alguien que lo ha vivido, que "
                    "Dios es real y fiel. No hace falta predicar. Hace falta contar lo que has visto: a un "
                    "nieto, a un vecino, a un joven de la iglesia.",
                ),
                "simple": L(
                    "Older people have many stories about how God helped them. They can share those "
                    "stories with children like you.",
                    "Las personas mayores tienen muchas historias de cómo Dios las ayudó. Pueden "
                    "compartirlas con niños como tú.",
                ),
                "ask": L(
                    "Who in the next generation is within your reach, and what do you most want them to "
                    "know about God?",
                    "¿Quién de la siguiente generación está a tu alcance, y qué es lo que más quieres que "
                    "sepa de Dios?",
                ),
                "kid_ask": L(
                    "What story about God would you like to hear from a grandparent or an older friend?",
                    "¿Qué historia sobre Dios te gustaría escuchar de un abuelo o de un amigo mayor?",
                ),
                "do": L(
                    "Write one page, or record a few minutes, telling one story of God's faithfulness in "
                    "your life for a particular younger person. Give it to them this month.",
                    "Escribe una página, o graba unos minutos, contando una historia de la fidelidad de "
                    "Dios en tu vida para una persona más joven en particular. Entrégasela este mes.",
                ),
                "kid_do": L(
                    "Ask a grandparent or an older friend to tell you how they came to know God.",
                    "Pídele a un abuelo o a un amigo mayor que te cuente cómo llegó a conocer a Dios.",
                ),
                "pray": L(
                    "God, you have taught me since I was young. Do not let me go until I have told … what "
                    "you have done. Give me the words and the opening.",
                    "Dios, tú me has enseñado desde mi juventud. No me sueltes hasta que le haya contado "
                    "a … lo que has hecho. Dame las palabras y la oportunidad.",
                ),
            },
            {
                "key": "aging-5",
                "ref": "Psalm 90:12-17",
                "title": L("Number your days", "Cuenta tus días"),
                "truth": L(
                    "This prayer, handed down under the name of Moses, asks God to teach us to count our "
                    "days so that we gain a wise heart. Counting them is not morbid. It is how you learn "
                    "what matters. Then the prayer turns hopeful: fill us in the morning with your "
                    "faithful love, make us glad, show your work to your servants and your splendor to "
                    "their children. It ends by asking twice that God would make the work of our hands "
                    "last. What you leave behind is not finally in your control. You can place it in the "
                    "hands of the one who makes things endure.",
                    "Esta oración, transmitida con el nombre de Moisés, le pide a Dios que nos enseñe a "
                    "contar nuestros días para que tengamos un corazón sabio. Contarlos no es algo "
                    "morboso. Es la manera de aprender qué importa. Luego la oración se llena de "
                    "esperanza: sácianos por la mañana con tu amor fiel, alégranos, muestra tu obra a tus "
                    "siervos y tu esplendor a sus hijos. Termina pidiendo dos veces que Dios haga durar la "
                    "obra de nuestras manos. Lo que dejas no está, al final, bajo tu control. Puedes "
                    "ponerlo en las manos de quien hace que las cosas permanezcan.",
                ),
                "simple": L(
                    "Every day is a gift from God. We can ask him to help us use each day well.",
                    "Cada día es un regalo de Dios. Podemos pedirle que nos ayude a usar bien cada día.",
                ),
                "ask": L(
                    "If you counted your days honestly, what would you stop spending them on, and what "
                    "would you begin?",
                    "Si contaras tus días con honestidad, ¿en qué dejarías de gastarlos, y qué empezarías?",
                ),
                "kid_ask": L(
                    "What is one good thing you would like to do with today?",
                    "¿Qué cosa buena te gustaría hacer con el día de hoy?",
                ),
                "do": L(
                    "Choose one piece of unfinished business (a conversation, a letter, a will, a "
                    "reconciliation, a blessing to speak) and take the first step this week.",
                    "Elige un asunto pendiente (una conversación, una carta, un testamento, una "
                    "reconciliación, una bendición que decir) y da el primer paso esta semana.",
                ),
                "kid_do": L(
                    "Tonight, thank God for one good thing that happened today.",
                    "Esta noche, dale gracias a Dios por una cosa buena que pasó hoy.",
                ),
                "pray": L(
                    "Lord, teach me to number my days. Satisfy me with your love this morning, and make "
                    "what my hands have done outlast me.",
                    "Señor, enséñame a contar mis días. Sáciame de tu amor esta mañana, y haz que lo que "
                    "hicieron mis manos dure más que yo.",
                ),
            },
        ],
    },
    {
        "key": "change",
        "category": "seasons",
        "title": L("Change and new beginnings", "Cambios y nuevos comienzos"),
        "summary": L(
            "For when life is shifting under you: a move, a new school or job, an ending you did not "
            "choose, a fresh start. Five readings on the God who goes ahead of you and does not change.",
            "Para cuando la vida se mueve bajo tus pies: una mudanza, una escuela o un trabajo nuevo, un "
            "final que no elegiste, un nuevo comienzo. Cinco lecturas sobre el Dios que va delante de ti "
            "y no cambia.",
        ),
        "keywords": [
            "change",
            "moving",
            "new job",
            "new school",
            "transition",
            "starting over",
            "uncertain",
            "cambio",
            "mudanza",
            "mudar",
            "nuevo trabajo",
            "nueva escuela",
            "transici",
            "empezar de nuevo",
            "incertidumbre",
        ],
        "situations": ["moving", "student", "job_seeking", "retired", "divorced"],
        "traits": ["trust", "courage", "hope"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "A new school, a new house or a new baby can feel scary. God goes with you into every "
                "new thing.",
                "Una escuela nueva, una casa nueva o un bebé nuevo pueden dar miedo. Dios va contigo a "
                "cada cosa nueva.",
            ),
            "teen": L(
                "New school, new friends, a family that is changing. When nothing feels solid, here is "
                "something that is.",
                "Escuela nueva, amigos nuevos, una familia que está cambiando. Cuando nada se siente "
                "firme, aquí hay algo que sí lo es.",
            ),
            "young_adult": L(
                "Graduating, moving, first jobs, relationships beginning and ending. For walking forward "
                "without a map.",
                "Graduarte, mudarte, los primeros trabajos, relaciones que empiezan y terminan. Para "
                "caminar hacia adelante sin mapa.",
            ),
            "adult": L(
                "A job lost or changed, a move, a child leaving home, a life to rebuild. God is already "
                "ahead of you there.",
                "Un trabajo que se pierde o cambia, una mudanza, un hijo que se va de casa, una vida por "
                "reconstruir. Dios ya está allí, delante de ti.",
            ),
            "senior": L(
                "Retirement, a smaller home, new limits, faces missing. Even now God leads people into "
                "new chapters.",
                "La jubilación, una casa más pequeña, nuevos límites, rostros que faltan. Aun ahora Dios "
                "guía a las personas hacia capítulos nuevos.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "change-1",
                "ref": "Genesis 12:1-4",
                "title": L("Going without a map", "Salir sin mapa"),
                "truth": L(
                    "God tells Abram to leave his country, his relatives and his father's house for a "
                    "land he will be shown later. There is no map, only a promise: God will bless him, "
                    "and through him others will be blessed. And Abram goes. The passage notes that he "
                    "was seventy-five. Many big changes come like this, with one clear next step and very "
                    "little view of the road beyond it. Faith is not knowing how it turns out. It is "
                    "taking the step you have been given, trusting the one who goes with you.",
                    "Dios le dice a Abram que deje su tierra, a sus parientes y la casa de su padre, y "
                    "vaya a una tierra que le mostrará después. No hay mapa, solo una promesa: Dios lo "
                    "bendecirá, y por medio de él otros serán bendecidos. Y Abram sale. El pasaje anota "
                    "que tenía setenta y cinco años. Muchos cambios grandes llegan así: con un siguiente "
                    "paso claro y muy poca vista del camino que sigue. La fe no es saber cómo va a "
                    "terminar. Es dar el paso que se te ha dado, confiando en quien va contigo.",
                ),
                "simple": L(
                    "God asked Abram to move to a new place far away. Abram did not know what it would be "
                    "like, but he trusted God and went.",
                    "Dios le pidió a Abram que se fuera a un lugar nuevo y lejano. Abram no sabía cómo "
                    "sería, pero confió en Dios y fue.",
                ),
                "ask": L(
                    "What is the one next step you can see in the change you are facing, even if you "
                    "cannot see past it?",
                    "¿Cuál es el siguiente paso que sí alcanzas a ver en el cambio que enfrentas, aunque "
                    "no veas más allá?",
                ),
                "kid_ask": L(
                    "What new thing is happening in your life, or coming soon?",
                    "¿Qué cosa nueva está pasando en tu vida, o va a pasar pronto?",
                ),
                "do": L(
                    "Write down the next step you can actually take this week, and take it. Leave the "
                    "steps after it with God for now.",
                    "Escribe el siguiente paso que de verdad puedes dar esta semana, y dalo. Por ahora, "
                    "deja con Dios los pasos que vienen después.",
                ),
                "kid_do": L(
                    "Draw something new in your life, and draw God right there with you.",
                    "Dibuja algo nuevo en tu vida, y dibuja a Dios ahí mismo contigo.",
                ),
                "pray": L(
                    "God, I cannot see where this goes. You can. Show me the next step, and give me the "
                    "trust to take it.",
                    "Dios, yo no veo adónde lleva esto. Tú sí. Muéstrame el siguiente paso, y dame "
                    "confianza para darlo.",
                ),
            },
            {
                "key": "change-2",
                "ref": "Ecclesiastes 3:1-8",
                "title": L("Endings are real", "Los finales son reales"),
                "truth": L(
                    "The Teacher lists the seasons of a life in pairs: planting and uprooting, weeping "
                    "and laughing, keeping and letting go. He does not rank them or hurry past the hard "
                    "ones. Each has its time. Every new beginning is also an ending, and even a change "
                    "you wanted takes something from you: a place, a routine, people you saw every day. "
                    "You are allowed to grieve what is over while you walk into what is next. Naming the "
                    "loss is not ingratitude. It is part of moving on honestly.",
                    "El Maestro enumera por pares las épocas de una vida: plantar y arrancar, llorar y "
                    "reír, guardar y soltar. No las ordena por importancia ni pasa de prisa por las "
                    "difíciles. Cada una tiene su tiempo. Todo comienzo es también un final, y hasta un "
                    "cambio que deseabas te quita algo: un lugar, una rutina, gente que veías todos los "
                    "días. Tienes permiso de llorar lo que terminó mientras caminas hacia lo que sigue. "
                    "Ponerle nombre a la pérdida no es ingratitud. Es parte de avanzar con honestidad.",
                ),
                "simple": L(
                    "There is a time for everything: a time to be happy and a time to be sad. When "
                    "something changes, it is okay to miss the way it was.",
                    "Hay un tiempo para todo: un tiempo para estar alegre y un tiempo para estar triste. "
                    "Cuando algo cambia, está bien extrañar cómo era antes.",
                ),
                "ask": L(
                    "What is ending for you in this change, and have you let yourself be sad about it?",
                    "¿Qué está terminando para ti con este cambio, y te has permitido sentir tristeza "
                    "por ello?",
                ),
                "kid_ask": L(
                    "Is there something or someone you miss?",
                    "¿Hay algo o alguien que extrañas?",
                ),
                "do": L(
                    "Make two short lists: what I am leaving behind, and what I am walking toward. Thank "
                    "God for one thing on the first list before you ask him about the second.",
                    "Haz dos listas cortas: lo que dejo atrás y hacia dónde voy. Dale gracias a Dios por "
                    "una cosa de la primera lista antes de pedirle por la segunda.",
                ),
                "kid_do": L(
                    "Tell a grown-up one thing you miss and one thing you are looking forward to.",
                    "Cuéntale a un adulto una cosa que extrañas y una cosa que esperas con ganas.",
                ),
                "pray": L(
                    "Lord, a season is ending and I feel it. Thank you for … Help me let go with "
                    "gratitude, and open my hands for what is next.",
                    "Señor, una etapa se está acabando y lo siento. Gracias por … Ayúdame a soltar con "
                    "gratitud, y abre mis manos para lo que sigue.",
                ),
            },
            {
                "key": "change-3",
                "ref": "Deuteronomy 31:6-8",
                "title": L("God goes ahead of you", "Dios va delante de ti"),
                "truth": L(
                    "Israel is about to enter an unknown land, and Moses, the only leader they have "
                    "known, is not going with them. So he tells the people, and then Joshua in front of "
                    "them all, the one thing they most need to hear: be strong and brave, because the "
                    "Lord himself goes before you. He will be with you. He will not leave you or abandon "
                    "you. The new place is new to you, not to God. He is already there. Courage here is "
                    "not a personality trait. It comes from knowing who is ahead of you and beside you.",
                    "Israel está por entrar a una tierra desconocida, y Moisés, el único líder que han "
                    "tenido, no irá con ellos. Así que le dice al pueblo, y luego a Josué delante de "
                    "todos, lo que más necesitan oír: sean fuertes y valientes, porque el Señor mismo va "
                    "delante de ustedes. Él estará con ustedes. No los dejará ni los abandonará. El lugar "
                    "nuevo es nuevo para ti, no para Dios. Él ya está allí. Aquí la valentía no es un "
                    "rasgo de carácter. Nace de saber quién va delante de ti y a tu lado.",
                ),
                "simple": L(
                    "God goes ahead of you to every new place, and he stays right with you. You are never "
                    "alone there.",
                    "Dios va delante de ti a cada lugar nuevo, y se queda contigo. Allí nunca estás solo.",
                ),
                "ask": L(
                    "What part of what lies ahead feels most unknown? How does it change things to "
                    "picture God already there?",
                    "¿Qué parte de lo que viene sientes más desconocida? ¿Qué cambia si imaginas que Dios "
                    "ya está allí?",
                ),
                "kid_ask": L(
                    "What new place or new thing makes you feel a little nervous?",
                    "¿Qué lugar nuevo o qué cosa nueva te pone un poco nervioso?",
                ),
                "do": L(
                    "Before you walk into the new thing this week (the office, the classroom, the empty "
                    "house), stop at the door and say: you are already here.",
                    "Esta semana, antes de entrar a lo nuevo (la oficina, el aula, la casa vacía), "
                    "detente en la puerta y di: tú ya estás aquí.",
                ),
                "kid_do": L(
                    'Before you go somewhere new, whisper, "God, you are with me."',
                    'Antes de ir a un lugar nuevo, di bajito: "Dios, tú estás conmigo".',
                ),
                "pray": L(
                    "Lord, you go before me and you will not leave me. I am walking into … Be there ahead "
                    "of me, and make me brave.",
                    "Señor, tú vas delante de mí y no me vas a dejar. Estoy entrando a … Espérame allí, "
                    "y dame valor.",
                ),
            },
            {
                "key": "change-4",
                "ref": "Lamentations 3:21-24",
                "title": L("Starting over", "Empezar de nuevo"),
                "truth": L(
                    "These lines were written in the ruins of Jerusalem, by someone who had lost nearly "
                    "everything. In the middle of his grief he deliberately calls something to mind: the "
                    "Lord's faithful love has not run out. His mercies are new every morning. This is not "
                    "cheerfulness. It is a choice about where to look when starting again feels "
                    "impossible. You are not asked to find strength today for the whole rebuilt life. You "
                    "are given mercy for this morning, and tomorrow there will be more.",
                    "Estas líneas se escribieron entre las ruinas de Jerusalén, por alguien que lo había "
                    "perdido casi todo. En medio de su dolor, trae algo a la memoria a propósito: el amor "
                    "fiel del Señor no se ha acabado. Sus misericordias son nuevas cada mañana. Esto no es "
                    "optimismo. Es decidir hacia dónde mirar cuando volver a empezar parece imposible. No "
                    "se te pide encontrar hoy las fuerzas para toda la vida reconstruida. Se te da "
                    "misericordia para esta mañana, y mañana habrá más.",
                ),
                "simple": L(
                    "Every morning God gives us a fresh start and new love. Even after a bad day, "
                    "tomorrow is new.",
                    "Cada mañana Dios nos da un comienzo fresco y un amor nuevo. Aun después de un mal "
                    "día, mañana es un día nuevo.",
                ),
                "ask": L(
                    "Where are you having to start over, and what is one mercy, however small, that was "
                    "new for you today?",
                    "¿En qué te está tocando empezar de nuevo, y cuál es una misericordia, por pequeña "
                    "que sea, que fue nueva para ti hoy?",
                ),
                "kid_ask": L(
                    "What is good about a brand new day?",
                    "¿Qué tiene de bueno un día completamente nuevo?",
                ),
                "do": L(
                    "Each morning this week, before anything else, write down one mercy from the day "
                    "before. If starting over feels too heavy to face alone, tell a friend or a pastor.",
                    "Cada mañana de esta semana, antes que nada, anota una misericordia del día anterior. "
                    "Si empezar de nuevo te pesa demasiado para enfrentarlo a solas, cuéntaselo a un "
                    "amigo o a un pastor.",
                ),
                "kid_do": L(
                    'When you wake up tomorrow, say, "Thank you, God, for a new day."',
                    'Mañana, cuando despiertes, di: "Gracias, Dios, por un día nuevo".',
                ),
                "pray": L(
                    "Lord, I did not want to start again, and here I am. Your mercy is new this morning. "
                    "Give me enough for today.",
                    "Señor, yo no quería volver a empezar, y aquí estoy. Tu misericordia es nueva esta "
                    "mañana. Dame la suficiente para hoy.",
                ),
            },
            {
                "key": "change-5",
                "ref": "Psalm 102:25-27",
                "title": L("The one who does not change", "El que no cambia"),
                "truth": L(
                    "The writer of this psalm is frail and feels his days slipping away. He looks at the "
                    "most permanent things he knows, the earth and the sky, and says even these will wear "
                    "out like old clothes and be changed. Then he says to God: but you remain the same, "
                    "and your years never end. Everything in your life can shift: your address, your "
                    "work, your body, the people around your table. God's character does not. He is the "
                    "fixed point from which you can face everything that moves.",
                    "Quien escribe este salmo está débil y siente que los días se le escapan. Mira las "
                    "cosas más permanentes que conoce, la tierra y el cielo, y dice que hasta ellas se "
                    "gastarán como ropa vieja y serán cambiadas. Entonces le dice a Dios: pero tú sigues "
                    "siendo el mismo, y tus años no se acaban. Todo en tu vida puede moverse: tu "
                    "dirección, tu trabajo, tu cuerpo, las personas alrededor de tu mesa. El carácter de "
                    "Dios no. Él es el punto fijo desde el cual puedes enfrentar todo lo que se mueve.",
                ),
                "simple": L(
                    "Lots of things change, but God never changes. He always loves you the same.",
                    "Muchas cosas cambian, pero Dios nunca cambia. Siempre te ama igual.",
                ),
                "ask": L(
                    "What has stayed true about God through every change you have lived through so far?",
                    "¿Qué ha seguido siendo verdad acerca de Dios en cada cambio que has vivido hasta "
                    "ahora?",
                ),
                "kid_ask": L(
                    "What is something about God that is always the same?",
                    "¿Qué es algo de Dios que siempre es igual?",
                ),
                "do": L(
                    "Write down three things that have changed in your life this year, and beneath them "
                    "three things about God that have not. Read the second list aloud.",
                    "Escribe tres cosas que cambiaron en tu vida este año, y debajo tres cosas de Dios "
                    "que no han cambiado. Lee la segunda lista en voz alta.",
                ),
                "kid_do": L(
                    "Name three things in your life that stay the same. God's love is one of them.",
                    "Nombra tres cosas de tu vida que siguen igual. El amor de Dios es una de ellas.",
                ),
                "pray": L(
                    "God, everything around me is moving, and you are the same. Be my fixed point today.",
                    "Dios, todo a mi alrededor se mueve, y tú eres el mismo. Sé hoy mi punto fijo.",
                ),
            },
        ],
    },
    {
        "key": "eternity",
        "category": "seasons",
        "title": L(
            "Death and the hope of resurrection",
            "La muerte y la esperanza de la resurrección",
        ),
        "summary": L(
            "For anyone facing death: your own, or that of someone you love. Five gentle readings, honest "
            "about fear and grief, that hold to the hope Christians share: Jesus is risen, and death "
            "does not have the last word.",
            "Para quien está frente a la muerte: la propia o la de alguien amado. Cinco lecturas suaves, "
            "honestas sobre el miedo y el duelo, que se aferran a la esperanza que comparten los "
            "cristianos: Jesús resucitó, y la muerte no tiene la última palabra.",
        ),
        "keywords": [
            "death",
            "dying",
            "died",
            "funeral",
            "heaven",
            "afterlife",
            "terminal",
            "passed away",
            "eternal",
            "muerte",
            "morir",
            "murió",
            "falleci",
            "cielo",
            "eternidad",
            "vida eterna",
            "resurrec",
        ],
        "situations": ["grieving", "ill", "widowed", "caregiver"],
        "traits": ["hope", "trust", "peace"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "When someone dies we feel very sad, and we have questions. Jesus understands, and he "
                "gives us hope.",
                "Cuando alguien muere nos sentimos muy tristes y tenemos preguntas. Jesús lo entiende, y "
                "nos da esperanza.",
            ),
            "teen": L(
                "Maybe someone you love has died, or the thought of death keeps you awake. You can bring "
                "the fear and the questions here.",
                "Quizá murió alguien que quieres, o pensar en la muerte no te deja dormir. Aquí puedes "
                "traer el miedo y las preguntas.",
            ),
            "young_adult": L(
                "Death can feel far away until it is not. Honest readings for a first real loss, and for "
                "the questions it raises.",
                "La muerte puede parecer lejana hasta que deja de serlo. Lecturas honestas para una "
                "primera pérdida real, y para las preguntas que despierta.",
            ),
            "adult": L(
                "Burying parents, friends, sometimes a child; facing your own diagnosis. Hope that does "
                "not ask you to pretend.",
                "Despedir a los padres, a amigos, a veces a un hijo; enfrentar tu propio diagnóstico. Una "
                "esperanza que no te pide fingir.",
            ),
            "senior": L(
                "There are more goodbyes now, and your own is in view. These readings are about who meets "
                "you there.",
                "Ahora hay más despedidas, y la tuya ya se alcanza a ver. Estas lecturas tratan de quién "
                "te recibe allí.",
            ),
        },
        "sensitive": True,
        "lessons": [
            {
                "key": "eternity-1",
                "ref": "John 11:32-36",
                "title": L("Jesus cried at a grave", "Jesús lloró ante una tumba"),
                "truth": L(
                    "Lazarus has died, and his sister Mary falls at Jesus' feet, saying that if he had "
                    "been there her brother would not have died. Jesus does not correct her. Seeing her "
                    "weep, he is deeply moved, and he weeps too. He does this knowing he is about to raise "
                    "Lazarus, so his tears are not hopelessness. They show that death is an enemy, that "
                    "grief is right, and that God is not distant from it. If you are afraid of death, or "
                    "broken by someone's, you have not failed at faith. You are standing where Jesus "
                    "stood.",
                    "Lázaro ha muerto, y su hermana María cae a los pies de Jesús y le dice que si él "
                    "hubiera estado allí, su hermano no habría muerto. Jesús no la corrige. Al verla "
                    "llorar, se conmueve profundamente, y él también llora. Lo hace sabiendo que está por "
                    "resucitar a Lázaro, así que sus lágrimas no son desesperanza. Muestran que la muerte "
                    "es un enemigo, que el duelo es justo y que Dios no está lejos de él. Si le tienes "
                    "miedo a la muerte, o la muerte de alguien te ha quebrado, no has fallado en la fe. "
                    "Estás donde estuvo Jesús.",
                ),
                "simple": L(
                    "When Jesus' friend died, Jesus cried. It is okay to cry when someone dies. Jesus "
                    "understands how sad it feels.",
                    "Cuando murió su amigo, Jesús lloró. Está bien llorar cuando alguien muere. Jesús "
                    "entiende lo triste que se siente.",
                ),
                "ask": L(
                    "What have you felt about death, or about one particular death, that you thought you "
                    "were not allowed to say to God?",
                    "¿Qué has sentido sobre la muerte, o sobre una muerte en particular, que creías que "
                    "no tenías permiso de decirle a Dios?",
                ),
                "kid_ask": L(
                    "What helps you when you feel very sad?",
                    "¿Qué te ayuda cuando te sientes muy triste?",
                ),
                "do": L(
                    "Say to God today what Mary said: your own honest sentence that begins, if you had "
                    "been here. Then tell one trusted person how you are really doing with this loss or "
                    "this fear.",
                    "Dile hoy a Dios lo que dijo María: tu propia frase honesta que empieza con si "
                    "hubieras estado aquí. Luego cuéntale a una persona de confianza cómo estás de verdad "
                    "con esta pérdida o este miedo.",
                ),
                "kid_do": L(
                    "If you feel sad about someone who died, tell a grown-up, and let them give you "
                    "a hug.",
                    "Si te sientes triste por alguien que murió, cuéntaselo a un adulto y deja que te dé "
                    "un abrazo.",
                ),
                "pray": L(
                    "Jesus, you wept at a grave, so you know. Here is what I am carrying: … Stay near me "
                    "in it.",
                    "Jesús, tú lloraste ante una tumba, así que lo sabes. Esto es lo que estoy cargando: … "
                    "Quédate cerca de mí en esto.",
                ),
            },
            {
                "key": "eternity-2",
                "ref": "1 Corinthians 15:20-26",
                "title": L(
                    "Death is not the end of the story",
                    "La muerte no es el final de la historia",
                ),
                "truth": L(
                    "Christian hope rests on an event: God raised Jesus from the dead. Paul calls him the "
                    "firstfruits, the first sheaf of a harvest, which is the sign that the rest is "
                    "coming. Because he was raised, those who belong to him will be raised too. Paul "
                    "names death for what it is, an enemy, and says it is the last enemy that will be "
                    "destroyed. The Bible gives few details about how, and it is wise not to add any. "
                    "What it gives is a person: the risen Christ, who went through death and came out the "
                    "other side.",
                    "La esperanza cristiana descansa en un hecho: Dios resucitó a Jesús de entre los "
                    "muertos. Pablo lo llama las primicias, el primer manojo de una cosecha, que es la "
                    "señal de que viene el resto. Porque él resucitó, los que son suyos también "
                    "resucitarán. Pablo llama a la muerte por lo que es, un enemigo, y dice que es el "
                    "último enemigo que será destruido. La Biblia da pocos detalles sobre el cómo, y es "
                    "sabio no añadir ninguno. Lo que da es una persona: Cristo resucitado, que atravesó "
                    "la muerte y salió del otro lado.",
                ),
                "simple": L(
                    "Jesus died and came back to life. Because of Jesus, death is not the end. One day "
                    "God will make everything new.",
                    "Jesús murió y volvió a vivir. Gracias a Jesús, la muerte no es el final. Un día Dios "
                    "hará nuevas todas las cosas.",
                ),
                "ask": L(
                    "Right now, does the resurrection of Jesus feel to you more like a teaching, a hope "
                    "or a question? Say why.",
                    "En este momento, ¿la resurrección de Jesús es para ti más una enseñanza, una "
                    "esperanza o una pregunta? Di por qué.",
                ),
                "kid_ask": L(
                    "What do you know about what happened at Easter?",
                    "¿Qué sabes de lo que pasó en la Pascua?",
                ),
                "do": L(
                    "Read today's passage aloud once, slowly. Write down the single phrase you most need, "
                    "and carry it with you this week.",
                    "Lee el pasaje de hoy en voz alta una vez, despacio. Anota la frase que más "
                    "necesitas, y llévala contigo esta semana.",
                ),
                "kid_do": L(
                    'Draw the empty tomb on Easter morning, and say, "Jesus is alive."',
                    'Dibuja la tumba vacía en la mañana de Pascua, y di: "Jesús está vivo".',
                ),
                "pray": L(
                    "Risen Lord, you went into death and came out again. I want to trust that. Where I "
                    "cannot, help me. Keep me in that hope today.",
                    "Señor resucitado, tú entraste en la muerte y saliste de ella. Quiero confiar en eso. "
                    "Donde no puedo, ayúdame. Mantenme hoy en esa esperanza.",
                ),
            },
            {
                "key": "eternity-3",
                "ref": "John 14:1-3",
                "title": L("A place prepared", "Un lugar preparado"),
                "truth": L(
                    "On the night before his own death, Jesus speaks to friends whose hearts are "
                    "troubled. He does not explain what dying is like, or describe in detail what lies "
                    "beyond. He gives a promise in the plainest terms: there is room in his Father's "
                    "house, he is going to prepare a place, and he will come himself and take them to be "
                    "with him. The center of the promise is not a location. It is company: being where "
                    "he is. If you are facing your own death, the one who waits on the other side is "
                    "someone who already loves you.",
                    "La noche antes de su propia muerte, Jesús les habla a unos amigos con el corazón "
                    "angustiado. No les explica cómo es morir, ni describe en detalle lo que hay más "
                    "allá. Les da una promesa en los términos más sencillos: en la casa de su Padre hay "
                    "lugar, él va a preparar un sitio, y vendrá él mismo a llevarlos para que estén con "
                    "él. El centro de la promesa no es un lugar. Es la compañía: estar donde él está. Si "
                    "estás frente a tu propia muerte, quien espera del otro lado es alguien que ya te ama.",
                ),
                "simple": L(
                    "Jesus told his friends that he is getting a place ready for them, so they can be "
                    "with him always.",
                    "Jesús les dijo a sus amigos que les está preparando un lugar, para que estén con él "
                    "para siempre.",
                ),
                "ask": L(
                    "When you think about your own death, what are you most afraid of: pain, leaving "
                    "people, the unknown, being alone? Which of these does Jesus' promise touch?",
                    "Cuando piensas en tu propia muerte, ¿qué es lo que más temes: el dolor, dejar a los "
                    "tuyos, lo desconocido, la soledad? ¿Cuál de estos temores toca la promesa de Jesús?",
                ),
                "kid_ask": L(
                    "What makes a place feel like home to you?",
                    "¿Qué hace que un lugar se sienta como tu hogar?",
                ),
                "do": L(
                    "Tell one person you trust what you fear most about dying, and ask them to pray with "
                    "you. If you are seriously ill, also tell your doctor or a chaplain what frightens "
                    "you; they can help with more of it than you might expect.",
                    "Cuéntale a una persona de confianza qué es lo que más temes de morir, y pídele que "
                    "ore contigo. Si tienes una enfermedad grave, dile también a tu médico o a un "
                    "capellán lo que te asusta; pueden ayudarte con más de lo que imaginas.",
                ),
                "kid_do": L(
                    "Ask a grown-up any question you have about heaven. It is okay if they do not know "
                    "every answer.",
                    "Hazle a un adulto cualquier pregunta que tengas sobre el cielo. Está bien si no sabe "
                    "todas las respuestas.",
                ),
                "pray": L(
                    "Jesus, my heart is troubled. You said there is room, and that you will come for me "
                    "yourself. Let that be enough for today.",
                    "Jesús, mi corazón está angustiado. Tú dijiste que hay lugar, y que vendrás tú mismo "
                    "por mí. Que eso me baste por hoy.",
                ),
            },
            {
                "key": "eternity-4",
                "ref": "1 Thessalonians 4:13-14",
                "title": L("Grief with hope in it", "Un duelo con esperanza"),
                "truth": L(
                    "Paul writes to believers whose friends have died, and he chooses his words with "
                    "care. He does not say do not grieve. He says they need not grieve the way people do "
                    "who have no hope. Christian grief is still grief, with its tears and its empty "
                    "chair. But there is hope inside it, because Jesus died and rose, and God will bring "
                    "with him those who have died trusting him. You do not have to choose between "
                    "mourning and believing. You may do both, for as long as it takes.",
                    "Pablo les escribe a creyentes cuyos amigos han muerto, y elige sus palabras con "
                    "cuidado. No dice que no lloren. Dice que no tienen que llorar como quienes no tienen "
                    "esperanza. El duelo cristiano sigue siendo duelo, con sus lágrimas y su silla vacía. "
                    "Pero lleva una esperanza por dentro, porque Jesús murió y resucitó, y Dios traerá "
                    "con él a quienes murieron confiando en él. No tienes que elegir entre llorar y "
                    "creer. Puedes hacer las dos cosas, todo el tiempo que haga falta.",
                ),
                "simple": L(
                    "When someone we love dies, we are sad and we miss them. We also have hope, because "
                    "Jesus is alive and takes care of those who belong to him.",
                    "Cuando muere alguien que amamos, nos ponemos tristes y lo extrañamos. También "
                    "tenemos esperanza, porque Jesús está vivo y cuida a los que son suyos.",
                ),
                "ask": L(
                    "Whom are you missing? Where do you feel pressure, from others or from yourself, to "
                    "be finished grieving?",
                    "¿A quién extrañas? ¿Dónde sientes presión, de otros o de ti, para dar por terminado "
                    "tu duelo?",
                ),
                "kid_ask": L(
                    "Is there someone you miss? What do you remember about them?",
                    "¿Hay alguien a quien extrañas? ¿Qué recuerdas de esa persona?",
                ),
                "do": L(
                    "Do one thing this week to remember the person: tell a story about them, visit a "
                    "place, write a letter you will not send. If grief is making it hard to eat, sleep "
                    "or want to go on living, tell a doctor, counselor or pastor now. Do not carry that "
                    "alone.",
                    "Haz esta semana algo para recordar a esa persona: cuenta una historia suya, visita "
                    "un lugar, escribe una carta que no vas a enviar. Si el duelo te está quitando el "
                    "hambre, el sueño o las ganas de seguir viviendo, díselo ya a un médico, consejero o "
                    "pastor. No cargues eso a solas.",
                ),
                "kid_do": L(
                    "Draw a picture or tell a story about someone you miss, and share it with a grown-up.",
                    "Haz un dibujo o cuenta una historia de alguien a quien extrañas, y compártelo con "
                    "un adulto.",
                ),
                "pray": L(
                    "Father, I miss … so much. Thank you for their life. I place them in your hands, and "
                    "myself too, until the day you make all things right.",
                    "Padre, extraño muchísimo a … Gracias por su vida. Pongo su vida en tus manos, y la mía "
                    "también, hasta el día en que lo hagas todo nuevo.",
                ),
            },
            {
                "key": "eternity-5",
                "ref": "Revelation 21:1-5",
                "title": L("Every tear", "Cada lágrima"),
                "truth": L(
                    "The Bible's last pages do not picture people escaping the world. They picture God "
                    "coming to live with his people in a creation made new. John hears a voice from the "
                    "throne: God himself will be with them and will wipe every tear from their eyes. "
                    "There will be no more death, no more mourning or crying or pain. Much about this is "
                    "beyond us, and Scripture does not ask us to fill in the blanks. It asks us to trust "
                    "the one who says he is making everything new, and whose words can be relied on.",
                    "Las últimas páginas de la Biblia no muestran a la gente escapando del mundo. "
                    "Muestran a Dios viniendo a vivir con su pueblo en una creación hecha nueva. Juan oye "
                    "una voz desde el trono: Dios mismo estará con ellos y secará toda lágrima de sus "
                    "ojos. Ya no habrá muerte, ni duelo, ni llanto, ni dolor. Mucho de esto nos "
                    "sobrepasa, y la Escritura no nos pide llenar los espacios en blanco. Nos pide confiar "
                    "en aquel que dice que está haciendo nuevas todas las cosas, y cuyas palabras son "
                    "dignas de confianza.",
                ),
                "simple": L(
                    "One day God will make everything new. He will wipe away every tear, and no one will "
                    "be sad or hurt anymore.",
                    "Un día Dios hará nuevas todas las cosas. Secará cada lágrima, y nadie volverá a "
                    "estar triste ni a sentir dolor.",
                ),
                "ask": L(
                    "Of the things God promises to end (death, mourning, crying, pain), which do you most "
                    "long to see gone, and why that one?",
                    "De las cosas que Dios promete terminar (la muerte, el duelo, el llanto, el dolor), "
                    "¿cuál es la que más anhelas ver desaparecer, y por qué esa?",
                ),
                "kid_ask": L(
                    "What do you think it will be like when nobody is sad anymore?",
                    "¿Cómo crees que será cuando ya nadie esté triste?",
                ),
                "do": L(
                    "Write the name of your grief or fear on a card. On the back, write in your own "
                    "words what God promises in this passage. Keep it by your bed this week.",
                    "Escribe en una tarjeta el nombre de tu duelo o de tu miedo. Al reverso, escribe con "
                    "tus propias palabras lo que Dios promete en este pasaje. Tenla junto a tu cama esta "
                    "semana.",
                ),
                "kid_do": L(
                    "Draw a picture of a world where everyone is happy and safe with God.",
                    "Haz un dibujo de un mundo donde todos están felices y seguros con Dios.",
                ),
                "pray": L(
                    "God, you have promised to wipe away every tear. I am counting on it. Until that day, "
                    "be with me in this one.",
                    "Dios, tú prometiste secar toda lágrima. Cuento con eso. Hasta ese día, quédate "
                    "conmigo en este.",
                ),
            },
        ],
    },
]
