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
        results = response.data["results"] if isinstance(response.data, dict) else response.data
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
