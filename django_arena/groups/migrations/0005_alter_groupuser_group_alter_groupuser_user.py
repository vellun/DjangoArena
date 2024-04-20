# Generated by Django 4.2.9 on 2024-04-19 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("groups", "0004_remove_group_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupuser",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="group",
                to="groups.group",
            ),
        ),
        migrations.AlterField(
            model_name="groupuser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]