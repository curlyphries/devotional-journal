"""
Views for reading plans.
"""

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
        plans = ReadingPlan.objects.filter(is_active=True)

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
