# Generated by Django 4.2.9 on 2024-04-14 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("problems", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="problem",
            name="author_id",
        ),
        migrations.AddField(
            model_name="problem",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="problems",
                to=settings.AUTH_USER_MODEL,
                verbose_name="автор задачи",
            ),
        ),
        migrations.AddField(
            model_name="problem",
            name="difficulty",
            field=models.CharField(
                choices=[
                    ("easy", "Easy"),
                    ("medium", "Medium"),
                    ("hard", "Hard"),
                ],
                default="easy",
                help_text="Укажите сложность задачи",
                max_length=256,
                verbose_name="сложность",
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="answer_file",
            field=models.FileField(
                help_text="Загрузите файл с ответами для задачи",
                upload_to="tasks_attaches/answers/",
                verbose_name="файл с ответами",
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="day_task",
            field=models.BooleanField(
                default=False,
                help_text="Это задача дня?",
                verbose_name="задача дня",
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="hard_reject_accumulation",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text="Столько раз вы отправили какой-то кринж вместо задачи",
                verbose_name="количество жестких отказов",
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="status",
            field=models.CharField(
                choices=[
                    ("HR", "Hard-reject"),
                    ("SR", "Soft-reject"),
                    ("AC", "Accepted"),
                ],
                default="AC",
                max_length=2,
                verbose_name="статус",
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="tests_file",
            field=models.FileField(
                help_text="Загрузите файл с тестами для задачи",
                upload_to="tasks_attaches/tests/",
                verbose_name="файл с тестами",
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="text",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Введите описание задачи",
                null=True,
                verbose_name="описание",
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="title",
            field=models.CharField(
                help_text="Введите название задачи",
                max_length=255,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="problem",
            name="week_task",
            field=models.BooleanField(
                default=False,
                help_text="Это задача недели?",
                verbose_name="задача недели",
            ),
        ),
    ]
