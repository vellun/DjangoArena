import uuid
import re

from django.core.cache import cache
import django.http
from django.http import HttpResponse
import django.shortcuts
import django.views.decorators.http


class CodeTester:
    def __init__(self, code, tests):
        self.code = code
        self.tests_code = tests
        self.function_names = []
        self.exec_code = self.create_file()

    def create_file(self):
        regex = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
        function_names = re.findall(regex, self.tests_code)
        function_names = [name + "()" for name in function_names]
        self.function_names = function_names
        return self.code + "\n" + self.tests_code

    def validate(self):
        stop_words = ["print(", "exit(", "sleep("]
        for word in stop_words:
            if word in self.exec_code:
                return False
        return True

    def run_tests(self):
        cur_errors = ""
        tests_all = len(self.function_names)
        tests_passed = 0
        cur_code = ""
        for function_name in self.function_names:
            try:
                globals_dict = {}
                cur_code = self.exec_code + "\n" + function_name
                exec(cur_code, globals_dict, globals_dict)
            except AssertionError as e:
                print("AssertionError", e)
                print(cur_code)
                cur_errors += str(e)
            except SyntaxError as e:
                print("SyntaxError", e)
                cur_errors += str(e)
            except NameError as e:
                print("NameError", e)
                cur_errors += str(e)
            except Exception as e:
                print("Unexpected error, probably send it to feedback form", e)
                cur_errors += str(e)
            else:
                tests_passed += 1

        return tests_all, tests_passed, cur_errors


class HomeView(django.views.View):
    def get(self, *args, **kwargs):
        context = {"title": "Главная", "link": uuid.uuid4().hex}
        return django.shortcuts.render(
            self.request,
            template_name="homepage/main.html",
            context=context,
        )


class LobbyView(django.views.View):
    def get(self, *args, **kwargs):
        uidb_url = kwargs.get("uidb")
        game_started = cache.get("lobby_game_started_" + uidb_url)
        cur_lobby = set(cache.get("lobby_users_" + uidb_url) or [])
        are_you_in_game = self.request.user.id in cur_lobby

        if not self.request.user.is_authenticated or (
                game_started and not are_you_in_game
        ):
            return HttpResponse("ВОООООООООООООООООН")

        cur_lobby.add(self.request.user.id)
        cache.set("lobby_users_" + uidb_url, set(cur_lobby))
        if cache.get("lobby_leader_" + uidb_url) is None:
            cache.set("lobby_leader_" + uidb_url, self.request.user.id)

        if cache.get("lobby_game_started_" + uidb_url) is None:
            cache.set("lobby_game_started_" + uidb_url, False)

        are_you_leader = (
                cache.get("lobby_leader_" + uidb_url) == self.request.user.id
        )

        context = {
            "title": "Главная",
            "are_you_leader": are_you_leader,
            "game_started": game_started,
        }

        return django.shortcuts.render(
            self.request,
            "homepage/lobby.html",
            context,
        )

    def post(self, *args, **kwargs):
        uidb_url = kwargs.get("uidb")
        cache.set("lobby_game_started_" + uidb_url, True)
        return django.shortcuts.redirect(
            django.urls.reverse("homepage:lobby", kwargs={"uidb": uidb_url}),
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

        return django.shortcuts.render(self.request, "homepage/test.html", context={"errors": errors, "tests_all": tests_all, "tests_passed": tests_passed})

    def post(self, *args, **kwargs):
        code_text = self.request.POST.get("code")
        tests_text = self.request.POST.get("test")
        code_tester = CodeTester(code_text, tests_text)
        validation_res = code_tester.validate()
        if not validation_res:
            cur_errors = "Недопустимые ключевые слова в тексте"
            return self.get(args, kwargs, errors=cur_errors)
        tests_all, tests_passed, cur_errors = code_tester.run_tests()
        print("Тестов всего было вот столько:", tests_all, "а прошло всего", tests_passed)
        print(cur_errors)
        return self.get(args, kwargs, errors=cur_errors, tests_all=tests_all, tests_passed=tests_passed)


__all__ = []
