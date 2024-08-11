import django.forms

import notes.models


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class NoteForm(BootstrapForm):
    """Form for creating posts"""

    class Meta:
        model = notes.models.Note
        fields = ("title", "text")


__all__ = []
