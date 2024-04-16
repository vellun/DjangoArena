import django.forms


class BootstrapForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CommonGameplaySettingsForm(BootstrapForm):
    """Form for selecting the number and difficulty
    of tasks for the entire duel"""

    tasks = django.forms.IntegerField(
        label="Укажите количество задач",
        min_value=1,
        max_value=10,
        initial=3,
    )

    difficulty = django.forms.ChoiceField(
        label="Установите уровень сложности соревнования",
        choices=[
            ("easy", "Легкий"),
            ("medium", "Средний"),
            ("hard", "Высокий"),
        ],
        initial="easy",
        help_text="Все задачи будут выбранного уровня сложности",
    )


class DetailedGameplaySettingsForm(BootstrapForm):
    """Form for selecting the number of tasks
    of each difficulty level"""

    easy_tasks = django.forms.IntegerField(
        label="Укажите количество задач легкого уровня",
        min_value=0,
        max_value=10,
        initial=1,
    )

    medium_tasks = django.forms.IntegerField(
        label="Укажите количество задач среднего уровня",
        min_value=0,
        max_value=10,
        initial=1,
    )

    hard_tasks = django.forms.IntegerField(
        label="Укажите количество задач высокого уровня",
        min_value=0,
        max_value=10,
        initial=1,
    )

    def clean(self):
        cleaned_data = super().clean()
        total = (
            cleaned_data.get("easy_tasks")
            + cleaned_data.get("medium_tasks")
            + cleaned_data.get("hard_tasks")
        )

        if total > 10:
            raise django.forms.ValidationError(
                "Можно выбрать макс. 10 задач",
            )

        if not total:
            raise django.forms.ValidationError(
                "Выберете минимум одну задачу",
            )


__all__ = [CommonGameplaySettingsForm, DetailedGameplaySettingsForm]
