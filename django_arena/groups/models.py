import pathlib
import uuid

import django.db.models

import core.models


def get_path_image(instance, filename):
    file_extension = pathlib.Path(filename).suffix
    return f"groups/{uuid.uuid4()}{file_extension}"


class Group(django.db.models.Model):
    title = django.db.models.CharField(
        verbose_name="название",
        help_text="Придумайте крутое название для своей группы",
        max_length=255,
        default="Group",
    )
    name = django.db.models.CharField(
        verbose_name="никнейм",
        help_text="Придумайте уникальное название",
        max_length=255,
        unique=True,
    )
    theme = django.db.models.CharField(
        verbose_name="тематика",
        help_text="Определитесь с тематикой группы(например 'для развлечения'"
        + "'друзья' и тд.)",
        max_length=30,
        default="Для развлечения",
        blank=True,
    )

    image = django.db.models.ImageField(
        "аватарка",
        help_text="Загрузите аватарку",
        upload_to=get_path_image,
        null=True,
        blank=True,
    )
    description = django.db.models.TextField(
        verbose_name="описание",
        help_text="Опишите группу",
    )
    is_public = django.db.models.BooleanField(
        default=False,
        verbose_name="публичная ли группа?",
        help_text="В публичную группу могут вступить все желающие",
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
        related_name="group_user",
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


class GroupInvite(django.db.models.Model):
    ANSWER = (
        (1, "Принять"),
        (0, "Отклонить"),
    )
    user = django.db.models.ForeignKey(
        core.models.User,
        on_delete=django.db.models.CASCADE,
    )
    group = django.db.models.OneToOneField(
        Group,
        on_delete=django.db.models.CASCADE,
    )
    text = django.db.models.CharField(
        max_length=255,
    )
    accept = django.db.models.BooleanField(
        choices=ANSWER,
        default=0,
    )


__all__ = [Group, GroupUser, GroupInvite]
