import django.urls

import homepage.views

app_name = "homepage"

urlpatterns = [
    django.urls.path("", homepage.views.HomeView.as_view(), name="main"),
    django.urls.path(
        "test_code/",
        homepage.views.TestCodeView.as_view(),
        name="test_code",
    ),
]
