# Generated by Django 4.2.11 on 2024-04-23 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0009_alter_groupinvite_accept"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="title",
            field=models.CharField(default="Group", max_length=255),
        ),
    ]
