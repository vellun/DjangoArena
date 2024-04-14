import django.forms


class BootstrapForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class GameplaySettingsForm(BootstrapForm):
    """A form for selecting the number and difficulty of tasks
    before starting a duel"""

    code = django.forms.CharField(
        label="Введите все свои данные срочно",
        initial="from django.views.generic import View\n\nclass MyView(View):\
            \n\t'''\n\tWrite your code here\n\t'''\n\tpass",
    )


__all__ = [GameplaySettingsForm]
