import django.conf
import django.db.models

import problems.models


class Duel(django.db.models.Model):
    uuid = django.db.models.UUIDField(unique=True)
    problems = django.db.models.ManyToManyField(problems.models.Problem)
    competitors = django.db.models.ManyToManyField(
        django.conf.settings.AUTH_USER_MODEL,
    )
    started_at = django.db.models.DateTimeField(
        auto_now_add=True,
    )

    # TODO: add more fields later

    class Meta:
        verbose_name = "дуэль"
        verbose_name_plural = "дуэли"


__all__ = [Duel]
