import django.urls

import lobby.views

app_name = "lobby"

urlpatterns = [
    django.urls.path(
        "gameplay-settings/",
        lobby.views.GameplaySettingsView.as_view(),
        name="gameplay-settings",
    ),
    django.urls.path(
        "invite-users/<uidb>",
        lobby.views.InviteUsersView.as_view(),
        name="invite-users",
    ),
    django.urls.path(
        "<uidb>/",
        lobby.views.LobbyView.as_view(),
        name="lobby",
    ),
]
