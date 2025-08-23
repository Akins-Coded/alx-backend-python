import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from chats.models import User, Conversation


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(username, email, password="pass123", role=User.Roles.USER, is_staff=False, is_superuser=False):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
    return make_user


@pytest.mark.django_db
def test_user_list_requires_admin(api_client, create_user):
    admin = create_user("admin", "admin@example.com", is_staff=True, role=User.Roles.ADMIN)
    user = create_user("user", "user@example.com")

    api_client.force_authenticate(user=admin)
    url = reverse("user-list")  # DRF router name
    response = api_client.get(url)
    assert response.status_code == 200

    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_conversation_creation_and_retrieval(api_client, create_user):
    user1 = create_user("alice", "alice@example.com")
    user2 = create_user("bob", "bob@example.com")

    api_client.force_authenticate(user=user1)
    url = reverse("conversation-list")
    response = api_client.post(url, {"participants": [str(user2.user_id)]}, format="json")
    assert response.status_code == 201

    # Fetch conversation list
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1

    # Bob should see the conversation after being added
    api_client.force_authenticate(user=user2)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_non_participant_cannot_access_conversation(api_client, create_user):
    user1 = create_user("alice", "alice@example.com")
    outsider = create_user("outsider", "outsider@example.com")

    api_client.force_authenticate(user=user1)
    conversation = Conversation.objects.create()
    conversation.participants.add(user1)

    api_client.force_authenticate(user=outsider)
    url = reverse("conversation-list")
    response = api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_message_creation_and_filters(api_client, create_user):
    user1 = create_user("alice", "alice@example.com")
    user2 = create_user("bob", "bob@example.com")

    conversation = Conversation.objects.create()
    conversation.participants.add(user1, user2)

    api_client.force_authenticate(user=user1)
    url = reverse("message-list")

    # Missing conversation_id → should fail
    response = api_client.get(url)
    assert response.status_code == 403

    
        # Create a message
    response = api_client.post(
        url,
        {
            "conversation": str(conversation.conversation_id),
            "message_body": "Hello Bob!",
        },
        format="json",
    )
    assert response.status_code == 201


