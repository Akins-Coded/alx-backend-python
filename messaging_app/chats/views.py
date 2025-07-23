from django.contrib.auth import get_user_model
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
from .auth import get_user_conversations, get_user_messages

User = get_user_model()


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
