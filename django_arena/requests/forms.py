import django.forms


class InviteFriendForm(django.forms.Form):
    name = django.forms.CharField(max_length=255, label="Имя пользоавтеля")
    text = django.forms.CharField(
        max_length=255,
        label="Тест приглашения",
    )


class AcceptOrReject(django.forms.Form):
    ANSWER = (
        (0, "Отклонить"),
        (1, "Принять"),
    )
    is_accept = django.forms.ChoiceField(
        choices=ANSWER,
    )


__all__ = [InviteFriendForm]
