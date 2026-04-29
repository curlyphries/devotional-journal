"""
Management command to seed LifeArea reference data.
"""

from django.core.management.base import BaseCommand

from apps.reflections.models import LifeArea

LIFE_AREAS = [
    {
        "code": "integrity",
        "name": "Integrity & Honesty",
        "description": "Living truthfully, keeping your word, and maintaining consistent character whether anyone is watching or not.",
        "icon": "shield-check",
        "display_order": 1,
        "scripture_tags": [
            "truth",
            "honest",
            "lie",
            "deceive",
            "word",
            "promise",
            "faithful",
            "trustworthy",
            "upright",
            "blameless",
        ],
        "reflection_prompts": [
            "Was I honest in all my interactions today?",
            "Did I keep the commitments I made?",
            "Were my private actions consistent with my public image?",
            "Did I take responsibility for my mistakes?",
        ],
    },
    {
        "code": "relationships",
        "name": "Relationships & Family",
        "description": "Loving well in marriage, fatherhood, friendships, and community. Being present and sacrificial.",
        "icon": "users",
        "display_order": 2,
        "scripture_tags": [
            "love",
            "neighbor",
            "brother",
            "wife",
            "children",
            "father",
            "friend",
            "family",
            "marriage",
            "forgive",
            "reconcile",
        ],
        "reflection_prompts": [
            "Was I fully present with my family today?",
            "Did I prioritize people over tasks?",
            "How did I show love to those closest to me?",
            "Is there a relationship I need to repair?",
        ],
    },
    {
        "code": "work",
        "name": "Work & Purpose",
        "description": "Working diligently as unto the Lord, finding meaning in your calling, and providing with integrity.",
        "icon": "briefcase",
        "display_order": 3,
        "scripture_tags": [
            "work",
            "labor",
            "diligent",
            "lazy",
            "serve",
            "calling",
            "purpose",
            "provision",
            "excellence",
            "steward",
        ],
        "reflection_prompts": [
            "Did I work with excellence today?",
            "Was I a good steward of my time and resources?",
            "Did I serve others through my work?",
            "Am I finding purpose in what I do?",
        ],
    },
    {
        "code": "self_control",
        "name": "Self-Control & Discipline",
        "description": "Mastering desires, controlling anger, and building habits that honor God and serve your goals.",
        "icon": "target",
        "display_order": 4,
        "scripture_tags": [
            "tempt",
            "flesh",
            "spirit",
            "desire",
            "lust",
            "anger",
            "patient",
            "discipline",
            "self-control",
            "sober",
            "alert",
        ],
        "reflection_prompts": [
            "Did I resist temptation today?",
            "How did I handle my anger or frustration?",
            "Did I maintain my commitments to healthy habits?",
            "Where did I give in when I should have held firm?",
        ],
    },
    {
        "code": "faith",
        "name": "Faith & Spiritual Practice",
        "description": "Prayer, scripture study, obedience, and trust in God through all circumstances.",
        "icon": "book-open",
        "display_order": 5,
        "scripture_tags": [
            "pray",
            "trust",
            "faith",
            "believe",
            "obey",
            "word",
            "worship",
            "praise",
            "meditate",
            "seek",
            "follow",
        ],
        "reflection_prompts": [
            "Did I spend time with God today?",
            "How did I respond when things didn't go my way?",
            "Did I trust God or try to control the situation?",
            "What is God teaching me right now?",
        ],
    },
    {
        "code": "service",
        "name": "Service & Generosity",
        "description": "Helping others, giving sacrificially, and using your gifts to serve beyond yourself.",
        "icon": "heart-handshake",
        "display_order": 6,
        "scripture_tags": [
            "give",
            "serve",
            "help",
            "poor",
            "generous",
            "sacrifice",
            "tithe",
            "offering",
            "compassion",
            "mercy",
            "need",
        ],
        "reflection_prompts": [
            "Did I help someone today without expecting anything back?",
            "Was I generous with my time, money, or attention?",
            "Did I notice someone in need and respond?",
            "How am I using my gifts to serve others?",
        ],
    },
    {
        "code": "growth",
        "name": "Growth & Humility",
        "description": "Continuous learning, accepting correction, and pursuing transformation over comfort.",
        "icon": "trending-up",
        "display_order": 7,
        "scripture_tags": [
            "learn",
            "humble",
            "grow",
            "renew",
            "transform",
            "wisdom",
            "teachable",
            "correction",
            "change",
            "mature",
            "sanctify",
        ],
        "reflection_prompts": [
            "Did I learn something new today?",
            "How did I respond to criticism or correction?",
            "Am I the same person I was a year ago?",
            "What area of my life needs the most growth?",
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the LifeArea reference data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force update existing life areas",
        )

    def handle(self, *args, **options):
        force = options["force"]
        created_count = 0
        updated_count = 0

        for area_data in LIFE_AREAS:
            code = area_data["code"]

            if force:
                obj, created = LifeArea.objects.update_or_create(
                    code=code, defaults=area_data
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Created: {code}"))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f"Updated: {code}"))
            else:
                obj, created = LifeArea.objects.get_or_create(
                    code=code, defaults=area_data
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Created: {code}"))
                else:
                    self.stdout.write(f"Skipped (exists): {code}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Created: {created_count}, Updated: {updated_count}"
            )
        )
