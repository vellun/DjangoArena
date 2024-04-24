import django.urls

import invitations.views


app_name = "invitations"

urlpatterns = [
    django.urls.path(
        "add/", invitations.views.SendInvite.as_view(), name="add_friend",
    ),
    django.urls.path(
        "invites/", invitations.views.Invites.as_view(), name="invite_list",
    ),
    django.urls.path(
        "invite_card/<int:pk>",
        invitations.views.InviteCard.as_view(),
        name="invite_card",
    ),
]
