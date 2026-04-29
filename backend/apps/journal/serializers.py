"""
Serializers for journal entries.
"""
from rest_framework import serializers

from .models import JournalEntry


class JournalEntrySerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)
    decrypted_content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JournalEntry
        fields = [
            'id', 'date', 'plan_enrollment', 'plan_day',
            'content', 'decrypted_content', 'reflection_prompts_used',
            'mood_tag', 'is_private', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_decrypted_content(self, obj):
        return obj.get_content()

    def create(self, validated_data):
        content = validated_data.pop('content')
        user = self.context['request'].user
        entry = JournalEntry(user=user, **validated_data)
        entry.set_content(content)
        entry.save()
        return entry

    def update(self, instance, validated_data):
        if 'content' in validated_data:
            content = validated_data.pop('content')
            instance.set_content(content)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class JournalEntryListSerializer(serializers.ModelSerializer):
    content_preview = serializers.SerializerMethodField()

    class Meta:
        model = JournalEntry
        fields = ['id', 'date', 'mood_tag', 'content_preview', 'created_at']

    def get_content_preview(self, obj):
        content = obj.get_content()
        if len(content) > 300:
            return content[:300] + '...'
        return content
