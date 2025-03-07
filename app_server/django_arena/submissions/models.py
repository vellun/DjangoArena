import django.conf
import django.core.validators
import django.db.models

import duel.models
import problems.models


class Submission(django.db.models.Model):
    code = django.db.models.TextField()

    score = django.db.models.IntegerField(
        "Оценка",
        null=True,
        blank=True,
        validators=[
            django.core.validators.MaxValueValidator(100),
            django.core.validators.MinValueValidator(1),
        ],
    )

    created_at = django.db.models.DateTimeField(
        "Дата создания",
        auto_now=True,
    )

    problem = django.db.models.ForeignKey(
        problems.models.Problem,
        on_delete=django.db.models.CASCADE,
        related_name="submissions",
        related_query_name="submissions",
    )

    duel = django.db.models.ForeignKey(
        duel.models.Duel,
        on_delete=django.db.models.CASCADE,
        related_name="submissions",
        related_query_name="submissions",
    )

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="submissions",
        related_query_name="submissions",
    )

    exec_time = django.db.models.IntegerField(
        "Время выполнения",
        default=-1,
    )

    verdict = django.db.models.CharField(
        "Вердикт",
        max_length=127,
        default="",
    )

    def __str__(self):
        return f"{self.problem.title}"

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = "Решения"


__all__ = [Submission]
