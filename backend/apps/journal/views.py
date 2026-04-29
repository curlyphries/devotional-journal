"""
Views for journal entries.
"""
import json

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.permissions import IsOwner
from .models import JournalEntry
from .serializers import JournalEntrySerializer, JournalEntryListSerializer
from apps.reflections.services import get_study_guide_service
from apps.reflections.models import StudyGuideSession


DJ_META_START = '<!-- DJ_META_START -->'
DJ_META_END = '<!-- DJ_META_END -->'


def _extract_journal_metadata(content: str) -> dict:
    """Extract optional JSON metadata block embedded in journal content."""
    start_idx = content.find(DJ_META_START)
    end_idx = content.find(DJ_META_END)
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        return {}

    raw_json = content[start_idx + len(DJ_META_START):end_idx].strip()
    if not raw_json:
        return {}

    try:
        meta = json.loads(raw_json)
        return meta if isinstance(meta, dict) else {}
    except json.JSONDecodeError:
        return {}


def _upsert_journal_study_session(user, entry: JournalEntry, guide: dict) -> StudyGuideSession:
    session = StudyGuideSession.objects.filter(
        user=user,
        source_type='journal_entry',
        source_journal_entry=entry,
    ).order_by('-started_at').first()

    source_reference = str(entry.date)
    if session:
        session.source_reference = source_reference
        session.guide_data = guide
        if session.status == 'archived':
            session.status = 'active'
        session.save(update_fields=['source_reference', 'guide_data', 'status', 'last_activity_at'])
        return session

    return StudyGuideSession.objects.create(
        user=user,
        source_type='journal_entry',
        source_reference=source_reference,
        source_journal_entry=entry,
        guide_data=guide,
    )


class JournalListCreateView(APIView):
    """
    List and create journal entries.
    """
    def get(self, request):
        entries = JournalEntry.objects.filter(user=request.user)

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        mood = request.query_params.get('mood')

        if date_from:
            entries = entries.filter(date__gte=date_from)
        if date_to:
            entries = entries.filter(date__lte=date_to)
        if mood:
            entries = entries.filter(mood_tag=mood)

        serializer = JournalEntryListSerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JournalEntrySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JournalDetailView(APIView):
    """
    Retrieve, update, or delete a journal entry.
    """
    permission_classes = [IsOwner]

    def get_object(self, entry_id, user):
        try:
            entry = JournalEntry.objects.get(id=entry_id, user=user)
            return entry
        except JournalEntry.DoesNotExist:
            return None

    def get(self, request, entry_id):
        entry = self.get_object(entry_id, request.user)
        if not entry:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JournalEntrySerializer(entry, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, entry_id):
        entry = self.get_object(entry_id, request.user)
        if not entry:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JournalEntrySerializer(entry, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, entry_id):
        entry = self.get_object(entry_id, request.user)
        if not entry:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JournalExportView(APIView):
    """
    Export all journal entries.
    """
    def get(self, request):
        entries = JournalEntry.objects.filter(user=request.user).order_by('date')

        export_data = []
        for entry in entries:
            export_data.append({
                'date': str(entry.date),
                'content': entry.get_content(),
                'mood': entry.mood_tag,
                'prompts': entry.reflection_prompts_used,
            })

        return Response({
            'entries': export_data,
            'count': len(export_data)
        })


class JournalEntryDeepDiveView(APIView):
    """
    Generate a personalized deep-dive study guide from a journal entry.
    """
    permission_classes = [IsOwner]

    def post(self, request, entry_id):
        try:
            entry = JournalEntry.objects.get(id=entry_id, user=request.user)
        except JournalEntry.DoesNotExist:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        content = entry.get_content()
        metadata = _extract_journal_metadata(content)

        from apps.reflections.models import FocusIntention

        today = timezone.now().date()
        active_focus = FocusIntention.objects.filter(
            user=request.user,
            status='active',
            period_start__lte=today,
            period_end__gte=today,
        ).order_by('-period_start').first()

        source_context = {
            'entry_date': str(entry.date),
            'mood': entry.mood_tag,
            'journal_content': content,
            'reflection_prompts_used': entry.reflection_prompts_used,
            'linked_passage': metadata.get('passage'),
            'linked_theme': metadata.get('theme'),
            'linked_ai_insight': metadata.get('aiInsight'),
            'extra_context': request.data.get('context', ''),
        }

        user_context = {
            'focus_intention': active_focus.intention_text if active_focus else '',
            'focus_themes': active_focus.themes if active_focus else [],
            'related_life_areas': active_focus.related_life_areas if active_focus else [],
        }

        guide = get_study_guide_service().generate_study_guide(
            source_type='journal_entry',
            source_context=source_context,
            user_context=user_context,
        )

        session = _upsert_journal_study_session(request.user, entry, guide)

        guide = {
            **guide,
            'study_session_id': str(session.id),
            'study_progress': {
                'status': session.status,
                'total_days': session.total_days,
                'completed_days': session.completed_days,
                'next_day': session.next_day,
                'progress_percentage': session.progress_percentage,
            },
        }

        return Response(guide)
