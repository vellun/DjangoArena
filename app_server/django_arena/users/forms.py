import datetime

import django.conf
import django.contrib.auth.forms
import django.forms

import core.models


class BootstrapForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class SignUpForm(django.contrib.auth.forms.UserCreationForm, BootstrapForm):
    class Meta:
        model = core.models.User
        fields = ("email", "username")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            core.models.User.objects.get(email=email)
            raise django.forms.ValidationError(
                "Пользователь с такой почтой уже существует.",
            )
        except core.models.User.DoesNotExist:
            return email


class CustomAuthenticationForm(
    django.contrib.auth.forms.AuthenticationForm,
    BootstrapForm,
):
    username = django.forms.CharField(
        label="Почта или имя пользователя",
        max_length=254,
    )

    class Meta:
        model = django.contrib.auth.get_user_model()
        fields = (model.username.field.name, model.password.field.name)

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            user = django.contrib.auth.authenticate(
                username=username_or_email,
                password=password,
            )
            if not user:
                user = django.contrib.auth.authenticate(
                    email=username_or_email,
                    password=password,
                )
                if not user:
                    raise django.forms.ValidationError(
                        "Неправильные логин или пароль.",
                    )

        return super(CustomAuthenticationForm, self).clean()


class EditUserProfileForm(
    django.contrib.auth.forms.UserChangeForm,
    BootstrapForm,
):
    password = None

    class Meta:
        model = django.contrib.auth.get_user_model()
        fields = [
            model.birthday.field.name,
            model.image.field.name,
            model.shortname.field.name,
            model.username.field.name,
            model.github_link.field.name,
            model.gitlab_link.field.name,
        ]

    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.fields["birthday"].widget = django.forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "min": datetime.datetime.now().date()
                - datetime.timedelta(days=365 * 100),
                "max": datetime.datetime.now().date(),
            },
        )


def set_custom_form(form):
    class CustomForm(form, BootstrapForm):
        pass

    return CustomForm


__all__ = [
    SignUpForm,
]
