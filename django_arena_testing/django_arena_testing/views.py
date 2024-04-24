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


def testing(request, uidb):
    if request.method == "POST":
        json_data = json.loads(request.body)
        submission_id = json_data["submission_id"]
        uidb = "start" + str(submission_id) + uidb
        os.system("python manage.py startapp " + uidb)
        os.system("cd " + uidb)
        code = json_data["code"]
        tests = json_data["tests"]
        tests = tests.replace("~~~", uidb)
        print(code)
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
        print(output)
        ran_tests_count = re.search(r"Ran (\d+)", output)
        failures_count = re.search(r"failures=(\d+)", output)
        errors_count = re.search(r"errors=(\d+)", output)
        if ran_tests_count:
            ran_tests_count = int(ran_tests_count.group(1))
        else:
            ran_tests_count = 0

        if failures_count:
            failures_count = int(failures_count.group(1))
        else:
            failures_count = 0

        if errors_count:
            errors_count = int(errors_count.group(1))
        else:
            errors_count = 0

        failed_tests_count = failures_count + errors_count

        if failed_tests_count == 0:
            verdict = "Accepted"
        else:
            verdict = str(failed_tests_count) + " failures"

        time.sleep(15)

        os.system("cd ..")
        shutil.rmtree(uidb)
        text_to_remove = uidb

        with Path("django_arena_testing/urls.py").open(mode="r") as file:
            lines = file.readlines()

        lines = [line for line in lines if text_to_remove not in line]
        with Path("django_arena_testing/urls.py").open(mode="w") as file:
            file.writelines(lines)

        return django.http.JsonResponse(
            {
                "ran_tests_count": ran_tests_count,
                "failures_count": failed_tests_count,
                "elapsed_time": elapsed_time,
                "verdict": verdict,
            },
            status=200,
        )

    return django.http.HttpResponse("Use post method instead", status=400)


__all__ = []
