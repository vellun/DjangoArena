from django.contrib import admin
from django.urls import path
import django_arena_testing.views

urlpatterns = [
    path(
        "test/<uidb>/",
        django_arena_testing.views.TestCodeView.as_view(),
        name="testing",
    ),
    path("admin/", admin.site.urls),
]
