"""
Serializers for Bible data and highlights.
"""
from rest_framework import serializers
from .models import BibleTranslation, BibleVerse, VerseHighlight


class BibleTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleTranslation
        fields = ['code', 'name', 'language', 'is_public_domain']


class BibleVerseSerializer(serializers.ModelSerializer):
    translation_code = serializers.CharField(source='translation.code', read_only=True)

    class Meta:
        model = BibleVerse
        fields = ['book', 'book_name', 'chapter', 'verse', 'text', 'translation_code']


class PassageRequestSerializer(serializers.Serializer):
    translation = serializers.CharField(default='KJV')
    book = serializers.CharField()
    chapter = serializers.IntegerField()
    verse_start = serializers.IntegerField(required=False)
    verse_end = serializers.IntegerField(required=False)


class SearchRequestSerializer(serializers.Serializer):
    translation = serializers.CharField(default='KJV')
    query = serializers.CharField()
    limit = serializers.IntegerField(default=20, max_value=100)


class VerseHighlightSerializer(serializers.ModelSerializer):
    reference = serializers.ReadOnlyField()

    class Meta:
        model = VerseHighlight
        fields = [
            'id', 'book', 'chapter', 'verse_start', 'verse_end',
            'translation', 'color', 'note', 'reference',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
