from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, NotificationViewSet, MessageHistoryViewSet, DeleteUserView

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet)
router.register(r'history', MessageHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
]
