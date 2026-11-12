"""
Serializers for journal entries.
"""

from rest_framework import serializers

from .models import JournalEntry


class JournalEntrySerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)
    decrypted_content = serializers.SerializerMethodField(read_only=True)
    focus_intention_id = serializers.UUIDField(
        source="focus_intention.id", read_only=True
    )

    class Meta:
        model = JournalEntry
        fields = [
            "id",
            "date",
            "plan_enrollment",
            "plan_day",
            "focus_intention_id",
            "focus_themes",
            "content",
            "decrypted_content",
            "reflection_prompts_used",
            "mood_tag",
            "is_private",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "focus_intention_id", "created_at", "updated_at"]

    def get_decrypted_content(self, obj):
        return obj.get_content()

    def validate_plan_enrollment(self, value):
        # A related object must belong to the person making the request.
        if value is not None and value.user_id != self.context["request"].user.id:
            raise serializers.ValidationError("That plan enrollment is not yours.")
        return value

    def create(self, validated_data):
        from django.utils import timezone

        from apps.reflections.models import FocusIntention

        content = validated_data.pop("content")
        user = self.context["request"].user

        today = timezone.now().date()
        active_focus = (
            FocusIntention.objects.filter(
                user=user,
                status="active",
                period_start__lte=today,
                period_end__gte=today,
            )
            .order_by("-period_start")
            .first()
        )

        entry = JournalEntry(user=user, **validated_data)
        if active_focus:
            entry.focus_intention = active_focus
            entry.focus_themes = active_focus.themes or []
        entry.set_content(content)
        entry.save()
        return entry

    def update(self, instance, validated_data):
        if "content" in validated_data:
            content = validated_data.pop("content")
            instance.set_content(content)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class JournalEntryListSerializer(serializers.ModelSerializer):
    content_preview = serializers.SerializerMethodField()
    has_feedback = serializers.SerializerMethodField()
    scripture_reference = serializers.SerializerMethodField()

    class Meta:
        model = JournalEntry
        fields = [
            "id",
            "date",
            "mood_tag",
            "focus_themes",
            "content_preview",
            "has_feedback",
            "scripture_reference",
            "created_at",
        ]

    def get_content_preview(self, obj):
        from .feedback import strip_metadata

        # Never leak the embedded metadata block into a preview.
        content = strip_metadata(obj.get_content())
        if len(content) > 300:
            return content[:300] + "..."
        return content

    def _current_feedback(self, obj):
        # The list view prefetches this as `current_feedback`.
        records = getattr(obj, "current_feedback", None)
        if records is None:
            records = list(obj.feedback_records.filter(is_current=True)[:1])
        return records[0] if records else None

    def get_has_feedback(self, obj):
        return self._current_feedback(obj) is not None

    def get_scripture_reference(self, obj):
        feedback = self._current_feedback(obj)
        return (feedback.scripture_reference or None) if feedback else None
