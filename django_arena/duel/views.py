import random

import django.contrib
import django.core.cache
import django.http
import django.shortcuts
import django.views
import django.views.generic
import django.views.generic.edit

import duel.forms
import submissions.models


class DuelView(django.views.generic.edit.FormView):
    form_class = duel.forms.DuelCodeForm
    template_name = "duel/duel.html"

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uidb = self.kwargs["uidb"]
        context["uidb"] = uidb
        return context

    def form_valid(self, form):
        code = form.cleaned_data.get("code")

        submission = submissions.models.Submission(
            code=code,
            score=random.randrange(100),
            problem_id=1,
            user_id=self.request.user.id,
        )
        submission.save()

        django.contrib.messages.success(
            self.request,
            "Ваше решение отправлено!",
        )

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        uidb_url = self.kwargs.get("uidb")
        code = django.core.cache.cache.get(
            "duel_submission_code_"
            + uidb_url
            + "_user_"
            + str(self.request.user.id),
        )
        if code:
            initial["code"] = code

        return initial


class CacheCodeView(django.views.generic.View):
    """Handle ajax requests and cache the code when
    changing the code in the editor so that when the page
    reloads the user's solution is not lost"""

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")

        if code is None:
            raise django.http.Http404

        uidb_url = self.kwargs.get("uidb")

        # TODO: add the problem id to the cache key
        django.core.cache.cache.set(
            "duel_submission_code_"
            + uidb_url
            + "_user_"
            + str(self.request.user.id),
            code,
        )

        return django.http.JsonResponse({"result": "Success"})


__all__ = [DuelView]
