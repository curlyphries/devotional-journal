"""
Views for reading plans.
"""

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.prompts.services import get_prompt_service

from .models import ReadingPlan, ReadingPlanDay, UserPlanEnrollment
from .serializers import (
    ReadingPlanDetailSerializer,
    ReadingPlanSerializer,
    UserPlanEnrollmentSerializer,
)


class PlanListView(APIView):
    """
    List available reading plans.
    """

    def get(self, request):
        user = request.user
        plans = ReadingPlan.objects.filter(
            is_active=True
        ).filter(
            Q(is_public=True) | Q(created_by=user)
        )

        category = request.query_params.get("category")
        if category:
            plans = plans.filter(category=category)

        is_premium = request.query_params.get("is_premium")
        if is_premium is not None:
            plans = plans.filter(is_premium=is_premium.lower() == "true")

        serializer = ReadingPlanSerializer(
            plans, many=True, context={"request": request}
        )
        return Response(serializer.data)


class PlanDetailView(APIView):
    """
    Get plan details with day list.
    """

    def get(self, request, plan_id):
        try:
            plan = ReadingPlan.objects.prefetch_related("days").get(
                id=plan_id, is_active=True
            )
        except ReadingPlan.DoesNotExist:
            return Response(
                {"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReadingPlanDetailSerializer(plan, context={"request": request})
        return Response(serializer.data)


class EnrollView(APIView):
    """
    Enroll in a reading plan.
    """

    def post(self, request, plan_id):
        try:
            plan = ReadingPlan.objects.get(id=plan_id, is_active=True)
        except ReadingPlan.DoesNotExist:
            return Response(
                {"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND
            )

        existing = UserPlanEnrollment.objects.filter(
            user=request.user, plan=plan, is_active=True
        ).first()

        if existing:
            return Response(
                {"error": "Already enrolled in this plan"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        enrollment = UserPlanEnrollment.objects.create(user=request.user, plan=plan)

        serializer = UserPlanEnrollmentSerializer(
            enrollment, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EnrolledPlansView(APIView):
    """
    List user's enrolled plans.
    """

    def get(self, request):
        enrollments = (
            UserPlanEnrollment.objects.filter(user=request.user)
            .select_related("plan")
            .order_by("-started_at")
        )

        active_only = request.query_params.get("active")
        if active_only and active_only.lower() == "true":
            enrollments = enrollments.filter(is_active=True, completed_at__isnull=True)

        serializer = UserPlanEnrollmentSerializer(
            enrollments, many=True, context={"request": request}
        )
        return Response(serializer.data)


class TodayReadingView(APIView):
    """
    Get today's reading for an enrollment.
    """

    def get(self, request, enrollment_id):
        try:
            enrollment = UserPlanEnrollment.objects.select_related("plan").get(
                id=enrollment_id, user=request.user
            )
        except UserPlanEnrollment.DoesNotExist:
            return Response(
                {"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            day = ReadingPlanDay.objects.get(
                plan=enrollment.plan, day_number=enrollment.current_day
            )
        except ReadingPlanDay.DoesNotExist:
            return Response(
                {"error": "Day not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "enrollment": UserPlanEnrollmentSerializer(
                    enrollment, context={"request": request}
                ).data,
                "day": {
                    "day_number": day.day_number,
                    "passages": day.passages,
                    "theme": day.get_theme(request.user.language_preference),
                },
            }
        )


class AdvanceDayView(APIView):
    """
    Mark today complete and advance to next day.
    """

    def post(self, request, enrollment_id):
        try:
            enrollment = UserPlanEnrollment.objects.select_related("plan").get(
                id=enrollment_id, user=request.user, is_active=True
            )
        except UserPlanEnrollment.DoesNotExist:
            return Response(
                {"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if enrollment.current_day >= enrollment.plan.duration_days:
            enrollment.completed_at = timezone.now()
            enrollment.save()
            return Response(
                {
                    "message": "Plan completed!",
                    "enrollment": UserPlanEnrollmentSerializer(
                        enrollment, context={"request": request}
                    ).data,
                }
            )

        enrollment.current_day += 1
        enrollment.save()

        return Response(
            {
                "message": f"Advanced to day {enrollment.current_day}",
                "enrollment": UserPlanEnrollmentSerializer(
                    enrollment, context={"request": request}
                ).data,
            }
        )


class PlanGenerateView(APIView):
    """
    AI-generate a reading plan draft from a topic description.
    Saves the plan as a personal (non-public) plan owned by the requesting user.
    Admins can pass is_public=true to publish immediately.
    """

    def post(self, request):
        topic = request.data.get("topic", "").strip()
        if not topic:
            return Response(
                {"error": "topic is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        duration_days = int(request.data.get("duration_days", 7))
        if duration_days < 3 or duration_days > 90:
            return Response(
                {"error": "duration_days must be between 3 and 90"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        category = request.data.get("category", "general")
        anchor_passages = request.data.get("anchor_passages", [])
        if isinstance(anchor_passages, str):
            anchor_passages = [p.strip() for p in anchor_passages.split(",") if p.strip()]

        language = getattr(request.user, "language_preference", "en")
        is_public = request.data.get("is_public", False)
        if is_public and not request.user.is_staff:
            is_public = False

        service = get_prompt_service()
        plan_data = service.generate_reading_plan(
            topic=topic,
            duration_days=duration_days,
            category=category,
            anchor_passages=anchor_passages,
            language=language,
        )

        if not plan_data:
            return Response(
                {"error": "AI generation failed. Please try again."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        days_data = plan_data.get("days", [])
        if len(days_data) != duration_days:
            return Response(
                {
                    "error": f"AI returned {len(days_data)} days instead of {duration_days}. Please retry."
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        plan = ReadingPlan.objects.create(
            title_en=plan_data.get("title_en", topic),
            title_es=plan_data.get("title_es", ""),
            description_en=plan_data.get("description_en", ""),
            description_es=plan_data.get("description_es", ""),
            duration_days=duration_days,
            category=category,
            is_active=True,
            is_public=bool(is_public),
            created_by=request.user,
        )

        for day in days_data:
            ReadingPlanDay.objects.create(
                plan=plan,
                day_number=int(day["day_number"]),
                passages=day.get("passages", []),
                theme_en=day.get("theme_en", ""),
                theme_es=day.get("theme_es", ""),
                reflection_prompts_seed=day.get("reflection_prompt", ""),
            )

        serializer = ReadingPlanDetailSerializer(plan, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlanDeleteView(APIView):
    """
    Delete a personal plan owned by the requesting user.
    """

    def delete(self, request, plan_id):
        try:
            plan = ReadingPlan.objects.get(
                id=plan_id, created_by=request.user, is_public=False
            )
        except ReadingPlan.DoesNotExist:
            return Response(
                {"error": "Plan not found or not deletable"},
                status=status.HTTP_404_NOT_FOUND,
            )
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
