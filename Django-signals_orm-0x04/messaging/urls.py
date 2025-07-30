from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MessageViewSet,
    NotificationViewSet,
    MessageHistoryViewSet,
    DeleteUserView
)

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'message-history', MessageHistoryViewSet, basename='messagehistory')

urlpatterns = [
    path('', include(router.urls)),
    path('delete-account/', DeleteUserView.as_view(), name='delete-account'),
]
