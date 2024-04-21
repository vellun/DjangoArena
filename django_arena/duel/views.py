import random

import django.contrib
import django.core.cache
import django.db.models
import django.http
import django.shortcuts
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

        context["task"] = tasks[task_num - 1]  # current task
        context["cnt"] = tasks
        context["task_num"] = task_num

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


class TestCodeView(django.views.View):
    def get(self, *args, **kwargs):
        if "errors" in kwargs:
            errors = kwargs["errors"]
            tests_all = kwargs["tests_all"]
            tests_passed = kwargs["tests_passed"]
        else:
            errors = ""
            tests_all = "Тестов нет"
            tests_passed = "Тестов нет"

        return django.shortcuts.render(
            self.request,
            "homepage/test.html",
            context={
                "errors": errors,
                "tests_all": tests_all,
                "tests_passed": tests_passed,
            },
        )

    def post(self, *args, **kwargs):
        code_text = self.request.POST.get("code")
        tests_text = self.request.POST.get("test")
        code_tester = CodeTester(code_text, tests_text)
        validation_res = code_tester.validate()
        if not validation_res:
            cur_errors = "Недопустимые ключевые слова в тексте"
            return self.get(args, kwargs, errors=cur_errors)

        tests_all, tests_passed, cur_errors = code_tester.run_tests()
        print(
            "Тестов всего было вот столько:",
            tests_all,
            "а прошло всего",
            tests_passed,
        )
        print(cur_errors)
        return self.get(
            args,
            kwargs,
            errors=cur_errors,
            tests_all=tests_all,
            tests_passed=tests_passed,
        )


class ResultsView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        uidb = self.kwargs["uidb"]

        cur_duel = django.shortcuts.get_object_or_404(
            duel.models.Duel,
            uuid=uidb,
        )

        str_parameter = (
            "duel_"
            + uidb
            + "_"
            + str(request.user.id)
            + "_"
            + "currently_testing"
        )
        currently_testing = django.core.cache.cache.get(str_parameter)

        user_score = None

        print(currently_testing)

        if currently_testing is None:
            django.core.cache.cache.set(str_parameter, "Testing")
            tasks = cur_duel.problems.all()
            code_tester = CodeTester()
            code_tester.test(
                request,
                tasks,
                uidb,
                request.user.id,
                str_parameter,
            )
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
