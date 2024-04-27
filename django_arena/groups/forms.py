import django.forms

import groups.models


class BootstrapForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.name != "is_public":
                field.field.widget.attrs["class"] = "form-control"


class GroupForm(BootstrapForm, django.forms.ModelForm):
    class Meta:
        model = groups.models.Group
        fields = (
            groups.models.Group.title.field.name,
            groups.models.Group.description.field.name,
            groups.models.Group.theme.field.name,
            groups.models.Group.name.field.name,
            groups.models.Group.is_public.field.name,
            groups.models.Group.image.field.name,
        )


class EnterGroupForm(BootstrapForm, django.forms.ModelForm):
    class Meta:
        model = groups.models.Group
        fields = (groups.models.Group.name.field.name,)
        labels = {
            groups.models.Group.name.field.name: "Название группы",
        }


class InviteGroupForm(BootstrapForm):
    user = django.forms.CharField(max_length=255)
    text = django.forms.CharField(max_length=255)


class AcceptRejectForm(BootstrapForm, django.forms.ModelForm):
    class Meta:
        model = groups.models.GroupInvite
        fields = (groups.models.GroupInvite.accept.field.name,)


class DeleteForm(BootstrapForm):
    is_delete = django.forms.CharField(
        help_text="Напишите слово 'Удалить', чтобы удалить группу",
        label="Удалить группу",
    )


__all__ = [GroupForm, InviteGroupForm, DeleteForm]
