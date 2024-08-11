import django.urls

import groups.views

app_name = "groups"


urlpatterns = [
    django.urls.path("my/", groups.views.GroupMyView.as_view(), name="my"),
    django.urls.path("all/", groups.views.GroupAllView.as_view(), name="all"),
    django.urls.path(
        "create/",
        groups.views.GroupCreateView.as_view(),
        name="new_groups",
    ),
    django.urls.path(
        "add/",
        groups.views.GroupEnterUser.as_view(),
        name="enter_user_in_group",
    ),
    django.urls.path(
        "invitations/",
        groups.views.GroupInvitations.as_view(),
        name="invitations",
    ),
    django.urls.path(
        "invite_request/<int:pk>",
        groups.views.GroupInviteRequest.as_view(),
        name="invite_request",
    ),
    django.urls.path(
        "invitations/<int:pk>/",
        groups.views.GroupInviteCard.as_view(),
        name="invite_card",
    ),
    django.urls.path(
        "groups/<int:pk>/",
        groups.views.GroupPage.as_view(),
        name="groups_detail",
    ),
]
