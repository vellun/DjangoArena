# Generated by Django 5.0 on 2024-04-22 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0006_groupinvite"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupinvite",
            name="accept",
            field=models.BooleanField(default=0),
        ),
    ]
