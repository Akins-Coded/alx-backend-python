from rest_framework import serializers
from .models import User, Conversation, Message


# === User Serializer (safe, excludes sensitive fields) ===
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email',
            'first_name', 'last_name',
            'phone_number', 'role'
        ]


# === Message Serializer for READ operations ===
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id', 'conversation', 'sender',
            'message_body', 'sent_at', 'is_read', 'preview'
        ]

    def get_preview(self, obj):
        # Return the first 20 characters of the message
        return obj.message_body[:20] + '...' if len(obj.message_body) > 20 else obj.message_body

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Message cannot be empty or whitespace."
                )
        if len(value) > 1000:
            raise serializers.ValidationError(
                "Message is too long (max 1000 characters)."
                )
        return value


# === Conversation Serializer with nested messages and participants ===
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants',
            'created_at', 'messages'
        ]


# === Message Serializer for CREATE (POST) operations ===
class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'conversation', 'sender', 'message_body'
        ]


# === Conversation Serializer for CREATE operations ===
class CreateConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            'participants'
        ]
