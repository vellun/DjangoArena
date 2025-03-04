import django.contrib.admin
import tags.models


@django.contrib.admin.register(tags.models.Tag)
class AdminTag(django.contrib.admin.ModelAdmin):
    list_display = (
        tags.models.Tag.title.field.name,
        tags.models.Tag.description.field.name,
    )


__all__ = []
