import django.forms

import groups.models


class GroupForm(django.forms.ModelForm):
    class Meta:
        model = groups.models.Group
        fields = (
            groups.models.Group.name.field.name,
            groups.models.Group.description.field.name,
            groups.models.Group.is_public.field.name,
        )
        labels = {
            groups.models.Group.name.field.name: "Название группы",
            groups.models.Group.description.field.name: "Описание группы",
            groups.models.Group.is_public.field.name: "Публичная",
        }


class EnterGroupForm(django.forms.ModelForm):
    class Meta:
        model = groups.models.Group
        fields = (groups.models.Group.name.field.name,)
        labels = {
            groups.models.Group.name.field.name: "Название группы",
        }


__all__ = [GroupForm]
