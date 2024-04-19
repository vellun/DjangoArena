import django.db.models

import core.models


class Group(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=255,
        unique=True,
    )
    description = django.db.models.TextField()
    is_public = django.db.models.BooleanField(
        default=False,
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Группы"
        verbose_name_plural = "Группы"


class GroupUser(django.db.models.Model):
    user = django.db.models.ForeignKey(
        core.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="user",
    )
    group = django.db.models.ForeignKey(
        Group,
        on_delete=django.db.models.CASCADE,
        related_name="group",
    )
    leader = django.db.models.BooleanField(
        default=False,
    )
    moderator = django.db.models.BooleanField(
        default=False,
    )


__all__ = [Group]
