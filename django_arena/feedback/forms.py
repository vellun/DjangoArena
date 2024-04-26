import django.forms

import feedback.models


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FeedbackForm(BootstrapForm):
    class Meta:
        model = feedback.models.Feedback
        fields = "__all__"
        exclude = [
            feedback.models.Feedback.created_on.field.name,
            feedback.models.Feedback.status.field.name,
        ]

        widgets = {"text": django.forms.Textarea(attrs={"rows": 5})}


__all__ = [
    FeedbackForm,
]
