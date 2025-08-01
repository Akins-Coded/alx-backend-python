# Generated by Django 5.2.4 on 2025-07-29 10:19

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_rename_read_notification_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='MessageHistory',
            fields=[
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('previous_body', models.TextField()),
                ('edited_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edit_history', to='messaging.message')),
            ],
        ),
    ]
