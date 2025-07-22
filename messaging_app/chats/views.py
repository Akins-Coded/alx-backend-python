from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOfConversation, IsOwnerOfMessage
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, CreateConversationSerializer,
    MessageSerializer, CreateMessageSerializer, UserSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOfConversation]

    filter_backends = [DjangoFilterBackend]
    filters = {
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
        user = self.request.user
        return Conversation.objects.filter(
            sender=user) | Conversation.objects.filter(recipient=user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOfMessage]
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
        user = self.request.user

        # Filter messages where user is sender or recipient in the conversation
        queryset = Message.objects.filter(
            conversation__sender=user
        ) | Message.objects.filter(
            conversation__recipient=user
        )

        # Optional status filter
        status_param = self.request.query_params.get('status')
        if status_param:
            status_param = status_param.lower()
            if status_param == 'read':
                queryset = queryset.filter(is_read=True)
            elif status_param == 'unread':
                queryset = queryset.filter(is_read=False)

        return queryset
