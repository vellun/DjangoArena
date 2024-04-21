import django.urls

import user_profile.views

app_name = "profile"

urlpatterns = [
    django.urls.path(
        "<int:user_id>/",
        user_profile.views.ProfileView.as_view(),
        name="profile",
    ),
]
