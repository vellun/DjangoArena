# Generated by Django 4.2.9 on 2024-04-10 12:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
            },
        ),
        migrations.AddField(
            model_name="user",
            name="friends",
            field=models.ManyToManyField(
                blank=True, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
