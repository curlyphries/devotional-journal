from apps.guides.catalog import L

TOPICS = [
    # ======================================================================
    # FOUNDATIONS
    # ======================================================================
    {
        "key": "who_god_is",
        "category": "foundations",
        "title": L("Who God is", "Quién es Dios"),
        "summary": L(
            "For anyone asking what God is actually like. Five short readings on the God the Bible "
            "describes: the maker of everything, holy, faithful, full of compassion, and closer than "
            "you think.",
            "Para quien se pregunta cómo es Dios en realidad. Cinco lecturas breves sobre el Dios que "
            "describe la Biblia: creador de todo, santo, fiel, lleno de compasión y más cercano de lo "
            "que imaginas.",
        ),
        "keywords": [
            "creator",
            "holy",
            "faithful",
            "compassion",
            "exist",
            "wonder",
            "awe",
            "almighty",
            "creador",
            "santo",
            "fiel",
            "compasi",
            "existe",
            "asombr",
            "cercan",
            "todopoderoso",
        ],
        "situations": ["exploring", "new_believer", "returning"],
        "traits": ["trust", "humility", "gratitude"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "God made everything, and God is good and kind. Here are five things to know about God.",
                "Dios hizo todo, y es bueno y cariñoso. Aquí hay cinco cosas para conocer de Dios.",
            ),
            "teen": L(
                "Before deciding what you think about God, it helps to know what the Bible actually says "
                "God is like.",
                "Antes de decidir qué piensas de Dios, ayuda saber cómo dice la Biblia que es en realidad.",
            ),
            "young_adult": L(
                "You may be sorting out what you were taught from what you believe. Start with the "
                "character of God himself.",
                "Quizá estás separando lo que te enseñaron de lo que tú crees. Empieza por el carácter de "
                "Dios mismo.",
            ),
            "adult": L(
                "In a full life God can shrink to an idea. These readings bring back the size and the "
                "kindness of who he is.",
                "En una vida llena, Dios puede reducirse a una idea. Estas lecturas devuelven la grandeza "
                "y la bondad de quien él es.",
            ),
            "senior": L(
                "After many years, the oldest truths are still worth sitting with: the God who has been "
                "faithful this far has not changed.",
                "Después de muchos años, vale la pena detenerse en las verdades más antiguas: el Dios que "
                "ha sido fiel hasta aquí no ha cambiado.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "who_god_is-1",
                "ref": "Genesis 1:1-5",
                "title": L("The God who made everything", "El Dios que lo hizo todo"),
                "truth": L(
                    "The Bible opens without arguing that God exists. It simply starts with him: before "
                    "anything else was there, God was, and everything else came from him. He speaks into "
                    "darkness and emptiness, and there is light, and he sees that it is good. That means the "
                    "world is not an accident, and neither are you. You live in a place someone wanted to "
                    "exist.",
                    "La Biblia comienza sin discutir si Dios existe. Simplemente parte de él: antes de que "
                    "hubiera cualquier otra cosa, Dios ya estaba, y todo lo demás vino de él. Habla sobre la "
                    "oscuridad y el vacío, y hay luz, y ve que es buena. Eso significa que el mundo no es un "
                    "accidente, y tú tampoco. Vives en un lugar que alguien quiso que existiera.",
                ),
                "simple": L(
                    "God made everything: the light, the day, the night, and you. God looked at what he made "
                    "and saw that it was good.",
                    "Dios hizo todo: la luz, el día, la noche y a ti. Dios miró lo que hizo y vio que era "
                    "bueno.",
                ),
                "ask": L(
                    "If the world was made on purpose by someone good, what would change about how you look "
                    "at an ordinary day?",
                    "Si el mundo fue hecho a propósito por alguien bueno, ¿qué cambiaría en tu manera de "
                    "mirar un día cualquiera?",
                ),
                "kid_ask": L(
                    "What is your favorite thing that God made?",
                    "¿Qué es lo que más te gusta de todo lo que Dios hizo?",
                ),
                "do": L(
                    "Step outside for five minutes today without your phone. Notice three things you did not "
                    "make and could not make, and thank God for each one, even if you are not sure anyone is "
                    "listening.",
                    "Hoy sal cinco minutos sin el teléfono. Fíjate en tres cosas que tú no hiciste ni podrías "
                    "hacer, y da gracias a Dios por cada una, aunque no tengas claro que alguien escuche.",
                ),
                "kid_do": L(
                    "Draw one thing God made that you love, and say: Thank you, God, for making this.",
                    "Dibuja algo que Dios hizo y que te encanta, y di: Gracias, Dios, por hacer esto.",
                ),
                "pray": L(
                    "God, you were here before anything. Thank you for light, for this day, for my own life. "
                    "Help me see your world as something you made on purpose.",
                    "Dios, tú estabas antes que todo. Gracias por la luz, por este día, por mi propia vida. "
                    "Ayúdame a ver tu mundo como algo que hiciste a propósito.",
                ),
            },
            {
                "key": "who_god_is-2",
                "ref": "Isaiah 6:1-8",
                "title": L("The God who is holy", "El Dios que es santo"),
                "truth": L(
                    "Isaiah sees God on a throne, and the word the heavenly beings keep calling out is holy: "
                    "completely good, completely pure, unlike anyone else. Isaiah's first reaction is to feel "
                    "how unclean he is beside that goodness. But God does not send him away. He takes away "
                    "Isaiah's guilt and then invites him into his work. God's holiness is not coldness. It is "
                    "a goodness so real that it changes whoever comes near.",
                    "Isaías ve a Dios en un trono, y la palabra que los seres celestiales repiten es santo: "
                    "del todo bueno, del todo puro, distinto a cualquier otro. Lo primero que siente Isaías "
                    "es lo impuro que es junto a tanta bondad. Pero Dios no lo echa. Le quita la culpa y luego "
                    "lo invita a participar en su obra. La santidad de Dios no es frialdad. Es una bondad tan "
                    "real que cambia a quien se acerca.",
                ),
                "simple": L(
                    "God is holy. That means God is all good, with nothing bad in him at all. And this good "
                    "God wants us close to him.",
                    "Dios es santo. Eso quiere decir que es completamente bueno, sin nada malo. Y este Dios "
                    "tan bueno quiere tenernos cerca.",
                ),
                "ask": L(
                    "When you think of God as perfectly good, do you feel drawn toward him or do you want to "
                    "keep your distance? Why?",
                    "Cuando piensas que Dios es perfectamente bueno, ¿te dan ganas de acercarte o de mantener "
                    "distancia? ¿Por qué?",
                ),
                "kid_ask": L(
                    "What do you think it means that God is always good?",
                    "¿Qué crees que significa que Dios siempre es bueno?",
                ),
                "do": L(
                    "Take two quiet minutes today. Tell God one thing in you that you would rather hide, and "
                    "then stay there a moment longer instead of rushing off.",
                    "Hoy toma dos minutos en silencio. Dile a Dios una cosa de ti que preferirías esconder, y "
                    "quédate ahí un momento más en vez de salir corriendo.",
                ),
                "kid_do": L(
                    "Say this out loud with a grown-up: God, you are good all the time.",
                    "Di en voz alta con un adulto: Dios, tú eres bueno todo el tiempo.",
                ),
                "pray": L(
                    "Holy God, you are better than I can picture. I do not come to you with clean hands. Take "
                    "away what is wrong in me, and let me be near you anyway.",
                    "Dios santo, eres mejor de lo que puedo imaginar. No llego a ti con las manos limpias. "
                    "Quita lo que está mal en mí y déjame estar cerca de ti de todos modos.",
                ),
            },
            {
                "key": "who_god_is-3",
                "ref": "Lamentations 3:21-26",
                "title": L("The God who stays faithful", "El Dios que permanece fiel"),
                "truth": L(
                    "These lines were written in the ruins of a city, by someone who had lost nearly "
                    "everything. In the middle of that grief the writer deliberately calls one thing to mind: "
                    "God's faithful love has not run out, and his mercy arrives fresh with each morning. "
                    "Faithful means God does not change with your circumstances or with your mood. He stays "
                    "who he is, and that is why it is good to wait for him.",
                    "Estas líneas se escribieron entre las ruinas de una ciudad, por alguien que lo había "
                    "perdido casi todo. En medio de ese dolor, quien escribe trae a la memoria una cosa a "
                    "propósito: el amor fiel de Dios no se ha agotado, y su misericordia llega fresca con "
                    "cada mañana. Fiel quiere decir que Dios no cambia según tus circunstancias ni según tu "
                    "ánimo. Sigue siendo quien es, y por eso vale la pena esperar en él.",
                ),
                "simple": L(
                    "God never stops loving us. Every single morning his love is there again, like the sun "
                    "coming up.",
                    "Dios nunca deja de amarnos. Cada mañana su amor está ahí otra vez, como el sol que "
                    "vuelve a salir.",
                ),
                "ask": L(
                    "What is one thing you could call to mind, on a bad morning, that reminds you God has not "
                    "let go of you?",
                    "¿Qué podrías traer a la memoria, en una mala mañana, que te recuerde que Dios no te ha "
                    "soltado?",
                ),
                "kid_ask": L(
                    "What is something that happens every single morning, no matter what?",
                    "¿Qué cosa pasa todas las mañanas, sin falta?",
                ),
                "do": L(
                    "For the next three mornings, before you look at your phone, say one sentence: Your mercy "
                    "is here again today. Then name one thing you need mercy for.",
                    "Durante las próximas tres mañanas, antes de mirar el teléfono, di una frase: Tu "
                    "misericordia está aquí otra vez hoy. Luego nombra una cosa para la que necesitas "
                    "misericordia.",
                ),
                "kid_do": L(
                    "Tomorrow when you wake up, say: Good morning, God. Thank you for loving me today.",
                    "Mañana al despertar di: Buenos días, Dios. Gracias por amarme hoy.",
                ),
                "pray": L(
                    "Lord, a lot has changed and some of it hurts. You have not changed. Give me today's "
                    "mercy for today, and help me wait for you.",
                    "Señor, muchas cosas han cambiado y algunas duelen. Tú no has cambiado. Dame la "
                    "misericordia de hoy para hoy, y ayúdame a esperar en ti.",
                ),
            },
            {
                "key": "who_god_is-4",
                "ref": "Psalm 103:8-14",
                "title": L("The God who is compassionate", "El Dios compasivo"),
                "truth": L(
                    "This psalm describes God's character: slow to get angry and overflowing with love. He does "
                    "not treat us as our wrongs deserve, and he puts those wrongs as far from us as the east "
                    "is from the west. Then comes a picture, a father who is tender with his children, and a "
                    "reason: God remembers what we are made of. He knows how fragile you are, and knowing it "
                    "makes him gentle, not impatient.",
                    "Este salmo describe el carácter de Dios: lento para enojarse y desbordante de amor. No "
                    "nos trata como merecen nuestras faltas, y las aleja de nosotros tanto como el oriente "
                    "está del occidente. Luego viene una imagen, la de un padre tierno con sus hijos, y una "
                    "razón: Dios recuerda de qué estamos hechos. Sabe lo frágil que eres, y saberlo lo vuelve "
                    "tierno, no impaciente.",
                ),
                "simple": L(
                    "God is kind and slow to get angry. He knows we are small and that we make mistakes, and "
                    "he is gentle with us.",
                    "Dios es bueno y tarda mucho en enojarse. Sabe que somos pequeños y que nos equivocamos, "
                    "y nos trata con ternura.",
                ),
                "ask": L(
                    "Do you tend to picture God as easily annoyed with you? How does this psalm's description "
                    "differ from that picture?",
                    "¿Sueles imaginar a Dios fácilmente molesto contigo? ¿En qué se diferencia de esa imagen "
                    "la descripción de este salmo?",
                ),
                "kid_ask": L(
                    "How does it feel when someone is gentle with you after you make a mistake?",
                    "¿Cómo te sientes cuando alguien te trata con cariño después de que te equivocas?",
                ),
                "do": L(
                    "Think of one failure you keep replaying. Write it on paper, then write beside it: God "
                    "knows how fragile I am. Throw the paper away.",
                    "Piensa en un error que no dejas de repasar. Escríbelo en un papel y al lado escribe: "
                    "Dios sabe lo frágil que soy. Luego tira el papel.",
                ),
                "kid_do": L(
                    "Be gentle with someone today when they make a mistake, the way God is gentle with you.",
                    "Hoy trata con cariño a alguien que se equivoque, como Dios te trata a ti.",
                ),
                "pray": L(
                    "Father, you know me through and through, and my weakness does not surprise you. Thank "
                    "you for not treating me as I deserve. Teach me to believe you are this kind.",
                    "Padre, tú me conoces por dentro y mi debilidad no te sorprende. Gracias por no tratarme "
                    "como merezco. Enséñame a creer que eres así de bueno.",
                ),
            },
            {
                "key": "who_god_is-5",
                "ref": "Acts 17:24-28",
                "title": L("The God who is near", "El Dios que está cerca"),
                "truth": L(
                    "Paul is speaking in Athens to people who were curious about God but unsure who he was. "
                    "He tells them that the God who made the world does not live in buildings and does not "
                    "need anything from us; he is the one who gives everyone life and breath. And he made "
                    "people so that they would look for him and find him, because he is not far from any of "
                    "us. You do not have to climb up to God. He is already closer than you thought.",
                    "Pablo habla en Atenas a personas con curiosidad por Dios pero sin saber bien quién era. "
                    "Les dice que el Dios que hizo el mundo no vive en edificios ni necesita nada de nosotros; "
                    "es él quien da a todos la vida y el aliento. Y nos hizo para que lo busquemos y lo "
                    "encontremos, porque no está lejos de ninguno de nosotros. No tienes que escalar hasta "
                    "Dios. Ya está más cerca de lo que pensabas.",
                ),
                "simple": L(
                    "God is not far away. He is close to you wherever you are: at home, at school, and in bed "
                    "at night.",
                    "Dios no está lejos. Está cerca de ti donde sea que estés: en casa, en la escuela y en tu "
                    "cama por la noche.",
                ),
                "ask": L(
                    "Where in your life right now would it matter most to know that God is not far away?",
                    "¿En qué parte de tu vida importaría más ahora mismo saber que Dios no está lejos?",
                ),
                "kid_ask": L(
                    "Where is a place you would like to remember that God is with you?",
                    "¿En qué lugar te gustaría acordarte de que Dios está contigo?",
                ),
                "do": L(
                    "Three times today, at ordinary moments, stop for one breath and say silently: You are "
                    "here. Notice what it does to that moment.",
                    "Tres veces hoy, en momentos comunes, detente lo que dura una respiración y di en "
                    "silencio: Estás aquí. Observa qué cambia en ese momento.",
                ),
                "kid_do": L(
                    "At bedtime tonight, whisper: God, you are here with me. Good night.",
                    "Esta noche antes de dormir, susurra: Dios, estás aquí conmigo. Buenas noches.",
                ),
                "pray": L(
                    "God, I have sometimes thought of you as far off. You gave me this breath. Help me reach "
                    "for you and find that you were near all along.",
                    "Dios, a veces te he imaginado lejos. Tú me diste este aliento. Ayúdame a buscarte y a "
                    "descubrir que estuviste cerca todo el tiempo.",
                ),
            },
        ],
    },
    {
        "key": "jesus",
        "category": "foundations",
        "title": L("Who Jesus is", "Quién es Jesús"),
        "summary": L(
            "For anyone who wants to know what Christians actually believe about Jesus. Five readings "
            "on who he is, how he lived, why he died, and what it means that he rose again.",
            "Para quien quiere saber qué creen de verdad los cristianos acerca de Jesús. Cinco lecturas "
            "sobre quién es, cómo vivió, por qué murió y qué significa que haya resucitado.",
        ),
        "keywords": [
            "jesus",
            "christ",
            "gospel",
            "cross",
            "resurrect",
            "savior",
            "easter",
            "messiah",
            "jesús",
            "cristo",
            "evangelio",
            "cruz",
            "resurrec",
            "resucit",
            "salvador",
            "mesías",
        ],
        "situations": ["exploring", "new_believer", "returning"],
        "traits": ["trust", "love", "hope"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Jesus loves you. These lessons tell who he is and the best news there is: he is alive.",
                "Jesús te ama. Estas lecciones cuentan quién es y la mejor noticia que existe: está vivo.",
            ),
            "teen": L(
                "Not the Jesus of memes or arguments. Read what the people who knew him wrote down, and "
                "decide for yourself.",
                "No el Jesús de los memes ni de las discusiones. Lee lo que escribieron quienes lo "
                "conocieron, y saca tus propias conclusiones.",
            ),
            "young_adult": L(
                "Whatever you end up doing with your life, the question of who Jesus is deserves a direct "
                "look.",
                "Hagas lo que hagas con tu vida, la pregunta de quién es Jesús merece que la mires de "
                "frente.",
            ),
            "adult": L(
                "You may have heard this story so often that it stopped landing. Read it slowly, as if for "
                "the first time.",
                "Quizá has oído esta historia tantas veces que dejó de tocarte. Léela despacio, como si "
                "fuera la primera vez.",
            ),
            "senior": L(
                "The center of the faith does not wear out. The one who died and rose is the same one who "
                "walks with you now.",
                "El centro de la fe no se gasta. El que murió y resucitó es el mismo que hoy camina "
                "contigo.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "jesus-1",
                "ref": "John 1:9-14",
                "title": L("God came close", "Dios se acercó"),
                "truth": L(
                    "John calls Jesus the Word and the true light, the one through whom the world was made. "
                    "Then he says something no one expected: this Word became a human being and lived among "
                    "us. Christians believe that Jesus is not only a teacher sent by God but God himself come "
                    "near, in a life people could see and touch. Many did not recognize him. Yet to everyone "
                    "who received him, he gave the right to become a child of God.",
                    "Juan llama a Jesús la Palabra y la luz verdadera, aquel por medio de quien fue hecho el "
                    "mundo. Luego dice algo que nadie esperaba: esa Palabra se hizo ser humano y vivió entre "
                    "nosotros. Los cristianos creen que Jesús no es solo un maestro enviado por Dios, sino "
                    "Dios mismo que se acercó, en una vida que la gente podía ver y tocar. Muchos no lo "
                    "reconocieron. Pero a todos los que lo recibieron les dio el derecho de llegar a ser "
                    "hijos de Dios.",
                ),
                "simple": L(
                    "God loves us so much that he came to live with us as a person. His name is Jesus.",
                    "Dios nos ama tanto que vino a vivir con nosotros como una persona. Su nombre es Jesús.",
                ),
                "ask": L(
                    "What difference does it make to you whether God stayed at a distance or actually came to "
                    "live a human life?",
                    "¿Qué diferencia hace para ti que Dios se haya quedado a distancia o que de verdad haya "
                    "venido a vivir una vida humana?",
                ),
                "kid_ask": L(
                    "If Jesus came to visit your house today, what would you want to show him?",
                    "Si Jesús viniera hoy a tu casa, ¿qué te gustaría mostrarle?",
                ),
                "do": L(
                    "Read these verses out loud once, slowly. Then finish this sentence in your own words: If "
                    "this is true, then God is…",
                    "Lee estos versículos en voz alta una vez, despacio. Luego completa esta frase con tus "
                    "palabras: Si esto es verdad, entonces Dios es…",
                ),
                "kid_do": L(
                    "Draw a picture of Jesus with children around him, and put yourself in the picture.",
                    "Dibuja a Jesús rodeado de niños, y dibújate a ti también.",
                ),
                "pray": L(
                    "Jesus, I want to know who you really are. If you are God come near, help me recognize "
                    "you and receive you.",
                    "Jesús, quiero saber quién eres de verdad. Si eres Dios que se acercó, ayúdame a "
                    "reconocerte y a recibirte.",
                ),
            },
            {
                "key": "jesus-2",
                "ref": "Luke 19:1-10",
                "title": L("He came looking for people", "Vino a buscar a la gente"),
                "truth": L(
                    "Zacchaeus was a wealthy tax collector, the kind of man his neighbors considered a cheat. "
                    "He climbs a tree just to catch sight of Jesus, and Jesus stops, calls him by name, and "
                    "invites himself to his house. The crowd grumbles, but that welcome changes Zacchaeus: he "
                    "gives to the poor and promises to pay back anyone he has cheated. Jesus then explains "
                    "his whole life in one line: he came to look for the lost and to save them.",
                    "Zaqueo era un cobrador de impuestos rico, de esos a quienes sus vecinos consideraban "
                    "tramposos. Se sube a un árbol solo para ver pasar a Jesús, y Jesús se detiene, lo llama "
                    "por su nombre y se invita a su casa. La gente murmura, pero esa bienvenida cambia a "
                    "Zaqueo: da a los pobres y promete devolver lo que haya cobrado de más. Entonces Jesús "
                    "explica toda su vida en una frase: vino a buscar a los perdidos y a salvarlos.",
                ),
                "simple": L(
                    "Nobody liked Zacchaeus, but Jesus knew his name and wanted to be his friend. Jesus looks "
                    "for people who feel left out.",
                    "A Zaqueo nadie lo quería, pero Jesús sabía su nombre y quiso ser su amigo. Jesús busca a "
                    "los que se sienten dejados de lado.",
                ),
                "ask": L(
                    "Jesus went to Zacchaeus before Zacchaeus had changed anything. What would it mean for "
                    "you to be sought out like that, as you are now?",
                    "Jesús fue a Zaqueo antes de que Zaqueo cambiara nada. ¿Qué significaría para ti que te "
                    "busquen así, tal como estás ahora?",
                ),
                "kid_ask": L(
                    "How do you think Zacchaeus felt when Jesus said his name?",
                    "¿Cómo crees que se sintió Zaqueo cuando Jesús dijo su nombre?",
                ),
                "do": L(
                    "Think of someone others tend to avoid. This week, greet that person by name and give "
                    "them five unhurried minutes.",
                    "Piensa en alguien a quien los demás suelen evitar. Esta semana saluda a esa persona por "
                    "su nombre y regálale cinco minutos sin prisa.",
                ),
                "kid_do": L(
                    "Find someone who is alone at school or at the park and ask them to play with you.",
                    "Busca a alguien que esté solo en la escuela o en el parque e invítalo a jugar contigo.",
                ),
                "pray": L(
                    "Jesus, you know my name and you know what I have done. Come to my house anyway. Change "
                    "in me whatever needs to change.",
                    "Jesús, sabes mi nombre y sabes lo que he hecho. Ven a mi casa de todos modos. Cambia en "
                    "mí lo que haga falta cambiar.",
                ),
            },
            {
                "key": "jesus-3",
                "ref": "Luke 23:32-43",
                "title": L("Why he died", "Por qué murió"),
                "truth": L(
                    "Jesus was executed on a cross between two criminals, though he had done nothing wrong. "
                    "While it is happening he asks his Father to forgive the people doing it. One of the men "
                    "dying beside him admits his own guilt and simply asks Jesus to remember him, and Jesus "
                    "promises that he will be with him in paradise that very day. Christians believe that on "
                    "the cross Jesus took on himself the wrong of the world, so that anyone, even at the last "
                    "hour, can be forgiven and welcomed home.",
                    "A Jesús lo ejecutaron en una cruz, entre dos criminales, aunque no había hecho nada malo. "
                    "Mientras sucede, le pide a su Padre que perdone a quienes lo hacen. Uno de los hombres "
                    "que muere a su lado reconoce su propia culpa y solo le pide a Jesús que se acuerde de él, "
                    "y Jesús le promete que ese mismo día estará con él en el paraíso. Los cristianos creen "
                    "que en la cruz Jesús cargó con el mal del mundo, para que cualquiera, aun a última hora, "
                    "pueda recibir perdón y ser bienvenido en casa.",
                ),
                "simple": L(
                    "Jesus died on a cross because he loves us. Even while he was hurting, he forgave people. "
                    "Because of Jesus, God forgives us too.",
                    "Jesús murió en una cruz porque nos ama. Aun cuando le dolía, perdonó a la gente. Gracias "
                    "a Jesús, Dios también nos perdona a nosotros.",
                ),
                "ask": L(
                    "The man beside Jesus had nothing to offer and no time to make things right. What does "
                    "Jesus' answer to him tell you about how forgiveness works?",
                    "El hombre junto a Jesús no tenía nada que ofrecer ni tiempo para arreglar las cosas. "
                    "¿Qué te dice la respuesta de Jesús sobre cómo funciona el perdón?",
                ),
                "kid_ask": L(
                    "Jesus forgave people who were unkind to him. Is there someone you find hard to forgive?",
                    "Jesús perdonó a quienes lo trataron mal. ¿Hay alguien a quien te cuesta perdonar?",
                ),
                "do": L(
                    "Find a quiet place and make that man's request your own: ask Jesus, in your own words, "
                    "not to forget you. Add nothing to make yourself look better.",
                    "Busca un lugar tranquilo y haz tuya la petición de aquel hombre: pídele a Jesús, con tus "
                    "palabras, que no se olvide de ti. No agregues nada para quedar mejor.",
                ),
                "kid_do": L(
                    "Say thank you to Jesus in one sentence for loving you so much.",
                    "Dile gracias a Jesús en una frase por amarte tanto.",
                ),
                "pray": L(
                    "Jesus, you did nothing wrong and you died forgiving. I have nothing to bargain with. Do "
                    "not forget me, and forgive me.",
                    "Jesús, no hiciste nada malo y moriste perdonando. No tengo nada con qué negociar. No te "
                    "olvides de mí, y perdóname.",
                ),
            },
            {
                "key": "jesus-4",
                "ref": "Luke 24:1-12",
                "title": L("He is alive", "Está vivo"),
                "truth": L(
                    "Early on the Sunday after Jesus died, some women went to his tomb with burial spices and "
                    "found the stone rolled away and the body gone. Two messengers told them he was not there "
                    "because he had risen, just as he had said he would. When the women told the others, it "
                    "sounded like nonsense to them at first. The resurrection is the center of Christian "
                    "faith: death did not get the last word over Jesus, and so it does not get the last word "
                    "over those who belong to him.",
                    "Muy temprano, el domingo después de la muerte de Jesús, unas mujeres fueron a su tumba "
                    "con especias y encontraron la piedra removida y la tumba sin el cuerpo. Dos mensajeros "
                    "les dijeron que no estaba allí porque había resucitado, tal como él lo había anunciado. "
                    "Cuando ellas lo contaron a los demás, al principio les pareció una locura. La "
                    "resurrección es el centro de la fe cristiana: la muerte no tuvo la última palabra sobre "
                    "Jesús, y por eso tampoco la tiene sobre quienes son de él.",
                ),
                "simple": L(
                    "Jesus did not stay dead. On the third day he was alive again! That is the happiest news "
                    "in the whole Bible.",
                    "Jesús no se quedó muerto. ¡Al tercer día volvió a vivir! Es la noticia más feliz de toda "
                    "la Biblia.",
                ),
                "ask": L(
                    "The first people to hear this news found it hard to believe. What makes it hard, or what "
                    "makes it good news, for you?",
                    "A los primeros que oyeron esta noticia les costó creerla. ¿Qué la hace difícil, o qué la "
                    "hace buena noticia, para ti?",
                ),
                "kid_ask": L(
                    "How do you think the women felt when they found out Jesus was alive?",
                    "¿Cómo crees que se sintieron las mujeres al saber que Jesús estaba vivo?",
                ),
                "do": L(
                    "Name one place in your life that feels like a closed tomb, finished and sealed. Write it "
                    "down, and write beside it: Not the last word.",
                    "Nombra un lugar de tu vida que parezca una tumba cerrada, terminada y sellada. "
                    "Escríbelo, y al lado escribe: No es la última palabra.",
                ),
                "kid_do": L(
                    "Tell someone in your family today: Jesus is alive!",
                    "Hoy dile a alguien de tu familia: ¡Jesús está vivo!",
                ),
                "pray": L(
                    "Risen Jesus, some of this is hard for me to take in. Meet me in my wondering, as you met "
                    "your first friends, and let your life reach the dead places in mine.",
                    "Jesús resucitado, hay cosas de esto que me cuesta asimilar. Sal a mi encuentro en mi "
                    "desconcierto, como saliste al encuentro de tus primeros amigos, y que tu vida alcance "
                    "los lugares muertos de la mía.",
                ),
            },
            {
                "key": "jesus-5",
                "ref": "Matthew 16:13-17",
                "title": L("Who do you say he is?", "¿Y tú quién dices que es?"),
                "truth": L(
                    "Jesus asks his friends what people are saying about him, and the answers are respectful: "
                    "a prophet, a great man returned. Then he makes it personal and asks what they themselves "
                    "say. Peter answers that Jesus is the Messiah, the rescuer and king God had promised, the "
                    "Son of the living God. Jesus calls him blessed and says this is something God showed "
                    "him. Sooner or later everyone who meets Jesus is asked the same question, and no one "
                    "else can answer it for you.",
                    "Jesús pregunta a sus amigos qué dice la gente de él, y las respuestas son respetuosas: "
                    "un profeta, un gran hombre que volvió. Luego lo hace personal y les pregunta qué dicen "
                    "ellos. Pedro responde que Jesús es el Mesías, el rey y salvador que Dios había "
                    "prometido, el Hijo del Dios viviente. Jesús lo llama dichoso y dice que eso se lo mostró "
                    "Dios. Tarde o temprano, todo el que se encuentra con Jesús recibe la misma pregunta, y "
                    "nadie puede contestarla por ti.",
                ),
                "simple": L(
                    "Jesus asked his friends who they thought he was. Peter said that Jesus is God's own Son. "
                    "Jesus was glad that Peter knew.",
                    "Jesús les preguntó a sus amigos quién pensaban que era él. Pedro dijo que Jesús es el "
                    "Hijo de Dios. Jesús se alegró de que Pedro lo supiera.",
                ),
                "ask": L(
                    "Leaving aside what your family, your church or your friends say: who do you say Jesus is "
                    "today? Give an honest answer, even if it is unfinished.",
                    "Dejando de lado lo que dicen tu familia, tu iglesia o tus amigos: ¿quién dices tú que es "
                    "Jesús hoy? Da una respuesta honesta, aunque esté incompleta.",
                ),
                "kid_ask": L(
                    "If a friend asked you who Jesus is, what would you say?",
                    "Si un amigo te preguntara quién es Jesús, ¿qué le dirías?",
                ),
                "do": L(
                    "Write two or three sentences beginning: Today, I would say Jesus is… Date it and keep it "
                    "where you can find it again in a month.",
                    "Escribe dos o tres frases que empiecen así: Hoy yo diría que Jesús es… Ponle fecha y "
                    "guárdalo donde puedas volver a encontrarlo en un mes.",
                ),
                "kid_do": L(
                    "Finish this sentence out loud with a grown-up: Jesus is…",
                    "Completa esta frase en voz alta con un adulto: Jesús es…",
                ),
                "pray": L(
                    "Jesus, you ask me who I say you are. Here is my honest answer today: … Show me more of "
                    "who you are.",
                    "Jesús, me preguntas quién digo yo que eres. Esta es mi respuesta honesta hoy: … "
                    "Muéstrame más de quién eres.",
                ),
            },
        ],
    },
    {
        "key": "grace",
        "category": "foundations",
        "title": L("Grace and forgiveness", "Gracia y perdón"),
        "summary": L(
            "For anyone who feels they must earn God's love, or who has failed and wonders if they can "
            "come back. Four readings on forgiveness as a gift and on trusting Christ rather than your "
            "own record.",
            "Para quien siente que debe ganarse el amor de Dios, o ha fallado y se pregunta si puede "
            "volver. Cuatro lecturas sobre el perdón como regalo y sobre confiar en Cristo y no en tu "
            "propio historial.",
        ),
        "keywords": [
            "grace",
            "forgiv",
            "guilt",
            "shame",
            "earn",
            "deserv",
            "unworthy",
            "mercy",
            "regret",
            "gracia",
            "perdón",
            "perdon",
            "culpa",
            "vergüenza",
            "merec",
            "indign",
            "misericordia",
            "arrepent",
        ],
        "situations": ["new_believer", "exploring", "returning", "recovery"],
        "traits": ["forgiveness", "humility", "gratitude"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "You are graded and ranked all day. With God you start somewhere else: loved first, before "
                "you have proved anything.",
                "Te califican y te comparan todo el día. Con Dios empiezas en otro lugar: su amor llega "
                "primero, antes de que demuestres nada.",
            ),
            "young_adult": L(
                "For the pressure to become someone impressive, and for the mistakes you would rather no "
                "one knew about.",
                "Para la presión de llegar a ser alguien admirable, y para los errores que preferirías que "
                "nadie conociera.",
            ),
            "adult": L(
                "For those who have been strong and dependable for years and are tired of earning "
                "everything. Grace is not a wage.",
                "Para quienes llevan años siendo fuertes y responsables y se cansaron de ganárselo todo. "
                "La gracia no es un sueldo.",
            ),
            "senior": L(
                "For looking back at a long life with its regrets. What you could not fix, God is able to "
                "forgive.",
                "Para mirar atrás una vida larga con sus pesares. Lo que no pudiste arreglar, Dios puede "
                "perdonarlo.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "grace-1",
                "ref": "Ephesians 2:4-10",
                "title": L("A gift, not a wage", "Un regalo, no un sueldo"),
                "truth": L(
                    "Grace means a gift you did not earn. Paul says that God, because of his great love, "
                    "made us alive with Christ when we could do nothing for ourselves. Being rescued is not a "
                    "reward for good behavior, so nobody gets to boast. Good works still matter, but they "
                    "come afterward, as the life God made us for, not as the price of being accepted. You do "
                    "not work your way toward God's love. You start from it.",
                    "Gracia quiere decir un regalo que no te ganaste. Pablo dice que Dios, por su gran amor, "
                    "nos dio vida junto con Cristo cuando no podíamos hacer nada por nosotros mismos. Ser "
                    "rescatados no es un premio por portarse bien, así que nadie puede presumir. Las buenas "
                    "obras siguen importando, pero vienen después, como la vida para la que Dios nos hizo, no "
                    "como el precio de ser aceptados. No te abres camino a fuerza de trabajo hacia el amor de "
                    "Dios. Partes de él.",
                ),
                "simple": L(
                    "God's love is a present. You do not have to earn it by being good. You just say thank "
                    "you and receive it.",
                    "El amor de Dios es un regalo. No tienes que ganártelo portándote bien. Solo dices "
                    "gracias y lo recibes.",
                ),
                "ask": L(
                    "In what ways do you try to earn God's approval, or other people's? What would be "
                    "different if it were already given?",
                    "¿De qué maneras intentas ganarte la aprobación de Dios, o la de otros? ¿Qué sería "
                    "distinto si ya te la hubieran dado?",
                ),
                "kid_ask": L(
                    "What is the best present you ever got? Did you have to pay for it?",
                    "¿Cuál es el mejor regalo que has recibido? ¿Tuviste que pagarlo?",
                ),
                "do": L(
                    "The next time you do something good today, notice whether you are doing it to be "
                    "accepted or because you already are. Say quietly: This is a thank-you, not a payment.",
                    "La próxima vez que hagas algo bueno hoy, fíjate si lo haces para que te acepten o porque "
                    "ya te aceptaron. Di en voz baja: Esto es un gracias, no un pago.",
                ),
                "kid_do": L(
                    "Say: Thank you, God, for loving me for free.",
                    "Di: Gracias, Dios, por amarme sin que yo tenga que pagar nada.",
                ),
                "pray": L(
                    "God, I keep trying to deserve you. Thank you that your love came first. Help me receive "
                    "it as a gift and live out of thanks.",
                    "Dios, sigo tratando de merecerte. Gracias porque tu amor llegó primero. Ayúdame a "
                    "recibirlo como regalo y a vivir desde la gratitud.",
                ),
            },
            {
                "key": "grace-2",
                "ref": "Luke 18:9-14",
                "title": L("What it means to trust", "Qué significa confiar"),
                "truth": L(
                    "Jesus tells of two men praying. One is religious and lists his good record, thanking "
                    "God that he is better than other people. The other, a tax collector everyone looked "
                    "down on, cannot even lift his eyes; he only asks God for mercy. Jesus says it is the "
                    "second man who goes home right with God. Trusting Christ begins here: you stop "
                    "presenting your record, good or bad, and lean your whole weight on God's mercy instead.",
                    "Jesús cuenta de dos hombres que oran. Uno es religioso y enumera su buena conducta, "
                    "dando gracias por ser mejor que los demás. El otro, un cobrador de impuestos a quien "
                    "todos despreciaban, ni siquiera levanta la mirada; solo le pide a Dios misericordia. "
                    "Jesús dice que es el segundo quien vuelve a su casa en paz con Dios. Confiar en Cristo "
                    "empieza aquí: dejas de presentar tu historial, bueno o malo, y apoyas todo tu peso en la "
                    "misericordia de Dios.",
                ),
                "simple": L(
                    "One man told God how good he was. Another man just asked God to be kind to him. God was "
                    "pleased with the one who asked for help.",
                    "Un hombre le dijo a Dios lo bueno que era. Otro solo le pidió a Dios que tuviera "
                    "compasión de él. A Dios le agradó el que pidió ayuda.",
                ),
                "ask": L(
                    "Which are you more tempted to bring to God: a list of what you have done right, or a "
                    "list of why you are beyond help? What would it look like to bring neither?",
                    "¿Qué te tienta más llevarle a Dios: una lista de lo que has hecho bien, o una lista de "
                    "por qué no tienes remedio? ¿Cómo sería no llevar ninguna?",
                ),
                "kid_ask": L(
                    "Is it hard for you to ask for help? Why?",
                    "¿Te cuesta pedir ayuda? ¿Por qué?",
                ),
                "do": L(
                    "Pray once today with no explanations and no comparisons. One sentence asking for mercy, "
                    "and then be quiet for a minute.",
                    "Hoy ora una vez sin explicaciones ni comparaciones. Una sola frase pidiendo "
                    "misericordia, y luego guarda silencio un minuto.",
                ),
                "kid_do": L(
                    "Pray one short sentence: God, please help me.",
                    "Ora una frase corta: Dios, ayúdame, por favor.",
                ),
                "pray": L(
                    "God, I need your mercy. I am not better than anyone, and I am not beyond your reach. I "
                    "trust your kindness, not my record.",
                    "Dios, necesito tu misericordia. No soy mejor que nadie, ni estoy fuera de tu alcance. "
                    "Confío en tu bondad, no en mi historial.",
                ),
            },
            {
                "key": "grace-3",
                "ref": "Luke 15:17-24",
                "title": L("Coming home", "Volver a casa"),
                "truth": L(
                    "A son has taken his inheritance, wasted it, and ended up hungry and ashamed. He decides "
                    "to go home and rehearses a speech asking to be taken back as a hired hand. But his "
                    "father sees him from far off, runs to him, and embraces him before the speech is "
                    "finished. Then come the best robe, a ring and a feast. Jesus told this story to show "
                    "what God is like toward people who come back. He is not waiting to lecture you. He is "
                    "watching the road.",
                    "Un hijo ha tomado su herencia, la ha malgastado y ha terminado con hambre y vergüenza. "
                    "Decide volver a casa y ensaya un discurso para pedir que lo reciban como un empleado "
                    "más. Pero su padre lo ve desde lejos, corre hacia él y lo abraza antes de que termine "
                    "el discurso. Luego vienen la mejor ropa, un anillo y una fiesta. Jesús contó esta "
                    "historia para mostrar cómo es Dios con quienes regresan. No te espera para regañarte. "
                    "Está mirando el camino.",
                ),
                "simple": L(
                    "A boy left home and made bad choices. When he came back, his dad ran to hug him. God is "
                    "like that dad. He is always glad when we come back.",
                    "Un muchacho se fue de casa y tomó malas decisiones. Cuando volvió, su papá corrió a "
                    "abrazarlo. Dios es como ese papá. Siempre se alegra cuando volvemos.",
                ),
                "ask": L(
                    "What speech have you been rehearsing for God? What do you imagine his face looks like "
                    "while you give it?",
                    "¿Qué discurso has estado ensayando para Dios? ¿Cómo te imaginas su rostro mientras lo "
                    "dices?",
                ),
                "kid_ask": L(
                    "How do you think the boy felt when his dad hugged him?",
                    "¿Cómo crees que se sintió el muchacho cuando su papá lo abrazó?",
                ),
                "do": L(
                    "If something has kept you away from God, say it to him plainly today, in one or two "
                    "sentences. If it weighs on you, also tell a pastor or a trusted friend this week.",
                    "Si hay algo que te ha mantenido lejos de Dios, díselo hoy con claridad, en una o dos "
                    "frases. Si te pesa, cuéntaselo también esta semana a un pastor o a alguien de confianza.",
                ),
                "kid_do": L(
                    "If you did something wrong today, tell a grown-up and tell God you are sorry. Then ask "
                    "for a hug.",
                    "Si hoy hiciste algo malo, cuéntaselo a un adulto y dile a Dios que lo sientes. Luego "
                    "pide un abrazo.",
                ),
                "pray": L(
                    "Father, I have been far away. I am coming home with nothing to show for it. Thank you "
                    "for running to meet me.",
                    "Padre, he estado lejos. Vuelvo a casa con las manos vacías. Gracias por correr a mi "
                    "encuentro.",
                ),
            },
            {
                "key": "grace-4",
                "ref": "John 21:15-19",
                "title": L("After you have failed", "Después de haber fallado"),
                "truth": L(
                    "Peter had insisted he would never abandon Jesus, and then three times denied even "
                    "knowing him. After the resurrection, Jesus meets him by the lake and asks him three "
                    "times whether he loves him. It hurts, but it is not a punishment: each time Peter "
                    "answers, Jesus gives him work to do, caring for his people. Then he says again what he "
                    "said at the very start: follow me. Failure did not end Peter's story, and it does not "
                    "have to end yours.",
                    "Pedro había asegurado que nunca abandonaría a Jesús, y luego negó tres veces siquiera "
                    "conocerlo. Después de la resurrección, Jesús se encuentra con él junto al lago y le "
                    "pregunta tres veces si lo ama. Duele, pero no es un castigo: cada vez que Pedro "
                    "responde, Jesús le encarga una tarea, cuidar de los suyos. Luego le repite lo que le "
                    "dijo al principio de todo: sígueme. El fracaso no terminó la historia de Pedro, y no "
                    "tiene por qué terminar la tuya.",
                ),
                "simple": L(
                    "Peter let Jesus down. But Jesus came to find him, forgave him, and gave him an important "
                    "job. Jesus gives new starts.",
                    "Pedro le falló a Jesús. Pero Jesús fue a buscarlo, lo perdonó y le dio un trabajo "
                    "importante. Jesús da nuevos comienzos.",
                ),
                "ask": L(
                    "Is there a failure you have treated as the end of your usefulness to God? What might "
                    "Jesus be asking you, and giving you to do, now?",
                    "¿Hay algún fracaso que has tratado como el fin de tu utilidad para Dios? ¿Qué podría "
                    "estar preguntándote Jesús, y qué podría encargarte, ahora?",
                ),
                "kid_ask": L(
                    "Have you ever needed a new start after a mistake? What happened?",
                    "¿Alguna vez necesitaste empezar de nuevo después de un error? ¿Qué pasó?",
                ),
                "do": L(
                    "Answer Jesus' question honestly in writing: do you love him? Then choose one small act "
                    "of care for someone this week as your way of following again.",
                    "Responde por escrito y con honestidad la pregunta de Jesús: ¿lo amas? Luego elige un "
                    "pequeño acto de cuidado hacia alguien esta semana como tu manera de volver a seguirlo.",
                ),
                "kid_do": L(
                    "Do one kind thing to take care of someone today, like Jesus asked Peter to do.",
                    "Haz hoy algo amable para cuidar a alguien, como Jesús le pidió a Pedro.",
                ),
                "pray": L(
                    "Jesus, nothing about me is hidden from you, including how I have failed you. I do love "
                    "you, however weakly. Show me the next step of following you.",
                    "Jesús, nada de mí te es oculto, tampoco cómo te he fallado. Sí te amo, aunque sea con "
                    "poca fuerza. Muéstrame el siguiente paso para seguirte.",
                ),
            },
        ],
    },
    {
        "key": "prayer",
        "category": "foundations",
        "title": L("Learning to pray", "Aprender a orar"),
        "summary": L(
            "For anyone who wants to talk with God and is not sure how. Five readings on praying simply "
            "and honestly, the prayer Jesus taught, and what to do when words will not come.",
            "Para quien quiere hablar con Dios y no sabe bien cómo. Cinco lecturas sobre orar con "
            "sencillez y honestidad, la oración que Jesús enseñó y qué hacer cuando no salen las "
            "palabras.",
        ),
        "keywords": [
            "pray",
            "unanswered",
            "silence",
            "listen",
            "amen",
            "distract",
            "orar",
            "oraci",
            "orando",
            "rezar",
            "rezo",
            "silencio",
            "escuch",
            "padrenuestro",
        ],
        "situations": ["new_believer", "exploring", "returning"],
        "traits": ["prayerfulness", "honesty", "trust"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "You can talk to God about anything, anytime, with your own words. He loves to listen to "
                "you.",
                "Puedes hablar con Dios de cualquier cosa, a cualquier hora, con tus propias palabras. A "
                "él le encanta escucharte.",
            ),
            "teen": L(
                "Prayer is not a performance or a formula. It is saying what is true to someone who already "
                "knows and still wants to hear it.",
                "Orar no es una actuación ni una fórmula. Es decirle la verdad a alguien que ya la sabe y "
                "aun así quiere oírla.",
            ),
            "young_adult": L(
                "If prayer feels awkward, or like talking to the ceiling, start small and start honest. "
                "That is how everyone learns.",
                "Si orar te resulta incómodo, o como hablarle al techo, empieza con poco y con honestidad. "
                "Así aprende todo el mundo.",
            ),
            "adult": L(
                "For people with little time and a lot on their minds. A few true words count for more "
                "than many tired ones.",
                "Para quienes tienen poco tiempo y mucho en la cabeza. Unas pocas palabras sinceras valen "
                "más que muchas repetidas sin ganas.",
            ),
            "senior": L(
                "Whether you have prayed for decades or are starting late, there is still more of God to "
                "know in the quiet.",
                "Hayas orado por décadas o empieces tarde, todavía hay más de Dios por conocer en el "
                "silencio.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "prayer-1",
                "ref": "Matthew 6:5-8",
                "title": L("Simple and unseen", "Sencilla y en secreto"),
                "truth": L(
                    "Jesus begins his teaching on prayer by taking the pressure off. Prayer is not a show for "
                    "other people, and it is not a matter of piling up words so that God will pay attention. "
                    "He says to go somewhere private and speak to your Father, who sees what no one else sees "
                    "and knows what you need before you ask. You are not informing God or impressing him. You "
                    "are keeping company with someone who is already listening.",
                    "Jesús empieza su enseñanza sobre la oración quitando la presión. Orar no es un "
                    "espectáculo para los demás, ni se trata de amontonar palabras para que Dios preste "
                    "atención. Dice que busques un lugar privado y le hables a tu Padre, que ve lo que nadie "
                    "más ve y sabe lo que necesitas antes de que lo pidas. No estás informando a Dios ni "
                    "impresionándolo. Estás pasando tiempo con alguien que ya te está escuchando.",
                ),
                "simple": L(
                    "You do not need big words to pray. You can talk to God quietly in your room, and he "
                    "hears every word.",
                    "No necesitas palabras difíciles para orar. Puedes hablar con Dios bajito en tu cuarto, y "
                    "él oye cada palabra.",
                ),
                "ask": L(
                    "If God already knows what you need, what do you think prayer is for? What would you say "
                    "if you were not trying to get it right?",
                    "Si Dios ya sabe lo que necesitas, ¿para qué crees que sirve orar? ¿Qué dirías si no "
                    "estuvieras tratando de hacerlo bien?",
                ),
                "kid_ask": L(
                    "Where is a quiet place where you could talk to God?",
                    "¿Cuál es un lugar tranquilo donde podrías hablar con Dios?",
                ),
                "do": L(
                    "Choose a place and a time for tomorrow: three minutes, door closed, phone elsewhere. Say "
                    "what is on your mind in plain words, then stop.",
                    "Elige un lugar y una hora para mañana: tres minutos, puerta cerrada, el teléfono en otro "
                    "lado. Di lo que tienes en mente con palabras sencillas y luego termina.",
                ),
                "kid_do": L(
                    "Find your quiet place and tell God one thing about your day.",
                    "Ve a tu lugar tranquilo y cuéntale a Dios una cosa de tu día.",
                ),
                "pray": L(
                    "Father, no one else is listening, and I do not need to impress you. Here is what is "
                    "really on my mind today: …",
                    "Padre, nadie más está escuchando, y no necesito impresionarte. Esto es lo que de verdad "
                    "tengo en mente hoy: …",
                ),
            },
            {
                "key": "prayer-2",
                "ref": "Matthew 6:9-13",
                "title": L("The prayer Jesus taught", "La oración que Jesús enseñó"),
                "truth": L(
                    "When Jesus gives his friends words to pray, they are few, and they can be said in under "
                    "a minute. The prayer starts with God: who he is to us, the honor of his name, his "
                    "kingdom and what he wants. Only then does it turn to us: food for today, forgiveness "
                    "for our wrongs as we forgive others, and help when we are tested. It is both a prayer to "
                    "say and a pattern to follow. Start with God, then bring everything you need.",
                    "Cuando Jesús les da a sus amigos palabras para orar, son pocas, y se dicen en menos de "
                    "un minuto. La oración empieza con Dios: quién es para nosotros, la honra de su nombre, "
                    "su reino y lo que él quiere. Solo después se vuelve hacia nosotros: el alimento de hoy, "
                    "el perdón de nuestras faltas así como perdonamos a otros, y ayuda cuando somos puestos "
                    "a prueba. Es una oración para decir y también un modelo para seguir. Empieza por Dios y "
                    "luego trae todo lo que necesitas.",
                ),
                "simple": L(
                    "Jesus taught his friends a prayer. In it we call God our Father, ask for food for today, "
                    "and ask him to forgive us and keep us safe.",
                    "Jesús les enseñó una oración a sus amigos. En ella llamamos Padre a Dios, le pedimos la "
                    "comida de hoy, que nos perdone y que nos cuide.",
                ),
                "ask": L(
                    "Which line of this prayer do you most need today, and which one do you find hardest to "
                    "mean?",
                    "¿Qué frase de esta oración necesitas más hoy, y cuál te cuesta más decir de corazón?",
                ),
                "kid_ask": L(
                    "What is one thing you would like to ask God for today?",
                    "¿Qué es una cosa que te gustaría pedirle a Dios hoy?",
                ),
                "do": L(
                    "Pray this prayer slowly once a day this week, pausing after each line to add one "
                    "sentence of your own.",
                    "Ora esta oración despacio una vez al día esta semana, deteniéndote después de cada frase "
                    "para agregar una tuya.",
                ),
                "kid_do": L(
                    "Say the Lord's Prayer with a grown-up tonight, slowly, one line at a time.",
                    "Esta noche di el Padrenuestro con un adulto, despacio, frase por frase.",
                ),
                "pray": L(
                    "Father, I want what you want more than what I want, though not yet with my whole heart. "
                    "Give me what I need for this day, forgive me, and help me forgive.",
                    "Padre, quiero lo que tú quieres más que lo que quiero yo, aunque todavía no con todo el "
                    "corazón. Dame lo que necesito para este día, perdóname y ayúdame a perdonar.",
                ),
            },
            {
                "key": "prayer-3",
                "ref": "Psalm 13:1-6",
                "title": L(
                    "Praying when you are upset", "Orar con el corazón revuelto"
                ),
                "truth": L(
                    "This prayer begins by asking God, four times over, how long he is going to stay away. "
                    "David does not tidy up his feelings first; he tells God he feels forgotten and worn out "
                    "by sorrow. This complaint sits in the Bible's own prayer book, which means God wants "
                    "this kind of honesty. By the end David chooses to trust God's faithful love, though "
                    "nothing in the psalm says his situation has changed. You can bring God the truth and "
                    "trust him in the same breath.",
                    "Esta oración empieza preguntándole a Dios, cuatro veces seguidas, hasta cuándo va a "
                    "seguir lejos. David no ordena primero sus sentimientos; le dice a Dios que se siente "
                    "olvidado y agotado por la tristeza. Esta queja está en el libro de oraciones de la "
                    "Biblia misma, lo que significa que Dios quiere esa clase de honestidad. Al final David "
                    "decide confiar en el amor fiel de Dios, aunque nada en el salmo dice que su situación "
                    "haya cambiado. Puedes llevarle a Dios la verdad y confiar en él al mismo tiempo.",
                ),
                "simple": L(
                    "You can tell God when you are sad or mad. He is not upset by your feelings. He wants to "
                    "hear them.",
                    "Puedes decirle a Dios cuando sientes tristeza o enojo. A él no le molestan tus "
                    "sentimientos. Quiere escucharlos.",
                ),
                "ask": L(
                    "What have you been holding back from God because it did not seem like a proper thing to "
                    "pray?",
                    "¿Qué le has estado callando a Dios porque no te parecía algo apropiado para una oración?",
                ),
                "kid_ask": L(
                    "What is a feeling you have had this week that you could tell God about?",
                    "¿Qué sentimiento tuviste esta semana que podrías contarle a Dios?",
                ),
                "do": L(
                    "Write your own four-line prayer: two lines that begin How long, one request, and one "
                    "line that begins But I trust.",
                    "Escribe tu propia oración de cuatro líneas: dos que empiecen con Hasta cuándo, una "
                    "petición, y una que empiece con Pero confío.",
                ),
                "kid_do": L(
                    "Draw a face that shows how you feel today, and show it to God and to a grown-up.",
                    "Dibuja una carita que muestre cómo te sientes hoy, y muéstrasela a Dios y a un adulto.",
                ),
                "pray": L(
                    "Lord, honestly, this is how I feel: … I do not understand what you are doing. Still, I "
                    "choose to trust your love.",
                    "Señor, con honestidad, así me siento: … No entiendo lo que estás haciendo. Aun así, "
                    "elijo confiar en tu amor.",
                ),
            },
            {
                "key": "prayer-4",
                "ref": "Romans 8:26-27",
                "title": L("When you have no words", "Cuando no tienes palabras"),
                "truth": L(
                    "Paul admits something freeing: we do not know how to pray as we should. That is normal, "
                    "not a failure. He says God's own Spirit helps us in that weakness and prays for us from "
                    "the inside, with a longing deeper than words. And God, who searches hearts, understands "
                    "exactly what the Spirit means. So a sigh, tears, or sitting in silence before God can be "
                    "real prayer. You do not have to find the right words for God to hear you.",
                    "Pablo admite algo que libera: no sabemos orar como deberíamos. Eso es normal, no un "
                    "fracaso. Dice que el Espíritu de Dios nos ayuda en esa debilidad y ora por nosotros "
                    "desde adentro, con un anhelo más hondo que las palabras. Y Dios, que examina los "
                    "corazones, entiende exactamente lo que el Espíritu quiere decir. Así que un suspiro, "
                    "unas lágrimas o sentarte en silencio ante Dios pueden ser oración verdadera. No tienes "
                    "que hallar las palabras correctas para que Dios te oiga.",
                ),
                "simple": L(
                    "Sometimes you do not know what to say to God. That is okay. God understands what is in "
                    "your heart even without words.",
                    "A veces no sabes qué decirle a Dios. Está bien. Dios entiende lo que hay en tu corazón "
                    "aunque no uses palabras.",
                ),
                "ask": L(
                    "When have you had no words for God? How does it change things to think the Spirit was "
                    "praying for you then?",
                    "¿Cuándo te has quedado sin palabras ante Dios? ¿Qué cambia al pensar que el Espíritu "
                    "estaba orando por ti en ese momento?",
                ),
                "kid_ask": L(
                    "Has there been a time you did not know what to say? What did you do?",
                    "¿Alguna vez no supiste qué decir? ¿Qué hiciste?",
                ),
                "do": L(
                    "Sit for three minutes today with open hands and say nothing. When your mind wanders, "
                    "return with a single word: Help, or Thanks, or Here.",
                    "Hoy siéntate tres minutos con las manos abiertas y sin decir nada. Cuando tu mente se "
                    "distraiga, vuelve con una sola palabra: Ayuda, o Gracias, o Aquí.",
                ),
                "kid_do": L(
                    "Sit still for one minute, close your eyes, and just think: God, I am here.",
                    "Siéntate sin moverte un minuto, cierra los ojos y solo piensa: Dios, aquí estoy.",
                ),
                "pray": L(
                    "God, I do not know what to say. You know what is in me better than I do. Hear what I "
                    "cannot put into words.",
                    "Dios, no sé qué decir. Tú sabes lo que hay en mí mejor que yo. Escucha lo que no logro "
                    "poner en palabras.",
                ),
            },
            {
                "key": "prayer-5",
                "ref": "Mark 14:32-36",
                "title": L(
                    "Asking, and trusting the answer",
                    "Pedir, y confiar en la respuesta",
                ),
                "truth": L(
                    "On the night before he died, Jesus prayed in a place called Gethsemane, overwhelmed with "
                    "sorrow. He called God by the close family name Abba, said plainly what he wanted, that this "
                    "suffering would pass him by, and then placed himself in his Father's hands. The "
                    "suffering was not taken away. So when a request is not granted, it is not proof of weak "
                    "faith or of God's absence. Prayer is not a way of controlling God. It is telling him "
                    "everything and trusting him with the outcome.",
                    "La noche antes de morir, Jesús oró en un lugar llamado Getsemaní, abrumado por la "
                    "tristeza. Llamó a Dios con el nombre familiar y cercano de Abba, dijo con claridad lo que quería, que ese "
                    "sufrimiento pasara de largo, y luego se puso en manos de su Padre. El sufrimiento no le "
                    "fue quitado. Así que cuando una petición no se concede, no es prueba de poca fe ni de "
                    "que Dios esté ausente. Orar no es una forma de controlar a Dios. Es decirle todo y "
                    "confiarle el resultado.",
                ),
                "simple": L(
                    "Jesus told his Father exactly how he felt and what he wanted. Then he trusted his "
                    "Father's plan. We can pray like that too.",
                    "Jesús le dijo a su Padre exactamente cómo se sentía y lo que quería. Luego confió en el "
                    "plan de su Padre. Nosotros también podemos orar así.",
                ),
                "ask": L(
                    "What have you asked God for that has not been given? Can you tell him honestly how that "
                    "feels, and what trusting him with it would mean?",
                    "¿Qué le has pedido a Dios que no has recibido? ¿Puedes decirle con honestidad cómo te "
                    "hace sentir, y qué significaría confiárselo?",
                ),
                "kid_ask": L(
                    "Have you ever asked for something and the answer was no or not yet? How did that feel?",
                    "¿Alguna vez pediste algo y la respuesta fue no o todavía no? ¿Cómo te sentiste?",
                ),
                "do": L(
                    "Write down one request you care about deeply. Pray it in two parts: first exactly what "
                    "you want, then one sentence handing the outcome to God. If the burden is heavy, share it "
                    "with a trusted person too.",
                    "Escribe una petición que te importe mucho. Órala en dos partes: primero exactamente lo "
                    "que quieres, luego una frase entregándole a Dios el resultado. Si la carga es pesada, "
                    "compártela también con alguien de confianza.",
                ),
                "kid_do": L(
                    "Ask God for one thing you really want, then say: And I trust you, God.",
                    "Pídele a Dios una cosa que de verdad quieras y luego di: Y confío en ti, Dios.",
                ),
                "pray": L(
                    "Abba, Father, this is what I want: … Nothing is too hard for you. I put this, and "
                    "myself, in your hands.",
                    "Abba, Padre, esto es lo que quiero: … Nada es demasiado difícil para ti. Pongo esto, y "
                    "me pongo yo, en tus manos.",
                ),
            },
        ],
    },
    {
        "key": "scripture",
        "category": "foundations",
        "title": L("Reading the Bible", "Leer la Biblia"),
        "summary": L(
            "For anyone opening the Bible for the first time, or the first time in a long while. Four "
            "readings on why it matters, how to read it slowly, who it points to, and how to live what "
            "you read.",
            "Para quien abre la Biblia por primera vez, o por primera vez en mucho tiempo. Cuatro "
            "lecturas sobre por qué importa, cómo leerla despacio, a quién señala y cómo vivir lo que "
            "lees.",
        ),
        "keywords": [
            "bible",
            "scripture",
            "read",
            "verse",
            "devotion",
            "understand",
            "study",
            "biblia",
            "escritura",
            "leer",
            "lectura",
            "versículo",
            "devocional",
            "entender",
            "estudi",
        ],
        "situations": ["new_believer", "exploring", "returning", "student"],
        "traits": ["wisdom", "faithfulness"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "The Bible is God's big book of true stories, and it shows us how much he loves us.",
                "La Biblia es el gran libro de Dios, lleno de historias verdaderas, y nos muestra cuánto "
                "nos ama.",
            ),
            "teen": L(
                "It is a big, old, sometimes strange book. Here is how to start reading it for yourself "
                "instead of only hearing about it.",
                "Es un libro grande, antiguo y a veces extraño. Así puedes empezar a leerlo por tu cuenta "
                "en vez de solo oír hablar de él.",
            ),
            "young_adult": L(
                "With a thousand voices telling you how to live, here is how to listen to one that has "
                "outlasted them all.",
                "Con mil voces diciéndote cómo vivir, aquí aprendes a escuchar una que ha durado más que "
                "todas.",
            ),
            "adult": L(
                "A few verses read slowly will feed you more than a chapter skimmed out of guilt. Start "
                "small and keep going.",
                "Unos pocos versículos leídos con calma te alimentan más que un capítulo leído a la "
                "carrera por culpa. Empieza con poco y continúa.",
            ),
            "senior": L(
                "Old, familiar passages still have something new to say, and you have a lifetime of "
                "experience to read them with.",
                "Los pasajes viejos y conocidos todavía tienen algo nuevo que decir, y tú tienes toda una "
                "vida de experiencia para leerlos.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "scripture-1",
                "ref": "2 Timothy 3:14-17",
                "title": L("Why read it at all", "Para qué leerla"),
                "truth": L(
                    "Paul reminds Timothy that he has known the Scriptures since he was small, taught by "
                    "people he could trust. He gives two reasons they matter. First, they make a person wise "
                    "about being rescued through faith in Jesus. Second, they come from God and are useful: "
                    "they teach, they show us where we have gone wrong, they set us right, and they train us "
                    "to live well. The Bible is not mainly a rule book or a book of quick answers. It is how "
                    "God shapes people and equips them to do good.",
                    "Pablo le recuerda a Timoteo que conoce las Escrituras desde pequeño, enseñado por "
                    "personas en quienes podía confiar. Le da dos razones por las que importan. Primero, "
                    "hacen sabia a una persona para recibir la salvación por la fe en Jesús. Segundo, vienen "
                    "de Dios y son útiles: enseñan, nos muestran en qué nos hemos desviado, nos enderezan y "
                    "nos entrenan para vivir bien. La Biblia no es ante todo un reglamento ni un libro de "
                    "respuestas rápidas. Es la manera en que Dios forma a las personas y las prepara para "
                    "hacer el bien.",
                ),
                "simple": L(
                    "The Bible is God's book. It helps us know Jesus and teaches us how to live in a good "
                    "way.",
                    "La Biblia es el libro de Dios. Nos ayuda a conocer a Jesús y nos enseña a vivir bien.",
                ),
                "ask": L(
                    "What do you honestly expect when you open the Bible: rules, comfort, confusion, nothing? "
                    "Where did that expectation come from?",
                    "Con toda honestidad, ¿qué esperas cuando abres la Biblia: reglas, consuelo, confusión, "
                    "nada? ¿De dónde salió esa expectativa?",
                ),
                "kid_ask": L(
                    "Who has read you a Bible story? Which one do you remember best?",
                    "¿Quién te ha leído una historia de la Biblia? ¿Cuál recuerdas mejor?",
                ),
                "do": L(
                    "Pick one short book to read this month, a few verses a day. The Gospel of Mark is a good "
                    "place to begin. Put the Bible, or the app, where you will see it each morning.",
                    "Elige un libro corto para leer este mes, unos pocos versículos al día. El Evangelio de "
                    "Marcos es un buen lugar para comenzar. Pon la Biblia, o la aplicación, donde la veas "
                    "cada mañana.",
                ),
                "kid_do": L(
                    "Ask a grown-up to read you one Bible story tonight, and tell them your favorite part.",
                    "Pídele a un adulto que te lea una historia de la Biblia esta noche, y cuéntale cuál fue "
                    "tu parte favorita.",
                ),
                "pray": L(
                    "God, I want to hear from you and not only about you. As I read, teach me, correct me "
                    "where I need it, and make me ready to do good.",
                    "Dios, quiero oírte a ti, y no solo oír hablar de ti. Mientras leo, enséñame, corrígeme "
                    "donde lo necesite y prepárame para hacer el bien.",
                ),
            },
            {
                "key": "scripture-2",
                "ref": "Psalm 1:1-6",
                "title": L("Slow reading, deep roots", "Lectura lenta, raíces hondas"),
                "truth": L(
                    "The first psalm describes a person who delights in God's teaching and turns it over in "
                    "their mind day and night. That person is compared to a tree planted beside a stream: it "
                    "bears fruit when the season comes, and its leaves do not dry out. The picture is not one "
                    "of speed or quantity. A tree does not gulp water; it stays put and drinks slowly. "
                    "Reading a little, often, and chewing on it is how the Bible gets from the page into your "
                    "life.",
                    "El primer salmo describe a una persona que se deleita en la enseñanza de Dios y la "
                    "repasa en su mente de día y de noche. A esa persona la compara con un árbol plantado "
                    "junto a un arroyo: da fruto cuando llega el tiempo, y sus hojas no se secan. La imagen "
                    "no habla de velocidad ni de cantidad. Un árbol no traga el agua de golpe; se queda en "
                    "su sitio y bebe despacio. Leer un poco, con frecuencia, y darle vueltas: así es como "
                    "la Biblia pasa de la página a tu vida.",
                ),
                "simple": L(
                    "A tree by a river grows strong because it drinks water every day. When we listen to "
                    "God's words a little every day, we grow strong inside too.",
                    "Un árbol junto al río crece fuerte porque bebe agua todos los días. Cuando escuchamos "
                    "las palabras de Dios un poquito cada día, también crecemos fuertes por dentro.",
                ),
                "ask": L(
                    "What do you turn over in your mind most during a normal day? What would it take to give "
                    "one verse a place there?",
                    "¿A qué le das más vueltas en tu mente en un día normal? ¿Qué haría falta para darle a "
                    "un versículo un lugar ahí?",
                ),
                "kid_ask": L(
                    "What does a tree need to grow big and strong? What do you need to grow?",
                    "¿Qué necesita un árbol para crecer grande y fuerte? ¿Y tú qué necesitas para crecer?",
                ),
                "do": L(
                    "Choose one sentence from today's reading. Write it on a card or your lock screen, and "
                    "come back to it three times today: morning, midday and night.",
                    "Elige una frase de la lectura de hoy. Escríbela en una tarjeta o en la pantalla de tu "
                    "teléfono, y vuelve a ella tres veces hoy: mañana, mediodía y noche.",
                ),
                "kid_do": L(
                    "Draw a big tree next to a river. Ask a grown-up to help you write one Bible sentence "
                    "under it.",
                    "Dibuja un árbol grande junto a un río. Pídele a un adulto que te ayude a escribir "
                    "debajo una frase de la Biblia.",
                ),
                "pray": L(
                    "Lord, I rush through so much. Slow me down in your word. Plant me beside it, and let "
                    "something good grow in its season.",
                    "Señor, paso corriendo por tantas cosas. Hazme ir despacio en tu palabra. Plántame junto "
                    "a ella, y que algo bueno crezca a su tiempo.",
                ),
            },
            {
                "key": "scripture-3",
                "ref": "Luke 24:25-32",
                "title": L(
                    "The whole story points to Jesus", "Toda la historia señala a Jesús"
                ),
                "truth": L(
                    "Two discouraged followers are walking to a village outside Jerusalem after Jesus' death "
                    "when a stranger joins them. It is the risen Jesus, though they do not know it yet. Starting with the oldest "
                    "books of the Bible, he explains how all of it spoke about him. Later, when he breaks "
                    "bread at their table, they recognize him, and they remember how their hearts burned "
                    "while he opened the Scriptures. The Bible is many books, but it tells one story, and "
                    "Jesus is at its center. When a passage is hard, ask what it shows you about him.",
                    "Dos seguidores desanimados van camino a una aldea, después de la muerte de Jesús, cuando "
                    "un desconocido se les une. Es Jesús resucitado, aunque todavía no lo saben. Empezando por "
                    "los libros más antiguos de la Biblia, les explica cómo todo hablaba de él. Más tarde, "
                    "cuando parte el pan en su mesa, lo reconocen, y recuerdan cómo les ardía el corazón "
                    "mientras les abría las Escrituras. La Biblia son muchos libros, pero cuenta una sola "
                    "historia, y Jesús está en el centro. Cuando un pasaje sea difícil, pregunta qué te "
                    "muestra de él.",
                ),
                "simple": L(
                    "The whole Bible, from beginning to end, tells one big story about God's love. Jesus is "
                    "the most important person in it.",
                    "Toda la Biblia, de principio a fin, cuenta una gran historia del amor de Dios. Jesús es "
                    "la persona más importante de esa historia.",
                ),
                "ask": L(
                    "Has a Bible passage ever unexpectedly moved you or made something clear? What was it, "
                    "and what did it show you about Jesus?",
                    "¿Alguna vez un pasaje de la Biblia te conmovió o te aclaró algo sin que lo esperaras? "
                    "¿Cuál fue, y qué te mostró de Jesús?",
                ),
                "kid_ask": L(
                    "What is your favorite story about Jesus?",
                    "¿Cuál es tu historia favorita de Jesús?",
                ),
                "do": L(
                    "Before you read this week, pray one line: Jesus, walk with me and explain this. "
                    "Afterward, write one sentence about what the passage shows of him.",
                    "Esta semana, antes de leer, ora una línea: Jesús, camina conmigo y explícame esto. "
                    "Después escribe una frase sobre lo que el pasaje muestra de él.",
                ),
                "kid_do": L(
                    "Tell a grown-up your favorite Jesus story in your own words.",
                    "Cuéntale a un adulto tu historia favorita de Jesús con tus propias palabras.",
                ),
                "pray": L(
                    "Jesus, walk with me as I read. Open what I do not understand, and let me recognize you "
                    "in these pages.",
                    "Jesús, camina conmigo mientras leo. Ábreme lo que no entiendo, y déjame reconocerte en "
                    "estas páginas.",
                ),
            },
            {
                "key": "scripture-4",
                "ref": "Matthew 7:24-27",
                "title": L("Hearing and doing", "Oír y hacer"),
                "truth": L(
                    "Jesus ends his best-known sermon with two builders. Both hear his words, and both are "
                    "hit by the same storm. The difference is that one puts the words into practice and the "
                    "other does not, and only the first house is still standing afterward. Notice that doing "
                    "what Jesus says does not keep the rain away. It gives you something solid underneath "
                    "when it comes. The aim of reading the Bible is never just to know more. It is to do one "
                    "thing differently.",
                    "Jesús termina su sermón más conocido con dos constructores. Los dos oyen sus palabras, "
                    "y a los dos les cae la misma tormenta. La diferencia es que uno las pone en práctica y "
                    "el otro no, y solo la primera casa sigue en pie después. Fíjate en que hacer lo que "
                    "Jesús dice no aleja la lluvia. Te da algo firme debajo cuando llega. La meta de leer la "
                    "Biblia nunca es solo saber más. Es hacer una cosa de otra manera.",
                ),
                "simple": L(
                    "A house built on rock stays up in a storm. When we do what Jesus says, we are like that "
                    "strong house.",
                    "Una casa construida sobre roca aguanta la tormenta. Cuando hacemos lo que Jesús dice, "
                    "somos como esa casa fuerte.",
                ),
                "ask": L(
                    "What is one thing you already know Jesus teaches, that you have heard many times but "
                    "not yet done?",
                    "¿Qué cosa sabes ya que Jesús enseña, que has oído muchas veces pero todavía no has "
                    "hecho?",
                ),
                "kid_ask": L(
                    "What is one thing Jesus tells us to do that you could do today?",
                    "¿Qué cosa nos dice Jesús que hagamos que tú podrías hacer hoy?",
                ),
                "do": L(
                    "After each reading this week, finish one sentence in writing: Because of this, today I "
                    "will… Make it small enough to actually do before bedtime.",
                    "Después de cada lectura esta semana, completa por escrito una frase: Por esto, hoy voy "
                    "a… Que sea algo tan pequeño que de verdad lo hagas antes de dormir.",
                ),
                "kid_do": L(
                    "Build a little house with blocks, or draw one on a rock. Then do one good thing Jesus "
                    "teaches, like sharing.",
                    "Arma una casita con bloques, o dibuja una sobre una roca. Luego haz algo bueno que "
                    "Jesús enseña, como compartir.",
                ),
                "pray": L(
                    "Jesus, I have heard a lot and done little with it. Show me one thing to put into "
                    "practice today, and give me the will to do it.",
                    "Jesús, he oído mucho y he hecho poco con ello. Muéstrame una cosa para poner en práctica "
                    "hoy, y dame la voluntad de hacerla.",
                ),
            },
        ],
    },
    {
        "key": "holy_spirit",
        "category": "foundations",
        "title": L("The Holy Spirit", "El Espíritu Santo"),
        "summary": L(
            "For anyone who wonders how God can be present in an ordinary life. Four readings on the "
            "Spirit as God's nearness and help: the one who stays with you, assures you, and slowly "
            "grows good fruit in you.",
            "Para quien se pregunta cómo puede Dios estar presente en una vida común. Cuatro lecturas "
            "sobre el Espíritu como la cercanía y la ayuda de Dios: quien se queda contigo, te da "
            "seguridad y poco a poco hace crecer en ti buen fruto.",
        ),
        "keywords": [
            "spirit",
            "helper",
            "presence",
            "fruit",
            "guidance",
            "comforter",
            "empty",
            "strength",
            "espíritu",
            "espiritu",
            "ayudador",
            "presencia",
            "fruto",
            "guía",
            "consolador",
            "vací",
        ],
        "situations": ["new_believer", "returning", "exploring"],
        "traits": ["love", "peace", "self_control"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "Following Jesus is not something you grit your teeth through alone. God gives his own "
                "presence to help from the inside.",
                "Seguir a Jesús no es algo que aguantas a solas apretando los dientes. Dios da su propia "
                "presencia para ayudarte desde adentro.",
            ),
            "young_adult": L(
                "When you are on your own for the first time, it matters that God is not only above you "
                "but with you and in you.",
                "Cuando por primera vez te las arreglas por tu cuenta, importa que Dios no esté solo "
                "arriba, sino contigo y en ti.",
            ),
            "adult": L(
                "For people running on their own strength and running low. The Christian life was never "
                "meant to be powered by effort alone.",
                "Para quienes funcionan con sus propias fuerzas y ya les queda poco. La vida cristiana "
                "nunca fue pensada para sostenerse a puro esfuerzo.",
            ),
            "senior": L(
                "As outward strength lessens, the Spirit's quiet work inside goes on: comforting, "
                "assuring, still growing fruit.",
                "Mientras la fuerza exterior disminuye, la obra callada del Espíritu continúa por dentro: "
                "consuela, da seguridad y sigue dando fruto.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "holy_spirit-1",
                "ref": "John 14:15-17",
                "title": L("Someone who stays", "Alguien que se queda"),
                "truth": L(
                    "On his last evening with his friends, Jesus knows they are about to feel abandoned. He "
                    "promises that the Father will give them another helper, the Spirit of truth, who will "
                    "be with them for good. Jesus walked beside them for a few years; the Spirit would live "
                    "in them and not leave. Christians believe the Holy Spirit is not a force or a feeling "
                    "but God himself, present with everyone who belongs to Jesus. You may not always feel "
                    "him. He is there all the same.",
                    "En su última noche con sus amigos, Jesús sabe que están por sentirse abandonados. Les "
                    "promete que el Padre les dará otro ayudador, el Espíritu de verdad, que estará con "
                    "ellos para siempre. Jesús caminó a su lado unos pocos años; el Espíritu viviría en "
                    "ellos y no se iría. Los cristianos creen que el Espíritu Santo no es una fuerza ni una "
                    "sensación, sino Dios mismo, presente con todo el que pertenece a Jesús. Quizá no "
                    "siempre lo sientas. Está ahí de todos modos.",
                ),
                "simple": L(
                    "Jesus promised to send a Helper who never leaves. The Helper is God's Holy Spirit, and "
                    "he is with everyone who loves Jesus.",
                    "Jesús prometió enviar un Ayudador que nunca se va. Ese Ayudador es el Espíritu Santo de "
                    "Dios, y está con todos los que aman a Jesús.",
                ),
                "ask": L(
                    "Where do you most feel that you are handling life alone? What would it mean to have a "
                    "helper present in exactly that place?",
                    "¿Dónde sientes más que enfrentas la vida a solas? ¿Qué significaría tener un ayudador "
                    "presente justo en ese lugar?",
                ),
                "kid_ask": L(
                    "Who helps you when something is hard? How does it feel to have a helper?",
                    "¿Quién te ayuda cuando algo es difícil? ¿Cómo se siente tener a alguien que te ayuda?",
                ),
                "do": L(
                    "At the start of one hard task today, pause and say: Holy Spirit, you are here; help me "
                    "with this. Then begin.",
                    "Hoy, al comenzar una tarea difícil, detente y di: Espíritu Santo, estás aquí; ayúdame "
                    "con esto. Luego empieza.",
                ),
                "kid_do": L(
                    "Before something hard today, say: God, please be my helper.",
                    "Hoy, antes de algo difícil, di: Dios, sé mi ayudador, por favor.",
                ),
                "pray": L(
                    "Father, thank you for not leaving me to manage alone. Holy Spirit, make me aware of you "
                    "today, especially where I feel most on my own.",
                    "Padre, gracias por no dejarme a mi suerte. Espíritu Santo, hazme consciente de ti hoy, "
                    "sobre todo donde más siento que estoy por mi cuenta.",
                ),
            },
            {
                "key": "holy_spirit-2",
                "ref": "Romans 8:14-17",
                "title": L(
                    "The Spirit tells you whose you are",
                    "El Espíritu te dice de quién eres",
                ),
                "truth": L(
                    "Paul says the Spirit does not make us slaves who live in fear. He brings us into God's "
                    "family as adopted children, so that we can call God by the close name Abba, Father. "
                    "More than that, the Spirit himself assures us inwardly that we really are God's "
                    "children. That quiet confidence that you belong, that you may come to God and are not "
                    "an intruder, is his work. Paul is honest that God's children still suffer. But they "
                    "suffer as heirs, with a future, not as orphans.",
                    "Pablo dice que el Espíritu no nos hace esclavos que viven con miedo. Nos trae a la "
                    "familia de Dios como hijos adoptivos, para que podamos llamar a Dios con el nombre "
                    "cercano de Abba, Padre. Más aún, el Espíritu mismo nos asegura por dentro que de verdad "
                    "somos hijos de Dios. Esa confianza callada de que perteneces, de que puedes acercarte a "
                    "Dios sin ser un intruso, es obra suya. Pablo es honesto: los hijos de Dios todavía "
                    "sufren. Pero sufren como herederos, con un futuro, no como huérfanos.",
                ),
                "simple": L(
                    "God's Spirit helps us know deep inside that we are God's children and that we can call "
                    "him Father.",
                    "El Espíritu de Dios nos ayuda a saber muy adentro que somos hijos de Dios y que podemos "
                    "llamarlo Padre.",
                ),
                "ask": L(
                    "Do you relate to God more like a nervous employee or like a child at home? What feeds "
                    "the fear?",
                    "¿Te relacionas con Dios más como alguien que teme a su jefe o como quien está en su "
                    "casa? ¿Qué alimenta el miedo?",
                ),
                "kid_ask": L(
                    "What does it feel like to belong to a family?",
                    "¿Cómo se siente ser parte de una familia?",
                ),
                "do": L(
                    "Begin your prayers this week with the single word Father, and wait ten seconds before "
                    "saying anything else. Let the word do its work.",
                    "Esta semana empieza tus oraciones con una sola palabra, Padre, y espera diez segundos "
                    "antes de decir algo más. Deja que la palabra haga su trabajo.",
                ),
                "kid_do": L(
                    "Pray starting with the words Dear Father, and tell him one thing.",
                    "Ora empezando con las palabras Querido Padre, y cuéntale una cosa.",
                ),
                "pray": L(
                    "Abba, Father. I am not here as a stranger. Spirit of God, quiet my fear and tell me "
                    "again that I belong to you.",
                    "Abba, Padre. No vengo como alguien ajeno a tu casa. Espíritu de Dios, calma mi miedo y "
                    "vuelve a decirme que te pertenezco.",
                ),
            },
            {
                "key": "holy_spirit-3",
                "ref": "Galatians 5:22-25",
                "title": L("Fruit that grows", "Fruto que crece"),
                "truth": L(
                    "Paul lists nine qualities the Spirit produces in a person, beginning with love and "
                    "ending with self-control. He calls them fruit, and the word matters. Fruit is not "
                    "manufactured by trying harder; it grows, slowly, on a branch that stays connected. "
                    "These qualities are also a portrait of Jesus. Your part is not to force them but to "
                    "keep in step with the Spirit: turning toward him in the small choices of a day, and "
                    "letting him do what you cannot.",
                    "Pablo enumera nueve cualidades que el Espíritu produce en una persona, empezando por el "
                    "amor y terminando por el dominio propio. Las llama fruto, y la palabra importa. El "
                    "fruto no se fabrica a fuerza de empeño; crece, despacio, en una rama que se mantiene "
                    "unida. Estas cualidades son también un retrato de Jesús. Tu parte no es forzarlas, sino "
                    "andar al paso del Espíritu: volverte hacia él en las decisiones pequeñas del día y "
                    "dejar que haga lo que tú no puedes.",
                ),
                "simple": L(
                    "When God's Spirit lives in us, good things grow in us like fruit on a tree: love, joy, "
                    "kindness and more.",
                    "Cuando el Espíritu de Dios vive en nosotros, crecen cosas buenas como fruta en un "
                    "árbol: amor, alegría, bondad y más.",
                ),
                "ask": L(
                    "Looking at the list, which quality has actually grown in you over the past few years, "
                    "and which one do you most want the Spirit to grow next?",
                    "Mirando la lista, ¿qué cualidad ha crecido de verdad en ti en los últimos años, y cuál "
                    "quisieras que el Espíritu hiciera crecer ahora?",
                ),
                "kid_ask": L(
                    "Which fruit would you like to grow more in you: love, joy or kindness?",
                    "¿Qué fruto te gustaría que creciera más en ti: el amor, la alegría o la bondad?",
                ),
                "do": L(
                    "Pick one quality from the list for this week. Each morning ask the Spirit for it by "
                    "name, and each night write down one moment when you saw it or missed it.",
                    "Elige una cualidad de la lista para esta semana. Cada mañana pídesela al Espíritu por "
                    "su nombre, y cada noche anota un momento en que la viste o te faltó.",
                ),
                "kid_do": L(
                    "Draw a tree with fruit and write love, joy and kindness on the fruit. Then do one kind "
                    "thing today.",
                    "Dibuja un árbol con frutas y escribe amor, alegría y bondad en las frutas. Luego haz "
                    "hoy una cosa amable.",
                ),
                "pray": L(
                    "Holy Spirit, I cannot make myself loving or patient by willpower. Grow in me what I "
                    "cannot produce, and help me keep in step with you today.",
                    "Espíritu Santo, no puedo llenarme de amor ni de paciencia a pura fuerza de voluntad. "
                    "Haz crecer en mí lo que yo no puedo producir, y ayúdame a andar a tu paso hoy.",
                ),
            },
            {
                "key": "holy_spirit-4",
                "ref": "Ephesians 3:14-19",
                "title": L("Strength on the inside", "Fuerza por dentro"),
                "truth": L(
                    "Paul kneels and prays for his friends, and what he asks for is not easier "
                    "circumstances. He asks that God would strengthen them through his Spirit in their inner "
                    "being, so that Christ would be at home in their hearts. And he asks that they would be "
                    "able to take in the full size of Christ's love, in every direction, a love too great to "
                    "know completely. This is what the Spirit's power is first of all for: to make you strong "
                    "inside and sure that you are loved.",
                    "Pablo se arrodilla y ora por sus amigos, y lo que pide no son circunstancias más "
                    "fáciles. Pide que Dios los fortalezca por medio de su Espíritu en lo más íntimo de su "
                    "ser, para que Cristo habite a gusto en sus corazones. Y pide que puedan captar el "
                    "tamaño completo del amor de Cristo, en todas sus dimensiones, un amor demasiado grande "
                    "para conocerlo del todo. Para esto es, ante todo, el poder del Espíritu: para darte "
                    "fuerza por dentro y la certeza de que te aman.",
                ),
                "simple": L(
                    "God's Spirit makes us strong on the inside and helps us know how very big Jesus' love "
                    "is.",
                    "El Espíritu de Dios nos hace fuertes por dentro y nos ayuda a saber lo grandísimo que "
                    "es el amor de Jesús.",
                ),
                "ask": L(
                    "If you prayed for inner strength instead of changed circumstances, what would you be "
                    "asking for today?",
                    "Si oraras por fuerza interior en lugar de un cambio de circunstancias, ¿qué estarías "
                    "pidiendo hoy?",
                ),
                "kid_ask": L(
                    "How big do you think Jesus' love is? Show it with your arms.",
                    "¿Qué tan grande crees que es el amor de Jesús? Muéstralo con tus brazos.",
                ),
                "do": L(
                    "Pray Paul's request for one other person by name today: that the Spirit would "
                    "strengthen them inside and let them know they are loved. Then tell them you prayed.",
                    "Hoy ora la petición de Pablo por otra persona, con su nombre: que el Espíritu la "
                    "fortalezca por dentro y le haga saber que es amada. Luego dile que oraste por ella.",
                ),
                "kid_do": L(
                    "Stretch your arms as wide as you can and say: Jesus loves me this much and more.",
                    "Abre los brazos lo más que puedas y di: Jesús me ama así de mucho y más.",
                ),
                "pray": L(
                    "Father, strengthen me by your Spirit where I am weakest inside. Let Christ be at home "
                    "in me, and help me grasp a little more of how much I am loved.",
                    "Padre, fortaléceme con tu Espíritu donde soy más débil por dentro. Que Cristo habite a "
                    "gusto en mí, y ayúdame a comprender un poco más cuánto me amas.",
                ),
            },
        ],
    },
    {
        "key": "doubt",
        "category": "foundations",
        "title": L("Doubt and honest questions", "Dudas y preguntas honestas"),
        "summary": L(
            "For anyone whose faith feels shaky, or who has questions they are afraid to ask. Four "
            "readings about people in the Bible who doubted, and how Jesus met them without shaming "
            "them.",
            "Para quien siente que su fe tambalea, o tiene preguntas que no se atreve a hacer. Cuatro "
            "lecturas sobre personas de la Biblia que dudaron, y cómo Jesús las recibió sin "
            "avergonzarlas.",
        ),
        "keywords": [
            "doubt",
            "question",
            "unsure",
            "uncertain",
            "skeptic",
            "unbelief",
            "deconstruct",
            "proof",
            "duda",
            "dudo",
            "dudar",
            "pregunta",
            "insegur",
            "incrédul",
            "escéptic",
            "incertidumbre",
            "prueba",
        ],
        "situations": ["exploring", "returning", "student", "new_believer"],
        "traits": ["honesty", "trust", "courage"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "Asking hard questions does not mean you are losing your faith. It may mean it is becoming "
                "your own.",
                "Hacer preguntas difíciles no significa que estés perdiendo la fe. Puede significar que "
                "está empezando a ser tuya.",
            ),
            "young_adult": L(
                "If what you were taught no longer fits neatly, you are in good company. Bring the "
                "questions into the open; do not carry them alone.",
                "Si lo que te enseñaron ya no encaja tan fácil, estás en buena compañía. Saca las "
                "preguntas a la luz; no las cargues a solas.",
            ),
            "adult": L(
                "Sometimes doubt arrives late, after loss or disappointment. These readings make room for "
                "it without pretending.",
                "A veces la duda llega tarde, después de una pérdida o una decepción. Estas lecturas le "
                "hacen lugar sin fingir.",
            ),
            "senior": L(
                "Even after a lifetime of believing, questions can return. The Lord who was patient with "
                "Thomas is patient with you.",
                "Aun después de toda una vida creyendo, las preguntas pueden volver. El Señor que tuvo "
                "paciencia con Tomás la tiene contigo.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "doubt-1",
                "ref": "Matthew 11:2-6",
                "title": L("Even John asked", "Hasta Juan preguntó"),
                "truth": L(
                    "John the Baptist had announced Jesus to the world. Now he is in prison, things have not "
                    "gone as he expected, and he sends some of his followers to ask whether Jesus really is the one or "
                    "whether they should wait for someone else. Jesus does not scold him. He points to what "
                    "is actually happening: the blind see, the lame walk, the poor hear good news. Then he "
                    "blesses whoever does not give up on him. Doubt often comes when God does not act the way "
                    "we assumed he would. Jesus answers it with evidence and with kindness.",
                    "Juan el Bautista había anunciado a Jesús ante todos. Ahora está en la cárcel, las cosas "
                    "no han salido como esperaba, y envía a algunos de sus seguidores a preguntar si Jesús es de verdad el "
                    "que había de venir o si deben esperar a otro. Jesús no lo regaña. Señala lo que "
                    "realmente está pasando: los ciegos ven, los cojos caminan, los pobres reciben buenas "
                    "noticias. Luego llama dichoso a quien no se aparta de él. La duda suele llegar cuando "
                    "Dios no actúa como suponíamos. Jesús le responde con hechos y con bondad.",
                ),
                "simple": L(
                    "John was in a hard place and started to wonder about Jesus. So he asked. Jesus was not "
                    "angry. He answered kindly.",
                    "Juan estaba en un lugar difícil y empezó a tener dudas sobre Jesús. Entonces preguntó. "
                    "Jesús no se enojó. Le respondió con cariño.",
                ),
                "ask": L(
                    "What did you expect God to do that he has not done? How has that shaped your questions?",
                    "¿Qué esperabas que Dios hiciera y no ha hecho? ¿Cómo ha influido eso en tus preguntas?",
                ),
                "kid_ask": L(
                    "What is a question about God you have wondered about?",
                    "¿Qué pregunta sobre Dios te has hecho alguna vez?",
                ),
                "do": L(
                    "Write your biggest question about God as an actual question addressed to Jesus, as John "
                    "did. Do not answer it yet. Keep it where you can return to it.",
                    "Escribe tu mayor pregunta sobre Dios como una pregunta dirigida a Jesús, como hizo "
                    "Juan. No la respondas todavía. Guárdala donde puedas volver a ella.",
                ),
                "kid_do": L(
                    "Ask a grown-up one question you have about God. It is good to ask!",
                    "Hazle a un adulto una pregunta que tengas sobre Dios. ¡Preguntar es bueno!",
                ),
                "pray": L(
                    "Jesus, this is not what I expected, and I have started to wonder. Here is my question: "
                    "… Show me what you are really doing.",
                    "Jesús, esto no es lo que esperaba, y he empezado a dudar. Esta es mi pregunta: … "
                    "Muéstrame lo que de verdad estás haciendo.",
                ),
            },
            {
                "key": "doubt-2",
                "ref": "John 20:24-29",
                "title": L("Jesus comes back for Thomas", "Jesús vuelve por Tomás"),
                "truth": L(
                    "Thomas was not there when the risen Jesus first appeared, and he refused to believe on "
                    "his friends' word alone; he wanted to see and touch the wounds. Notice two things. The "
                    "others did not push him out: a week later he was still with them. And Jesus came back "
                    "and offered Thomas exactly what he had asked for. Thomas answered with one of the "
                    "strongest confessions of faith in the Bible. Jesus then blessed those who would believe "
                    "without seeing, which includes anyone who trusts him today.",
                    "Tomás no estaba cuando Jesús resucitado apareció por primera vez, y se negó a creer "
                    "solo por la palabra de sus amigos; quería ver y tocar las heridas. Fíjate en dos cosas. "
                    "Los demás no lo apartaron: una semana después seguía con ellos. Y Jesús volvió y le "
                    "ofreció a Tomás justo lo que había pedido. Tomás respondió con una de las confesiones "
                    "de fe más firmes de la Biblia. Luego Jesús llamó dichosos a quienes creyeran sin ver, y "
                    "eso incluye a cualquiera que hoy confía en él.",
                ),
                "simple": L(
                    "Thomas said he would not believe Jesus was alive unless he saw him. Jesus came and "
                    "showed him. Jesus is patient with our questions.",
                    "Tomás dijo que no creería que Jesús estaba vivo si no lo veía. Jesús vino y se lo "
                    "mostró. Jesús tiene paciencia con nuestras preguntas.",
                ),
                "ask": L(
                    "What would you need in order to believe, or to believe more? Have you told Jesus that "
                    "as plainly as Thomas told his friends?",
                    "¿Qué necesitarías para creer, o para creer más? ¿Se lo has dicho a Jesús tan claramente "
                    "como Tomás se lo dijo a sus amigos?",
                ),
                "kid_ask": L(
                    "Is it hard to believe in something you cannot see? Why?",
                    "¿Es difícil creer en algo que no puedes ver? ¿Por qué?",
                ),
                "do": L(
                    "Stay near people of faith while you question. This week, tell one trusted believer "
                    "about a doubt you have, and ask them to pray with you rather than fix it.",
                    "Quédate cerca de personas de fe mientras preguntas. Esta semana cuéntale a un creyente "
                    "de confianza una duda que tengas, y pídele que ore contigo en vez de resolverla.",
                ),
                "kid_do": L(
                    "Tell Jesus: I cannot see you, but I want to know you. Help me believe.",
                    "Dile a Jesús: No puedo verte, pero quiero conocerte. Ayúdame a creer.",
                ),
                "pray": L(
                    "Jesus, I was not there and I cannot see you. Come to me as you came to Thomas, and give "
                    "me what I need in order to trust you.",
                    "Jesús, yo no estuve allí y no puedo verte. Ven a mí como viniste a Tomás, y dame lo que "
                    "necesito para confiar en ti.",
                ),
            },
            {
                "key": "doubt-3",
                "ref": "Mark 9:21-27",
                "title": L("Belief and unbelief together", "Fe y duda al mismo tiempo"),
                "truth": L(
                    "A father brings his suffering son to Jesus and asks for help, if Jesus can do anything. "
                    "When Jesus speaks about believing, the father gives one of the most honest answers in "
                    "the Gospels: he does believe, and he needs help with the part of him that does not. "
                    "Jesus does not wait for that faith to become perfect. He helps the boy. Faith and doubt "
                    "can live in the same heart at the same time. What matters most is not how much faith "
                    "you have but who you bring it to.",
                    "Un padre lleva a su hijo, que sufre, ante Jesús y le pide ayuda, si es que puede hacer "
                    "algo. Cuando Jesús habla de creer, el padre da una de las respuestas más honestas de "
                    "los Evangelios: sí cree, y necesita ayuda con la parte de él que no cree. Jesús no "
                    "espera a que esa fe sea perfecta. Ayuda al muchacho. La fe y la duda pueden vivir en el "
                    "mismo corazón al mismo tiempo. Lo que más importa no es cuánta fe tienes, sino a quién "
                    "se la llevas.",
                ),
                "simple": L(
                    "A dad told Jesus that he believed, but not all the way, and he asked for help. Jesus "
                    "helped him. You can ask Jesus to help you believe too.",
                    "Un papá le dijo a Jesús que creía, pero no del todo, y le pidió ayuda. Jesús lo ayudó. "
                    "Tú también puedes pedirle a Jesús que te ayude a creer.",
                ),
                "ask": L(
                    "If you divided yourself honestly, which part of you believes and which part does not? "
                    "What would you ask Jesus to do for the second part?",
                    "Si te dividieras con honestidad, ¿qué parte de ti cree y qué parte no? ¿Qué le pedirías "
                    "a Jesús que hiciera por la segunda?",
                ),
                "kid_ask": L(
                    "When is it hard for you to trust?",
                    "¿Cuándo te cuesta confiar?",
                ),
                "do": L(
                    "Make the father's prayer your own this week, in your words: say what you do believe, "
                    "name what you do not, and ask for help. Pray it once a day.",
                    "Haz tuya esta semana la oración del padre, con tus palabras: di lo que sí crees, nombra "
                    "lo que no, y pide ayuda. Órala una vez al día.",
                ),
                "kid_do": L(
                    "Pray one sentence: Jesus, help me trust you more.",
                    "Ora una frase: Jesús, ayúdame a confiar más en ti.",
                ),
                "pray": L(
                    "Jesus, part of me trusts you and part of me does not. I bring you both. Help the part "
                    "that cannot believe yet.",
                    "Jesús, una parte de mí confía en ti y otra no. Te traigo las dos. Ayuda a la parte que "
                    "todavía no logra creer.",
                ),
            },
            {
                "key": "doubt-4",
                "ref": "Matthew 28:16-20",
                "title": L("Doubters are sent too", "También envía a los que dudan"),
                "truth": L(
                    "This is the last scene of Matthew's Gospel. The disciples meet the risen Jesus on a "
                    "mountain and worship him, and Matthew adds, without embarrassment, that some doubted. "
                    "Jesus does not sort the group into the sure and the unsure. He gives them all the same "
                    "work, to make disciples of every nation, and the same promise: he will be with them "
                    "always. Doubt is not the opposite of faith. You can worship, serve and follow while "
                    "some questions are still open, and Jesus promises to stay with you as you do.",
                    "Esta es la última escena del Evangelio de Mateo. Los discípulos se encuentran con Jesús "
                    "resucitado en un monte y lo adoran, y Mateo añade, sin vergüenza, que algunos dudaban. "
                    "Jesús no separa al grupo entre seguros e inseguros. A todos les da la misma tarea, "
                    "hacer discípulos en todas las naciones, y la misma promesa: estará con ellos siempre. "
                    "La duda no es lo contrario de la fe. Puedes adorar, servir y seguir a Jesús con algunas "
                    "preguntas todavía abiertas, y él promete quedarse contigo mientras lo haces.",
                ),
                "simple": L(
                    "Some of Jesus' friends still had questions. Jesus still gave them a job and promised to "
                    "be with them always.",
                    "Algunos amigos de Jesús todavía tenían preguntas. Aun así Jesús les dio una tarea y les "
                    "prometió estar siempre con ellos.",
                ),
                "ask": L(
                    "Have you been waiting to be certain before you take a next step with God? What step "
                    "could you take with your questions still in hand?",
                    "¿Has estado esperando tener certeza antes de dar un paso con Dios? ¿Qué paso podrías "
                    "dar con tus preguntas todavía en la mano?",
                ),
                "kid_ask": L(
                    "Jesus promised to be with us always. When would you like to remember that?",
                    "Jesús prometió estar siempre con nosotros. ¿Cuándo te gustaría recordarlo?",
                ),
                "do": L(
                    "Do one act of faith this week that does not require certainty: go to church, serve "
                    "someone, or pray. Notice whether Jesus meets you in the doing.",
                    "Esta semana haz un acto de fe que no exija certeza: ve a la iglesia, sirve a alguien u "
                    "ora. Observa si Jesús te sale al encuentro mientras lo haces.",
                ),
                "kid_do": L(
                    "Say three times today: Jesus is with me always.",
                    "Di tres veces hoy: Jesús está conmigo siempre.",
                ),
                "pray": L(
                    "Jesus, I worship you, and I still have questions. Thank you for not sending me away. "
                    "Stay with me, as you promised, and give me something to do for you.",
                    "Jesús, te adoro, y todavía tengo preguntas. Gracias por no apartarme. Quédate conmigo, "
                    "como prometiste, y dame algo que hacer por ti.",
                ),
            },
        ],
    },
    {
        "key": "identity",
        "category": "foundations",
        "title": L("Who you are", "Quién eres"),
        "summary": L(
            "For anyone measuring their worth by results, by their past or by what others think. Five "
            "readings on what God says about you: made in his image, fully known, loved, and counted "
            "among his children.",
            "Para quien mide su valor por sus logros, su pasado o la opinión de otros. Cinco lecturas "
            "sobre lo que Dios dice de ti: que llevas su imagen, que te conoce por completo, que te ama "
            "y te cuenta entre sus hijos.",
        ),
        "keywords": [
            "identity",
            "worth",
            "esteem",
            "compar",
            "insecur",
            "enough",
            "belong",
            "failure",
            "identidad",
            "valgo",
            "autoestima",
            "inseguri",
            "suficiente",
            "pertene",
            "fracas",
        ],
        "situations": [
            "student",
            "new_believer",
            "exploring",
            "job_seeking",
            "moving",
            "retired",
        ],
        "traits": ["contentment", "trust", "humility"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "God made you, God knows you, and God loves you. Nothing can change that.",
                "Dios te hizo, Dios te conoce y Dios te ama. Nada puede cambiar eso.",
            ),
            "teen": L(
                "When everyone has an opinion about who you should be, it helps to hear what the one who "
                "made you says.",
                "Cuando todos opinan sobre quién deberías ser, ayuda escuchar lo que dice quien te hizo.",
            ),
            "young_adult": L(
                "You are more than your degree, your job, your relationship status or your follower count. "
                "Start from what is already true.",
                "Eres más que tu carrera, tu trabajo, tu situación sentimental o tus seguidores. Parte de "
                "lo que ya es verdad.",
            ),
            "adult": L(
                "For when you have become your role: the provider, the parent, the reliable one. "
                "Underneath all of it, you are someone God loves.",
                "Para cuando te has vuelto tu papel: quien provee, quien cría, quien nunca falla. Debajo "
                "de todo eso, eres alguien a quien Dios ama.",
            ),
            "senior": L(
                "When work ends and roles change, who you are does not. Your worth was never in what you "
                "could produce.",
                "Cuando el trabajo termina y los papeles cambian, quien eres no cambia. Tu valor nunca "
                "estuvo en lo que podías producir.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "identity-1",
                "ref": "Genesis 1:26-31",
                "title": L("Made in God's image", "A imagen de Dios"),
                "truth": L(
                    "Before the first human beings had done anything at all, God said something about them: "
                    "they were made in his image, to reflect him in the world. This is said of male and "
                    "female alike, and of no other creature. Then God looked at everything he had made and "
                    "called it very good. Your worth, then, is not a score you build up. It was given at the "
                    "start, and it belongs equally to every person you will meet today.",
                    "Antes de que los primeros seres humanos hicieran cosa alguna, Dios ya había dicho algo "
                    "de ellos: fueron hechos a su imagen, para reflejarlo en el mundo. Lo dice del hombre y "
                    "de la mujer por igual, y de ninguna otra criatura. Luego Dios miró todo lo que había "
                    "hecho y lo llamó muy bueno. Tu valor, entonces, no es un puntaje que vas acumulando. Te "
                    "fue dado desde el principio, y pertenece por igual a cada persona con la que te cruces "
                    "hoy.",
                ),
                "simple": L(
                    "God made people to be like him in a special way. That means you are very precious, and "
                    "so is everyone else.",
                    "Dios hizo a las personas parecidas a él de una manera especial. Eso quiere decir que "
                    "vales muchísimo, y también todos los demás.",
                ),
                "ask": L(
                    "What do you usually point to when you want to feel that you matter? How would your day "
                    "change if your worth were already settled?",
                    "¿A qué sueles recurrir cuando quieres sentir que vales? ¿Cómo cambiaría tu día si tu "
                    "valor ya estuviera resuelto?",
                ),
                "kid_ask": L(
                    "What is something special about the way God made you?",
                    "¿Qué tiene de especial la manera en que Dios te hizo?",
                ),
                "do": L(
                    "Today, each time you catch yourself comparing, say silently: In God's image. Say it "
                    "about yourself, then about the person you compared yourself with.",
                    "Hoy, cada vez que te descubras comparándote, di en silencio: A imagen de Dios. Dilo de "
                    "ti, y luego de la persona con quien te comparaste.",
                ),
                "kid_do": L(
                    "Look in a mirror and say: God made me, and God is glad he did.",
                    "Mírate en un espejo y di: Dios me hizo, y está contento de haberme hecho.",
                ),
                "pray": L(
                    "God, you made me in your image before I achieved anything. Help me stop earning what "
                    "you already gave, and help me see your image in the people around me.",
                    "Dios, me hiciste a tu imagen antes de que yo lograra nada. Ayúdame a dejar de ganarme "
                    "lo que ya me diste, y a ver tu imagen en quienes me rodean.",
                ),
            },
            {
                "key": "identity-2",
                "ref": "Psalm 139:1-6",
                "title": L("Fully known", "Te conoce por completo"),
                "truth": L(
                    "David says God has searched him and knows him: when he sits and when he stands, what he "
                    "thinks, where he goes, even what he is going to say before he says it. For many people, "
                    "being completely known sounds like a threat. Here it is a comfort, because the one who "
                    "knows everything has not turned away. He surrounds David and rests a hand on him. You do "
                    "not have to manage God's impression of you. He already knows, and he has stayed.",
                    "David dice que Dios lo ha examinado y lo conoce: cuándo se sienta y cuándo se levanta, "
                    "lo que piensa, por dónde anda, hasta lo que va a decir antes de decirlo. A muchos, ser "
                    "conocidos por completo les suena a amenaza. Aquí es un consuelo, porque quien lo sabe "
                    "todo no se ha apartado. Rodea a David y pone su mano sobre él. No tienes que cuidar la "
                    "impresión que Dios tiene de ti. Él ya lo sabe todo, y se ha quedado.",
                ),
                "simple": L(
                    "God knows everything about you: what you think, where you go, and what you are going to "
                    "say. And he loves you and stays close.",
                    "Dios sabe todo de ti: lo que piensas, a dónde vas y lo que vas a decir. Y te ama y se "
                    "queda cerca.",
                ),
                "ask": L(
                    "What part of you do you work hardest to keep others from seeing? How does it feel to "
                    "know God already sees it and has not left?",
                    "¿Qué parte de ti te esfuerzas más por ocultar a los demás? ¿Cómo se siente saber que "
                    "Dios ya la ve y no se ha ido?",
                ),
                "kid_ask": L(
                    "What is something about you that only a few people know?",
                    "¿Qué cosa de ti saben solo unas pocas personas?",
                ),
                "do": L(
                    "Write three true sentences about yourself that you rarely say aloud. Read them to God. "
                    "If one of them is a heavy secret, consider telling one trusted person this week.",
                    "Escribe tres frases verdaderas sobre ti que casi nunca dices en voz alta. Léeselas a "
                    "Dios. Si alguna es un secreto pesado, considera contársela esta semana a una persona de "
                    "confianza.",
                ),
                "kid_do": L(
                    "Tell God one thing about you that he already knows, like your favorite game. He likes "
                    "hearing it from you.",
                    "Cuéntale a Dios una cosa de ti que él ya sabe, como tu juego favorito. Le gusta oírlo "
                    "de ti.",
                ),
                "pray": L(
                    "Lord, you know me better than I know myself, and you have not gone anywhere. Help me "
                    "stop hiding from the one who already sees.",
                    "Señor, me conoces mejor que yo, y no te has ido a ninguna parte. Ayúdame a dejar de "
                    "esconderme de quien ya me ve.",
                ),
            },
            {
                "key": "identity-3",
                "ref": "1 John 3:1-3",
                "title": L("Children of God", "Hijos de Dios"),
                "truth": L(
                    "John writes with something like astonishment at the Father's love: it is so great that "
                    "it gives us the name of God's children. And he insists this is not just a nice title; "
                    "it is what those who belong to Jesus really are. He admits that what we will become is "
                    "not yet visible, but one day we will see Jesus and be like him. Your deepest identity is "
                    "not a label you chose or one someone stuck on you. It is a family name, given by a "
                    "Father who wanted you.",
                    "Juan escribe casi con asombro ante el amor del Padre: es tan grande que nos da el "
                    "nombre de hijos de Dios. E insiste en que no es solo un título bonito; es lo que de "
                    "verdad son quienes pertenecen a Jesús. Admite que todavía no se ve lo que llegaremos a "
                    "ser, pero un día veremos a Jesús y seremos como él. Tu identidad más profunda no es una "
                    "etiqueta que elegiste ni una que alguien te pegó. Es un apellido de familia, dado por "
                    "un Padre que te quiso tener.",
                ),
                "simple": L(
                    "God loves you so much that he calls you his child. You belong in God's family.",
                    "Dios te ama tanto que te llama su hijo o su hija. Tienes un lugar en la familia de Dios.",
                ),
                "ask": L(
                    "Which labels, given by you or by others, have you been living under? What changes if "
                    "child of God is the truest one?",
                    "¿Bajo qué etiquetas, puestas por ti o por otros, has estado viviendo? ¿Qué cambia si la "
                    "más verdadera es la de hijo o hija de Dios?",
                ),
                "kid_ask": L(
                    "What does it mean to you to be part of God's family?",
                    "¿Qué significa para ti ser parte de la familia de Dios?",
                ),
                "do": L(
                    "On one side of a page, write the labels you carry: your role, your failures, what "
                    "people call you. On the other side write: Child of God. Keep the page where you will "
                    "see it.",
                    "En un lado de una hoja escribe las etiquetas que cargas: tu papel, tus fracasos, lo que "
                    "la gente dice de ti. En el otro lado escribe: De la familia de Dios. Deja la hoja donde "
                    "la veas.",
                ),
                "kid_do": L(
                    "Say your name and add: child of God. Say it out loud twice.",
                    "Di tu nombre y agrega: hijo de Dios, o hija de Dios. Dilo dos veces en voz alta.",
                ),
                "pray": L(
                    "Father, thank you for giving me a place among your children. When other names feel "
                    "louder, remind me whose I am.",
                    "Padre, gracias por darme un lugar entre tus hijos. Cuando otros nombres suenen más "
                    "fuerte, recuérdame a quién pertenezco.",
                ),
            },
            {
                "key": "identity-4",
                "ref": "2 Corinthians 5:16-19",
                "title": L("Not your past", "No eres tu pasado"),
                "truth": L(
                    "Paul says he no longer sizes people up the way the world does. The reason is that "
                    "anyone who is in Christ is a new creation: the old has gone and something new has "
                    "begun. This is God's doing. Through Christ he made peace with us and stopped counting "
                    "our wrongs against us. Your past is real, and some of its consequences may remain. But "
                    "it is no longer the truest thing about you, and it does not get to name you.",
                    "Pablo dice que ya no evalúa a las personas como lo hace el mundo. La razón es que quien "
                    "está unido a Cristo es una nueva creación: lo viejo quedó atrás y algo nuevo ha "
                    "comenzado. Esto es obra de Dios. Por medio de Cristo hizo las paces con nosotros y dejó "
                    "de tomarnos en cuenta nuestras faltas. Tu pasado es real, y puede que algunas de sus "
                    "consecuencias sigan. Pero ya no es lo más verdadero de ti, y no le corresponde ponerte "
                    "nombre.",
                ),
                "simple": L(
                    "Jesus gives new starts. The wrong things you did are not who you are. With Jesus, you "
                    "can begin again.",
                    "Jesús da nuevos comienzos. Las cosas malas que hiciste no son quien eres. Con Jesús, "
                    "puedes empezar de nuevo.",
                ),
                "ask": L(
                    "What from your past still introduces itself as your name? What would it mean to regard "
                    "yourself the way God now regards you?",
                    "¿Qué cosa de tu pasado todavía se presenta como si fuera tu nombre? ¿Qué significaría "
                    "mirarte como Dios te mira ahora?",
                ),
                "kid_ask": L(
                    "How does it feel to get a fresh start after a bad day?",
                    "¿Cómo se siente empezar de nuevo después de un mal día?",
                ),
                "do": L(
                    "Finish this sentence in writing: I used to think of myself as… but in Christ I am… Read "
                    "the second half aloud each morning this week.",
                    "Completa por escrito esta frase: Antes me veía como… pero en Cristo soy… Lee la segunda "
                    "mitad en voz alta cada mañana esta semana.",
                ),
                "kid_do": L(
                    "Draw a caterpillar and a butterfly. Tell a grown-up how Jesus makes things new.",
                    "Dibuja una oruga y una mariposa. Cuéntale a un adulto cómo Jesús hace nuevas las cosas.",
                ),
                "pray": L(
                    "God, you know my past and you have not held it against me. Help me stop answering to "
                    "old names, and live as someone you have made new.",
                    "Dios, conoces mi pasado y no me lo has tomado en cuenta. Ayúdame a dejar de responder a "
                    "nombres viejos y a vivir como alguien a quien hiciste de nuevo.",
                ),
            },
            {
                "key": "identity-5",
                "ref": "Romans 8:31-39",
                "title": L("The last word about you", "La última palabra sobre ti"),
                "truth": L(
                    "Paul asks a string of questions. With God on our side, who is left to fear? Who can "
                    "accuse those God has accepted? Who can condemn, when Christ himself died, rose, and now "
                    "speaks up for us? Then he lists everything that might seem able to cut us off from "
                    "God's love, hardship, danger, death, powers of any kind, and says none of it can. Other "
                    "people's opinions are real, and so is your own inner critic. But neither one is the "
                    "judge, and the judge has already spoken in your favor.",
                    "Pablo hace una serie de preguntas. Con Dios de nuestra parte, ¿a quién queda temer? "
                    "¿Quién puede acusar a los que Dios aceptó? ¿Quién puede condenar, si Cristo mismo "
                    "murió, resucitó y ahora intercede por nosotros? Luego enumera todo lo que parecería "
                    "capaz de separarnos del amor de Dios, las dificultades, el peligro, la muerte, poderes "
                    "de cualquier clase, y dice que nada lo logra. Las opiniones ajenas son reales, y "
                    "también tu crítico interior. Pero ninguno de los dos es el juez, y el juez ya habló a "
                    "tu favor.",
                ),
                "simple": L(
                    "Nothing in the whole world can make God stop loving you. Not a bad day, not a mistake, "
                    "not what anyone says.",
                    "Nada en todo el mundo puede hacer que Dios deje de amarte. Ni un mal día, ni un error, "
                    "ni lo que alguien diga.",
                ),
                "ask": L(
                    "Whose verdict about you carries the most weight right now: a parent's, a boss's, the "
                    "crowd's, your own? What would it take to let God's verdict outrank it?",
                    "¿El veredicto de quién pesa más sobre ti ahora mismo: el de tu padre o tu madre, el de "
                    "un jefe, el de la gente, el tuyo? ¿Qué haría falta para que el de Dios pesara más?",
                ),
                "kid_ask": L(
                    "Has someone ever said something unkind about you? What does God say about you?",
                    "¿Alguna vez alguien dijo algo feo de ti? ¿Qué dice Dios de ti?",
                ),
                "do": L(
                    "The next time criticism, or your own harsh voice, stings this week, pause before "
                    "reacting and say: That is not the final word. Then decide calmly what, if anything, to "
                    "learn from it.",
                    "La próxima vez que esta semana te duela una crítica, o tu propia voz dura, detente "
                    "antes de reaccionar y di: Esa no es la última palabra. Luego decide con calma qué "
                    "puedes aprender de ella, si es que hay algo.",
                ),
                "kid_do": L(
                    "Make a card that says Nothing can stop God from loving me, and put it by your bed.",
                    "Haz una tarjeta que diga Nada puede hacer que Dios deje de amarme, y ponla junto a tu "
                    "cama.",
                ),
                "pray": L(
                    "God, you are for me. When I am accused, by others or by myself, let me hear your voice "
                    "above theirs. Thank you that nothing can cut me off from your love.",
                    "Dios, tú estás de mi parte. Cuando me acusen otros, o me acuse yo, hazme oír tu voz por "
                    "encima de las demás. Gracias porque nada puede apartarme de tu amor.",
                ),
            },
        ],
    },
    # ======================================================================
    # CHARACTER
    # ======================================================================
    {
        "key": "patience",
        "category": "character",
        "title": L("Patience", "Paciencia"),
        "summary": L(
            "For anyone who is short with people, tired of waiting on God, or hard on themselves. Four "
            "readings on the patience God has shown you, and how it grows into patience with others, "
            "with his timing and with your own slow progress.",
            "Para quien pierde la paciencia con la gente, se cansa de esperar a Dios o se exige "
            "demasiado. Cuatro lecturas sobre la paciencia que Dios te ha tenido, y cómo se vuelve "
            "paciencia con otros, con sus tiempos y con tu propio avance lento.",
        ),
        "keywords": [
            "patien",
            "impatien",
            "irritat",
            "frustrat",
            "snap",
            "waiting",
            "temper",
            "annoy",
            "pacien",
            "impacien",
            "irrit",
            "frustra",
            "esperar",
            "desesper",
            "molest",
            "prisa",
        ],
        "situations": [
            "parent",
            "single_parent",
            "caregiver",
            "married",
            "working",
            "leader",
        ],
        "traits": ["patience", "gentleness", "perseverance"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Waiting is hard! God is very patient with us, and he helps us learn to wait and to be "
                "kind.",
                "¡Esperar es difícil! Dios nos tiene mucha paciencia, y nos ayuda a aprender a esperar y a "
                "ser amables.",
            ),
            "teen": L(
                "With siblings, parents, slow friends and your own unfinished self: patience is strength "
                "under control, not weakness.",
                "Con hermanos, padres, amigos lentos y contigo, que todavía estás en proceso: la paciencia "
                "es fuerza bajo control, no debilidad.",
            ),
            "young_adult": L(
                "For when your life is not moving as fast as you planned, or as fast as everyone else's "
                "seems to be.",
                "Para cuando tu vida no avanza tan rápido como planeabas, o tan rápido como parece avanzar "
                "la de los demás.",
            ),
            "adult": L(
                "For the tenth interruption of the day, the long wait for an answer, and the habits you "
                "thought you would have beaten by now.",
                "Para la décima interrupción del día, la larga espera de una respuesta y los hábitos que "
                "pensabas haber vencido ya.",
            ),
            "senior": L(
                "For slower days, a slower body and other people's hurry. Patience learned over a lifetime "
                "is a gift you can hand on.",
                "Para días más lentos, un cuerpo más lento y la prisa de los demás. La paciencia aprendida "
                "en toda una vida es un regalo que puedes dejar a otros.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "patience-1",
                "ref": "1 Timothy 1:12-17",
                "title": L(
                    "The patience God has had with you",
                    "La paciencia que Dios te ha tenido",
                ),
                "truth": L(
                    "Paul looks back on who he was: a man who insulted Jesus and hurt his followers. He says "
                    "he was shown mercy, and that Christ displayed immense patience toward him so that "
                    "others would see it and take heart. Patience in the Bible begins here, not with a "
                    "personality type or a technique. It begins with noticing how long and how kindly God "
                    "has waited for you. People who know they have been waited for find it easier to wait "
                    "for others.",
                    "Pablo mira atrás a quien fue: un hombre que insultaba a Jesús y hacía daño a sus "
                    "seguidores. Dice que recibió misericordia, y que Cristo le mostró una paciencia inmensa "
                    "para que otros la vieran y cobraran ánimo. En la Biblia la paciencia empieza aquí, no "
                    "con un tipo de personalidad ni con una técnica. Empieza al notar con cuánto tiempo y "
                    "cuánta bondad te ha esperado Dios. A quien sabe que lo han esperado le resulta más "
                    "fácil esperar a los demás.",
                ),
                "simple": L(
                    "God is very, very patient with us. He does not give up on us when we get things wrong.",
                    "Dios nos tiene muchísima paciencia. No se da por vencido con nosotros cuando nos "
                    "equivocamos.",
                ),
                "ask": L(
                    "Where has God been patient with you over years, not days? Whom in your life does that "
                    "put in a different light?",
                    "¿En qué te ha tenido Dios paciencia durante años, no días? ¿A quién de tu vida te hace "
                    "ver eso de otra manera?",
                ),
                "kid_ask": L(
                    "Who is patient with you? How do they show it?",
                    "¿Quién te tiene paciencia? ¿Cómo te lo demuestra?",
                ),
                "do": L(
                    "List three ways God has been patient with you. Tonight, read the list before you think "
                    "about the person who tried your patience today.",
                    "Haz una lista de tres maneras en que Dios te ha tenido paciencia. Esta noche léela "
                    "antes de pensar en la persona que hoy puso a prueba la tuya.",
                ),
                "kid_do": L(
                    "Say thank you to someone who was patient with you today.",
                    "Dale las gracias a alguien que hoy te tuvo paciencia.",
                ),
                "pray": L(
                    "Lord Jesus, you have waited for me longer than I have waited for anyone. Thank you. Let "
                    "your patience with me become my patience with others.",
                    "Señor Jesús, me has esperado más de lo que yo he esperado a nadie. Gracias. Que tu "
                    "paciencia conmigo se vuelva mi paciencia con los demás.",
                ),
            },
            {
                "key": "patience-2",
                "ref": "Colossians 3:12-14",
                "title": L("Patience with people", "Paciencia con la gente"),
                "truth": L(
                    "Paul writes to people who are already chosen and dearly loved by God, and tells them to "
                    "put on, like clothes each morning, a set of qualities that includes kindness, "
                    "gentleness and patience. Then he gets practical: they are to bear with one another and "
                    "forgive their complaints, as the Lord forgave them. Bearing with someone means putting "
                    "up with what annoys you without making them pay for it. Notice the order. You are not "
                    "patient in order to be loved. You are loved, and so you can afford to be patient.",
                    "Pablo escribe a personas que ya son escogidas y muy amadas por Dios, y les dice que se "
                    "pongan, como ropa cada mañana, un conjunto de cualidades que incluye la bondad, la "
                    "mansedumbre y la paciencia. Luego se pone práctico: deben soportarse unos a otros y "
                    "perdonar sus quejas, como el Señor los perdonó. Soportar a alguien es aguantar lo que "
                    "te molesta sin cobrárselo. Fíjate en el orden. No tienes paciencia para que te amen. Ya "
                    "te aman, y por eso puedes darte el lujo de tener paciencia.",
                ),
                "simple": L(
                    "God loves you, so you can be patient and kind with other people, even when they bother "
                    "you.",
                    "Dios te ama, y por eso puedes tener paciencia y ser amable con otras personas, aunque "
                    "te molesten.",
                ),
                "ask": L(
                    "Who most tests your patience right now? What specifically would bearing with them, "
                    "without making them pay, look like this week?",
                    "¿Quién pone más a prueba tu paciencia ahora? ¿Cómo sería en concreto, esta semana, "
                    "soportar a esa persona sin cobrárselo?",
                ),
                "kid_ask": L(
                    "What do you do when someone bothers you? What could you do instead?",
                    "¿Qué haces cuando alguien te molesta? ¿Qué podrías hacer en vez de eso?",
                ),
                "do": L(
                    "Choose the one person who irritates you most. Before you next see them, decide one "
                    "thing you will let pass without comment, and pray one sentence for their good.",
                    "Elige a la persona que más te irrita. Antes de volver a verla, decide una cosa que vas "
                    "a dejar pasar sin comentario, y ora una frase por su bien.",
                ),
                "kid_do": L(
                    "Next time someone bothers you, take three slow breaths before you answer.",
                    "La próxima vez que alguien te moleste, respira despacio tres veces antes de contestar.",
                ),
                "pray": L(
                    "Father, I am loved by you, and still I am short with people. Clothe me with patience "
                    "today, especially with …, and help me forgive as you forgave me.",
                    "Padre, tú me amas, y aun así pierdo la paciencia con la gente. Vísteme de paciencia "
                    "hoy, sobre todo con …, y ayúdame a perdonar como tú me perdonaste.",
                ),
            },
            {
                "key": "patience-3",
                "ref": "James 5:7-11",
                "title": L(
                    "Patience with God's timing", "Paciencia con los tiempos de Dios"
                ),
                "truth": L(
                    "James points to a farmer. The farmer does real work, but cannot make the rain fall or "
                    "hurry the crop; he waits through the seasons for what the land will give. James says to "
                    "be patient like that and to stand firm, because the Lord is coming and has not gone "
                    "missing. He also warns against turning frustration into grumbling at each other. And he "
                    "recalls Job, whose long suffering ended by showing how deeply kind and merciful the "
                    "Lord is. Waiting on God is not wasted time. Something is growing that you cannot see "
                    "yet.",
                    "Santiago señala a un agricultor. El agricultor trabaja de verdad, pero no puede hacer "
                    "llover ni apurar la cosecha; espera a lo largo de las estaciones lo que la tierra dará. "
                    "Santiago dice que tengamos esa paciencia y nos mantengamos firmes, porque el Señor "
                    "viene y no ha desaparecido. También advierte contra convertir la frustración en quejas "
                    "de unos contra otros. Y recuerda a Job, cuyo largo sufrimiento terminó mostrando lo "
                    "bondadoso y misericordioso que es el Señor. Esperar a Dios no es tiempo perdido. Está "
                    "creciendo algo que todavía no ves.",
                ),
                "simple": L(
                    "A farmer plants seeds and waits a long time for them to grow. Some good things from God "
                    "take time, and waiting is part of it.",
                    "Un agricultor siembra semillas y espera mucho tiempo a que crezcan. Algunas cosas "
                    "buenas de Dios toman tiempo, y esperar es parte de eso.",
                ),
                "ask": L(
                    "What are you waiting on God for? Where has the waiting leaked out as grumbling at the "
                    "people nearest you?",
                    "¿Qué estás esperando de Dios? ¿Dónde se te ha escapado esa espera en forma de quejas "
                    "contra quienes tienes más cerca?",
                ),
                "kid_ask": L(
                    "What is something you are waiting for? What is hard about waiting?",
                    "¿Qué cosa estás esperando? ¿Qué es lo difícil de esperar?",
                ),
                "do": L(
                    "Name the thing you are waiting for. Then ask the farmer's question: What is my part "
                    "today? Do that one part, and leave the rain to God.",
                    "Nombra lo que estás esperando. Luego hazte la pregunta del agricultor: ¿Cuál es mi "
                    "parte hoy? Haz esa parte, y deja la lluvia en manos de Dios.",
                ),
                "kid_do": L(
                    "Plant a seed or a bean in a cup with a grown-up. Water it and watch how slowly it grows.",
                    "Siembra una semilla o un frijol en un vasito con un adulto. Riégalo y mira qué despacio "
                    "crece.",
                ),
                "pray": L(
                    "Lord, I am tired of waiting for … I cannot make it rain. Keep me steady, keep me from "
                    "grumbling, and help me trust that you are kind.",
                    "Señor, me cansa esperar … No puedo hacer que llueva. Mantenme firme, líbrame de la "
                    "queja y ayúdame a confiar en que eres bueno.",
                ),
            },
            {
                "key": "patience-4",
                "ref": "Philippians 3:12-14",
                "title": L("Patience with yourself", "Paciencia contigo"),
                "truth": L(
                    "Paul, after many years of following Jesus, says plainly that he has not arrived and is "
                    "not yet what he will be. He is not crushed by that, and he does not use it as an "
                    "excuse. He lets go of what is behind him and keeps moving toward what is ahead, because "
                    "Christ has already taken hold of him. Being patient with yourself is not lowering the "
                    "standard. It is accepting that growth takes a lifetime, getting up again without "
                    "self-contempt, and taking the next step.",
                    "Pablo, después de muchos años siguiendo a Jesús, dice con claridad que no ha llegado y "
                    "que todavía no es lo que será. Eso no lo aplasta, ni lo usa de excusa. Suelta lo que "
                    "queda atrás y sigue avanzando hacia lo que está adelante, porque Cristo ya lo alcanzó a "
                    "él. Tenerte paciencia no es exigirte menos. Es aceptar que crecer toma toda la vida, "
                    "levantarte otra vez sin despreciarte y dar el siguiente paso.",
                ),
                "simple": L(
                    "Nobody is finished growing, not even grown-ups. When you make a mistake, you can get up "
                    "and try again. God is still helping you.",
                    "Nadie ha terminado de crecer, ni siquiera los adultos. Cuando te equivocas, puedes "
                    "levantarte e intentarlo otra vez. Dios te sigue ayudando.",
                ),
                "ask": L(
                    "How do you speak to yourself after you fail at something you thought you had outgrown? "
                    "What would Paul's attitude sound like in your own words?",
                    "¿Cómo te hablas después de fallar en algo que creías superado? ¿Cómo sonaría la actitud "
                    "de Pablo dicha con tus palabras?",
                ),
                "kid_ask": L(
                    "What is something you are still learning to do? Who helps you keep trying?",
                    "¿Qué cosa todavía estás aprendiendo a hacer? ¿Quién te ayuda a seguir intentándolo?",
                ),
                "do": L(
                    "Pick one area where you are discouraged about your progress. Write one thing to leave "
                    "behind and one small next step, and take that step today.",
                    "Elige un área en la que tu avance te desanima. Escribe una cosa para dejar atrás y un "
                    "pequeño paso siguiente, y da ese paso hoy.",
                ),
                "kid_do": L(
                    "Try again today at something that is hard for you, and say: I am still learning.",
                    "Hoy vuelve a intentar algo que te cuesta, y di: Todavía estoy aprendiendo.",
                ),
                "pray": L(
                    "Jesus, I am not who I hoped to be by now. You have taken hold of me and you are not "
                    "finished. Help me leave behind what is behind and take the next step.",
                    "Jesús, no soy quien esperaba ser a estas alturas. Tú me tienes en tus manos y no has "
                    "terminado. Ayúdame a soltar lo que quedó atrás y a dar el siguiente paso.",
                ),
            },
        ],
    },
    {
        "key": "hope",
        "category": "character",
        "title": L("Hope", "Esperanza"),
        "summary": L(
            "For anyone who finds it hard to expect anything good. Four readings on a hope that is more "
            "than optimism: a steady expectation of good, resting on who God is and what he has "
            "promised.",
            "Para quien le cuesta esperar algo bueno. Cuatro lecturas sobre una esperanza que es más "
            "que optimismo: una expectativa firme del bien, apoyada en quién es Dios y en lo que ha "
            "prometido.",
        ),
        "keywords": [
            "hope",
            "discourag",
            "future",
            "weary",
            "bleak",
            "pointless",
            "optimis",
            "expect",
            "esperanza",
            "desesperanz",
            "desanim",
            "desalent",
            "futuro",
            "agotad",
            "sin sentido",
            "ilusión",
        ],
        "situations": [
            "grieving",
            "ill",
            "job_seeking",
            "caregiver",
            "moving",
            "recovery",
        ],
        "traits": ["hope", "perseverance", "trust"],
        "stages": ["teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "teen": L(
                "When the future looks dark or just blank, hope is not pretending. It is trusting that God "
                "is good and is not done.",
                "Cuando el futuro se ve oscuro o simplemente en blanco, tener esperanza no es fingir. Es "
                "confiar en que Dios es bueno y no ha terminado.",
            ),
            "young_adult": L(
                "For when plans fall through and the world's news is heavy. Hope rests on something "
                "sturdier than how things look.",
                "Para cuando los planes se caen y las noticias del mundo pesan. La esperanza se apoya en "
                "algo más firme que las apariencias.",
            ),
            "adult": L(
                "For the long middle, when you are tired and little seems to change. Hope gives strength "
                "for today, not only for someday.",
                "Para el largo trecho de en medio, cuando hay cansancio y poco parece cambiar. La "
                "esperanza da fuerza para hoy, no solo para algún día.",
            ),
            "senior": L(
                "For when there is more road behind than ahead. Christian hope reaches further than this "
                "life, and it holds.",
                "Para cuando hay más camino atrás que adelante. La esperanza cristiana llega más allá de "
                "esta vida, y sostiene.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "hope-1",
                "ref": "Romans 5:1-5",
                "title": L("More than optimism", "Más que optimismo"),
                "truth": L(
                    "Optimism says things will probably turn out fine. Hope, as Paul describes it, rests on "
                    "something else: through Jesus we have peace with God and stand in his favor. That is "
                    "why Paul can say hardship is not the end of hope but one of the places it grows, as "
                    "endurance forms character and character deepens hope. And this hope will not let us "
                    "down, because God has already poured his love into our hearts by the Holy Spirit. It "
                    "rests on what God has done, not on how things look.",
                    "El optimismo dice que probablemente todo saldrá bien. La esperanza, como la describe "
                    "Pablo, se apoya en otra cosa: por medio de Jesús tenemos paz con Dios y vivimos en su "
                    "favor. Por eso Pablo puede decir que la dificultad no es el fin de la esperanza, sino "
                    "uno de los lugares donde crece: la constancia forma el carácter, y el carácter hace más "
                    "honda la esperanza. Y esta esperanza no nos va a fallar, porque Dios ya derramó su amor "
                    "en nuestro corazón por el Espíritu Santo. Se apoya en lo que Dios ha hecho, no en cómo "
                    "se ven las cosas.",
                ),
                "simple": L(
                    "Hope means trusting that God is good and will take care of us, even when today is hard.",
                    "Tener esperanza es confiar en que Dios es bueno y nos va a cuidar, aunque hoy sea un "
                    "día difícil.",
                ),
                "ask": L(
                    "Is what you call hope closer to optimism about circumstances or to confidence in God? "
                    "What is it actually resting on?",
                    "Lo que llamas esperanza, ¿se parece más al optimismo sobre las circunstancias o a la "
                    "confianza en Dios? ¿En qué se apoya realmente?",
                ),
                "kid_ask": L(
                    "What is something good you are looking forward to?",
                    "¿Qué cosa buena estás esperando con ganas?",
                ),
                "do": L(
                    "Write two short lists: what I hope will happen, and what I know about God. Underline "
                    "one item in the second list and carry it with you today.",
                    "Escribe dos listas cortas: lo que espero que pase, y lo que sé de Dios. Subraya una "
                    "cosa de la segunda lista y llévala contigo hoy.",
                ),
                "kid_do": L(
                    "Tell a grown-up one thing you know about God that makes you feel safe.",
                    "Cuéntale a un adulto una cosa que sabes de Dios y que te da seguridad.",
                ),
                "pray": L(
                    "God, I cannot promise myself that things will turn out as I want. Thank you that I have "
                    "peace with you through Jesus. Pour your love into my heart again today.",
                    "Dios, no puedo prometerme que las cosas saldrán como quiero. Gracias porque tengo paz "
                    "contigo por medio de Jesús. Derrama hoy otra vez tu amor en mi corazón.",
                ),
            },
            {
                "key": "hope-2",
                "ref": "Hebrews 6:17-20",
                "title": L("An anchor", "Un ancla"),
                "truth": L(
                    "The writer says God wanted to make it very clear that his purpose does not change, so "
                    "he backed his promise with an oath. God cannot lie, and that gives strong encouragement "
                    "to people who have run to him for safety. This hope is called an anchor for the soul, "
                    "one that holds. An anchor does not stop the storm or the waves; it keeps the boat from "
                    "drifting. And this anchor is fastened in the very presence of God, where Jesus has gone "
                    "ahead of us.",
                    "El autor dice que Dios quiso dejar muy claro que su propósito no cambia, y por eso "
                    "respaldó su promesa con un juramento. Dios no puede mentir, y eso da un ánimo fuerte a "
                    "quienes han corrido a refugiarse en él. A esta esperanza la llama un ancla para el "
                    "alma, un ancla que aguanta. Un ancla no detiene la tormenta ni las olas; impide que el "
                    "barco se vaya a la deriva. Y esta ancla está sujeta en la presencia misma de Dios, "
                    "adonde Jesús entró antes que nosotros.",
                ),
                "simple": L(
                    "An anchor keeps a boat from floating away in a storm. God's promises are like an anchor "
                    "for us. God always keeps his word.",
                    "Un ancla evita que la tormenta se lleve el barco. Las promesas de Dios son como un "
                    "ancla para nosotros. Dios siempre cumple su palabra.",
                ),
                "ask": L(
                    "What tends to set you adrift: bad news, a mood, a comparison? Which promise of God "
                    "could you fasten yourself to when that happens?",
                    "¿Qué suele dejarte a la deriva: una mala noticia, un estado de ánimo, una comparación? "
                    "¿A qué promesa de Dios podrías amarrarte cuando eso pase?",
                ),
                "kid_ask": L(
                    "What helps you feel steady when you are scared or upset?",
                    "¿Qué te ayuda a sentir calma cuando tienes miedo o algo te molesta?",
                ),
                "do": L(
                    "Choose one promise of God you know, such as his presence or his forgiveness. Write it "
                    "on a card and read it whenever today starts to pull you off course.",
                    "Elige una promesa de Dios que conozcas, como su presencia o su perdón. Escríbela en una "
                    "tarjeta y léela cada vez que el día empiece a sacarte de rumbo.",
                ),
                "kid_do": L(
                    "Draw a boat with an anchor. Next to the anchor write: God keeps his promises.",
                    "Dibuja un barco con un ancla. Junto al ancla escribe: Dios cumple sus promesas.",
                ),
                "pray": L(
                    "God, you do not lie and you do not go back on your promises. I am holding on to you. "
                    "Hold on to me when the waves are high.",
                    "Dios, tú no mientes ni te retractas de tus promesas. Me aferro a ti. Sujétame cuando "
                    "las olas estén altas.",
                ),
            },
            {
                "key": "hope-3",
                "ref": "1 Peter 1:3-9",
                "title": L("A living hope", "Una esperanza viva"),
                "truth": L(
                    "Peter says that God, in his great mercy, has given us a new birth into a living hope, "
                    "and he names the reason: Jesus rose from the dead. Because of that, there is an "
                    "inheritance kept safe where nothing can ruin it. Peter does not hide that his readers "
                    "are suffering trials of many kinds right now. He says both things are true together: "
                    "real sorrow for a while, and a future that cannot be taken. Christian hope is alive "
                    "because the one it depends on is alive.",
                    "Pedro dice que Dios, por su gran misericordia, nos hizo nacer de nuevo a una esperanza "
                    "viva, y da la razón: Jesús resucitó de entre los muertos. Por eso hay una herencia "
                    "guardada donde nada puede dañarla. Pedro no esconde que sus lectores están sufriendo "
                    "ahora mismo pruebas de muchas clases. Dice que las dos cosas son verdad a la vez: una "
                    "tristeza real por un tiempo, y un futuro que nadie puede quitar. La esperanza cristiana "
                    "está viva porque aquel de quien depende está vivo.",
                ),
                "simple": L(
                    "Jesus is alive, so our hope is alive too. God is keeping something wonderful safe for "
                    "us, and no one can take it.",
                    "Jesús está vivo, y por eso nuestra esperanza también está viva. Dios nos guarda algo "
                    "maravilloso, y nadie puede quitárnoslo.",
                ),
                "ask": L(
                    "Peter holds grief and hope in the same sentence. Where in your life do you need "
                    "permission to feel both?",
                    "Pedro pone el dolor y la esperanza en la misma frase. ¿En qué parte de tu vida "
                    "necesitas permiso para sentir las dos cosas?",
                ),
                "kid_ask": L(
                    "Can you feel sad and still know something good is coming? When has that happened?",
                    "¿Puedes sentir tristeza y saber al mismo tiempo que viene algo bueno? ¿Cuándo te ha "
                    "pasado?",
                ),
                "do": L(
                    "Say both halves aloud today: This is hard, and: Jesus is alive. If the hard part is very "
                    "heavy or has lasted a long time, tell a trusted person, and consider talking with a "
                    "pastor, doctor or counselor.",
                    "Hoy di en voz alta las dos mitades: Esto es difícil, y: Jesús está vivo. Si la parte "
                    "difícil pesa mucho o lleva mucho tiempo, cuéntaselo a alguien de confianza, y considera "
                    "hablar con un pastor, un médico o un consejero.",
                ),
                "kid_do": L(
                    "Say out loud: Jesus is alive, so there is always hope.",
                    "Di en voz alta: Jesús está vivo, así que siempre hay esperanza.",
                ),
                "pray": L(
                    "Father, thank you for a hope that is alive because Jesus is. I am hurting over … Keep "
                    "my faith through this, and keep my eyes on what cannot be taken.",
                    "Padre, gracias por una esperanza que está viva porque Jesús lo está. Me duele … Guarda "
                    "mi fe en medio de esto, y mantén mis ojos en lo que nadie puede quitar.",
                ),
            },
            {
                "key": "hope-4",
                "ref": "Isaiah 40:27-31",
                "title": L("Strength for the tired", "Fuerza para el cansancio"),
                "truth": L(
                    "God's people were saying that he had lost sight of them and no longer cared about their "
                    "case. Isaiah answers by reminding them who God is: the everlasting Creator, who does "
                    "not get tired and whose understanding has no limit. This God gives strength to the worn "
                    "out. Even the young and strong give out eventually, but those who put their hope in the "
                    "Lord find their strength renewed: sometimes to soar, sometimes to run, and sometimes "
                    "simply to keep walking without collapsing. Hope is where the strength for today comes "
                    "from.",
                    "El pueblo de Dios decía que él los había perdido de vista y ya no le importaba su "
                    "causa. Isaías responde recordándoles quién es Dios: el Creador eterno, que no se cansa "
                    "y cuyo entendimiento no tiene límite. Este Dios da fuerza a los agotados. Hasta los "
                    "jóvenes y fuertes se rinden tarde o temprano, pero quienes ponen su esperanza en el "
                    "Señor ven renovadas sus fuerzas: a veces para volar, a veces para correr, y a veces "
                    "simplemente para seguir caminando sin caer. De la esperanza sale la fuerza para hoy.",
                ),
                "simple": L(
                    "God never gets tired. When we are tired and trust him, he gives us new strength, like "
                    "an eagle flying high.",
                    "Dios nunca se cansa. Cuando ya no tenemos fuerzas y confiamos en él, nos da fuerzas "
                    "nuevas, como un águila que vuela alto.",
                ),
                "ask": L(
                    "Have you felt that God has lost sight of you? Which do you need strength for right now: "
                    "to soar, to run, or just to keep walking?",
                    "¿Has sentido que Dios te perdió de vista? ¿Para qué necesitas fuerza ahora: para volar, "
                    "para correr o solo para seguir caminando?",
                ),
                "kid_ask": L(
                    "When do you feel very tired? Who helps you then?",
                    "¿Cuándo sientes mucho cansancio? ¿Quién te ayuda entonces?",
                ),
                "do": L(
                    "Tell God plainly where you are worn out. Then choose the one next step that counts as "
                    "walking today, do only that, and let it be enough.",
                    "Dile a Dios con claridad dónde ya no puedes más. Luego elige el único paso que hoy "
                    "cuenta como caminar, haz solo eso, y deja que sea suficiente.",
                ),
                "kid_do": L(
                    "Stretch out your arms like eagle wings and say: God, give me strength today.",
                    "Abre los brazos como alas de águila y di: Dios, dame fuerzas hoy.",
                ),
                "pray": L(
                    "Everlasting God, you do not grow tired, and I do. I feel unseen in … I put my hope in "
                    "you. Renew my strength enough for today's walk.",
                    "Dios eterno, tú no te cansas, y yo sí. Siento que nadie me ve en … Pongo mi esperanza "
                    "en ti. Renueva mis fuerzas lo suficiente para el camino de hoy.",
                ),
            },
        ],
    },
    {
        "key": "joy",
        "category": "character",
        "title": L("Joy", "Gozo"),
        "summary": L(
            "For anyone who wonders where their joy went, or whether joy is even allowed in a hard "
            "season. Four readings on a gladness deeper than happiness, one that comes from God and can "
            "live alongside sorrow.",
            "Para quien se pregunta adónde se fue su alegría, o si se puede tener gozo en una temporada "
            "difícil. Cuatro lecturas sobre una alegría más honda que la felicidad, que viene de Dios y "
            "puede convivir con la tristeza.",
        ),
        "keywords": [
            "joy",
            "happy",
            "happiness",
            "delight",
            "celebrat",
            "rejoic",
            "numb",
            "glad",
            "gozo",
            "alegr",
            "feliz",
            "felicidad",
            "celebr",
            "regocij",
            "content",
            "apagad",
        ],
        "situations": [],
        "traits": ["joy", "gratitude", "contentment"],
        "stages": ["child", "teen", "young_adult", "adult", "senior"],
        "stage_notes": {
            "child": L(
                "Joy is a deep-down gladness that comes from knowing God loves you. You can have it even "
                "on a not-so-fun day.",
                "El gozo es una alegría muy adentro que viene de saber que Dios te ama. Puedes tenerla "
                "incluso en un día no tan divertido.",
            ),
            "teen": L(
                "Happiness comes and goes with how the day went. Joy goes deeper, and it does not require "
                "you to fake a smile.",
                "La felicidad va y viene según cómo te fue en el día. El gozo es más profundo, y no te "
                "exige fingir una sonrisa.",
            ),
            "young_adult": L(
                "For when the things that were supposed to make you happy have not, and you are looking "
                "for something that lasts.",
                "Para cuando lo que se suponía que te haría feliz no lo ha logrado, y buscas algo que "
                "dure.",
            ),
            "adult": L(
                "For busy, heavy years when joy feels like a luxury. It is closer to a source of strength "
                "than a reward for finishing.",
                "Para años ocupados y pesados en que el gozo parece un lujo. Se parece más a una fuente de "
                "fuerza que a un premio por terminar.",
            ),
            "senior": L(
                "Joy and sorrow have both been part of your road. Here is a joy that does not depend on "
                "health or circumstances.",
                "La alegría y la tristeza han sido parte de tu camino. Aquí hay un gozo que no depende de "
                "la salud ni de las circunstancias.",
            ),
        },
        "sensitive": False,
        "lessons": [
            {
                "key": "joy-1",
                "ref": "John 15:9-11",
                "title": L("Where joy comes from", "De dónde viene el gozo"),
                "truth": L(
                    "Hours before his arrest, Jesus talks about joy. He tells his friends that he has loved "
                    "them the way the Father has loved him, and asks them to stay in that love by living as "
                    "he taught. He says he is telling them this so that his own joy will be in them and "
                    "their joy will be full. Joy, then, is not a mood you work up. It is something of Jesus' "
                    "own that he shares, and it comes from living inside a love that is not in question.",
                    "Horas antes de que lo arresten, Jesús habla de gozo. Les dice a sus amigos que los ha "
                    "amado como el Padre lo ha amado a él, y les pide que permanezcan en ese amor viviendo "
                    "como él enseñó. Dice que les cuenta esto para que su propio gozo esté en ellos y el "
                    "gozo de ellos sea completo. El gozo, entonces, no es un ánimo que uno se fabrica. Es "
                    "algo del mismo Jesús que él comparte, y nace de vivir dentro de un amor que no está en "
                    "duda.",
                ),
                "simple": L(
                    "Jesus loves you, and he wants to share his own joy with you. Joy grows when we stay "
                    "close to him.",
                    "Jesús te ama y quiere compartir contigo su propia alegría. La alegría crece cuando nos "
                    "quedamos cerca de él.",
                ),
                "ask": L(
                    "What do you usually depend on for joy? How is that different from staying in the love "
                    "of Jesus?",
                    "¿De qué sueles depender para tener alegría? ¿En qué se diferencia eso de permanecer en "
                    "el amor de Jesús?",
                ),
                "kid_ask": L(
                    "What makes you feel really glad inside?",
                    "¿Qué te da mucha alegría por dentro?",
                ),
                "do": L(
                    "Set aside five minutes today to do nothing but remember that you are loved by Jesus. Do "
                    "not ask for anything. Notice what you feel afterward, without forcing it.",
                    "Aparta hoy cinco minutos solo para recordar que Jesús te ama. No pidas nada. Observa lo "
                    "que sientes después, sin forzarlo.",
                ),
                "kid_do": L(
                    "Sing a song you like to God, or hum it, just because he loves you.",
                    "Cántale a Dios una canción que te guste, o tararéala, solo porque él te ama.",
                ),
                "pray": L(
                    "Jesus, I have looked for joy in many places. Keep me in your love today, and let your "
                    "joy be in me, whatever kind of day this is.",
                    "Jesús, he buscado la alegría en muchos lugares. Mantenme en tu amor hoy, y que tu gozo "
                    "esté en mí, sea como sea este día.",
                ),
            },
            {
                "key": "joy-2",
                "ref": "Nehemiah 8:9-12",
                "title": L("Joy that gives strength", "Un gozo que da fuerzas"),
                "truth": L(
                    "The people had gathered to hear God's teaching read aloud and explained, and as they "
                    "listened they began to weep. Their leaders told them the day was holy and not for "
                    "mourning: they were to go, eat good food and share it with those who had nothing ready, "
                    "because the gladness that comes from the Lord would be their strength. So they "
                    "celebrated together, because they had understood what was read to them. Joy here is not "
                    "ignoring what is wrong. It is strength received from God, and it spills over into "
                    "sharing.",
                    "El pueblo se había reunido para oír la enseñanza de Dios leída en voz alta y explicada, "
                    "y mientras escuchaban empezaron a llorar. Sus líderes les dijeron que ese día era santo "
                    "y no para estar de luto: que fueran, comieran bien y compartieran con quienes no tenían "
                    "nada preparado, porque la alegría que viene del Señor sería su fuerza. Así que "
                    "celebraron juntos, porque habían entendido lo que se les leyó. Aquí el gozo no es "
                    "ignorar lo que está mal. Es fuerza recibida de Dios, y se desborda en compartir.",
                ),
                "simple": L(
                    "God's people had a big happy meal together and shared their food with those who had "
                    "none. Joy from God makes us strong.",
                    "El pueblo de Dios tuvo una gran comida alegre y compartió con los que no tenían. La "
                    "alegría que viene de Dios nos hace fuertes.",
                ),
                "ask": L(
                    "Do you treat joy as a reward for when everything is done and fixed? What would it mean "
                    "to receive it now, as strength for what is not?",
                    "¿Tratas el gozo como un premio para cuando todo esté hecho y arreglado? ¿Qué "
                    "significaría recibirlo ahora, como fuerza para lo que aún no lo está?",
                ),
                "kid_ask": L(
                    "What is your favorite thing to celebrate? Who do you like to share it with?",
                    "¿Qué es lo que más te gusta celebrar? ¿Con quién te gusta compartirlo?",
                ),
                "do": L(
                    "Plan one small celebration of God's goodness this week, a meal, a dessert or a walk, "
                    "and include someone who would otherwise be left out.",
                    "Planea esta semana una pequeña celebración de la bondad de Dios, una comida, un postre "
                    "o una caminata, e incluye a alguien que de otro modo quedaría fuera.",
                ),
                "kid_do": L(
                    "Share a snack or a treat with someone today and tell them: God is good!",
                    "Hoy comparte una merienda o un dulce con alguien y dile: ¡Dios es bueno!",
                ),
                "pray": L(
                    "Lord, I often feel I have not earned the right to be glad. Thank you that your joy is a "
                    "gift and a strength. Show me who to share it with.",
                    "Señor, a menudo siento que no me he ganado el derecho a alegrarme. Gracias porque tu "
                    "gozo es regalo y es fuerza. Muéstrame con quién compartirlo.",
                ),
            },
            {
                "key": "joy-3",
                "ref": "Habakkuk 3:17-19",
                "title": L(
                    "Joy when the fields are empty",
                    "Gozo cuando los campos están vacíos",
                ),
                "truth": L(
                    "Habakkuk imagines the worst case for a farming people: no figs, no grapes, no olives, "
                    "no grain, no animals left in the pens. And then he says that even so he will rejoice in "
                    "the Lord. This is not cheerfulness, and he is not pretending the loss does not hurt. He "
                    "is saying that his joy rests on God himself, who is still his rescuer and his strength "
                    "when everything else is gone. Joy and sorrow can be in the same heart at once. One does "
                    "not cancel the other.",
                    "Habacuc imagina lo peor para un pueblo que vive del campo: sin higos, sin uvas, sin "
                    "aceitunas, sin grano, sin animales en los corrales. Y entonces dice que aun así se "
                    "alegrará en el Señor. Esto no es buen humor, ni está fingiendo que la pérdida no duele. "
                    "Está diciendo que su gozo se apoya en Dios mismo, que sigue siendo su salvador y su "
                    "fuerza cuando todo lo demás falta. El gozo y la tristeza pueden estar en el mismo "
                    "corazón a la vez. Uno no anula a la otra.",
                ),
                "simple": L(
                    "Even when things go wrong, God is still with us and still good. We can be glad about "
                    "God even on a sad day.",
                    "Aunque las cosas salgan mal, Dios sigue con nosotros y sigue siendo bueno. Podemos "
                    "alegrarnos por Dios incluso en un día triste.",
                ),
                "ask": L(
                    "What are the empty fields in your life right now? Without pretending they are full, "
                    "what about God himself can you still be glad of?",
                    "¿Cuáles son los campos vacíos de tu vida ahora? Sin fingir que están llenos, ¿de qué "
                    "puedes alegrarte todavía en Dios mismo?",
                ),
                "kid_ask": L(
                    "What is something about God that is still true on a bad day?",
                    "¿Qué cosa de Dios sigue siendo verdad en un día malo?",
                ),
                "do": L(
                    "Write your own version: Though … and though …, I will still be glad in God, because … "
                    "Put the truth in the first part and something specific in the last. If the losses are "
                    "heavy, share what you wrote with someone you trust.",
                    "Escribe tu propia versión: Aunque … y aunque …, igual me alegraré en Dios, porque … Pon "
                    "la verdad en la primera parte y algo concreto en la última. Si las pérdidas pesan, "
                    "comparte lo que escribiste con alguien de confianza.",
                ),
                "kid_do": L(
                    "Tell God one sad thing and one thing you are glad about. Both are okay to say.",
                    "Cuéntale a Dios una cosa triste y una cosa que te alegra. Las dos se pueden decir.",
                ),
                "pray": L(
                    "Lord, a lot is missing right now: … I will not pretend otherwise. Still, you are my "
                    "strength, and I choose to be glad in you.",
                    "Señor, ahora mismo faltan muchas cosas: … No voy a fingir lo contrario. Aun así, tú "
                    "eres mi fuerza, y elijo alegrarme en ti.",
                ),
            },
            {
                "key": "joy-4",
                "ref": "John 16:20-22",
                "title": L("Joy no one can take", "Un gozo que nadie puede quitar"),
                "truth": L(
                    "Jesus tells his friends honestly that they are about to weep while others celebrate. He "
                    "does not promise to spare them grief; he promises that their grief will turn into joy. "
                    "He compares it to a mother in labor, whose pain is real but gives way to gladness when "
                    "her child is born. He was speaking of his death and of seeing them again after he rose. "
                    "For those who follow him the pattern holds: sorrow is real and it is not the end, and "
                    "the joy he gives cannot be taken away by anyone.",
                    "Jesús les dice con honestidad a sus amigos que están por llorar mientras otros "
                    "celebran. No promete ahorrarles el dolor; promete que su tristeza se convertirá en "
                    "alegría. Lo compara con una madre que da a luz: su dolor es real, pero deja paso a la "
                    "alegría cuando nace su hijo. Hablaba de su muerte y de volver a verlos después de "
                    "resucitar. Para quienes lo siguen, el patrón se mantiene: la tristeza es real y no es "
                    "el final, y el gozo que él da no se lo puede quitar nadie.",
                ),
                "simple": L(
                    "Jesus said sad times do not last forever. He turns sadness into joy, and no one can "
                    "take that joy away.",
                    "Jesús dijo que los tiempos tristes no duran para siempre. Él convierte la tristeza en "
                    "alegría, y nadie puede quitarnos esa alegría.",
                ),
                "ask": L(
                    "Jesus does not say sorrow is replaced by joy but that it turns into joy. Have you seen "
                    "that happen, even partly? Where are you still waiting for it?",
                    "Jesús no dice que la tristeza es reemplazada por la alegría, sino que se convierte en "
                    "alegría. ¿Lo has visto suceder, aunque sea en parte? ¿Dónde lo sigues esperando?",
                ),
                "kid_ask": L(
                    "Can you remember a time when you were sad and then felt happy again? What changed?",
                    "¿Recuerdas una vez que sentías tristeza y luego volvió la alegría? ¿Qué cambió?",
                ),
                "do": L(
                    "Tonight, write down one sorrow you are carrying and one joy that no circumstance has "
                    "been able to take from you. Thank God for the second while staying honest about the "
                    "first.",
                    "Esta noche anota una tristeza que cargas y una alegría que ninguna circunstancia ha "
                    "podido quitarte. Da gracias a Dios por la segunda sin dejar de decir la verdad sobre la "
                    "primera.",
                ),
                "kid_do": L(
                    "Give someone who is sad a hug or a drawing today, to share some joy.",
                    "Hoy dale un abrazo o un dibujo a alguien que esté triste, para compartirle alegría.",
                ),
                "pray": L(
                    "Jesus, you never told me I would not weep. You promised that sorrow is not the end. "
                    "Turn my grief toward joy in your time, and keep safe the joy you have given.",
                    "Jesús, nunca me dijiste que no lloraría. Prometiste que la tristeza no es el final. "
                    "Lleva mi dolor hacia la alegría a tu tiempo, y guarda el gozo que me has dado.",
                ),
            },
        ],
    },
]
