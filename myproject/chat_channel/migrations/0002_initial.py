# Generated by Django 5.0.7 on 2024-08-07 06:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("chat_channel", "0001_initial"),
        ("workspace", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="chatchannel",
            name="admins",
            field=models.ManyToManyField(
                related_name="chat_channel_admins", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="chatchannel",
            name="members",
            field=models.ManyToManyField(
                related_name="chat_channel_members", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="chatchannel",
            name="workspace",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chat_channel",
                to="workspace.workspace",
            ),
        ),
    ]
