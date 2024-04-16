import random

import django.contrib
import django.core.cache
import django.db.models
import django.http
import django.shortcuts
import django.views
import django.views.generic
import django.views.generic.edit

import duel.forms
import duel.models
import submissions.models


class DuelView(django.views.generic.edit.FormView):
    form_class = duel.forms.DuelCodeForm
    template_name = "duel/duel.html"

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uidb = self.kwargs["uidb"]
        task_num = self.kwargs.get("task_num", 1)

        context["uidb"] = uidb

        cur_duel = django.shortcuts.get_object_or_404(
            duel.models.Duel, uuid=uidb,
        )
        tasks = cur_duel.problems.all()

        context["task"] = tasks[task_num - 1]  # current task
        context["cnt"] = tasks
        context["task_num"] = task_num

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

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        uidb_url = self.kwargs.get("uidb")
        task_num = self.kwargs.get("task_num", 1)

        user_prefix = f"user_{str(self.request.user.id)}"
        task_prefix = f"task_{str(task_num)}"
        key = f"duel_submission_code_{uidb_url}_{user_prefix}_{task_prefix}"
        code = django.core.cache.cache.get(key)
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
        task_num = request.POST.get("task_num")

        if code is None:
            raise django.http.Http404

        uidb_url = self.kwargs.get("uidb")

        # TODO: add the problem id to the cache key
        django.core.cache.cache.set(
            f"duel_submission_code_{uidb_url}_user_"
            + f"{str(self.request.user.id)}_task_{str(task_num)}",
            code,
        )

        return django.http.JsonResponse({"result": "Success"})


__all__ = [DuelView]
