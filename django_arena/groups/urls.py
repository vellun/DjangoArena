import django.urls

import groups.views

app_name = "groups"


urlpatterns = [
    django.urls.path("", groups.views.GroupView.as_view(), name="groups"),
    django.urls.path(
        "create/",
        groups.views.GroupCreate.as_view(),
        name="new_groups",
    ),
    django.urls.path(
        "add/",
        groups.views.GroupEnterUser.as_view(),
        name="enter_user_in_group",
    ),
]
