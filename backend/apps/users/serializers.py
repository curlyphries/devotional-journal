"""
Serializers for user authentication and profile.
"""
from rest_framework import serializers

from .models import User


class MagicLinkRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class MagicLinkVerifySerializer(serializers.Serializer):
    token = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    # Don't expose the full API key, just show if it's set
    ai_api_key_set = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'display_name', 'language_preference', 'timezone',
            'ai_provider', 'ai_api_key_set', 'ai_model', 'ai_base_url',
            'created_at', 'last_active_at'
        ]
        read_only_fields = ['id', 'email', 'created_at', 'last_active_at', 'ai_api_key_set']
    
    def get_ai_api_key_set(self, obj):
        return bool(obj.ai_api_key)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['display_name', 'language_preference', 'timezone', 
                  'ai_provider', 'ai_api_key', 'ai_model', 'ai_base_url']


class AISettingsSerializer(serializers.Serializer):
    """Serializer for AI settings update with validation."""
    ai_provider = serializers.ChoiceField(choices=User.AI_PROVIDER_CHOICES)
    ai_api_key = serializers.CharField(required=False, allow_blank=True)
    ai_model = serializers.CharField(required=False, allow_blank=True)
    ai_base_url = serializers.CharField(required=False, allow_blank=True)
