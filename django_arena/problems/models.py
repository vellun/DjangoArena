from django.db import models
from django.utils.translation import gettext_lazy as _


class Problem(models.Model):
    class Status(models.TextChoices):
        HARD_REJECT = "HR", _("Hard-reject")
        SOFT_REJECT = "SR", _("Soft-reject")
        ACCEPTED = "AC", _("Accepted")

    author_id = models.IntegerField(default=1)
    title = models.CharField(max_length=255)
    tests_file = models.FileField(upload_to="tasks_attaches/tests/")
    answer_file = models.FileField(upload_to="tasks_attaches/answers/")
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.ACCEPTED,
    )
    text = models.TextField(default="", blank=True, null=True)
    hard_reject_accumulation = models.PositiveSmallIntegerField(default=0)
    day_task = models.BooleanField(default=False)
    week_task = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        db_column="created_at",
    )
    updated_at = models.DateTimeField(
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
