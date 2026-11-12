"""
Views for LLM prompt generation.
"""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_prompt_service

logger = logging.getLogger(__name__)


class GeneratePromptsView(APIView):
    """
    Generate reflection prompts for a passage.
    """

    def post(self, request):
        passage_text = request.data.get("passage_text", "")
        passage_reference = request.data.get("passage_reference", "")
        context = request.data.get("context")
        num_prompts = request.data.get("num_prompts", 3)

        if not passage_text:
            return Response(
                {"error": "passage_text is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        language = request.user.language_preference

        service = get_prompt_service(user=request.user)
        prompts = service.generate_reflection_prompts(
            passage_text=passage_text,
            passage_reference=passage_reference,
            language=language,
            num_prompts=num_prompts,
            context=context,
        )

        return Response({"prompts": prompts})


class HeartPromptGuidanceView(APIView):
    """
    AI-powered Bible exploration agent.
    Accepts freeform user input → asks the LLM to identify relevant passages,
    generate prompts, and suggest a plan category → hydrates passages with
    real verse text from the local Bible database.
    """

    def post(self, request):
        user_input = request.data.get("input", "").strip()
        if not user_input:
            return Response(
                {"error": "input is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        language = getattr(request.user, "language_preference", "english")
        service = get_prompt_service(user=request.user)
        ai_result = service.explore_heart_prompt(user_input, language)

        if not ai_result or not ai_result.get("passages"):
            return Response(
                {
                    "error": "The AI could not identify relevant passages. Please try rephrasing."
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # The model only suggests references. The words come from the Bible
        # source; a suggestion that does not exist there is dropped.
        from apps.bible.lookup import fetch_passage, preferred_translations

        translations = preferred_translations("es" if language == "es" else "en")
        hydrated_passages = []
        for p in ai_result.get("passages", []):
            if not isinstance(p, dict):
                continue
            passage = fetch_passage(
                p.get("book"),
                p.get("chapter"),
                p.get("verse_start"),
                p.get("verse_end") or p.get("verse_start"),
                translations=translations,
            )
            if passage is None:
                continue
            hydrated_passages.append(
                {
                    "reference": passage.reference,
                    "book": passage.book,
                    "chapter": passage.chapter,
                    "verse_start": passage.verse_start,
                    "verse_end": passage.verse_end,
                    "text": passage.text,
                    "translation": passage.translation,
                    "reason": str(p.get("reason", ""))[:600],
                }
            )

        if not hydrated_passages:
            from shared.errors import AppError

            raise AppError(
                "None of the passages the AI suggested could be found in the Bible source.",
                code="SCRIPTURE_UNAVAILABLE",
                status_code=502,
                suggestion="Try again or rephrase. If it keeps happening, the Bible "
                "text source may be unreachable (see docs/TROUBLESHOOTING.md).",
            )

        # Fetch recommended plans
        from apps.plans.models import ReadingPlan

        category = ai_result.get("category", "general")
        plans = list(
            ReadingPlan.objects.filter(category=category).values(
                "id", "title_en", "description_en", "category", "duration_days"
            )[:3]
        )
        if not plans and category != "general":
            plans = list(
                ReadingPlan.objects.filter(category="general").values(
                    "id", "title_en", "description_en", "category", "duration_days"
                )[:3]
            )
        # Normalize field names for frontend
        plans = [
            {
                "id": str(p["id"]),
                "title": p.get("title_en", ""),
                "description": p.get("description_en", ""),
                "category": p.get("category", ""),
                "total_days": p.get("duration_days", 0),
            }
            for p in plans
        ]

        # Auto-persist so the user never loses their results
        from .models import ExplorationHistory

        exploration = ExplorationHistory.objects.create(
            user=request.user,
            user_input=user_input,
            summary=ai_result.get("summary", ""),
            category=category,
            passages=hydrated_passages,
            prompts=ai_result.get("prompts", []),
            plans=plans,
        )

        return Response(
            {
                "id": str(exploration.id),
                "passages": hydrated_passages,
                "prompts": ai_result.get("prompts", []),
                "category": category,
                "summary": ai_result.get("summary", ""),
                "plans": plans,
                "created_at": exploration.created_at.isoformat(),
                "is_bookmarked": exploration.is_bookmarked,
            }
        )


class AIStatusView(APIView):
    """
    Which AI would serve this person, whether it is reachable, where it runs
    (on this network or in the cloud) and - if it cannot be used - why and
    what to do about it.
    """

    def get(self, request):
        from shared.llm import ai_status

        return Response(ai_status(request.user))


class ExplorationHistoryListView(APIView):
    """
    List recent explorations for the authenticated user.
    """

    def get(self, request):
        from .models import ExplorationHistory

        qs = ExplorationHistory.objects.filter(user=request.user)

        bookmarked = request.query_params.get("bookmarked")
        if bookmarked == "true":
            qs = qs.filter(is_bookmarked=True)

        explorations = qs[:20]
        data = [
            {
                "id": str(e.id),
                "user_input": e.user_input,
                "summary": e.summary,
                "category": e.category,
                "passage_count": len(e.passages),
                "is_bookmarked": e.is_bookmarked,
                "created_at": e.created_at.isoformat(),
            }
            for e in explorations
        ]
        return Response(data)


class ExplorationHistoryDetailView(APIView):
    """
    Retrieve a single saved exploration with full results.
    """

    def get(self, request, exploration_id):
        from .models import ExplorationHistory

        try:
            e = ExplorationHistory.objects.get(id=exploration_id, user=request.user)
        except ExplorationHistory.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "id": str(e.id),
                "user_input": e.user_input,
                "passages": e.passages,
                "prompts": e.prompts,
                "category": e.category,
                "summary": e.summary,
                "plans": e.plans,
                "is_bookmarked": e.is_bookmarked,
                "created_at": e.created_at.isoformat(),
            }
        )

    def delete(self, request, exploration_id):
        from .models import ExplorationHistory

        deleted, _ = ExplorationHistory.objects.filter(
            id=exploration_id, user=request.user
        ).delete()
        if not deleted:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExplorationBookmarkView(APIView):
    """
    Toggle bookmark status on an exploration.
    """

    def post(self, request, exploration_id):
        from .models import ExplorationHistory

        try:
            e = ExplorationHistory.objects.get(id=exploration_id, user=request.user)
        except ExplorationHistory.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        e.is_bookmarked = not e.is_bookmarked
        e.save(update_fields=["is_bookmarked"])
        return Response({"is_bookmarked": e.is_bookmarked})
