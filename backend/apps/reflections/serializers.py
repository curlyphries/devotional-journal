"""
Serializers for the Life Reflection system.
"""

from rest_framework import serializers

from .models import (
    AlignmentTrend,
    DailyReflection,
    DevotionalAudit,
    DevotionalPassage,
    FocusIntention,
    LifeArea,
    OpenThread,
    StudyGuideSession,
    ThreadPrompt,
    UserJourney,
)


class LifeAreaSerializer(serializers.ModelSerializer):
    """Serializer for LifeArea reference data."""

    class Meta:
        model = LifeArea
        fields = [
            "code",
            "name",
            "description",
            "icon",
            "scripture_tags",
            "reflection_prompts",
            "display_order",
        ]


class UserJourneySerializer(serializers.ModelSerializer):
    """Serializer for UserJourney."""

    progress_percentage = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    specific_struggle = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = UserJourney
        fields = [
            "id",
            "title",
            "duration_days",
            "started_at",
            "goal_categories",
            "goal_statement",
            "success_definition",
            "focus_areas",
            "specific_struggle",
            "reading_mode",
            "reading_plan",
            "custom_readings",
            "current_day",
            "status",
            "completed_at",
            "completion_reflection",
            "next_journey",
            "progress_percentage",
            "days_remaining",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "started_at"]

    def create(self, validated_data):
        specific_struggle = validated_data.pop("specific_struggle", None)
        journey = UserJourney.objects.create(**validated_data)
        if specific_struggle:
            journey.set_specific_struggle(specific_struggle)
            journey.save()
        return journey

    def update(self, instance, validated_data):
        specific_struggle = validated_data.pop("specific_struggle", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if specific_struggle is not None:
            instance.set_specific_struggle(specific_struggle)
        instance.save()
        return instance


class UserJourneyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new journey."""

    specific_struggle = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = UserJourney
        fields = [
            "title",
            "duration_days",
            "goal_categories",
            "goal_statement",
            "success_definition",
            "focus_areas",
            "specific_struggle",
            "reading_mode",
            "reading_plan",
            "custom_readings",
        ]

    def create(self, validated_data):
        specific_struggle = validated_data.pop("specific_struggle", None)
        user = self.context["request"].user
        journey = UserJourney.objects.create(user=user, **validated_data)
        if specific_struggle:
            journey.set_specific_struggle(specific_struggle)
            journey.save()
        return journey


class DailyReflectionSerializer(serializers.ModelSerializer):
    """Serializer for DailyReflection."""

    reflection_content = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    gratitude_note = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    struggle_note = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    tomorrow_intention = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    reflection = serializers.SerializerMethodField()
    gratitude = serializers.SerializerMethodField()
    struggle = serializers.SerializerMethodField()
    intention = serializers.SerializerMethodField()

    class Meta:
        model = DailyReflection
        fields = [
            "id",
            "journey",
            "date",
            "scripture_reference",
            "scripture_themes",
            "reflection_content",
            "reflection",
            "area_scores",
            "gratitude_note",
            "gratitude",
            "struggle_note",
            "struggle",
            "tomorrow_intention",
            "intention",
            "ai_insight",
            "ai_provider_used",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "scripture_themes",
            "ai_insight",
            "ai_provider_used",
            "created_at",
            "updated_at",
        ]

    def get_reflection(self, obj):
        """Return decrypted reflection content."""
        return obj.get_reflection()

    def get_gratitude(self, obj):
        return obj.get_gratitude_note()

    def get_struggle(self, obj):
        return obj.get_struggle_note()

    def get_intention(self, obj):
        return obj.get_tomorrow_intention()

    def _apply_encrypted_fields(self, instance, validated_data):
        reflection_content = validated_data.pop("reflection_content", None)
        gratitude = validated_data.pop("gratitude_note", None)
        struggle = validated_data.pop("struggle_note", None)
        intention = validated_data.pop("tomorrow_intention", None)
        if reflection_content is not None:
            instance.set_reflection(reflection_content)
        if gratitude is not None:
            instance.set_gratitude_note(gratitude)
        if struggle is not None:
            instance.set_struggle_note(struggle)
        if intention is not None:
            instance.set_tomorrow_intention(intention)

    def create(self, validated_data):
        user = self.context["request"].user
        reflection = DailyReflection.objects.create(
            user=user,
            **{
                k: v
                for k, v in validated_data.items()
                if k
                not in (
                    "reflection_content",
                    "gratitude_note",
                    "struggle_note",
                    "tomorrow_intention",
                )
            },
        )
        self._apply_encrypted_fields(reflection, validated_data)
        reflection.save()
        return reflection

    def update(self, instance, validated_data):
        self._apply_encrypted_fields(instance, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DailyReflectionCreateSerializer(serializers.Serializer):
    """Serializer for creating a daily reflection."""

    journey = serializers.PrimaryKeyRelatedField(
        queryset=UserJourney.objects.all(), required=False, allow_null=True
    )
    date = serializers.DateField()
    scripture_reference = serializers.CharField(
        max_length=200, required=False, allow_blank=True
    )
    reflection_content = serializers.CharField(required=False, allow_blank=True)
    area_scores = serializers.JSONField(required=False, default=dict)
    gratitude_note = serializers.CharField(required=False, allow_blank=True)
    struggle_note = serializers.CharField(required=False, allow_blank=True)
    tomorrow_intention = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        user = self.context["request"].user
        reflection_content = validated_data.pop("reflection_content", None)
        gratitude = validated_data.pop("gratitude_note", None)
        struggle = validated_data.pop("struggle_note", None)
        intention = validated_data.pop("tomorrow_intention", None)
        reflection = DailyReflection.objects.create(user=user, **validated_data)
        if reflection_content:
            reflection.set_reflection(reflection_content)
        if gratitude:
            reflection.set_gratitude_note(gratitude)
        if struggle:
            reflection.set_struggle_note(struggle)
        if intention:
            reflection.set_tomorrow_intention(intention)
        reflection.save()
        return reflection


class AlignmentTrendSerializer(serializers.ModelSerializer):
    """Serializer for AlignmentTrend."""

    class Meta:
        model = AlignmentTrend
        fields = [
            "id",
            "journey",
            "period_type",
            "period_start",
            "period_end",
            "area_averages",
            "area_deltas",
            "ai_summary",
            "patterns",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class TodayReflectionSerializer(serializers.Serializer):
    """
    Serializer for the /reflections/today/ endpoint.
    Returns today's scripture, existing reflection (if any), and thread prompts.
    """

    date = serializers.DateField()
    scripture = serializers.DictField()
    existing_reflection = DailyReflectionSerializer(allow_null=True)
    journey = UserJourneySerializer(allow_null=True)
    thread_prompts = serializers.ListField(child=serializers.DictField())
    entry_fields = serializers.ListField(child=serializers.DictField())


class OpenThreadSerializer(serializers.ModelSerializer):
    """Serializer for OpenThread."""

    summary = serializers.SerializerMethodField()
    original_context = serializers.SerializerMethodField()
    resolution_note = serializers.SerializerMethodField()
    days_since_mentioned = serializers.ReadOnlyField()
    needs_followup = serializers.ReadOnlyField()

    class Meta:
        model = OpenThread
        fields = [
            "id",
            "thread_type",
            "summary",
            "original_context",
            "related_life_area",
            "status",
            "created_at",
            "last_mentioned_at",
            "last_followup_at",
            "followup_count",
            "skip_count",
            "days_since_mentioned",
            "needs_followup",
            "resolved_at",
            "resolution_note",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "last_mentioned_at",
            "last_followup_at",
            "followup_count",
            "skip_count",
            "resolved_at",
        ]

    def get_summary(self, obj):
        return obj.get_summary()

    def get_original_context(self, obj):
        return obj.get_original_context()

    def get_resolution_note(self, obj):
        return obj.get_resolution_note()


class OpenThreadCreateSerializer(serializers.Serializer):
    """Serializer for creating an OpenThread manually."""

    thread_type = serializers.ChoiceField(choices=OpenThread.THREAD_TYPE_CHOICES)
    summary = serializers.CharField(max_length=200)
    original_context = serializers.CharField(required=False, allow_blank=True)
    related_life_area = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )
    journey_id = serializers.UUIDField(required=False, allow_null=True)

    def create(self, validated_data):
        user = self.context["request"].user
        summary = validated_data.pop("summary")
        original_context = validated_data.pop("original_context", "")
        journey_id = validated_data.pop("journey_id", None)

        thread = OpenThread(
            user=user,
            thread_type=validated_data["thread_type"],
            related_life_area=validated_data.get("related_life_area", ""),
        )

        if journey_id:
            thread.journey_id = journey_id

        thread.set_summary(summary)
        if original_context:
            thread.set_original_context(original_context)

        thread.save()
        return thread


class ThreadPromptSerializer(serializers.ModelSerializer):
    """Serializer for ThreadPrompt."""

    expanded_response = serializers.SerializerMethodField()
    thread_summary = serializers.SerializerMethodField()

    class Meta:
        model = ThreadPrompt
        fields = [
            "id",
            "thread",
            "thread_summary",
            "reflection",
            "prompt_text",
            "response",
            "expanded",
            "expanded_response",
            "shown_at",
            "responded_at",
        ]
        read_only_fields = ["id", "shown_at"]

    def get_expanded_response(self, obj):
        return obj.get_expanded_response()

    def get_thread_summary(self, obj):
        return obj.thread.get_summary()


class ThreadResponseSerializer(serializers.Serializer):
    """Serializer for responding to a thread prompt."""

    thread_id = serializers.UUIDField()
    response = serializers.ChoiceField(
        choices=["better", "same", "worse", "yes", "no", "skipped", "resolved"]
    )
    expanded_text = serializers.CharField(required=False, allow_blank=True)
    reflection_id = serializers.UUIDField(required=False, allow_null=True)


class FocusIntentionSerializer(serializers.ModelSerializer):
    """Serializer for FocusIntention."""

    intention_text = serializers.SerializerMethodField()
    is_active = serializers.ReadOnlyField()
    passages_count = serializers.SerializerMethodField()

    class Meta:
        model = FocusIntention
        fields = [
            "id",
            "period_type",
            "period_start",
            "period_end",
            "intention_text",
            "themes",
            "related_life_areas",
            "status",
            "passages_generated",
            "is_active",
            "passages_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "themes",
            "related_life_areas",
            "passages_generated",
            "created_at",
            "updated_at",
        ]

    def get_intention_text(self, obj):
        return obj.get_intention()

    def get_passages_count(self, obj):
        return obj.passages.count()


class FocusIntentionCreateSerializer(serializers.Serializer):
    """Serializer for creating a FocusIntention."""

    period_type = serializers.ChoiceField(
        choices=["day", "week", "month"], default="week"
    )
    intention = serializers.CharField(max_length=1000, required=False)
    intention_text = serializers.CharField(max_length=1000, required=False)
    themes = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    journey_id = serializers.UUIDField(required=False, allow_null=True)

    def validate(self, data):
        # Accept either 'intention' or 'intention_text'
        intention = data.get("intention") or data.get("intention_text")
        if not intention:
            raise serializers.ValidationError({"intention": "This field is required."})
        data["intention"] = intention
        return data

    def validate_period_type(self, value):
        # Check if user already has an active intention for this period
        user = self.context["request"].user
        from django.utils import timezone

        today = timezone.now().date()

        existing = FocusIntention.objects.filter(
            user=user,
            period_type=value,
            status="active",
            period_start__lte=today,
            period_end__gte=today,
        ).exists()

        if existing:
            raise serializers.ValidationError(
                f"You already have an active {value} focus intention."
            )
        return value

    def create(self, validated_data):
        from datetime import timedelta

        from django.utils import timezone

        from .crew.agents import DevotionalCurator

        user = self.context["request"].user
        period_type = validated_data["period_type"]
        intention_text = validated_data["intention"]
        provided_themes = validated_data.get("themes", [])
        journey_id = validated_data.get("journey_id")

        today = timezone.now().date()

        # Calculate period dates
        if period_type == "day":
            period_start = today
            period_end = today
            num_passages = 1
        elif period_type == "week":
            # Start from today, end in 7 days
            period_start = today
            period_end = today + timedelta(days=6)
            num_passages = 7
        else:  # month
            period_start = today
            period_end = today + timedelta(days=29)
            num_passages = 30

        # Create the intention
        intention = FocusIntention(
            user=user,
            period_type=period_type,
            period_start=period_start,
            period_end=period_end,
            status="active",
        )

        if journey_id:
            intention.journey_id = journey_id

        intention.set_intention(intention_text)
        intention.save()

        # Use provided themes or extract with AI
        curator = DevotionalCurator()
        if provided_themes:
            themes = provided_themes
        else:
            themes = curator.extract_themes(intention_text)
        life_areas = curator.suggest_life_areas(intention_text, themes)

        intention.themes = themes
        intention.related_life_areas = life_areas
        intention.save()

        # Generate devotional passages asynchronously (or sync for now)
        self._generate_passages(
            intention, curator, intention_text, period_type, themes, num_passages
        )

        return intention

    def _generate_passages(
        self, intention, curator, intention_text, period_type, themes, num_passages
    ):
        """Generate devotional passages for the intention."""
        from datetime import timedelta

        passages_data = curator.curate_passages(
            intention_text, period_type, themes, num_passages
        )

        for i, passage_data in enumerate(passages_data):
            scheduled_date = intention.period_start + timedelta(days=i)

            DevotionalPassage.objects.create(
                focus_intention=intention,
                user=intention.user,
                sequence_number=i + 1,
                scheduled_date=scheduled_date,
                scripture_reference=passage_data.get("scripture_reference", "Unknown"),
                scripture_text=passage_data.get("scripture_text", ""),
                translation=passage_data.get("translation", "NIV"),
                stylized_quote=passage_data.get("stylized_quote", ""),
                context_note=passage_data.get("context_note", ""),
                connection_to_focus=passage_data.get("connection_to_focus", ""),
                reflection_prompts=passage_data.get("reflection_prompts", []),
                application_suggestions=passage_data.get("application_suggestions", []),
            )

        intention.passages_generated = True
        intention.save(update_fields=["passages_generated"])


class DevotionalPassageSerializer(serializers.ModelSerializer):
    """Serializer for DevotionalPassage."""

    user_reflection = serializers.SerializerMethodField()

    class Meta:
        model = DevotionalPassage
        fields = [
            "id",
            "focus_intention",
            "sequence_number",
            "scheduled_date",
            "scripture_reference",
            "scripture_text",
            "translation",
            "stylized_quote",
            "context_note",
            "connection_to_focus",
            "reflection_prompts",
            "application_suggestions",
            "is_read",
            "read_at",
            "user_reflection",
            "reflection_saved_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "focus_intention",
            "sequence_number",
            "scheduled_date",
            "scripture_reference",
            "scripture_text",
            "translation",
            "stylized_quote",
            "context_note",
            "connection_to_focus",
            "reflection_prompts",
            "application_suggestions",
            "created_at",
        ]

    def get_user_reflection(self, obj):
        return obj.get_user_reflection()


class DevotionalPassageReflectionSerializer(serializers.Serializer):
    """Serializer for saving a reflection on a devotional passage."""

    reflection = serializers.CharField(max_length=5000)

    def update(self, instance, validated_data):
        instance.set_user_reflection(validated_data["reflection"])
        instance.mark_read()
        instance.save()
        return instance


class TodayDevotionalSerializer(serializers.Serializer):
    """Serializer for today's devotional content."""

    active_intentions = FocusIntentionSerializer(many=True)
    todays_passages = DevotionalPassageSerializer(many=True)
    has_daily_focus = serializers.BooleanField()
    has_weekly_focus = serializers.BooleanField()
    has_monthly_focus = serializers.BooleanField()


class StudyGuideSessionSerializer(serializers.ModelSerializer):
    """Serializer for persistent deep-dive study sessions."""

    progress_percentage = serializers.ReadOnlyField()
    total_days = serializers.ReadOnlyField()
    next_day = serializers.ReadOnlyField()
    source_passage_reference = serializers.SerializerMethodField()
    source_journal_date = serializers.SerializerMethodField()

    class Meta:
        model = StudyGuideSession
        fields = [
            "id",
            "source_type",
            "source_reference",
            "source_passage",
            "source_journal_entry",
            "source_passage_reference",
            "source_journal_date",
            "guide_data",
            "completed_days",
            "day_notes",
            "status",
            "started_at",
            "last_activity_at",
            "completed_at",
            "total_days",
            "next_day",
            "progress_percentage",
        ]
        read_only_fields = [
            "id",
            "source_type",
            "source_reference",
            "source_passage",
            "source_journal_entry",
            "source_passage_reference",
            "source_journal_date",
            "guide_data",
            "completed_days",
            "day_notes",
            "started_at",
            "last_activity_at",
            "completed_at",
            "total_days",
            "next_day",
            "progress_percentage",
        ]

    def get_source_passage_reference(self, obj):
        if obj.source_passage:
            return obj.source_passage.scripture_reference
        return ""

    def get_source_journal_date(self, obj):
        if obj.source_journal_entry:
            return str(obj.source_journal_entry.date)
        return ""


class StudyGuideSessionDaySerializer(serializers.Serializer):
    """Serializer for marking study-plan day progress."""

    day = serializers.IntegerField(min_value=1, max_value=31)
    completed = serializers.BooleanField(default=True)
    note = serializers.CharField(max_length=2000, required=False, allow_blank=True)


class DevotionalAuditSerializer(serializers.ModelSerializer):
    """Serializer for DevotionalAudit model."""

    passage_reference = serializers.CharField(
        source="devotional_passage.scripture_reference", read_only=True
    )
    passage_date = serializers.DateField(
        source="devotional_passage.scheduled_date", read_only=True
    )
    user_email = serializers.EmailField(
        source="devotional_passage.user.email", read_only=True
    )
    reviewer_email = serializers.EmailField(
        source="reviewed_by.email", read_only=True, allow_null=True
    )
    overall_score = serializers.SerializerMethodField()

    class Meta:
        model = DevotionalAudit
        fields = [
            "id",
            "devotional_passage",
            "passage_reference",
            "passage_date",
            "user_email",
            "scripture_accuracy_score",
            "scripture_warnings",
            "relevance_score",
            "theological_accuracy",
            "user_rating",
            "user_feedback",
            "reported_issue",
            "audit_status",
            "reviewed_by",
            "reviewer_email",
            "review_notes",
            "corrected_content",
            "created_at",
            "reviewed_at",
            "overall_score",
        ]
        read_only_fields = ["id", "created_at", "devotional_passage"]

    def get_overall_score(self, obj):
        return obj.calculate_overall_score()


class DevotionalAuditReviewSerializer(serializers.Serializer):
    """Serializer for submitting a manual review."""

    theological_accuracy = serializers.BooleanField(required=False)
    review_notes = serializers.CharField(
        max_length=2000, required=False, allow_blank=True
    )
    corrected_content = serializers.JSONField(required=False)
    status = serializers.ChoiceField(
        choices=["verified", "flagged", "corrected"], required=False
    )
    apply_corrections = serializers.BooleanField(default=False)
