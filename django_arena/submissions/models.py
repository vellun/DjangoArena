import django.conf
import django.db.models

import problems.models


class Submission(django.db.models.Model):
    code = django.db.models.TextField()
    created_at = django.db.models.DateTimeField(
        auto_now=True,
    )

    problem = django.db.models.ForeignKey(
        problems.models.Problem,
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

    def __str__(self):
        return f"{self.problem.title}"

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = "Решения"


__all__ = [Submission]
