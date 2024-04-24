import django.db.models

import core.models


class InviteModel(django.db.models.Model):
    user_from = django.db.models.ForeignKey(
        core.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="from+",
    )
    user_to = django.db.models.ForeignKey(
        core.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="to+",
    )
    text = django.db.models.CharField(max_length=255)


__all__ = [InviteModel]
