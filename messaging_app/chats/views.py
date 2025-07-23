from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    CreateConversationSerializer,
    MessageSerializer,
    CreateMessageSerializer,
    UserSerializer
)
from .permissions import IsParticipantOfConversation
from .auth import get_user_conversations

User = get_user_model()


def get_user_messages(user, status=None):
    """
    Return messages where the user is either the sender or recipient in the conversation.
    Optionally filter by read/unread status.
    """
    queryset = Message.objects.filter(
        Q(conversation__sender=user) | Q(conversation__recipient=user)
    )

    if status:
        status = status.lower()
        if status == 'read':
            queryset = queryset.filter(is_read=True)
        elif status == 'unread':
            queryset = queryset.filter(is_read=False)

    return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'participants__user_id': ['exact'],
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateConversationSerializer
        return ConversationSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    def get_queryset(self):
        return get_user_conversations(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'conversation__conversation_id': ['exact'],
        'sender__user_id': ['exact'],
        'is_read': ['exact'],
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateMessageSerializer
        return MessageSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        return get_user_messages(self.request.user, status_param)
