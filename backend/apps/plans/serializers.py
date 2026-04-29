"""
Serializers for reading plans.
"""
from rest_framework import serializers

from .models import ReadingPlan, ReadingPlanDay, UserPlanEnrollment


class ReadingPlanDaySerializer(serializers.ModelSerializer):
    theme = serializers.SerializerMethodField()

    class Meta:
        model = ReadingPlanDay
        fields = ['id', 'day_number', 'passages', 'theme', 'reflection_prompts_seed']

    def get_theme(self, obj):
        request = self.context.get('request')
        language = 'en'
        if request and request.user.is_authenticated:
            language = request.user.language_preference
        return obj.get_theme(language)


class ReadingPlanSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ReadingPlan
        fields = ['id', 'title', 'description', 'duration_days', 'category', 'is_premium', 'created_at']

    def get_title(self, obj):
        request = self.context.get('request')
        language = 'en'
        if request and request.user.is_authenticated:
            language = request.user.language_preference
        return obj.get_title(language)

    def get_description(self, obj):
        request = self.context.get('request')
        language = 'en'
        if request and request.user.is_authenticated:
            language = request.user.language_preference
        return obj.get_description(language)


class ReadingPlanDetailSerializer(ReadingPlanSerializer):
    days = ReadingPlanDaySerializer(many=True, read_only=True)

    class Meta(ReadingPlanSerializer.Meta):
        fields = ReadingPlanSerializer.Meta.fields + ['days']


class UserPlanEnrollmentSerializer(serializers.ModelSerializer):
    plan = ReadingPlanSerializer(read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()

    class Meta:
        model = UserPlanEnrollment
        fields = ['id', 'plan', 'started_at', 'current_day', 'completed_at', 'is_active', 'progress_percentage', 'is_completed']


class TodayReadingSerializer(serializers.Serializer):
    enrollment = UserPlanEnrollmentSerializer()
    day = ReadingPlanDaySerializer()
    passages_text = serializers.ListField(child=serializers.DictField())
    prompts = serializers.ListField(child=serializers.CharField())
