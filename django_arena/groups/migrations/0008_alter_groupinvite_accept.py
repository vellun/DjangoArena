# Generated by Django 5.0 on 2024-04-22 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0007_groupinvite_accept"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupinvite",
            name="accept",
            field=models.BooleanField(
                choices=[("1", "Принять"), ("0", "Отклонить")], default=0
            ),
        ),
    ]