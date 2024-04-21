from django.conf import settings
import django.core.cache
import requests

import core.models


class CodeTester:
    def test(self, request, tasks, duel_id, user_id, finish_parameter):
        user_score = 0
        cur_task = 1
        user = core.models.User.objects.get(pk=user_id)
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

            if data["ran_tests_count"] - data["failures_count"] > 0:
                if task.difficulty == "easy":
                    user.easy_problems += 1
                elif task.difficulty == "medium":
                    user.medium_problems += 1
                else:
                    user.hard_problems += 1

                user.save()

            user_score += (
                data["ran_tests_count"] / data["failures_count"] * 100
            )
            cur_task += 1

        user_score_parameter = (
            "duel_" + duel_id + "_" + str(user_id) + "_" + "score"
        )
        user.rating = max(user.rating + user_score, 0)
        user.games_played += 1
        user.save()
        django.core.cache.cache.set(user_score_parameter, user_score)
        django.core.cache.cache.set(finish_parameter, "Finished")


__all__ = [CodeTester]
