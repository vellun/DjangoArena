import django.conf
import django.db.models.signals
import django.dispatch

import chatrooms.models
import groups.models


@django.dispatch.receiver(
    django.db.models.signals.post_save,
    sender=groups.models.Group,
)
def create_profile(sender, instance, created, **kwargs):
    if created:
        chatrooms.models.ChatRoom.objects.create(group=instance)


__all__ = []
