import django.urls
import requests.views


app_name = "requests"

urlpatterns = [
    django.urls.path(
        "add/",
        requests.views.SendInvite.as_view(),
        name="add_friend",
    ),
    django.urls.path(
        "invites/",
        requests.views.Invites.as_view(),
        name="invite_list",
    ),
    django.urls.path(
        "invite_card/<int:pk>",
        requests.views.InviteCard.as_view(),
        name="invite_card",
    ),
]
