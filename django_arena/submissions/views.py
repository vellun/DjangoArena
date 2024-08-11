import django.contrib.auth.mixins
import django.views.generic

import submissions.models


class SubmissionListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    template_name = "submissions/submission-list.html"
    context_object_name = "submissions"
    model = submissions.models.Submission

    def get_queryset(self):
        return submissions.models.Submission.objects.filter(
            user_id=self.request.user.id,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваши решения"
        return context


class SubmissionDetailView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.DetailView,
):
    template_name = "submissions/submission-detail.html"
    context_object_name = "submission"
    pk_url_kwarg = "pk"
    model = submissions.models.Submission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Решение номер {self.object.id}"
        return context


__all__ = [SubmissionListView, SubmissionDetailView]
