"""
API for Bible study guides, the growth profile and growth plans.

Every view is scoped to request.user. Text is returned in the language asked
for with ?lang=en|es (default: the person's saved language).
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.errors import AppError

from . import library, plans, profile, study
from .catalog import (
    ALL_TOPIC_KEYS,
    ASSESSMENT_ITEMS,
    ASSESSMENT_KEYS,
    CATEGORIES,
    FAITH_BACKGROUND_KEYS,
    FAITH_BACKGROUNDS,
    LIFE_STAGE_KEYS,
    LIFE_STAGES,
    SCALE,
    SITUATION_KEYS,
    SITUATIONS,
    TRAIT_KEYS,
)
from .models import (
    GrowthGoal,
    GrowthPlan,
    GrowthProfile,
    ProfileAssessment,
    StudyEnrollment,
)
from .render import lang_for, topic_card, tr


def _not_found(what: str):
    return AppError(f"That {what} was not found.", code="NOT_FOUND", status_code=404)


def _enrollment(request, study_id) -> StudyEnrollment:
    try:
        return StudyEnrollment.objects.select_related("user").get(
            id=study_id, user=request.user
        )
    except StudyEnrollment.DoesNotExist:
        raise _not_found("study")


def _plan(request, plan_id) -> GrowthPlan:
    try:
        return GrowthPlan.objects.select_related("user").get(
            id=plan_id, user=request.user
        )
    except GrowthPlan.DoesNotExist:
        raise _not_found("growth plan")


class GuidesView(APIView):
    permission_classes = [IsAuthenticated]


class CatalogView(GuidesView):
    """Everything needed to browse the library and fill in a profile."""

    def get(self, request):
        lang = lang_for(request)
        stage_row = (
            GrowthProfile.objects.filter(user=request.user)
            .values_list("life_stage", flat=True)
            .first()
        )
        stage = stage_row or ""
        latest = {}
        for enrollment in StudyEnrollment.objects.filter(user=request.user).order_by(
            "started_at"
        ):
            latest[enrollment.topic_key] = enrollment  # newest wins
        topics = library.topics()
        return Response(
            {
                "life_stages": [
                    {
                        "key": s["key"],
                        "title": tr(s["title"], lang),
                        "note": tr(s["note"], lang),
                    }
                    for s in LIFE_STAGES
                ],
                "situations": [
                    {"key": s["key"], "title": tr(s["title"], lang)} for s in SITUATIONS
                ],
                "faith_backgrounds": [
                    {"key": s["key"], "title": tr(s["title"], lang)}
                    for s in FAITH_BACKGROUNDS
                ],
                "categories": [
                    {
                        "key": c["key"],
                        "title": tr(c["title"], lang),
                        "summary": tr(c["summary"], lang),
                        "topics": [
                            topic_card(
                                t,
                                lang,
                                stage,
                                profile._enrollment_brief(latest.get(t["key"])),
                            )
                            for t in topics.values()
                            if t["category"] == c["key"]
                        ],
                    }
                    for c in CATEGORIES
                ],
                "traits": [
                    {
                        "key": key,
                        "title": tr(trait["title"], lang),
                        "definition": tr(trait["definition"], lang),
                    }
                    for key, trait in library.traits().items()
                ],
                "assessment": {
                    "scale": tr(SCALE, lang),
                    "items": [
                        {
                            "key": i["key"],
                            "area": i["area"],
                            "text": tr(i["text"], lang),
                        }
                        for i in ASSESSMENT_ITEMS
                    ],
                },
            }
        )


class RecommendationsView(GuidesView):
    def get(self, request):
        return Response(
            profile.recommendations_payload(request.user, lang_for(request))
        )


# ---------------------------------------------------------------- studies


class StudyListView(GuidesView):
    def get(self, request):
        lang = lang_for(request)
        return Response(
            [
                study.study_payload(e, lang)
                for e in StudyEnrollment.objects.filter(user=request.user)
                if library.get_topic(e.topic_key)
            ]
        )

    def post(self, request):
        topic_key = request.data.get("topic")
        life_stage = request.data.get("life_stage") or ""
        if not isinstance(topic_key, str):
            raise AppError("“topic” is required.")
        if life_stage and life_stage not in LIFE_STAGE_KEYS:
            raise AppError("Unknown life stage.")
        enrollment, created = study.enroll(request.user, topic_key, life_stage)
        return Response(
            study.study_payload(enrollment, lang_for(request)),
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class StudyDetailView(GuidesView):
    def get(self, request, study_id):
        return Response(
            study.study_payload(
                _enrollment(request, study_id), lang_for(request), detail=True
            )
        )

    def delete(self, request, study_id):
        _enrollment(request, study_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonView(GuidesView):
    def get(self, request, study_id, number):
        return Response(
            study.lesson_payload(
                _enrollment(request, study_id), number, lang_for(request)
            )
        )


class LessonRespondView(GuidesView):
    def post(self, request, study_id, number):
        return Response(
            study.respond(
                _enrollment(request, study_id), number, request.data, lang_for(request)
            )
        )


class LessonSimplifyView(GuidesView):
    def post(self, request, study_id, number):
        enrollment = _enrollment(request, study_id)
        study.simplify(enrollment, number)
        return Response(study.lesson_payload(enrollment, number, lang_for(request)))


class LessonPersonalizeView(GuidesView):
    def post(self, request, study_id, number):
        enrollment = _enrollment(request, study_id)
        lang = lang_for(request)
        study.personalize(enrollment, number, lang)
        return Response(study.lesson_payload(enrollment, number, lang))


# ---------------------------------------------------------------- profile


def _key_list(value, allowed, name, limit=None):
    if not isinstance(value, list) or any(v not in allowed for v in value):
        raise AppError(f"“{name}” must be a list of known keys.")
    unique = list(dict.fromkeys(value))
    if limit and len(unique) > limit:
        raise AppError(f"Choose at most {limit} for “{name}”.")
    return unique


def _ratings(value, allowed, name):
    if not isinstance(value, dict):
        raise AppError(f"“{name}” must be an object of 1-5 ratings.")
    out = {}
    for key, score in value.items():
        if key not in allowed:
            raise AppError(f"Unknown item “{key}” in “{name}”.")
        if not isinstance(score, int) or isinstance(score, bool) or not 1 <= score <= 5:
            raise AppError(
                f"Each rating in “{name}” must be a whole number from 1 to 5."
            )
        out[key] = score
    return out


class ProfileView(GuidesView):
    def get(self, request):
        return Response(profile.profile_payload(request.user, lang_for(request)))

    def patch(self, request):
        data = request.data
        record = profile.get_or_create_profile(request.user)
        if "life_stage" in data:
            if data["life_stage"] not in LIFE_STAGE_KEYS:
                raise AppError("Unknown life stage.")
            record.life_stage = data["life_stage"]
            if not record.profiling_enabled:
                # Switching to a child: nothing inferred about them is kept.
                record.set_insights(None)
                record.insights_generated_at = None
                ProfileAssessment.objects.filter(user=request.user).delete()
        if "situations" in data:
            record.situations = _key_list(
                data["situations"], SITUATION_KEYS, "situations"
            )
        if "faith_background" in data:
            if data["faith_background"] not in (*FAITH_BACKGROUND_KEYS, None, ""):
                raise AppError("Unknown faith background.")
            record.faith_background = data["faith_background"] or ""
        if "needs" in data:
            record.needs = _key_list(data["needs"], ALL_TOPIC_KEYS, "needs")
        if "desired_traits" in data:
            record.desired_traits = _key_list(
                data["desired_traits"], TRAIT_KEYS, "desired_traits", limit=3
            )
        if "about_me" in data:
            if not isinstance(data["about_me"], str) or len(data["about_me"]) > 4000:
                raise AppError("“about_me” must be text of at most 4000 characters.")
            record.set_about_me(data["about_me"])
        record.save()
        return Response(profile.profile_payload(request.user, lang_for(request)))

    def delete(self, request):
        """Erase the profile, assessment history and insights. Studies, plans and entries stay."""
        GrowthProfile.objects.filter(user=request.user).delete()
        ProfileAssessment.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileAssessmentView(GuidesView):
    def post(self, request):
        answers = _ratings(request.data.get("answers", {}), ASSESSMENT_KEYS, "answers")
        trait_ratings = _ratings(
            request.data.get("trait_ratings", {}), TRAIT_KEYS, "trait_ratings"
        )
        if not answers and not trait_ratings:
            raise AppError("There is nothing to save yet.")
        profile.save_assessment(request.user, answers, trait_ratings)
        return Response(profile.profile_payload(request.user, lang_for(request)))


class ProfileInsightsView(GuidesView):
    def post(self, request):
        lang = lang_for(request)
        profile.generate_insights(request.user, lang)
        return Response(profile.profile_payload(request.user, lang))


class ProfileInsightFeedbackView(GuidesView):
    def post(self, request, insight_id):
        accurate = request.data.get("accurate")
        if accurate not in (True, False, None):
            raise AppError("“accurate” must be true, false or null.")
        record = (
            GrowthProfile.objects.filter(user=request.user)
            .select_related("user")
            .first()
        )
        insights = record.get_insights() if record else None
        item = next(
            (i for i in (insights or {}).get("items", []) if i.get("id") == insight_id),
            None,
        )
        if not item:
            raise _not_found("observation")
        item["accurate"] = accurate
        record.set_insights(insights)
        record.save(update_fields=["encrypted_insights", "updated_at"])
        return Response(profile.profile_payload(request.user, lang_for(request)))


# ---------------------------------------------------------------- growth plans


class PlanListView(GuidesView):
    def get(self, request):
        lang = lang_for(request)
        order = {"active": 0, "paused": 1, "completed": 2}
        rows = [
            plans.plan_payload(p, lang)
            for p in GrowthPlan.objects.filter(user=request.user).select_related("user")
            if library.get_trait(p.trait_key)
        ]
        rows.sort(key=lambda p: order.get(p["status"], 3))
        return Response(rows)

    def post(self, request):
        data = request.data
        baseline = data.get("baseline_rating")
        if baseline is not None and (
            not isinstance(baseline, int)
            or isinstance(baseline, bool)
            or not 1 <= baseline <= 5
        ):
            raise AppError("“baseline_rating” must be a whole number from 1 to 5.")
        why = data.get("why", "") or ""
        if not isinstance(why, str) or len(why) > 4000:
            raise AppError("“why” must be text of at most 4000 characters.")
        lang = lang_for(request)
        plan = plans.create_plan(
            request.user,
            data.get("trait"),
            why=why,
            baseline_rating=baseline,
            personalize=data.get("personalize") is True,
            lang=lang,
        )
        return Response(plans.plan_payload(plan, lang), status=status.HTTP_201_CREATED)


class PlanDetailView(GuidesView):
    def get(self, request, plan_id):
        return Response(plans.plan_payload(_plan(request, plan_id), lang_for(request)))

    def patch(self, request, plan_id):
        from django.utils import timezone

        plan = _plan(request, plan_id)
        if "status" in request.data:
            if request.data["status"] not in ("active", "paused", "completed"):
                raise AppError("“status” must be active, paused or completed.")
            plan.status = request.data["status"]
            plan.completed_at = timezone.now() if plan.status == "completed" else None
        if "why" in request.data:
            if (
                not isinstance(request.data["why"], str)
                or len(request.data["why"]) > 4000
            ):
                raise AppError("“why” must be text of at most 4000 characters.")
            plan.set_why(request.data["why"])
        plan.save()
        return Response(plans.plan_payload(plan, lang_for(request)))

    def delete(self, request, plan_id):
        _plan(request, plan_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanGoalsView(GuidesView):
    def post(self, request, plan_id):
        plan = _plan(request, plan_id)
        plans.add_goal(plan, request.data)
        return Response(plans.plan_payload(plan, lang_for(request)))


class PlanGoalDetailView(GuidesView):
    def _goal(self, plan, goal_id) -> GrowthGoal:
        try:
            goal = plan.goals.get(id=goal_id)
        except GrowthGoal.DoesNotExist:
            raise _not_found("goal")
        goal.plan = plan
        return goal

    def patch(self, request, plan_id, goal_id):
        plan = _plan(request, plan_id)
        plans.update_goal(self._goal(plan, goal_id), request.data)
        return Response(plans.plan_payload(plan, lang_for(request)))

    def delete(self, request, plan_id, goal_id):
        plan = _plan(request, plan_id)
        self._goal(plan, goal_id).delete()
        return Response(plans.plan_payload(plan, lang_for(request)))


class PlanCheckInsView(GuidesView):
    def post(self, request, plan_id):
        plan = _plan(request, plan_id)
        plans.add_checkin(plan, request.data)
        return Response(plans.plan_payload(plan, lang_for(request)))
