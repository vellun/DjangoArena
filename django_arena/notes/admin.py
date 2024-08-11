import django.contrib.admin

import notes.models


@django.contrib.admin.register(notes.models.Note)
class AdminNote(django.contrib.admin.ModelAdmin):
    list_display = (
        notes.models.Note.title.field.name,
        notes.models.Note.text.field.name,
        notes.models.Note.likes.field.name,
        notes.models.Note.dislikes.field.name,
        notes.models.Note.is_on_main.field.name,
        notes.models.Note.official_documentation.field.name,
    )


__all__ = []
