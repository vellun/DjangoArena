import django.urls

import submissions.views

app_name = "submissions"

urlpatterns = [
    django.urls.path(
        "",
        submissions.views.SubmissionListView.as_view(),
        name="submission-list",
    ),
    django.urls.path(
        "<int:pk>/",
        submissions.views.SubmissionDetailView.as_view(),
        name="submission-detail",
    ),
]

__all__ = []
