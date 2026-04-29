"""
Management command to seed curated reading plans.
Based on study Bible reading plans.
"""

from django.core.management.base import BaseCommand

from apps.plans.models import ReadingPlan, ReadingPlanDay


class Command(BaseCommand):
    help = "Seed curated reading plans"

    def handle(self, *args, **options):
        self.stdout.write("Seeding reading plans...")

        self.create_30_days_walk_with_christ()
        self.create_60_day_overview()
        self.create_30_famous_battles()
        self.create_not_so_famous_stories()

        self.stdout.write(self.style.SUCCESS("Successfully seeded reading plans"))

    def create_30_days_walk_with_christ(self):
        plan, created = ReadingPlan.objects.get_or_create(
            title_en="30 Days for Beginning Your Walk with Christ",
            defaults={
                "description_en": "A month-long journey through essential passages for new believers and those wanting to strengthen their faith foundation.",
                "duration_days": 30,
                "category": "faith",
                "is_premium": False,
            },
        )

        if not created:
            self.stdout.write(f'Plan "{plan.title_en}" already exists, skipping...')
            return

        days = [
            (1, "The Fall of Humanity", "Genesis 3:1-19"),
            (2, "A People for God", "Genesis 28:10-15; 32:22-28"),
            (3, "The Ten Commandments", "Exodus 20:1-17"),
            (4, "Sacrifices Required Under Law", "Leviticus 5:14-19"),
            (5, "Sacrifices Required Under Law", "Leviticus 20:1-17"),
            (6, "Punishments for Sin Under Law", "Deuteronomy 20:7-21"),
            (7, "Obedience from Love", "Deuteronomy 11:13-21"),
            (8, "Cycles of Disobedience", "Judges 2:10-19"),
            (9, "The People Demand a King", "1 Samuel 8"),
            (10, "Saul Fails and Is Rejected", "1 Samuel 15:17-23"),
            (11, "Many Kings Fail", "Jeremiah 1:1-17"),
            (12, "The Sin of the People", "Ezekiel 20:1-26"),
            (13, "An Eternal King Promised", "Isaiah 9:6-7; Zechariah 9:9-10"),
            (14, "The Promised King Is Born", "Luke 2:1-20"),
            (15, "The Word Became Flesh", "John 1:1-18"),
            (16, "Signs and Miracles of Authority", "Matthew 9:1-8; Luke 13:10-17"),
            (17, "Jesus Fulfills the Law", "Matthew 5:17-20; Romans 8:1-4"),
            (18, "Jesus Teaches About New Life", "John 3"),
            (19, "Jesus Willingly Taken", "John 18:1-11"),
            (20, "Christ's Death and Resurrection", "Luke 23:44-24:12"),
            (21, "Christ a Sacrifice for All", "Hebrews 9:11-10:18"),
            (22, "God's Wrath Explained", "Romans 1:18-32"),
            (23, "God's Judgment Explained", "Romans 2:5-11"),
            (24, "Righteousness by Faith", "Romans 3:9-26"),
            (25, "Life Through Christ", "Romans 5:12-21"),
            (26, "Life by the Spirit", "Romans 8:1-17; Galatians 5:16-26"),
            (27, "Living Sacrifices", "Romans 12"),
            (28, "Walking in the Light", "1 John 1-2"),
            (29, "Living for God", "1 Peter 5:1-11"),
            (30, "Promise of Eternity", "2 Corinthians 5:1-10; Revelation 21:1-4"),
        ]

        for day_num, theme, passages in days:
            ReadingPlanDay.objects.create(
                plan=plan,
                day_number=day_num,
                theme_en=theme,
                passages=passages.split("; ") if "; " in passages else [passages],
            )

        self.stdout.write(f"Created plan: {plan.title_en}")

    def create_60_day_overview(self):
        plan, created = ReadingPlan.objects.get_or_create(
            title_en="60-Day Overview of the Bible",
            defaults={
                "description_en": "Journey through the entire Bible in 60 days, covering major themes and stories from Genesis to Revelation.",
                "duration_days": 60,
                "category": "general",
                "is_premium": False,
            },
        )

        if not created:
            self.stdout.write(f'Plan "{plan.title_en}" already exists, skipping...')
            return

        days = [
            (1, "In the Beginning", "Genesis 1:1-2:25"),
            (2, "Sin Enters the Picture", "Genesis 3:1-24"),
            (3, "Water, Water Everywhere", "Genesis 6:1-9:29"),
            (4, "God's Promise to Abraham", "Genesis 12:1-18:15"),
            (5, "Goodbye, Sodom and Gomorrah", "Genesis 18:16-19:29"),
            (6, "Isaac Loves Rebekah", "Genesis 24:1-67"),
            (7, "Jacob's Brothers", "Genesis 25:19-34; 27:1-33:20"),
            (8, "Joseph's Egyptian Adventure", "Genesis 37:1-36; 39:1-50:26"),
            (9, "A Man Named Moses", "Exodus 1:1-4:31"),
            (10, "Escape From Egypt", "Exodus 5:22-14:31"),
            (11, "Life in the Wilderness", "Exodus 15:22-18:27"),
            (12, "Ten Commandments", "Exodus 19:1-21"),
            (13, "Calf Worship", "Exodus 32:1-35"),
            (14, "Assessment From God", "Numbers 33:1-10:38"),
            (15, "Moses Loses His Cool", "Numbers 20:1-13"),
            (16, "Joshua Takes Command", "Joshua 1:1-24"),
            (17, "Destination: Promised Land", "Joshua 8:1-8:35"),
            (18, "Gideon, the Reluctant Leader", "Judges 6:1-8:35"),
            (19, "The Weak Strong Man", "Judges 13:1-16:31"),
            (20, "Calling Samuel", "1 Samuel 1:1-3:21"),
            (21, "Israel Gets Its King", "1 Samuel 8:1-11:15"),
            (22, "David Versus Goliath", "1 Samuel 17:1-58"),
            (23, "King David", "2 Samuel 1:1-8:14"),
            (24, "Wise Guy", "1 Kings 1:1-4:34"),
            (25, "Elijah and the Battle Royale", "1 Kings 17:1-19:18"),
            (26, "The Exile of Israel", "2 Kings 17:1-41"),
            (27, "The Fall of Jerusalem", "2 Kings 25:1-30"),
            (28, "Return to Jerusalem", "Ezra 1:1-7:3"),
            (29, "Rebuilding the Walls", "Nehemiah 1:1-6:19"),
            (30, "Esther Saves Her People", "Esther 2:1-8:17"),
            (31, "Job, the Noble Sufferer", "Job 1:1-2:10; 42:1-17"),
            (32, "The Shepherd's Psalm", "Psalm 23:1-6"),
            (33, "Proverbs of Wisdom", "Proverbs 1:1-9:18"),
            (34, "The Preacher", "Ecclesiastes 1:1-12:14"),
            (35, "Song of Love", "Song of Solomon 1:1-8:14"),
            (36, "Isaiah's Vision", "Isaiah 1:1-6:13"),
            (37, "The Suffering Servant", "Isaiah 52:13-53:12"),
            (38, "Jeremiah's Call", "Jeremiah 1:1-3:5"),
            (39, "Valley of Dry Bones", "Ezekiel 37:1-14"),
            (40, "Daniel in Babylon", "Daniel 1:1-6:28"),
            (41, "Jonah and the Fish", "Jonah 1:1-4:11"),
            (42, "Micah's Message", "Micah 6:1-8"),
            (43, "The Birth of Jesus", "Matthew 1:18-2:23; Luke 2:1-20"),
            (44, "Jesus' Baptism and Temptation", "Matthew 3:1-4:11"),
            (45, "Sermon on the Mount", "Matthew 5:1-7:29"),
            (46, "Jesus' Miracles", "Matthew 8:1-9:38"),
            (47, "Parables of the Kingdom", "Matthew 13:1-58"),
            (48, "Peter's Confession", "Matthew 16:13-28"),
            (49, "The Transfiguration", "Matthew 17:1-13"),
            (50, "Entry into Jerusalem", "Matthew 21:1-17"),
            (51, "The Last Supper", "Matthew 26:17-35"),
            (52, "The Crucifixion", "Matthew 27:32-56"),
            (53, "The Resurrection", "Matthew 28:1-20"),
            (54, "The Day of Pentecost", "Acts 2:1-47"),
            (55, "Paul's Conversion", "Acts 9:1-31"),
            (56, "Paul's Missionary Journeys", "Acts 13:1-14:28"),
            (57, "Justification by Faith", "Romans 3:21-5:21"),
            (58, "Life in the Spirit", "Romans 8:1-39"),
            (59, "Love Chapter", "1 Corinthians 13:1-13"),
            (60, "New Heaven and Earth", "Revelation 21:1-22:21"),
        ]

        for day_num, theme, passages in days:
            ReadingPlanDay.objects.create(
                plan=plan,
                day_number=day_num,
                theme_en=theme,
                passages=passages.split("; ") if "; " in passages else [passages],
            )

        self.stdout.write(f"Created plan: {plan.title_en}")

    def create_30_famous_battles(self):
        plan, created = ReadingPlan.objects.get_or_create(
            title_en="30 Famous Battles",
            defaults={
                "description_en": "Explore 30 famous battles from Scripture, from Cain vs. Abel to God vs. Satan.",
                "duration_days": 30,
                "category": "general",
                "is_premium": False,
            },
        )

        if not created:
            self.stdout.write(f'Plan "{plan.title_en}" already exists, skipping...')
            return

        days = [
            (1, "Cain vs. Abel", "Genesis 4:1-16"),
            (2, "Abram vs. the Four Kings", "Genesis 14:1-24"),
            (3, "Jacob vs. Esau", "Genesis 27:1-45"),
            (4, "Jacob's Sons vs. the Shechemites", "Genesis 34:1-31"),
            (5, "Joseph vs. His Brothers", "Genesis 37:1-36"),
            (6, "The Israelites vs. the Amalekites", "Exodus 17:8-16"),
            (7, "The Israelites vs. the People of Jericho", "Joshua 5:13-6:27"),
            (8, "The Israelites vs. the People of Ai", "Joshua 8:1-29"),
            (9, "The Israelites vs. the Amorites", "Joshua 10:1-28"),
            (10, "The Israelites vs. the Northern Kings", "Joshua 11:1-23"),
            (11, "Gideon and His Men vs. the Midianites", "Judges 7:1-25"),
            (12, "Samson vs. the Philistines", "Judges 15:1-20"),
            (13, "The Israelites vs. the Benjamites", "Judges 20:1-48"),
            (14, "The Israelites vs. the Philistines", "1 Samuel 4:1-11"),
            (15, "David vs. Goliath", "1 Samuel 17:1-54"),
            (16, "David and His Men vs. the Amalekites", "1 Samuel 30:1-31"),
            (17, "Joab vs. Abner", "2 Samuel 3:22-39"),
            (18, "David and His Men vs. the Ammonites", "2 Samuel 10:1-19"),
            (19, "Absalom vs. Amnon", "2 Samuel 13:23-39"),
            (20, "The Israelites vs. the Moabites", "2 Kings 3:1-27"),
            (21, "Elijah vs. the Prophets of Baal", "1 Kings 18:16-40"),
            (22, "Babylon vs. Judah", "2 Kings 25:1-26"),
            (23, "Jesus vs. Satan", "Matthew 4:1-17"),
            (24, "Peter and John vs. the Sanhedrin", "Acts 4:1-22"),
            (25, "Paul vs. Barnabas", "Acts 15:36-41"),
            (26, "Followers vs. Followers", "1 Corinthians 1:10-31"),
            (27, "Paul vs. Peter", "Galatians 2:11-21"),
            (28, "The Rider vs. the Beast", "Revelation 19:11-21"),
            (29, "God vs. Satan", "Revelation 20:1-10"),
            (30, "Final Victory", "Revelation 20:11-15; 21:1-8"),
        ]

        for day_num, theme, passages in days:
            ReadingPlanDay.objects.create(
                plan=plan,
                day_number=day_num,
                theme_en=theme,
                passages=passages.split("; ") if "; " in passages else [passages],
            )

        self.stdout.write(f"Created plan: {plan.title_en}")

    def create_not_so_famous_stories(self):
        plan, created = ReadingPlan.objects.get_or_create(
            title_en="Not-So-Famous Bible Stories",
            defaults={
                "description_en": "Discover lesser-known but powerful stories from Scripture that often get overlooked.",
                "duration_days": 30,
                "category": "general",
                "is_premium": False,
            },
        )

        if not created:
            self.stdout.write(f'Plan "{plan.title_en}" already exists, skipping...')
            return

        days = [
            (1, "Fire and Birds: God Lays Down the Law", "Numbers 11"),
            (2, "Miriam: Leprous as Snow", "Numbers 12"),
            (3, "Korah, Dathan and Abiram: Gulp!", "Numbers 16"),
            (4, "Aaron: A Budding Leader", "Numbers 17"),
            (5, "Moses Strikes Out", "Numbers 20:1-13"),
            (6, "Balaam's Donkey", "Numbers 22"),
            (7, "Afraid of Snakes?", "Numbers 21:4-9"),
            (8, "Odd Obedience", "Deuteronomy 23-24"),
            (9, "Laws for a Special People", "Deuteronomy 21"),
            (10, "Moses: End of an Era", "Deuteronomy 32:44-52; 34"),
            (11, "The Passing of a Legend", "Joshua 10:1-15"),
            (12, "Solar Stand Still", "Joshua 3:1-17"),
            (13, "Ehud: Left-Handed Wonder", "Judges 3:12-30"),
            (14, "Deborah and Jael: Female Power", "Judges 4"),
            (15, "Jephthah: A Hero's Vow", "Judges 11"),
            (16, "A Levite: The Wickedness of Israel", "Judges 19"),
            (17, "Mephibosheth: Rags to Riches", "2 Samuel 9"),
            (18, "David and Abigail: The Good Guy Wins", "1 Samuel 25"),
            (19, "Elisha: Miracles Large and Small", "2 Kings 2:23-25; 4:8-37"),
            (20, "Asa: But If You Forsake Him...", "2 Chronicles 15"),
            (21, "Asa's Pride", "2 Chronicles 16"),
            (22, "Athaliah: The Usurper", "2 Chronicles 22:10-23:21"),
            (23, "Joash: Kindness Forgotten", "2 Chronicles 24:17-27"),
            (24, "Josiah: Youthful Ruler", "2 Chronicles 34"),
            (25, "Reviving Tradition", "Nehemiah 1"),
            (26, "Nehemiah: Homesickness", "Nehemiah 2"),
            (27, "End of the Exile", "Nehemiah 5:1-19"),
            (28, "Jerusalem Falls: Judgment Arrives", "Jeremiah 52"),
            (29, "The Writing on the Wall", "Daniel 5"),
            (30, "Handwriting Decoded", "Daniel 5:17-31"),
        ]

        for day_num, theme, passages in days:
            ReadingPlanDay.objects.create(
                plan=plan,
                day_number=day_num,
                theme_en=theme,
                passages=passages.split("; ") if "; " in passages else [passages],
            )

        self.stdout.write(f"Created plan: {plan.title_en}")
