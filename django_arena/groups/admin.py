import django.contrib.admin

import groups.models


@django.contrib.admin.register(groups.models.Group)
class AdminGroup(django.contrib.admin.ModelAdmin):
    list_display = (
        groups.models.Group.name.field.name,
        groups.models.Group.created_at.field.name,
    )


__all__ = []
