import django.db.models
import notes.models

import problems.models


class Tag(django.db.models.Model):
    title = django.db.models.CharField(max_length=255)
    description = django.db.models.TextField()
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
    )
    problem = django.db.models.ManyToManyField(
        problems.models.Problem,
        null=True,
    )
    note = django.db.models.ManyToManyField(
        notes.models.Note,
        related_name="tag",
        related_query_name="tag",
        null=True,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


__all__ = ["Tag"]
