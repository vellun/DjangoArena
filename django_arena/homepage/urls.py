import django.urls

import homepage.views

app_name = "homepage"

urlpatterns = [
    django.urls.path("", homepage.views.HomeView.as_view(), name="main"),
    django.urls.path(
        "play/<uidb>/",
        homepage.views.LobbyView.as_view(),
        name="lobby",
    ),
]
