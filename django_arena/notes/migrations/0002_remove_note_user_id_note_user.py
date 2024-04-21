# Generated by Django 4.2.11 on 2024-04-18 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notes", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="note",
            name="user_id",
        ),
        migrations.AddField(
            model_name="note",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notes",
                related_query_name="notes",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
