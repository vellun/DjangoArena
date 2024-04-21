import re
import uuid

import django.http
import django.shortcuts
import django.views.decorators.http

import core.models
from duel.code_tester import CodeTester


class HomeView(django.views.View):
    def get(self, *args, **kwargs):
        context = {"title": "Главная", "link": uuid.uuid4().hex}
        return django.shortcuts.render(
            self.request,
            template_name="homepage/main.html",
            context=context,
        )


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


class ProfileView(django.views.View):
    def get(self, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = django.shortcuts.get_object_or_404(core.models.User, pk=user_id)
        context = {
            "user": user,
        }
        return django.shortcuts.render(
            self.request,
            "homepage/profile.html",
            context,
        )


__all__ = []
