# Generated by Django 4.2.9 on 2024-04-06 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("problems", "0001_initial"),
        ("notes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "note",
                    models.ManyToManyField(
                        null=True,
                        related_name="tag",
                        related_query_name="tag",
                        to="notes.note",
                    ),
                ),
                (
                    "problem",
                    models.ManyToManyField(null=True, to="problems.problem"),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
    ]
