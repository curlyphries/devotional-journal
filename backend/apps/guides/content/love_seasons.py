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
            "love god", "worship", "devot", "close to god", "far from god", "obey", "lukewarm",
            "amar a dios", "ador", "devoc", "cerca de dios", "lejos de dios", "obedec", "tibi",
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
                    "\"I love you too.\"",
                    "Dios te amó antes de que tú lo amaras. Cuando amamos a Dios, le estamos respondiendo: "
                    "\"Yo también te amo\".",
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
            "neighbor", "kind", "difficult person", "annoy", "enemy", "selfish", "compassion",
            "prójimo", "vecin", "amab", "bondad", "enemig", "egoís", "compasi", "me cae mal",
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
                "El que se sienta sin compañía, quien se burla de ti, el hermano que te saca de quicio: ahí "
                "es donde el amor se pone a prueba.",
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
                    "mañana, como al vestirse. Y él parte de lo que ya eres: alguien escogido y muy amado por "
                    "Dios. No practicas la bondad para llegar a ser amado. La practicas porque ya lo eres, y "
                    "el amor es lo que mantiene unido todo lo demás.",
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
                "title": L("Love for the difficult person", "Amor para la persona difícil"),
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
                    "dinero, haz la visita, ofrece el aventón.",
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
            "forgiv", "grudge", "resent", "bitter", "betray", "guilt", "apolog", "hurt me",
            "perdon", "rencor", "resenti", "amarg", "traici", "culpa", "disculp", "me lastim",
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
                "Para heridas que ya tienen años: un matrimonio, un padre, una iglesia, tú mismo. Con "
                "honestidad sobre lo que esto puede tardar.",
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
                    "¿Qué estás cansado de esconder, de Dios o de alguien a quien le fallaste?",
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
                "title": L("Forgiven people forgive", "Quien ha sido perdonado, perdona"),
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
                    "¿Hay alguien con quien sigues molesto?",
                ),
                "do": L(
                    "On paper, finish this sentence about one person: what they owe me is … Then pray, as a "
                    "decision and not a feeling: God, I hand this debt to you.",
                    "En un papel, completa esta frase sobre una persona: lo que me debe es … Luego ora, como "
                    "decisión y no como sentimiento: Dios, te entrego esta deuda.",
                ),
                "kid_do": L(
                    "Think of someone who said sorry to you. Tell them, \"I forgive you.\"",
                    "Piensa en alguien que te pidió perdón. Dile: \"Te perdono\".",
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
            "marriage", "husband", "wife", "spouse", "wedding", "anniversar", "married",
            "matrimonio", "espos", "marido", "casad", "pareja", "boda", "aniversario",
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
                "title": L("How you speak when you are angry", "Cómo hablas cuando hay enojo"),
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
                    "\"I\" rather than \"you always,\" and say it before the day ends.",
                    "La próxima vez que no estén de acuerdo, di una cosa verdadera sobre lo que sientes, "
                    "empezando con \"yo\" y no con \"tú siempre\", y dila antes de que termine el día.",
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
                "title": L("Hard seasons, and help from outside", "Épocas difíciles y ayuda de afuera"),
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
            "parent", "my son", "my daughter", "my kids", "my child", "toddler", "teenager", "prodigal",
            "mi hijo", "mi hija", "mis hijos", "crianza", "criar", "adolescente", "pródig", "berrinche",
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
                "title": L("A gift, and not yours alone to build", "Un regalo, y no lo construyes a solas"),
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
                    "lo que no tienes, y no necesitas ser perfecto. Necesitas ser auténtico.",
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
                    "Jesús, tú recibiste a los niños. Hoy te traigo a … Tómalo en tus brazos y bendícelo, "
                    "y no permitas que yo sea un estorbo.",
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
                    "Padre, tú sabes lo que es quedarse mirando el camino. … es tuyo aún más que mío. Ve "
                    "adonde yo no puedo ir. Mantén tierno mi corazón y abierta mi puerta.",
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
            "family", "my parents", "my mom", "my dad", "brother", "sister", "sibling", "relatives", "in-law",
            "familia", "mis padres", "mi mamá", "mi papá", "herman", "parientes", "suegr", "abuel",
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
                "title": L("Honor goes both ways", "La honra va en las dos direcciones"),
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
                "title": L("Caring for those who cared for you", "Cuidar a quienes te cuidaron"),
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
                "title": L("When family has let you down", "Cuando la familia te ha fallado"),
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
    # --- next topic ---
]
