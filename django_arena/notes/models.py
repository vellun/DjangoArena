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
    author = django.db.models.ForeignKey(
        core.models.User,
        related_name="notes",
        related_query_name="notes",
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
    user_likes = django.db.models.ManyToManyField(core.models.User, related_name="note_likes")
    user_dislikes = django.db.models.ManyToManyField(core.models.User, related_name="note_dislikes")

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"


__all__ = [Note]
