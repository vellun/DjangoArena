# Generated by Django 4.2.11 on 2024-08-11 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("received", "получено"),
                            ("progress", "в обработке"),
                            ("complete", "ответ дан"),
                        ],
                        db_column="status",
                        default="received",
                        max_length=20,
                        verbose_name="статус",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        db_column="text",
                        help_text="Напишите что-нибудь",
                        max_length=300,
                        verbose_name="текст",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_column="created_on", null=True
                    ),
                ),
            ],
            options={
                "verbose_name": "отзыв",
                "verbose_name_plural": "отзывы",
            },
        ),
    ]
