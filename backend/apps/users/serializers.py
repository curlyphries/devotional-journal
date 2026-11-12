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
            "id",
            "email",
            "display_name",
            "language_preference",
            "timezone",
            "ai_provider",
            "ai_api_key_set",
            "ai_model",
            "ai_base_url",
            "allow_server_cloud_ai",
            "created_at",
            "last_active_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "created_at",
            "last_active_at",
            "ai_api_key_set",
        ]

    def get_ai_api_key_set(self, obj):
        return bool(obj.ai_api_key)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "display_name",
            "language_preference",
            "timezone",
            "ai_provider",
            "ai_api_key",
            "ai_model",
            "ai_base_url",
            "allow_server_cloud_ai",
        ]

    def validate_ai_base_url(self, value):
        from shared.errors import AppError
        from shared.llm import validate_ai_base_url

        try:
            return validate_ai_base_url(value)
        except AppError as exc:
            message = exc.message
            if exc.suggestion:
                message = f"{message} {exc.suggestion}"
            raise serializers.ValidationError(message)

    def validate(self, attrs):
        from django.conf import settings

        provider = attrs.get("ai_provider")
        if getattr(settings, "AI_LOCAL_ONLY", False) and provider in (
            "openai",
            "anthropic",
            "openrouter",
        ):
            raise serializers.ValidationError(
                {
                    "ai_provider": "This server only allows AI that runs on its own "
                    "network. Choose Ollama."
                }
            )
        return attrs

    def update(self, instance, validated_data):
        ai_api_key = validated_data.pop("ai_api_key", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if ai_api_key is not None:
            instance.set_ai_api_key(ai_api_key)
        instance.save()
        return instance


class AISettingsSerializer(serializers.Serializer):
    """Serializer for AI settings update with validation."""

    ai_provider = serializers.ChoiceField(choices=User.AI_PROVIDER_CHOICES)
    ai_api_key = serializers.CharField(required=False, allow_blank=True)
    ai_model = serializers.CharField(required=False, allow_blank=True)
    ai_base_url = serializers.CharField(required=False, allow_blank=True)
