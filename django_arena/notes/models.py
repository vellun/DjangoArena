import django.db.models

import core.models


class Note(django.db.models.Model):
    title = django.db.models.CharField(max_length=255)
    text = django.db.models.TextField()
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
    )
    user_id = django.db.models.ForeignKey(
        core.models.User,
        related_name="note",
        related_query_name="note",
        on_delete=django.db.models.CASCADE,
    )
    likes = django.db.models.IntegerField(
        default=0,
    )
    dislikes = django.db.models.IntegerField(
        default=0,
    )
    is_on_main = django.db.models.BooleanField(
        default=False,
    )
    official_documentation = django.db.models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"


__all__ = ["Note"]
