import django.urls

import users.views

app_name = "users"


def set_form(form):
    return users.forms.set_custom_form(form)

login_view = users.views.CustomLoginView.as_view(
    template_name="users/login.html",
    form_class=set_form(users.forms.CustomAuthenticationForm),
)

logout_view = django.contrib.auth.views.LogoutView.as_view(
    template_name="users/logout.html",
)

urlpatterns = [
    django.urls.path(
        "<int:user_id>/",
        users.views.ProfileView.as_view(),
        name="profile",
    ),
    django.urls.path("login/", login_view, name="login"),
    django.urls.path("signup/", users.views.SignupView.as_view(), name="signup"),
    django.urls.path("logout/", logout_view, name="logout"),
]
