# Generated by Django 4.2.9 on 2024-04-16 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0003_group_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="group",
            name="user",
        ),
    ]
