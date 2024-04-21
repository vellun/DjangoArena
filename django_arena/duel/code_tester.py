from django.conf import settings
import django.core.cache

import json
import requests


class CodeTester:
    def test(self, request, tasks, duel_id, user_id, finish_parameter):
        user_score = 0
        cur_task = 1
        for task in tasks:
            str_parameter = (
                "duel_" + duel_id + "_" + str(cur_task) + "_" + str(user_id)
            )
            code = django.core.cache.cache.get(str_parameter)
            with task.tests_file.open() as file:
                content = file.read()

            content = content.decode("utf-8")
            print(content)
            print(code)
            payload = {"code": code, "tests": content}
            url = (
                "http://"
                + settings.ARENA_TESTING_HOST
                + "/test/"
                + duel_id
                + "/"
            )
            response = requests.post(url, json=payload)
            data = response.json()
            print(data)
            if data["failures_count"] == 0:
                data["failures_count"] = 0.1

            user_score += (
                data["ran_tests_count"] / data["failures_count"] * 100
            )
            cur_task += 1

        user_score_parameter = (
            "duel_" + duel_id + "_" + str(user_id) + "_" + "score"
        )
        django.core.cache.cache.set(user_score_parameter, user_score)
        django.core.cache.cache.set(finish_parameter, "Finished")


__all__ = [CodeTester]