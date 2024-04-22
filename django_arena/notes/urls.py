import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import notes.views

app_name = "notes"

urlpatterns = [
    django.urls.path(
        "<int:pk>/",
        notes.views.NoteDetailView.as_view(),
        name="detail",
    ),
    django.urls.path(
        "all/",
        notes.views.NoteListAllView.as_view(),
        name="blog-all",
    ),
    django.urls.path(
        "my/",
        notes.views.NoteListMyView.as_view(),
        name="blog-my",
    ),
    django.urls.path(
        "like/",
        notes.views.NoteLikeView.as_view(),
        name="like",
    ),
    django.urls.path(
        "dislike/",
        notes.views.NoteDislikeView.as_view(),
        name="dislike",
    ),
    django.urls.path(
        "create/",
        notes.views.NoteCreateView.as_view(),
        name="create",
    ),
    django.urls.path(
        "update/<int:pk>",
        notes.views.NoteUpdateView.as_view(),
        name="update",
    ),
    django.urls.path(
        "delete/<int:pk>",
        notes.views.NoteDeleteView.as_view(),
        name="delete",
    ),
]


__all__ = []
