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

from duel.code_tester import CodeTester
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

        duration = datetime.timedelta(
            seconds=sum(task.duration.total_seconds() for task in self.tasks),
        )

        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60

        current_submissions = submissions.models.Submission.objects.filter(
            problem_id=self.task.id,
            user_id=self.request.user.id,
            duel=duel.models.Duel.objects.get(uuid=uidb),
        ).order_by("-id")

        last_submission = current_submissions.first()

        code_tester = CodeTester(
            duel_uidb=uidb,
            user_id=self.request.user.id,
        )

        if last_submission:
            testing_finished = django.core.cache.cache.get(
                code_tester.get_finish_parameter(last_submission.id)
            )
            testing_score = django.core.cache.cache.get(
                code_tester.get_score_parameter(last_submission.id)
            )
            testing_exec_time = django.core.cache.cache.get(
                code_tester.get_exec_time_parameter(last_submission.id)
            )
            testing_verdict = django.core.cache.cache.get(
                code_tester.get_verdict_parameter(last_submission.id)
            )

            if testing_finished == "Finished":
                last_submission = current_submissions.first()
                last_submission.score = testing_score
                last_submission.exec_time = testing_exec_time
                last_submission.verdict = testing_verdict
                last_submission.save()

        else:
            testing_finished = True

        context["duration"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        context["players"] = players
        context["uidb"] = uidb
        context["task_num"] = int(task_num)
        context["tab"] = tab
        context["task"] = self.task
        self.task = context["task"]
        context["cnt"] = self.tasks
        context["title"] = "Дуэль"
        context["submissions"] = current_submissions
        context["testing_finished"] = testing_finished

        return context

    def form_valid(self, form):
        code = form.cleaned_data.get("code")
        uidb_url = self.kwargs.get("uidb")
        task_num = self.kwargs.get("task_num", 1)

        submission = submissions.models.Submission(
            code=code,
            score=-1,
            problem_id=self.task.id,
            user_id=self.request.user.id,
            duel=duel.models.Duel.objects.get(uuid=uidb_url),
            exec_time=-1,
            verdict="",
        )
        submission.save()

        code_tester = CodeTester(
            duel_uidb=uidb_url,
            user_id=self.request.user.id,
        )

        code_parameter = code_tester.get_code_parameter(submission.id)
        django.core.cache.cache.set(code_parameter, code)

        testing_thread = Thread(
            target=code_tester.test_task,
            args=[submission.id],
        )
        testing_thread.start()

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

        current_duel = django.shortcuts.get_object_or_404(
            duel.models.Duel,
            uuid=uidb,
        )

        current_tasks = current_duel.problems.all()

        user_score = 0

        for task in current_tasks:
            task_submissions = submissions.models.Submission.objects.filter(
                duel=duel.models.Duel.objects.get(uuid=uidb),
                problem_id=task.id,
                user_id=self.request.user.id,
            ).order_by("-id")
            last_submission = task_submissions.first()
            if last_submission.score != -1:
                user_score += last_submission.score

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
