import pytest
from django.utils import timezone
from chats.models import User, Conversation, Message


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="securepassword123",
        first_name="John",
        last_name="Doe",
        phone_number="1234567890",
        role=User.Roles.ADMIN
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.phone_number == "1234567890"
    assert user.role == User.Roles.ADMIN
    assert str(user) == "testuser (ADMIN)"


@pytest.mark.django_db
def test_conversation_creation():
    user1 = User.objects.create_user(username="alice", email="alice@example.com", password="pass123")
    user2 = User.objects.create_user(username="bob", email="bob@example.com", password="pass123")

    conversation = Conversation.objects.create()
    conversation.participants.add(user1, user2)

    assert conversation.participants.count() == 2
    assert str(conversation).startswith("Conversation")
    assert "alice" in str(conversation)
    assert "bob" in str(conversation)


@pytest.mark.django_db
def test_message_creation():
    user = User.objects.create_user(username="charlie", email="charlie@example.com", password="pass123")
    conversation = Conversation.objects.create()
    conversation.participants.add(user)

    message = Message.objects.create(
        conversation=conversation,
        sender=user,
        message_body="Hello, world!",
        sent_at=timezone.now()
    )

    assert message.conversation == conversation
    assert message.sender == user
    assert message.message_body == "Hello, world!"
    assert message.is_read is False
    assert str(message).startswith("Message from charlie")
