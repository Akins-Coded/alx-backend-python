# Generated by Django 5.2.4 on 2025-07-30 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_message_parent_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
    ]
