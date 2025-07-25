from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Conversation, Message
User = get_user_model()

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
    status = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id', 'conversation', 'sender',
            'message_body', 'sent_at', 'is_read', 'preview', 'status'
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
    def get_status(self, obj):
        return "Read" if obj.is_read else "Unread"


# === Conversation Serializer with nested messages and participants ===
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants',
            'created_at', 'messages', 'status'
        ]
    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data

    def get_status(self, obj):
        # Example logic: show number of unread messages
        user = self.context['request'].user
        unread_count = obj.messages.filter(is_read=False, sender__isnull=False).exclude(sender=user).count()
        return f"{unread_count} unread message(s)" if unread_count > 0 else "No unread messages"


# === Message Serializer for CREATE (POST) operations ===
class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'conversation', 'message_body'
        ]
    def create(self, validated_data):
        sender = self.context['request'].user
       
    # Remove sender if it's already in validated_data
        validated_data.pop('sender', None)
        
        return Message.objects.create(sender=sender, **validated_data)
# === Conversation Serializer for CREATE operations ===
class CreateConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            'participants'
        ]
