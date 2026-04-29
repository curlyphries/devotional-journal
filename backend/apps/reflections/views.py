"""
Views for the Life Reflection system.
"""
import logging
from datetime import date

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    LifeArea, UserJourney, DailyReflection, AlignmentTrend, 
    OpenThread, ThreadPrompt, FocusIntention, DevotionalPassage, StudyGuideSession
)
from .serializers import (
    LifeAreaSerializer,
    UserJourneySerializer,
    UserJourneyCreateSerializer,
    DailyReflectionSerializer,
    DailyReflectionCreateSerializer,
    AlignmentTrendSerializer,
    OpenThreadSerializer,
    OpenThreadCreateSerializer,
    ThreadPromptSerializer,
    ThreadResponseSerializer,
    FocusIntentionSerializer,
    FocusIntentionCreateSerializer,
    DevotionalPassageSerializer,
    DevotionalPassageReflectionSerializer,
    StudyGuideSessionSerializer,
    StudyGuideSessionDaySerializer,
)
from .services import (
    get_theme_service, get_insight_service,
    get_thread_detection_service, get_thread_followup_service,
    get_study_guide_service,
)
from .crew import get_crew
from .crew.agents import DevotionalCurator

logger = logging.getLogger(__name__)


def _upsert_study_session(
    *,
    user,
    source_type: str,
    source_reference: str,
    guide: dict,
    source_passage: DevotionalPassage = None,
    source_journal_entry=None,
):
    filters = {
        'user': user,
        'source_type': source_type,
    }

    if source_passage is not None:
        filters['source_passage'] = source_passage
    if source_journal_entry is not None:
        filters['source_journal_entry'] = source_journal_entry

    session = StudyGuideSession.objects.filter(**filters).order_by('-started_at').first()
    if session:
        session.source_reference = source_reference
        session.guide_data = guide
        if session.status == 'archived':
            session.status = 'active'
        session.save(update_fields=['source_reference', 'guide_data', 'status', 'last_activity_at'])
        return session

    return StudyGuideSession.objects.create(
        user=user,
        source_type=source_type,
        source_reference=source_reference,
        source_passage=source_passage,
        source_journal_entry=source_journal_entry,
        guide_data=guide,
    )


class LifeAreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for LifeArea reference data.
    Read-only - life areas are pre-seeded.
    """
    queryset = LifeArea.objects.filter(is_active=True)
    serializer_class = LifeAreaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class UserJourneyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user journeys.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserJourney.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserJourneyCreateSerializer
        return UserJourneySerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get the user's active journey."""
        journey = self.get_queryset().filter(status='active').first()
        if journey:
            serializer = self.get_serializer(journey)
            return Response(serializer.data)
        return Response({'detail': 'No active journey'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def advance_day(self, request, pk=None):
        """Advance the journey to the next day."""
        journey = self.get_object()
        journey.current_day += 1
        journey.save()
        serializer = self.get_serializer(journey)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark the journey as completed."""
        journey = self.get_object()
        journey.status = 'completed'
        journey.completed_at = timezone.now()
        journey.save()
        serializer = self.get_serializer(journey)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """Pause the journey."""
        journey = self.get_object()
        journey.status = 'paused'
        journey.save()
        serializer = self.get_serializer(journey)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        """Resume a paused journey."""
        journey = self.get_object()
        journey.status = 'active'
        journey.save()
        serializer = self.get_serializer(journey)
        return Response(serializer.data)


class DailyReflectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing daily reflections.
    """
    serializer_class = DailyReflectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyReflection.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return DailyReflectionCreateSerializer
        return DailyReflectionSerializer

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's reflection."""
        today = date.today()
        reflection = self.get_queryset().filter(reflection_date=today).first()
        if reflection:
            serializer = self.get_serializer(reflection)
            return Response(serializer.data)
        return Response({'detail': 'No reflection for today'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='by-date/(?P<date_str>[0-9-]+)')
    def by_date(self, request, date_str=None):
        """Get reflection by date."""
        try:
            reflection_date = date.fromisoformat(date_str)
        except ValueError:
            return Response({'detail': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        
        reflection = self.get_queryset().filter(reflection_date=reflection_date).first()
        if reflection:
            serializer = self.get_serializer(reflection)
            return Response(serializer.data)
        return Response({'detail': 'No reflection for this date'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def generate_insight(self, request, pk=None):
        """Generate AI insight for a reflection."""
        reflection = self.get_object()
        crew = get_crew()
        
        context = {
            'gratitude': reflection.get_gratitude_note() if reflection.encrypted_gratitude else '',
            'struggle': reflection.get_struggle_note() if reflection.encrypted_struggle else '',
            'intention': reflection.get_tomorrow_intention() if reflection.encrypted_intention else '',
            'alignment_score': reflection.alignment_score,
        }
        
        insight = crew.generate_daily_insight(context)
        
        if insight:
            reflection.ai_insight = insight
            reflection.save()
            serializer = self.get_serializer(reflection)
            return Response(serializer.data)
        
        return Response({'error': 'Failed to generate insight'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class AlignmentTrendViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing alignment trends.
    """
    serializer_class = AlignmentTrendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AlignmentTrend.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def weekly(self, request):
        """Get weekly trends."""
        trends = self.get_queryset().filter(period_type='week').order_by('-period_start')[:4]
        serializer = self.get_serializer(trends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """Get monthly trends."""
        trends = self.get_queryset().filter(period_type='month').order_by('-period_start')[:12]
        serializer = self.get_serializer(trends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-area/(?P<area_code>[a-z_]+)')
    def by_area(self, request, area_code=None):
        """Get trends for a specific life area."""
        trends = self.get_queryset().filter(life_area__code=area_code).order_by('-period_start')[:12]
        serializer = self.get_serializer(trends, many=True)
        return Response(serializer.data)


class OpenThreadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing open threads.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OpenThread.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OpenThreadCreateSerializer
        return OpenThreadSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active threads."""
        threads = self.get_queryset().filter(status='open')
        serializer = OpenThreadSerializer(threads, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def needing_followup(self, request):
        """Get threads needing follow-up."""
        threads = [t for t in self.get_queryset().filter(status='open') if t.needs_followup]
        serializer = OpenThreadSerializer(threads, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get thread statistics."""
        qs = self.get_queryset()
        return Response({
            'total': qs.count(),
            'active': qs.filter(status='open').count(),
            'resolved': qs.filter(status='resolved').count(),
            'dropped': qs.filter(status='dropped').count(),
        })

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark a thread as resolved."""
        thread = self.get_object()
        resolution_note = request.data.get('resolution_note', '')
        thread.mark_resolved(resolution_note)
        serializer = OpenThreadSerializer(thread)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def defer(self, request, pk=None):
        """Defer a thread."""
        thread = self.get_object()
        thread.record_skip()
        serializer = OpenThreadSerializer(thread)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def drop(self, request, pk=None):
        """Drop a thread."""
        thread = self.get_object()
        thread.status = 'dropped'
        thread.save()
        serializer = OpenThreadSerializer(thread)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def respond(self, request):
        """Respond to a thread prompt."""
        serializer = ThreadResponseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result)


class ThreadPromptViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for thread prompts.
    """
    serializer_class = ThreadPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ThreadPrompt.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent prompts."""
        prompts = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(prompts, many=True)
        return Response(serializer.data)


class CrewView(APIView):
    """
    API view for interacting with the AI crew.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, action=None):
        if action == 'health':
            crew = get_crew()
            return Response({
                'status': 'healthy' if crew else 'unavailable',
                'agents': ['scripture_scholar', 'life_coach', 'prayer_guide', 'wisdom_synthesizer'] if crew else []
            })
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, action=None):
        crew = get_crew()
        if not crew:
            return Response({'error': 'AI crew unavailable'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if action == 'weekly-review':
            user = request.user
            reflections = DailyReflection.objects.filter(
                user=user,
                reflection_date__gte=timezone.now().date() - timezone.timedelta(days=7)
            )
            
            context = {
                'reflections': [
                    {
                        'date': str(r.reflection_date),
                        'alignment_score': r.alignment_score,
                        'gratitude': r.get_gratitude_note() if r.encrypted_gratitude else '',
                        'struggle': r.get_struggle_note() if r.encrypted_struggle else '',
                    }
                    for r in reflections
                ]
            }
            
            review = crew.generate_weekly_review(context)
            if review:
                return Response({'review': review})
            return Response({'error': 'Failed to generate review'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        elif action == 'monthly-recap':
            user = request.user
            trends = AlignmentTrend.objects.filter(
                user=user,
                period_type='week'
            ).order_by('-period_start')[:4]
            
            context = {
                'trends': [
                    {
                        'period': str(t.period_start),
                        'average_score': t.average_score,
                        'life_area': t.life_area.name if t.life_area else 'General',
                    }
                    for t in trends
                ]
            }
            
            recap = crew.generate_monthly_recap(context)
            if recap:
                return Response({'recap': recap})
            return Response({'error': 'Failed to generate recap'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        elif action == 'ask-agent':
            agent_name = request.data.get('agent')
            prompt = request.data.get('prompt')
            context = request.data.get('context', {})
            
            if not agent_name or not prompt:
                return Response(
                    {'error': 'agent and prompt are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            result = crew.ask_specific_agent(agent_name, prompt, context)
            if result:
                return Response({
                    'response': result,
                    'agent': agent_name,
                    'provider': 'ollama_crew'
                })
            return Response(
                {'error': f'Agent {agent_name} failed to respond'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)


class FocusIntentionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing focus intentions.
    Users can set daily, weekly, or monthly focus intentions.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FocusIntention.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return FocusIntentionCreateSerializer
        return FocusIntentionSerializer

    def create(self, request, *args, **kwargs):
        """Create a focus intention and return with proper serializer."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = FocusIntentionSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active focus intentions."""
        today = timezone.now().date()
        intentions = self.get_queryset().filter(
            status="active",
            period_start__lte=today,
            period_end__gte=today
        )
        serializer = FocusIntentionSerializer(intentions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's devotional content based on active intentions."""
        today = timezone.now().date()
        
        intentions = self.get_queryset().filter(
            status="active",
            period_start__lte=today,
            period_end__gte=today
        )
        
        todays_passages = DevotionalPassage.objects.filter(
            user=request.user,
            scheduled_date=today,
            focus_intention__in=intentions
        )
        
        period_types = set(intentions.values_list('period_type', flat=True))
        
        return Response({
            'active_intentions': FocusIntentionSerializer(intentions, many=True).data,
            'todays_passages': DevotionalPassageSerializer(todays_passages, many=True).data,
            'has_daily_focus': 'day' in period_types,
            'has_weekly_focus': 'week' in period_types,
            'has_monthly_focus': 'month' in period_types,
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a focus intention as completed."""
        intention = self.get_object()
        intention.mark_completed()
        serializer = FocusIntentionSerializer(intention)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def passages(self, request, pk=None):
        """Get all passages for a focus intention."""
        intention = self.get_object()
        passages = intention.passages.all()
        serializer = DevotionalPassageSerializer(passages, many=True)
        return Response(serializer.data)


class DevotionalPassageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for devotional passages.
    Passages are created automatically when a focus intention is set.
    """
    serializer_class = DevotionalPassageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DevotionalPassage.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a passage as read."""
        passage = self.get_object()
        passage.mark_read()
        serializer = self.get_serializer(passage)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reflect(self, request, pk=None):
        """Save a reflection on a passage."""
        passage = self.get_object()
        serializer = DevotionalPassageReflectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(passage, serializer.validated_data)
        return Response(DevotionalPassageSerializer(passage).data)

    @action(detail=True, methods=['post'])
    def deep_dive(self, request, pk=None):
        """Generate a personalized deep-dive study guide for this passage."""
        from apps.journal.models import JournalEntry

        passage = self.get_object()
        focus = passage.focus_intention
        extra_context = request.data.get('context', '')

        latest_journal_entry = JournalEntry.objects.filter(user=request.user).order_by('-date', '-created_at').first()
        latest_journal_excerpt = ''
        if latest_journal_entry:
            latest_journal_excerpt = latest_journal_entry.get_content()[:1200]

        source_context = {
            'scripture_reference': passage.scripture_reference,
            'scripture_text': passage.scripture_text,
            'translation': passage.translation,
            'context_note': passage.context_note,
            'connection_to_focus': passage.connection_to_focus,
            'reflection_prompts': passage.reflection_prompts,
            'application_suggestions': passage.application_suggestions,
            'user_reflection': passage.get_user_reflection(),
            'extra_context': extra_context,
        }

        user_context = {
            'focus_intention': focus.intention_text if focus else '',
            'focus_themes': focus.themes if focus else [],
            'related_life_areas': focus.related_life_areas if focus else [],
            'latest_journal_excerpt': latest_journal_excerpt,
        }

        guide = get_study_guide_service().generate_study_guide(
            source_type='devotional_passage',
            source_context=source_context,
            user_context=user_context,
        )

        session = _upsert_study_session(
            user=request.user,
            source_type='devotional_passage',
            source_reference=passage.scripture_reference,
            guide=guide,
            source_passage=passage,
        )

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

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's passages."""
        today = timezone.now().date()
        passages = self.get_queryset().filter(scheduled_date=today)
        serializer = self.get_serializer(passages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming passages for the next 7 days."""
        today = timezone.now().date()
        from datetime import timedelta
        end_date = today + timedelta(days=7)
        passages = self.get_queryset().filter(
            scheduled_date__gte=today,
            scheduled_date__lte=end_date
        )
        serializer = self.get_serializer(passages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_on_demand(self, request):
        """Generate a devotional passage on-demand for a specific topic."""
        topic = request.data.get('topic', '')
        themes = request.data.get('themes', [])
        scripture_reference = request.data.get('scripture_reference', None)
        
        if not topic:
            return Response(
                {'error': 'Topic is required for on-demand generation'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            curator = DevotionalCurator()
            
            # Generate a single devotional passage
            passages_data = curator.curate_passages(
                intention=topic,
                period_type='day',
                themes=themes or curator.extract_themes(topic),
                num_passages=1
            )
            
            if not passages_data:
                return Response(
                    {'error': 'Failed to generate devotional content'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            passage_data = passages_data[0]
            
            # Create the passage without a focus intention (on-demand)
            passage = DevotionalPassage.objects.create(
                user=request.user,
                focus_intention=None,  # No focus intention for on-demand
                sequence_number=1,
                scheduled_date=timezone.now().date(),
                scripture_reference=passage_data.get('scripture_reference', 'Unknown'),
                scripture_text=passage_data.get('scripture_text', ''),
                translation=passage_data.get('translation', 'NIV'),
                stylized_quote=passage_data.get('stylized_quote', ''),
                context_note=passage_data.get('context_note', ''),
                connection_to_focus=passage_data.get('connection_to_focus', ''),
                reflection_prompts=passage_data.get('reflection_prompts', []),
                application_suggestions=passage_data.get('application_suggestions', [])
            )
            
            serializer = DevotionalPassageSerializer(passage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"On-demand devotional generation failed: {e}")
            return Response(
                {'error': 'Failed to generate devotional content'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def provide_feedback(self, request, pk=None):
        """Allow users to provide feedback on devotional quality."""
        from .models import DevotionalAudit
        
        passage = self.get_object()
        rating = request.data.get('rating')
        feedback = request.data.get('feedback', '')
        issue = request.data.get('reported_issue', '')
        
        # Validate rating
        if rating is not None:
            try:
                rating = int(rating)
                if not 1 <= rating <= 5:
                    return Response(
                        {'error': 'Rating must be between 1 and 5'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {'error': 'Invalid rating value'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create or update audit record
        audit, created = DevotionalAudit.objects.get_or_create(
            devotional_passage=passage
        )
        
        if rating is not None:
            audit.user_rating = rating
        if feedback:
            audit.user_feedback = feedback
        if issue:
            audit.reported_issue = issue
            audit.flag_for_review(f"User reported issue: {issue}")
        
        audit.save()
        
        return Response({
            'message': 'Feedback recorded successfully',
            'audit_id': str(audit.id),
            'overall_score': audit.calculate_overall_score()
        })


class StudyGuideSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for persistent deep-dive study tracking."""
    serializer_class = StudyGuideSessionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = StudyGuideSession.objects.filter(user=self.request.user)
        status_filter = self.request.query_params.get('status')
        if status_filter in {'active', 'completed', 'archived'}:
            queryset = queryset.filter(status=status_filter)
        return queryset

    @action(detail=False, methods=['get'])
    def summary(self, request):
        sessions = StudyGuideSession.objects.filter(user=request.user)
        active_count = sessions.filter(status='active').count()
        completed_count = sessions.filter(status='completed').count()
        archived_count = sessions.filter(status='archived').count()

        avg_progress = 0
        session_list = list(sessions)
        if session_list:
            avg_progress = round(
                sum(session.progress_percentage for session in session_list) / len(session_list),
                1,
            )

        return Response({
            'total_sessions': len(session_list),
            'active_sessions': active_count,
            'completed_sessions': completed_count,
            'archived_sessions': archived_count,
            'average_progress_percentage': avg_progress,
        })

    @action(detail=True, methods=['post'])
    def mark_day(self, request, pk=None):
        session = self.get_object()
        serializer = StudyGuideSessionDaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        day = serializer.validated_data['day']
        completed = serializer.validated_data.get('completed', True)
        note = serializer.validated_data.get('note', '')

        total_days = session.total_days
        if total_days and day > total_days:
            return Response(
                {'error': f'Day must be between 1 and {total_days} for this guide.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session.mark_day(day=day, completed=completed, note=note)
        return Response(StudyGuideSessionSerializer(session).data)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        session = self.get_object()
        session.status = 'archived'
        session.save(update_fields=['status', 'last_activity_at'])
        return Response(StudyGuideSessionSerializer(session).data)

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        session = self.get_object()
        if session.completed_at:
            session.status = 'completed'
        else:
            session.status = 'active'
        session.save(update_fields=['status', 'last_activity_at'])
        return Response(StudyGuideSessionSerializer(session).data)


class DashboardStatsView(APIView):
    """
    Unified spiritual dashboard stats for the user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.db.models import Count
        from datetime import timedelta
        from apps.journal.models import JournalEntry
        from apps.bible.models import VerseHighlight
        from apps.plans.models import UserPlanEnrollment
        
        user = request.user
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        
        # Active Focus (FocusIntention: status, period_start, period_end, encrypted_intention/intention_text, themes, period_type, passages_generated)
        active_focus = FocusIntention.objects.filter(
            user=user,
            status="active",
            period_end__gte=today
        ).first()
        
        focus_data = None
        if active_focus:
            days_into_focus = (today - active_focus.period_start).days + 1
            total_days = (active_focus.period_end - active_focus.period_start).days + 1
            focus_data = {
                'intention': active_focus.intention_text,
                'themes': active_focus.themes,
                'period_type': active_focus.period_type,
                'day_number': days_into_focus,
                'total_days': total_days,
                'passages_count': active_focus.passages_generated,
                'passages_read': DevotionalPassage.objects.filter(
                    focus_intention=active_focus, is_read=True
                ).count(),
            }
        
        # Reading Plan Progress (UserPlanEnrollment: user, plan, started_at, current_day, completed_at, is_active)
        active_enrollment = UserPlanEnrollment.objects.filter(
            user=user,
            is_active=True
        ).select_related('plan').first()
        
        plan_data = None
        if active_enrollment:
            plan_data = {
                'plan_title': active_enrollment.plan.title_en,
                'current_day': active_enrollment.current_day,
                'total_days': active_enrollment.plan.duration_days,
                'completed_days': active_enrollment.current_day - 1,
            }
        
        # Journal Stats (JournalEntry: user, date, created_at)
        journal_entries_today = JournalEntry.objects.filter(user=user, date=today).count()
        journal_entries_week = JournalEntry.objects.filter(user=user, date__gte=week_start).count()
        journal_entries_month = JournalEntry.objects.filter(user=user, date__gte=month_start).count()
        
        # Calculate journal streak
        journal_dates = set(JournalEntry.objects.filter(user=user).values_list('date', flat=True))
        streak = 0
        check_date = today
        while check_date in journal_dates:
            streak += 1
            check_date -= timedelta(days=1)
        
        # Highlights Stats (VerseHighlight: user, book, chapter, verse_start, note, color, created_at)
        highlights_today = VerseHighlight.objects.filter(user=user, created_at__date=today).count()
        highlights_week = VerseHighlight.objects.filter(user=user, created_at__date__gte=week_start).count()
        
        recent_highlights = VerseHighlight.objects.filter(
            user=user, note__isnull=False
        ).exclude(note='').order_by('-created_at')[:3]
        
        highlights_with_notes = [{
            'book': h.book,
            'chapter': h.chapter,
            'verse': h.verse_start,
            'note': h.note[:100] + '...' if len(h.note) > 100 else h.note,
            'color': h.color,
        } for h in recent_highlights]
        
        # Daily Reflections (DailyReflection: user, date)
        reflections_week = DailyReflection.objects.filter(user=user, date__gte=week_start).count()
        
        # Open Threads (OpenThread: user, status)
        open_threads = OpenThread.objects.filter(user=user, status='open').count()
        
        # Life Area Trends (AlignmentTrend: area_averages JSON, area_deltas JSON, ai_summary, created_at)
        latest_trend = AlignmentTrend.objects.filter(user=user).order_by('-created_at').first()
        
        life_area_scores = []
        if latest_trend and latest_trend.area_averages:
            area_deltas = latest_trend.area_deltas or {}
            for area_name, score in latest_trend.area_averages.items():
                delta = area_deltas.get(area_name, 0)
                trend_dir = 'improving' if delta > 0 else ('declining' if delta < 0 else 'stable')
                life_area_scores.append({'area': area_name, 'score': score, 'trend': trend_dir})
        
        weekly_insight = None
        if latest_trend and latest_trend.ai_summary:
            weekly_insight = latest_trend.ai_summary
        
        return Response({
            'date': today.isoformat(),
            'greeting_name': user.display_name or 'Friend',
            'focus': focus_data,
            'reading_plan': plan_data,
            'stats': {
                'journal_streak': streak,
                'journal_today': journal_entries_today,
                'journal_week': journal_entries_week,
                'journal_month': journal_entries_month,
                'highlights_today': highlights_today,
                'highlights_week': highlights_week,
                'reflections_week': reflections_week,
                'open_threads': open_threads,
            },
            'recent_highlights': highlights_with_notes,
            'life_area_scores': life_area_scores,
            'weekly_insight': weekly_insight,
        })


class ThreadPromptPendingView(APIView):
    """
    Get pending thread prompts for the current user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from datetime import timedelta
        from django.utils import timezone
        from shared.encryption import decrypt_field
        
        user = request.user
        today = timezone.now().date()
        
        # Get open threads that need follow-up
        threads = OpenThread.objects.filter(
            user=user,
            status__in=['open', 'following_up']
        ).select_related('source_reflection')
        
        prompts = []
        for thread in threads:
            # Check if thread needs follow-up (at least 3 days old, not prompted today)
            days_since = (today - thread.created_at.date()).days
            if days_since < 3:
                continue
            
            # Check if already prompted today
            recent_prompt = ThreadPrompt.objects.filter(
                thread=thread,
                created_at__date=today
            ).exists()
            if recent_prompt:
                continue
            
            # Decrypt summary
            try:
                summary = decrypt_field(thread.encrypted_summary, user)
            except Exception:
                summary = "A topic you mentioned earlier"
            
            # Generate prompt text based on thread type
            prompt_text = self._generate_prompt_text(thread.thread_type, days_since)
            
            prompts.append({
                'id': str(thread.id),
                'thread_id': str(thread.id),
                'thread_type': thread.thread_type,
                'summary': summary,
                'prompt_text': prompt_text,
                'life_area': thread.related_life_area,
                'days_since': days_since,
                'followup_count': thread.followup_count,
            })
        
        # Limit to 2 prompts per session
        return Response(prompts[:2])
    
    def _generate_prompt_text(self, thread_type: str, days_since: int) -> str:
        prompts = {
            'struggle': f"You mentioned a challenge {days_since} days ago. How are things going with that?",
            'commitment': f"You made a commitment {days_since} days ago. How's your progress?",
            'question': f"You had a question {days_since} days ago. Did you find any clarity?",
            'relationship': f"You shared about a relationship {days_since} days ago. Any updates?",
            'decision': f"You mentioned a decision {days_since} days ago. Have you moved forward?",
            'confession': f"You shared something personal {days_since} days ago. How are you feeling about it now?",
        }
        return prompts.get(thread_type, f"Checking in on something from {days_since} days ago...")



class ThreadPromptRespondView(APIView):
    """
    Respond to a thread prompt.
    Supports both quick check-in format (better/same/worse/resolved) and legacy format.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, thread_id):
        from shared.encryption import encrypt_field
        
        user = request.user
        # Support both old format (action) and new format (response)
        response_status = request.data.get('response')  # better, same, worse, resolved
        expanded_text = request.data.get('expanded_text', '')
        action = request.data.get('action')  # Legacy: respond, resolved, skip
        
        try:
            thread = OpenThread.objects.get(id=thread_id, user=user)
        except OpenThread.DoesNotExist:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Handle new format (response status)
        if response_status in ['better', 'same', 'worse', 'resolved']:
            # Create a thread prompt record with the response
            ThreadPrompt.objects.create(
                user=user,
                thread=thread,
                encrypted_prompt="Quick check-in",
                encrypted_response=encrypt_field(f"{response_status}: {expanded_text}" if expanded_text else response_status, user),
            )
            thread.followup_count += 1
            thread.last_followup_at = timezone.now()
            
            if response_status == 'resolved':
                thread.status = 'resolved'
                thread.resolved_at = timezone.now()
            elif response_status == 'better':
                thread.status = 'progressing'
            elif response_status in ['same', 'worse']:
                thread.status = 'following_up'
            
            thread.save()
            return Response({'status': 'ok', 'thread_status': thread.status})
        
        # Handle legacy format (action)
        if action == 'respond':
            response_text = request.data.get('response', '')
            ThreadPrompt.objects.create(
                user=user,
                thread=thread,
                encrypted_prompt="Follow-up prompt",
                encrypted_response=encrypt_field(response_text, user) if response_text else None,
            )
            thread.followup_count += 1
            thread.status = 'progressing'
            thread.last_followup_at = timezone.now()
            thread.save()
            
        elif action == 'resolved':
            thread.status = 'resolved'
            thread.resolved_at = timezone.now()
            thread.save()
            
        elif action == 'skip':
            thread.skip_count += 1
            thread.last_followup_at = timezone.now()
            if thread.skip_count >= 3:
                thread.status = 'deferred'
            thread.save()
        
        return Response({'status': 'ok', 'thread_status': thread.status})


class MilestonesView(APIView):
    """
    Get user milestones and achievements.
    """
    permission_classes = [IsAuthenticated]

    MILESTONE_DEFINITIONS = [
        # Streak milestones
        {'id': 'streak_7', 'type': 'streak', 'title': 'Week Warrior', 'description': '7-day journal streak', 'target': 7},
        {'id': 'streak_30', 'type': 'streak', 'title': 'Monthly Master', 'description': '30-day journal streak', 'target': 30},
        {'id': 'streak_90', 'type': 'streak', 'title': 'Quarterly Champion', 'description': '90-day journal streak', 'target': 90},
        # Journal milestones
        {'id': 'journal_10', 'type': 'journal', 'title': 'Getting Started', 'description': 'Write 10 journal entries', 'target': 10},
        {'id': 'journal_50', 'type': 'journal', 'title': 'Consistent Writer', 'description': 'Write 50 journal entries', 'target': 50},
        {'id': 'journal_100', 'type': 'journal', 'title': 'Prolific Journaler', 'description': 'Write 100 journal entries', 'target': 100},
        # Highlight milestones
        {'id': 'highlight_25', 'type': 'highlight', 'title': 'Scripture Marker', 'description': 'Highlight 25 verses', 'target': 25},
        {'id': 'highlight_100', 'type': 'highlight', 'title': 'Verse Collector', 'description': 'Highlight 100 verses', 'target': 100},
        # Focus milestones
        {'id': 'focus_1', 'type': 'focus', 'title': 'First Focus', 'description': 'Complete your first focus intention', 'target': 1},
        {'id': 'focus_5', 'type': 'focus', 'title': 'Focused Growth', 'description': 'Complete 5 focus intentions', 'target': 5},
        {'id': 'focus_12', 'type': 'focus', 'title': 'Year of Focus', 'description': 'Complete 12 focus intentions', 'target': 12},
        # Reading milestones
        {'id': 'reading_plan_1', 'type': 'reading', 'title': 'Plan Starter', 'description': 'Complete a reading plan', 'target': 1},
        {'id': 'reading_plan_3', 'type': 'reading', 'title': 'Dedicated Reader', 'description': 'Complete 3 reading plans', 'target': 3},
    ]

    def get(self, request):
        from datetime import timedelta
        from apps.journal.models import JournalEntry
        from apps.bible.models import VerseHighlight
        from apps.plans.models import UserPlanEnrollment
        
        user = request.user
        today = date.today()
        
        # Calculate stats
        total_journal = JournalEntry.objects.filter(user=user).count()
        total_highlights = VerseHighlight.objects.filter(user=user).count()
        focus_completed = FocusIntention.objects.filter(user=user, status__in=["completed", "expired"]).count()
        plans_completed = UserPlanEnrollment.objects.filter(user=user, completed_at__isnull=False).count()
        
        # Calculate current and longest streak
        current_streak = 0
        longest_streak = 0
        check_date = today
        temp_streak = 0
        
        # Get all journal dates for efficiency
        journal_dates = set(
            JournalEntry.objects.filter(user=user)
            .values_list('created_at__date', flat=True)
        )
        
        # Calculate current streak
        while check_date in journal_dates:
            current_streak += 1
            check_date -= timedelta(days=1)
        
        # Calculate longest streak (simplified - check last 365 days)
        check_date = today
        for _ in range(365):
            if check_date in journal_dates:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0
            check_date -= timedelta(days=1)
        
        longest_streak = max(longest_streak, current_streak)
        
        # Build milestone progress
        progress_map = {
            'streak': current_streak,
            'journal': total_journal,
            'highlight': total_highlights,
            'focus': focus_completed,
            'reading': plans_completed,
        }
        
        # Find the NEXT milestone (closest to achieving, not yet achieved)
        next_milestone = None
        for milestone_def in self.MILESTONE_DEFINITIONS:
            progress = progress_map.get(milestone_def['type'], 0)
            if progress < milestone_def['target']:
                next_milestone = {
                    'id': milestone_def['id'],
                    'title': milestone_def['title'],
                    'description': milestone_def['description'],
                    'progress': progress,
                    'target': milestone_def['target'],
                    'percentage': round((progress / milestone_def['target']) * 100, 1),
                    'remaining': milestone_def['target'] - progress,
                    'type': milestone_def['type'],
                }
                break  # Take the first one (they're ordered by target size)
        
        recent_achievements = []
        total_achieved = 0
        
        for milestone_def in self.MILESTONE_DEFINITIONS:
            progress = progress_map.get(milestone_def['type'], 0)
            achieved = progress >= milestone_def['target']
            
            if achieved:
                total_achieved += 1
                if len(recent_achievements) < 4:
                    milestone = {
                        'id': milestone_def['id'],
                        'title': milestone_def['title'],
                        'description': milestone_def['description'],
                        'achieved': True,
                    }
                    recent_achievements.append(milestone)
        
        return Response({
            'next_milestone': next_milestone,
            'recent_achievements': recent_achievements,
            'stats': {
                'total_achieved': total_achieved,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'total_journal_entries': total_journal,
                'total_highlights': total_highlights,
                'focus_completed': focus_completed,
            }
        })


class GrowthDataView(APIView):
    """
    Get growth visualization data for the user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from datetime import timedelta
        from django.db.models import Count
        from django.db.models.functions import TruncWeek
        from apps.journal.models import JournalEntry
        from apps.bible.models import VerseHighlight
        
        user = request.user
        today = date.today()
        
        # Life Area Trends (AlignmentTrend: area_averages JSON, area_deltas JSON, created_at)
        life_areas = []
        latest_trend = AlignmentTrend.objects.filter(user=user).order_by('-created_at').first()
        previous_trend = None
        if latest_trend:
            previous_trend = AlignmentTrend.objects.filter(
                user=user, created_at__lt=latest_trend.created_at
            ).order_by('-created_at').first()
        
        if latest_trend and latest_trend.area_averages:
            prev_avgs = previous_trend.area_averages if previous_trend and previous_trend.area_averages else {}
            for area_name, score in latest_trend.area_averages.items():
                prev_score = prev_avgs.get(area_name, score)
                change = score - prev_score
                trend_dir = 'improving' if change > 0 else ('declining' if change < 0 else 'stable')
                life_areas.append({
                    'area': area_name,
                    'current_score': score,
                    'previous_score': prev_score,
                    'trend': trend_dir,
                    'change': change,
                })
        
        # Weekly Activity (last 8 weeks)
        eight_weeks_ago = today - timedelta(weeks=8)
        
        # JournalEntry uses 'date' field
        journal_by_week = dict(
            JournalEntry.objects.filter(
                user=user,
                date__gte=eight_weeks_ago
            ).annotate(
                week=TruncWeek('date')
            ).values('week').annotate(
                count=Count('id')
            ).values_list('week', 'count')
        )
        
        highlight_by_week = dict(
            VerseHighlight.objects.filter(
                user=user,
                created_at__date__gte=eight_weeks_ago
            ).annotate(
                week=TruncWeek('created_at')
            ).values('week').annotate(
                count=Count('id')
            ).values_list('week', 'count')
        )
        
        # DailyReflection uses 'date' field
        reflection_by_week = dict(
            DailyReflection.objects.filter(
                user=user,
                date__gte=eight_weeks_ago
            ).annotate(
                week=TruncWeek('date')
            ).values('week').annotate(
                count=Count('id')
            ).values_list('week', 'count')
        )
        
        weekly_activity = []
        for i in range(8):
            week_start = today - timedelta(weeks=7-i, days=today.weekday())
            week_label = week_start.strftime('%b %d')
            
            weekly_activity.append({
                'week': week_label,
                'journal_entries': journal_by_week.get(week_start, 0),
                'highlights': highlight_by_week.get(week_start, 0),
                'reflections': reflection_by_week.get(week_start, 0),
            })
        
        # Focus History
        focus_history = []
        focuses = FocusIntention.objects.filter(user=user).order_by('-created_at')[:10]
        for focus in focuses:
            focus_history.append({
                'intention': focus.intention_text,
                'period_type': focus.period_type,
                'completed': focus.status != 'active',
                'themes': focus.themes,
            })
        
        return Response({
            'life_areas': life_areas,
            'weekly_activity': weekly_activity,
            'focus_history': focus_history,
        })


class ScriptureInsightView(APIView):
    """
    Get scripture insights based on user's recent reflections and focus.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Get recent focus intentions
        recent_focus = FocusIntention.objects.filter(
            user=user,
            status='active'
        ).order_by('-created_at').first()
        
        # Get recent devotional passages
        recent_passages = DevotionalPassage.objects.filter(
            user=user
        ).order_by('-scheduled_date')[:5]
        
        insights = []
        for passage in recent_passages:
            insights.append({
                'scripture_reference': passage.scripture_reference,
                'scripture_text': passage.scripture_text,
                'connection': passage.connection_to_focus,
                'reflection_prompts': passage.reflection_prompts,
                'scheduled_date': passage.scheduled_date,
            })
        
        return Response({
            'current_focus': {
                'intention': recent_focus.intention_text if recent_focus else None,
                'themes': recent_focus.themes if recent_focus else [],
                'period_type': recent_focus.period_type if recent_focus else None,
            } if recent_focus else None,
            'insights': insights,
        })
