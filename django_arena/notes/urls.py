import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import notes.views

app_name = "notes"

urlpatterns = [
    django.urls.path(
        "",
        notes.views.NoteListView.as_view(),
        name="blog",
    ),
    django.urls.path(
        "create/",
        notes.views.NoteCreateView.as_view(),
        name="create",
    ),
]


__all__ = []
