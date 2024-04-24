import datetime

import django.conf
import django.db.models
from django.utils.translation import gettext_lazy as _


class Problem(django.db.models.Model):
    DEFAULT_DURATION = datetime.timedelta(minutes=15)

    class Status(django.db.models.TextChoices):
        HARD_REJECT = "HR", _("Hard-reject")
        SOFT_REJECT = "SR", _("Soft-reject")
        ACCEPTED = "AC", _("Accepted")

    class Difficulty(django.db.models.TextChoices):
        EASY = "easy", _("Easy")
        MEDIUM = "medium", _("Medium")
        HARD = "hard", _("Hard")

    author = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.SET_NULL,
        null=True,
        blank=True,
        related_name="problems",
        verbose_name="автор задачи",
    )

    title = django.db.models.CharField(
        verbose_name="название",
        help_text="Введите название задачи",
        max_length=255,
    )
    tests_file = django.db.models.FileField(
        verbose_name="файл с тестами",
        help_text="Загрузите файл с тестами для задачи",
        upload_to="tasks_attaches/tests/",
    )
    answer_file = django.db.models.FileField(
        verbose_name="файл с ответами",
        help_text="Загрузите файл с ответами для задачи",
        upload_to="tasks_attaches/answers/",
    )
    status = django.db.models.CharField(
        verbose_name="статус",
        max_length=2,
        choices=Status.choices,
        default=Status.ACCEPTED,
    )
    difficulty = django.db.models.CharField(
        verbose_name="сложность",
        max_length=256,
        help_text="Укажите сложность задачи",
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )
    duration = django.db.models.DurationField(
        verbose_name="время на выполнение задачи",
        help_text="Укажите время выполнения задачи",
        default=DEFAULT_DURATION,
    )
    text = django.db.models.TextField(
        verbose_name="описание",
        help_text="Введите описание задачи",
        default="",
        blank=True,
        null=True,
    )
    hard_reject_accumulation = django.db.models.PositiveSmallIntegerField(
        verbose_name="количество жестких отказов",
        help_text="Столько раз вы отправили какой-то кринж вместо задачи",
        default=0,
    )
    day_task = django.db.models.BooleanField(
        verbose_name="задача дня",
        help_text="Это задача дня?",
        default=False,
    )
    week_task = django.db.models.BooleanField(
        verbose_name="задача недели",
        help_text="Это задача недели?",
        default=False,
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        null=True,
        db_column="created_at",
    )
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        null=True,
        db_column="updated_at",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"


__all__ = [Problem]
