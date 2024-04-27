import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

import django.core.cache
import django.db.models
import django.http
import django.shortcuts
import django.views.decorators.http


def return_url_file(uidb):
    return (
        """
import django.urls
import """
        + uidb
        + """.views
urlpatterns = [
    django.urls.path(
        "",
        """
        + uidb
        + """.views.SolutionView.as_view(),
        name=\""""
        + uidb
        + """\",
    ),
]
"""
    )


class TestCodeView(django.views.generic.View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        uidb = self.kwargs.get("uidb")
        json_data = json.loads(request.body)
        submission_id = json_data["submission_id"]
        uidb = "start" + str(submission_id) + uidb

        os.system("python manage.py startapp " + uidb)
        os.system("cd " + uidb)

        code = json_data["code"]
        tests = json_data["tests"]
        tests = tests.replace("~~~", uidb)
        print("Отправленная задача:", code)
        print("Тесты:", tests)

        files_writelines(uidb, code, tests)

        start_time = time.time()
        output = subprocess.Popen(
            "python manage.py test " + uidb,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()[-1]

        end_time = time.time()
        elapsed_time = end_time - start_time
        output = output.decode("utf-8")
        print("Вывод:", output)

        remove_test_app(uidb)

        ran_tests_count = re.search(r"Ran (\d+)", output)
        failures_count = re.search(r"failures=(\d+)", output)
        errors_count = re.search(r"errors=(\d+)", output)

        match = re.search(
            r"(?P<error>[A-Za-z]+Error:.*$)",
            output,
            re.MULTILINE,
        )
        error_message = ""
        if match:
            error_message = match.group("error")

        ran_tests_count = (
            int(ran_tests_count.group(1)) if ran_tests_count else 0
        )
        failures_count = int(failures_count.group(1)) if failures_count else 0
        errors_count = int(errors_count.group(1)) if errors_count else 0

        failed_tests_count = failures_count + errors_count

        if failed_tests_count == 0:
            verdict = "Accepted"
            html = "<span style='color: #47b98d'> \
            Все тесты пройдены!</span>"
        else:
            verdict = f"{str(failed_tests_count)} failures"

        if failures_count:
            verdict = f"{str(failed_tests_count)} failures"
            html = f"Неверный ответ: {error_message}"
            html = html.replace("<", "&lt")
            html = html.replace(">", "&gt")
            html = "<span style='color:#ED9B6D'>" + html + "</span>"
        elif (
            error_message
            and "AssertionError" not in error_message
            or errors_count
        ):
            html = f"Ошибка: {error_message}"
            html = html.replace("<", "&lt")
            html = html.replace(">", "&gt")
            html = "<span style='color: red'>" + html + "</span>"

        print(error_message)

        return django.http.JsonResponse(
            {
                "ran_tests_count": ran_tests_count,
                "failures_count": failed_tests_count,
                "elapsed_time": elapsed_time,
                "verdict": verdict,
                "html": html,
            },
            status=200,
        )


def files_writelines(uidb, code, tests):
    with Path(f"{uidb}/views.py").open(mode="w") as file:
        file.writelines(code)

    with Path(f"{uidb}/tests.py").open(mode="w") as file:
        file.writelines(tests)

    with Path(f"{uidb}/urls.py").open(mode="w") as file:
        file.writelines(return_url_file(uidb))

    with Path("django_arena_testing/urls.py").open(mode="a") as file:
        new_url = [
            f"import {uidb}.views\n",
            f'urlpatterns += [path("{uidb}/", {uidb}'
            ".views.SolutionView.as_view(), "
            f"name='{uidb}')]\n",
        ]
        file.writelines(new_url)


def remove_test_app(uidb):
    os.system("cd ..")
    shutil.rmtree(uidb)
    text_to_remove = uidb

    with Path("django_arena_testing/urls.py").open(mode="r") as file:
        lines = file.readlines()

    lines = [line for line in lines if text_to_remove not in line]
    with Path("django_arena_testing/urls.py").open(mode="w") as file:
        file.writelines(lines)


__all__ = []
