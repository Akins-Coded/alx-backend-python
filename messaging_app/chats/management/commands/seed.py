from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chats.models import Conversation, Message
from faker import Faker
import random
from django.db.utils import IntegrityError

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with users, conversations, and messages"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        fake.unique.clear()
        users = []

        # Create users
        for _ in range(1500):
            try:
                user = User.objects.create_user(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    password="testpass123",
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=fake.phone_number()
                )
                users.append(user)
            except IntegrityError:
                # Skip duplicate emails/usernames gracefully
                continue

        # Create conversations
        conversations = []
        for _ in range(1500):
            sender, recipient = random.sample(users, 2)
            conv = Conversation.objects.create()
            conv.participants.set([sender, recipient])
            conv.save()
            conversations.append(conv)

        # Create messages
        for conv in conversations:
            participants = list(conv.participants.all())
            for _ in range(random.randint(2, 6)):
                sender = random.choice(participants)
                Message.objects.create(
                    conversation=conv,
                    sender=sender,
                    message_body=fake.text(max_nb_chars=200),
                    is_read=random.choice([True, False])
                )

        self.stdout.write(self.style.SUCCESS("✅ Seeding completed!"))
