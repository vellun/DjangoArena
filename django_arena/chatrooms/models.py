import django.conf
import django.db.models

import groups.models


class ChatRoom(django.db.models.Model):
    group = django.db.models.OneToOneField(
        to=groups.models.Group,
        on_delete=django.db.models.CASCADE,
        related_name="chat",
        related_query_name="chat",
    )

    class Meta:
        verbose_name = "чат"
        verbose_name_plural = "чаты"


class Message(django.db.models.Model):
    room = django.db.models.ForeignKey(
        to=ChatRoom,
        on_delete=django.db.models.CASCADE,
        related_name="room",
        related_query_name="room",
    )

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="messages",
        related_query_name="messages",
    )

    content = django.db.models.TextField(verbose_name="Сообщение")

    created_at = django.db.models.DateTimeField(
        "Дата отправки",
        auto_now_add=True,
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


__all__ = [ChatRoom, Message]
