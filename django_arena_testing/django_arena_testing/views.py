import uuid
import os
import re
import subprocess
import shutil
import time
import django.core.cache
import django.db.models
import django.http
import json
from django.http import JsonResponse
import django.shortcuts
from django.urls import reverse
import django.views.decorators.http


def return_url_file(uidb):
    return f"""
import django.urls
import """ + uidb + """.views
urlpatterns = [
    django.urls.path(
        "",
        """ + uidb + """.views.SolutionView.as_view(),
        name=\"""" + uidb + """\",
    ),
]
"""


def testing(request, uidb):
    uidb = "start" + uidb
    print(uidb)
    if request.method == 'POST':
        os.system("python manage.py startapp " + uidb)
        os.system("cd " + uidb)
        json_data = json.loads(request.body)
        code = json_data['code']
        tests = json_data['tests']
        tests = tests.replace("~~~", uidb)
        print(code)
        with open(f"{uidb}/views.py", "w") as file:
            file.writelines(code)
        with open(f"{uidb}/tests.py", "w") as file:
            file.writelines(tests)
        with open(f"{uidb}/urls.py", "w") as file:
            file.writelines(return_url_file(uidb))
        with open(f"django_arena_testing/urls.py", "a") as file:
            new_url = [
                f"import {uidb}.views\n",
                f"urlpatterns += [path(\"{uidb}/\", {uidb}.views.SolutionView.as_view(), name='{uidb}')]\n",
            ]
            file.writelines(new_url)

        output = subprocess.Popen("python manage.py test " + uidb, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[-1]
        output = output.decode("utf-8")
        ran_tests_count = re.search(r'Ran (\d+)', output)
        failures_count = re.search(r'failures=(\d+)', output)
        if ran_tests_count:
            ran_tests_count = int(ran_tests_count.group(1))
        else:
            ran_tests_count = 0

        if failures_count:
            failures_count = int(failures_count.group(1))
        else:
            failures_count = 0

        os.system("cd ..")
        shutil.rmtree(uidb)
        text_to_remove = uidb

        with open(f"django_arena_testing/urls.py", 'r') as file:
            lines = file.readlines()
        lines = [line for line in lines if text_to_remove not in line]
        with open(f"django_arena_testing/urls.py", 'w') as file:
            file.writelines(lines)

        return django.http.JsonResponse({"ran_tests_count": ran_tests_count, "failures_count": failures_count}, status=200)
    else:
        return django.http.HttpResponse("", status=400)
