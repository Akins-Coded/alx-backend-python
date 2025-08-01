from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination
from .filters import MessageFilter

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    CreateConversationSerializer,
    MessageSerializer,
    CreateMessageSerializer,
    UserSerializer
)
from .permissions import IsParticipantOfConversation, IsAdminOrStaff
from .auth import get_user_conversations

User = get_user_model()


def get_user_messages(user, status=None):
    """
    Return messages where the user is either the sender or recipient in the conversation.
    Optionally filter by read/unread status.
    """
    
    queryset = Message.objects.filter(conversation__participants=user)  # ✅ valid join
    if status == "read":
        queryset = queryset.filter(is_read=True)
    elif status == "unread":
        queryset = queryset.filter(is_read=False)
    return queryset




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminOrStaff()]
        return [IsAuthenticated()]

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
        

    def get_queryset(self):
        """
        Return all conversations where the user is either the sender or recipient.
        Raise 403 if the user is not part of any conversation.
        """
        user = self.request.user

        queryset = Conversation.objects.filter(
            Q(participants=user)
        )

        if not queryset.exists():
            raise PermissionDenied("HTTP_403_FORBIDDEN: You are not authorized to view any messages.")

        return queryset

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    
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
        status_param = self.request.query_params.get('status')
        conversation_id = self.request.query_params.get('conversation_id')

        # Must filter by conversation_id
        if not conversation_id:
            raise PermissionDenied("conversation_id query parameter is required.")

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation does not exist.")

        if not conversation.participants.filter(user_id=user.user_id).exists():
            raise PermissionDenied("HTTP_403_FORBIDDEN: You are not authorized to view any messages.")

        queryset = Message.objects.filter(conversation=conversation)

        if status_param == "read":
            queryset = queryset.filter(is_read=True)
        elif status_param == "unread":
            queryset = queryset.filter(is_read=False)

        return queryset
