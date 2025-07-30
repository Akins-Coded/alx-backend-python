from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name']



class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    edited_by = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'receiver', 'content', 'timestamp',
            'is_read', 'edited', 'edited_by'
        ]
        
    def get_replies(self, obj):
        return MessageSerializer(obj.replies.all(), many=True).data

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user', 'message']


class MessageHistorySerializer(serializers.ModelSerializer):
    message = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MessageHistory
        fields = ['history_id', 'message', 'previous_body', 'edited_at']
        read_only_fields = ['history_id', 'edited_at']  