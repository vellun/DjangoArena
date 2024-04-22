import datetime
import random
from threading import Thread

import django.contrib
import django.core.cache
import django.db.models
import django.http
import django.shortcuts
import django.urls
import django.views
import django.views.generic
import django.views.generic.edit

from duel.code_tester import test_code
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
            duel.models.Duel,
            uuid=uidb,
        )
        tasks = cur_duel.problems.all()
        task = tasks[task_num - 1]

        duration = datetime.timedelta(
            seconds=10,
        )  # Можно пока изменять секунды, это на время разработки

        # А в итоге будет так
        # duration = datetime.timedelta(
        #     seconds=sum(task.duration.total_seconds() for task in tasks),
        # )

        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60

        context["duration"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        context["task"] = task  # current task
        context["cnt"] = tasks
        context["task_num"] = task_num
        context["title"] = "Дуэль"

        return context

    def form_valid(self, form):
        code = form.cleaned_data.get("code")

        uidb_url = self.kwargs.get("uidb")
        task_num = self.kwargs.get("task_num", 1)

        str_parameter = (
            "duel_"
            + uidb_url
            + "_"
            + str(task_num)
            + "_"
            + str(self.request.user.id)
        )
        django.core.cache.cache.set(str_parameter, code)

        submission = submissions.models.Submission(
            code=code,
            score=random.randrange(100),
            problem_id=task_num,
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


class DuelTimerView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        duration = request.GET.get("duration")
        uidb = self.kwargs["uidb"]

        timer = django.core.cache.cache.get(
            f"duel_{uidb}_timer",
            duration,
        )

        return django.http.HttpResponse(timer)

    def post(self, request, *args, **kwargs):
        request_type = request.POST.get("type")
        uidb = self.kwargs["uidb"]

        if request_type == "cache":
            timer = request.POST.get("timer")
            django.core.cache.cache.set(f"duel_{uidb}_timer", timer)
        elif request_type == "redirect":
            django.core.cache.cache.delete(f"duel_{uidb}_timer")

        return django.http.HttpResponse("OK")


class LeaveDuelView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        uidb = self.kwargs["uidb"]
        django.core.cache.cache.delete(f"duel_{uidb}_timer")
        return django.shortcuts.redirect(django.urls.reverse("homepage:main"))


class ResultsView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        uidb = self.kwargs["uidb"]

        str_parameter = (
            "duel_"
            + uidb
            + "_"
            + str(request.user.id)
            + "_"
            + "currently_testing"
        )
        currently_testing = django.core.cache.cache.get(str_parameter)

        user_score = "Pending..."

        print(currently_testing)

        if currently_testing is None:
            testing_thread = Thread(
                target=test_code,
                args=(uidb, request.user.id, str_parameter),
            )
            testing_thread.start()
            django.core.cache.cache.set(str_parameter, "Testing")

        elif currently_testing == "Finished":
            user_score_parameter = (
                "duel_" + uidb + "_" + str(request.user.id) + "_" + "score"
            )
            user_score = django.core.cache.cache.get(user_score_parameter)

        context = {
            "user_score": user_score,
        }

        return django.shortcuts.render(request, "duel/results.html", context)


class CacheCodeView(django.views.generic.View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        task_num = request.POST.get("task_num")
        uidb_url = self.kwargs.get("uidb")

        if code is None:
            raise django.http.Http404

        django.core.cache.cache.set(
            f"duel_submission_code_{uidb_url}_user_"
            + f"{str(self.request.user.id)}_task_{str(task_num)}",
            code,
        )

        return django.http.JsonResponse({"result": "Success"})


__all__ = [DuelView]
