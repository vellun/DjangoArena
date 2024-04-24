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

    def dispatch(self, request, *args, **kwargs):
        task_num = self.kwargs.get("task_num", 1)
        uidb = self.kwargs["uidb"]
        cur_duel = django.shortcuts.get_object_or_404(
            duel.models.Duel,
            uuid=uidb,
        )
        self.tasks = cur_duel.problems.all()
        self.task = self.tasks[int(task_num) - 1]
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uidb = self.kwargs["uidb"]
        task_num = self.kwargs.get("task_num", 1)
        tab = self.kwargs["tab"]

        if tab == "submissions":
            subs = submissions.models.Submission.objects.filter(
                duel__uuid=uidb,
                problem__id=self.task.id,
            ).order_by("-pk")
            context["submissions"] = subs

        cur_lobby = django.core.cache.cache.get("lobby_users_" + uidb)
        players = (
            django.contrib.auth.get_user_model()
            .objects.filter(
                id__in=cur_lobby,
            )
            .all()
        )

        # duration = datetime.timedelta(
        #     seconds=20,
        # )  # Можно на время разработки регулировать секунды

        # А в итоге будет так
        duration = datetime.timedelta(
            seconds=sum(task.duration.total_seconds() for task in self.tasks),
        )

        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60

        context["duration"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        context["players"] = players
        context["uidb"] = uidb
        context["task_num"] = int(task_num)
        context["tab"] = tab
        context["task"] = self.task  # current task
        self.task = context["task"]
        print(self.task)
        context["cnt"] = self.tasks
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
            problem_id=self.task.id,
            user_id=self.request.user.id,
            duel=duel.models.Duel.objects.get(uuid=uidb_url),
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
            "title": "Результаты",
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
