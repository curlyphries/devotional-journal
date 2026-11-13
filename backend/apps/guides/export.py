"""Everything the guides app holds about a person, decrypted, for their data export."""

from .models import (
    GrowthPlan,
    GrowthProfile,
    LessonResponse,
    ProfileAssessment,
    StudyEnrollment,
)


def export_guides(user) -> dict:
    profile = GrowthProfile.objects.filter(user=user).select_related("user").first()
    data = {"profile": None, "assessments": [], "studies": [], "growth_plans": []}
    if profile:
        data["profile"] = {
            "life_stage": profile.life_stage,
            "situations": profile.situations,
            "faith_background": profile.faith_background,
            "needs": profile.needs,
            "desired_traits": profile.desired_traits,
            "about_me": profile.get_about_me(),
            "insights": profile.get_insights(),
            "insights_generated_at": (
                profile.insights_generated_at.isoformat()
                if profile.insights_generated_at
                else None
            ),
            "insights_provider": profile.insights_provider,
            "insights_model": profile.insights_model,
        }
    for record in (
        ProfileAssessment.objects.filter(user=user)
        .select_related("user")
        .order_by("taken_at")
    ):
        data["assessments"].append(
            {"taken_at": record.taken_at.isoformat(), **record.get_payload()}
        )
    for enrollment in StudyEnrollment.objects.filter(user=user).order_by("started_at"):
        lessons = []
        for response in LessonResponse.objects.filter(
            enrollment=enrollment
        ).select_related("enrollment", "enrollment__user"):
            lessons.append(
                {
                    "lesson": response.lesson_number,
                    "understanding": response.understanding,
                    "resonance": response.resonance,
                    "completed_at": (
                        response.completed_at.isoformat()
                        if response.completed_at
                        else None
                    ),
                    **response.get_payload(),
                    "personal": response.get_personal(),
                }
            )
        data["studies"].append(
            {
                "topic": enrollment.topic_key,
                "life_stage": enrollment.life_stage,
                "status": enrollment.status,
                "started_at": enrollment.started_at.isoformat(),
                "lessons": lessons,
            }
        )
    for plan in (
        GrowthPlan.objects.filter(user=user)
        .select_related("user")
        .order_by("started_at")
    ):
        goals = []
        for goal in plan.goals.all():
            goal.plan = plan
            goals.append(
                {
                    "horizon": goal.horizon,
                    "title": goal.get_title(),
                    "kind": goal.kind,
                    "target_count": goal.target_count,
                    "progress_count": goal.progress_count,
                    "due_date": str(goal.due_date),
                    "status": goal.status,
                }
            )
        checkins = []
        for checkin in plan.checkins.all():
            checkin.plan = plan
            checkins.append(
                {
                    "date": str(checkin.date),
                    "rating": checkin.rating,
                    "note": checkin.get_note(),
                }
            )
        data["growth_plans"].append(
            {
                "trait": plan.trait_key,
                "why": plan.get_why(),
                "status": plan.status,
                "started_at": plan.started_at.isoformat(),
                "target_date": str(plan.target_date),
                "baseline_rating": plan.baseline_rating,
                "goals": goals,
                "checkins": checkins,
            }
        )
    return data
