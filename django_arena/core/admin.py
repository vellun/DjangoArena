import django.contrib.admin

import core.models

import core.models


@django.contrib.admin.register(core.models.User)
class UserAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        core.models.User.username.field.name,
        core.models.User.rating.field.name,
        core.models.User.views.field.name,
    )


__all__ = []
