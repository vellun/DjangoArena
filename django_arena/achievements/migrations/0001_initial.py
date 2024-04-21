# Generated by Django 4.2.9 on 2024-04-06 20:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now=True)),
                (
                    "user_id",
                    models.ManyToManyField(
                        related_name="achievements",
                        related_query_name="achievements",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Достижение",
                "verbose_name_plural": "Достижения",
            },
        ),
        migrations.CreateModel(
            name="AchievementImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="achievements/")),
                (
                    "achievement",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="image",
                        related_query_name="image",
                        to="achievements.achievement",
                    ),
                ),
            ],
            options={
                "verbose_name": "Картинка",
                "verbose_name_plural": "Картинка",
            },
        ),
    ]
