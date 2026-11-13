"""
Tests for plans app.
"""

import pytest
from rest_framework import status

from apps.plans.models import UserPlanEnrollment


@pytest.mark.django_db
class TestReadingPlan:
    def test_plan_get_title_english(self, reading_plan):
        assert reading_plan.get_title("en") == "Test Plan"

    def test_plan_get_title_spanish(self, reading_plan):
        assert reading_plan.get_title("es") == "Plan de Prueba"

    def test_plan_get_title_fallback(self, reading_plan):
        reading_plan.title_es = ""
        reading_plan.save()
        assert reading_plan.get_title("es") == "Test Plan"


@pytest.mark.django_db
class TestUserPlanEnrollment:
    def test_enroll_in_plan(self, user, reading_plan):
        enrollment = UserPlanEnrollment.objects.create(
            user=user,
            plan=reading_plan,
            current_day=1,
        )
        assert enrollment.is_active
        assert enrollment.current_day == 1

    def test_progress_percentage(self, user, reading_plan):
        enrollment = UserPlanEnrollment.objects.create(
            user=user,
            plan=reading_plan,
            current_day=4,
        )
        # 4 out of 7 days = ~57%
        assert 50 < enrollment.progress_percentage < 60


@pytest.mark.django_db
class TestPlansAPI:
    def test_list_plans(self, authenticated_client, reading_plan):
        response = authenticated_client.get("/api/v1/plans/")
        assert response.status_code == status.HTTP_200_OK
        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )
        assert len(results) >= 1

    def test_get_plan_detail(self, authenticated_client, reading_plan):
        response = authenticated_client.get(f"/api/v1/plans/{reading_plan.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Plan"
        assert "days" in response.data

    def test_enroll_in_plan(self, authenticated_client, reading_plan):
        response = authenticated_client.post(f"/api/v1/plans/{reading_plan.id}/enroll/")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["current_day"] == 1

    def test_cannot_enroll_twice(self, authenticated_client, user, reading_plan):
        UserPlanEnrollment.objects.create(
            user=user,
            plan=reading_plan,
            current_day=1,
            is_active=True,
        )

        response = authenticated_client.post(f"/api/v1/plans/{reading_plan.id}/enroll/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_enrolled_plans(self, authenticated_client, user, reading_plan):
        UserPlanEnrollment.objects.create(
            user=user,
            plan=reading_plan,
            current_day=3,
        )

        response = authenticated_client.get("/api/v1/plans/enrolled/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_get_today_reading(self, authenticated_client, user, reading_plan):
        enrollment = UserPlanEnrollment.objects.create(
            user=user,
            plan=reading_plan,
            current_day=1,
        )

        response = authenticated_client.get(
            f"/api/v1/plans/enrolled/{enrollment.id}/today/"
        )
        assert response.status_code == status.HTTP_200_OK
        assert "day" in response.data
        assert "day_number" in response.data["day"]
        assert "theme" in response.data["day"]

    def test_advance_day(self, authenticated_client, user, reading_plan):
        enrollment = UserPlanEnrollment.objects.create(
            user=user,
            plan=reading_plan,
            current_day=1,
        )

        response = authenticated_client.post(
            f"/api/v1/plans/enrolled/{enrollment.id}/advance/"
        )
        assert response.status_code == status.HTTP_200_OK

        enrollment.refresh_from_db()
        assert enrollment.current_day == 2


@pytest.mark.django_db
class TestPlanCategories:
    """One shared category list: builder, filter, validation and AI suggestion."""

    def _plan(self, category="general", **kwargs):
        from apps.plans.models import ReadingPlan

        defaults = dict(
            title_en="Plan",
            title_es="Plan",
            description_en="d",
            description_es="d",
            duration_days=3,
            category=category,
            is_public=True,
        )
        defaults.update(kwargs)
        return ReadingPlan.objects.create(**defaults)

    def test_list_is_grouped_localised_and_far_larger_than_six(
        self, authenticated_client
    ):
        body = authenticated_client.get("/api/v1/plans/categories/").json()
        groups = body["groups"]
        assert [g["title"] for g in groups] == [
            "Faith",
            "Through the Bible",
            "Heart and Mind",
            "Relationships and Family",
            "Calling and Character",
            "Seasons of Life and the Year",
        ]
        values = [c["value"] for g in groups for c in g["categories"]]
        assert len(values) == len(set(values)) >= 40
        # Everything that existed before is still there, so old plans keep their category.
        assert {
            "general",
            "faith",
            "fatherhood",
            "leadership",
            "recovery",
            "marriage",
        } <= set(values)
        assert {
            "motherhood",
            "parenting",
            "anxiety",
            "grief",
            "kids",
            "later_years",
        } <= set(values)
        assert all(len(v) <= 30 for v in values)

        spanish = authenticated_client.get("/api/v1/plans/categories/?lang=es").json()[
            "groups"
        ]
        assert spanish[0]["title"] == "Fe"
        labels = {c["value"]: c["label"] for g in spanish for c in g["categories"]}
        assert (
            labels["motherhood"] == "Maternidad"
            and labels["grief"] == "Duelo y pérdida"
        )

    def test_model_choices_come_from_the_same_list(self):
        from apps.plans.categories import CATEGORY_CHOICES, CATEGORY_KEYS
        from apps.plans.models import ReadingPlan

        field = ReadingPlan._meta.get_field("category")
        assert [key for key, _ in field.choices] == CATEGORY_KEYS
        assert field.choices == CATEGORY_CHOICES
        assert field.max_length >= max(len(key) for key in CATEGORY_KEYS)

    def test_counts_cover_public_plans_and_your_own_only(
        self, authenticated_client, user, user_factory
    ):
        self._plan("grief")
        self._plan("grief", is_public=False, created_by=user)
        self._plan(
            "grief", is_public=False, created_by=user_factory()
        )  # someone else's
        self._plan("grief", is_active=False)
        groups = authenticated_client.get("/api/v1/plans/categories/").json()["groups"]
        counts = {c["value"]: c["plan_count"] for g in groups for c in g["categories"]}
        assert counts["grief"] == 2 and counts["marriage"] == 0

    def test_plans_carry_a_readable_category_label_and_filter_by_new_categories(
        self, authenticated_client
    ):
        self._plan("later_years")
        self._plan("marriage")
        rows = authenticated_client.get("/api/v1/plans/?category=later_years").json()
        rows = rows["results"] if isinstance(rows, dict) else rows
        assert [(r["category"], r["category_label"]) for r in rows] == [
            ("later_years", "Later Years")
        ]

    def test_saving_a_plan_accepts_new_categories_and_rejects_unknown_ones(
        self, authenticated_client
    ):
        body = {
            "title_en": "For new mothers",
            "description_en": "d",
            "duration_days": 1,
            "days": [{"day_number": 1, "passages": ["Psalm 127:1-3"], "theme_en": "t"}],
        }
        saved = authenticated_client.post(
            "/api/v1/plans/save/", {**body, "category": "motherhood"}, format="json"
        )
        assert saved.status_code == 201, saved.content
        assert saved.json()["category"] == "motherhood"
        assert saved.json()["category_label"] == "Motherhood"

        unknown = authenticated_client.post(
            "/api/v1/plans/save/", {**body, "category": "cooking"}, format="json"
        )
        assert unknown.status_code == 400
        assert (
            unknown.json()["code"] == "VALIDATION_ERROR"
            and unknown.json()["suggestion"]
        )

        default = authenticated_client.post("/api/v1/plans/save/", body, format="json")
        assert default.status_code == 201 and default.json()["category"] == "general"

    def test_generation_tells_the_model_the_category_name_and_validates_it(
        self, authenticated_client, monkeypatch
    ):
        from apps.plans import views

        seen = {}

        class FakeService:
            def generate_reading_plan(self, **kwargs):
                seen.update(kwargs)
                return {
                    "title_en": "Grief",
                    "days": [
                        {"day_number": n, "passages": ["Psalm 23:1-6"], "theme_en": "t"}
                        for n in (1, 2, 3)
                    ],
                }

        monkeypatch.setattr(
            views, "get_prompt_service", lambda user=None: FakeService()
        )
        ok = authenticated_client.post(
            "/api/v1/plans/generate/",
            {"topic": "losing my father", "duration_days": 3, "category": "grief"},
            format="json",
        )
        assert ok.status_code == 200, ok.content
        assert seen["category"] == "Grief and Loss"
        assert ok.json()["category"] == "grief"

        bad = authenticated_client.post(
            "/api/v1/plans/generate/",
            {"topic": "x", "duration_days": 3, "category": "nonsense"},
            format="json",
        )
        assert bad.status_code == 400

    def test_speak_your_mind_offers_the_full_list_and_only_visible_plans(
        self, authenticated_client, user_factory, web_bible, monkeypatch
    ):
        from apps.plans.categories import CATEGORY_KEYS
        from apps.prompts import views as prompt_views
        from apps.prompts.services import OllamaPromptService

        prompt = OllamaPromptService(
            base_url="http://x", model="m"
        )._get_explore_system_prompt("en")
        assert all(key in prompt for key in CATEGORY_KEYS)

        self._plan("grief", title_en="Public grief plan")
        self._plan(
            "grief",
            title_en="Someone's private plan",
            is_public=False,
            created_by=user_factory(),
        )

        class FakeService:
            category = "grief"

            def explore_heart_prompt(self, user_input, language):
                return {
                    "passages": [
                        {
                            "book": "Philippians",
                            "chapter": 4,
                            "verse_start": 6,
                            "verse_end": 7,
                            "reason": "r",
                        }
                    ],
                    "prompts": ["p"],
                    "category": self.category,
                    "summary": "s",
                }

        service = FakeService()
        monkeypatch.setattr(
            prompt_views, "get_prompt_service", lambda user=None: service
        )
        body = authenticated_client.post(
            "/api/v1/prompts/explore/", {"input": "My father died."}, format="json"
        )
        assert body.status_code == 200, body.content
        assert body.json()["category"] == "grief"
        assert [p["title"] for p in body.json()["plans"]] == ["Public grief plan"]

        service.category = "made_up_category"
        again = authenticated_client.post(
            "/api/v1/prompts/explore/", {"input": "Something else."}, format="json"
        ).json()
        assert again["category"] == "general"
