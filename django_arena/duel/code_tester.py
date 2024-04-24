from django.conf import settings
import django.core.cache
import requests

import core.models
import duel.models
import submissions.models


class CodeTester:
    def __init__(self, duel_uidb="", user_id=0):
        self.duel_uidb = duel_uidb
        self.user_id = user_id

    def get_finish_parameter(self, submission_id):
        submission = submissions.models.Submission.objects.get(
            pk=submission_id
        )
        task_id = submission.problem_id
        return f"duel_{ self.duel_uidb }_{ self.user_id }_finish_parameter_{ task_id }_submission_{ submission_id }"

    def get_score_parameter(self, submission_id):
        submission = submissions.models.Submission.objects.get(
            pk=submission_id
        )
        task_id = submission.problem_id
        return f"duel_{ self.duel_uidb }_{ self.user_id }_score_task_{ task_id }_submission_{ submission_id }"

    def get_verdict_parameter(self, submission_id):
        submission = submissions.models.Submission.objects.get(
            pk=submission_id
        )
        task_id = submission.problem_id
        return f"duel_{ self.duel_uidb }_{ self.user_id }_verdict_{ task_id }_submission_{ submission_id }"

    def get_exec_time_parameter(self, submission_id):
        submission = submissions.models.Submission.objects.get(
            pk=submission_id
        )
        task_id = submission.problem_id
        return f"duel_{ self.duel_uidb }_{ self.user_id }_exec_time_{ task_id }_submission_{ submission_id }"

    def get_code_parameter(self, submission_id):
        submission = submissions.models.Submission.objects.get(
            pk=submission_id
        )
        task_id = submission.problem_id
        return f"duel_{ self.duel_uidb }_{ self.user_id }_code_{ task_id }_submission_{ submission_id }"

    def prepare_parameters(self, submission_id):
        self.finish_parameter = self.get_finish_parameter(submission_id)
        self.score_parameter = self.get_score_parameter(submission_id)
        self.verdict_parameter = self.get_verdict_parameter(submission_id)
        self.exec_time_parameter = self.get_exec_time_parameter(submission_id)
        self.code_parameter = self.get_code_parameter(submission_id)

    def run_testing(self, submission_id):
        current_duel = django.shortcuts.get_object_or_404(
            duel.models.Duel,
            uuid=self.duel_uidb,
        )
        submission = submissions.models.Submission.objects.get(
            pk=submission_id
        )
        current_tasks = current_duel.problems.all()
        task_num = 1
        for task in current_tasks:
            if task.id == submission.problem_id:
                break
            task_num += 1

        self.task_num = task_num
        current_task = current_tasks[int(task_num)]
        current_code = django.core.cache.cache.get(self.code_parameter)

        with current_task.tests_file.open() as file:
            tests_content = file.read()

        tests_content = tests_content.decode("utf-8")

        payload = {
            "code": current_code,
            "tests": tests_content,
            "submission_id": submission_id,
        }
        url = (
            "http://"
            + settings.ARENA_TESTING_HOST
            + "/test/"
            + self.duel_uidb
            + "/"
        )
        print(url)
        print(payload)
        response = requests.post(url, json=payload)

        return response.json()

    def save_results(self, response_data, submission_id):
        current_duel = django.shortcuts.get_object_or_404(
            duel.models.Duel,
            uuid=self.duel_uidb,
        )
        current_task = current_duel.problems.all()[int(self.task_num)]
        current_user = core.models.User.objects.get(pk=self.user_id)

        if (
            response_data["ran_tests_count"] - response_data["failures_count"]
            > 0
        ):
            if current_task.difficulty == "easy":
                current_user.easy_problems += 1
            elif current_task.difficulty == "medium":
                current_user.medium_problems += 1
            else:
                current_user.hard_problems += 1
            current_user.save()

        user_score = (
            response_data["ran_tests_count"]
            / (response_data["failures_count"] + 1)
            * 100
        )
        verdict = response_data["verdict"]
        current_user.rating = max(current_user.rating + user_score, 0)
        current_user.games_played += 1
        current_user.save()
        execution_time = round(response_data["elapsed_time"] * 1000)
        django.core.cache.cache.set(self.finish_parameter, "Finished")
        django.core.cache.cache.set(self.score_parameter, user_score)
        django.core.cache.cache.set(self.exec_time_parameter, execution_time)
        django.core.cache.cache.set(self.verdict_parameter, verdict)

    def test_task(self, submission_id):
        self.prepare_parameters(submission_id)
        response_data = self.run_testing(submission_id)
        self.save_results(response_data, submission_id)


__all__ = []
