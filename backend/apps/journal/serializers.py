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
    decrypted_content = serializers.SerializerMethodField()
    plan_day_info = serializers.SerializerMethodField()

    class Meta:
        model = JournalEntry
        fields = [
            "id",
            "date",
            "mood_tag",
            "focus_themes",
            "content_preview",
            "decrypted_content",
            "plan_day_info",
            "created_at",
        ]

    def get_content_preview(self, obj):
        content = obj.get_content()
        if len(content) > 300:
            return content[:300] + "..."
        return content

    def get_decrypted_content(self, obj):
        # Full decrypted content so the client can extract embedded AI-insight
        # metadata for the Insights timeline. Already encrypted at rest; this
        # endpoint is auth-scoped to the owning user.
        return obj.get_content()

    def get_plan_day_info(self, obj):
        if not obj.plan_day_id:
            return None
        day = obj.plan_day
        return {
            "passages": day.passages,
            "theme_en": day.theme_en,
            "theme_es": day.theme_es,
            "day_number": day.day_number,
        }
