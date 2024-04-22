import uuid

import django.core.cache
import django.db.models
import django.http
import django.shortcuts
from django.urls import reverse
import django.views.decorators.http

import duel.models
import lobby.forms
import problems.models


class LobbyView(django.views.View):
    def get(self, *args, **kwargs):
        uidb_url = kwargs.get("uidb")
        game_started = django.core.cache.cache.get(
            "lobby_game_started_" + uidb_url,
        )
        cur_lobby = set(
            django.core.cache.cache.get("lobby_users_" + uidb_url) or [],
        )
        are_you_in_game = self.request.user.id in cur_lobby

        if not self.request.user.is_authenticated or (
            game_started and not are_you_in_game
        ):
            return django.http.HttpResponse("ВОООООООООООООООООН")

        cur_lobby.add(self.request.user.id)
        django.core.cache.cache.set("lobby_users_" + uidb_url, set(cur_lobby))
        if django.core.cache.cache.get("lobby_leader_" + uidb_url) is None:
            django.core.cache.cache.set(
                "lobby_leader_" + uidb_url,
                self.request.user.id,
            )

        if (
            django.core.cache.cache.get("lobby_game_started_" + uidb_url)
            is None
        ):
            django.core.cache.cache.set(
                "lobby_game_started_" + uidb_url,
                False,
            )

        are_you_leader = (
            django.core.cache.cache.get("lobby_leader_" + uidb_url)
            == self.request.user.id
        )

        context = {
            "title": "Лобби",
            "are_you_leader": are_you_leader,
            "game_started": game_started,
        }

        return django.shortcuts.render(
            self.request,
            "lobby/lobby.html",
            context,
        )

    def post(self, *args, **kwargs):
        uidb_url = kwargs.get("uidb")
        django.core.cache.cache.set("lobby_game_started_" + uidb_url, True)
        # Start duel
        return django.shortcuts.redirect(
            django.urls.reverse(
                "duel:duel",
                kwargs={"uidb": uidb_url, "task_num": 1, "tab": "description"},
            ),
        )


class GameplaySettingsView(django.views.View):
    def dispatch(self, request, *args, **kwargs):
        self.common_settings_form = lobby.forms.CommonGameplaySettingsForm(
            request.POST or None,
        )
        self.detailed_settings_form = lobby.forms.DetailedGameplaySettingsForm(
            request.POST or None,
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, checked_first=True):
        context = {
            "form1": self.common_settings_form,
            "form2": self.detailed_settings_form,
            "link": uuid.uuid4().hex,
            "checked_first": checked_first,
        }

        return django.shortcuts.render(
            request,
            "lobby/settings-form.html",
            context,
        )

    def post(self, request):
        form_type = request.POST.get("form_type")
        checked_first = True
        uidb = uuid.uuid4().hex
        success_json = django.http.JsonResponse(
            {
                "success": True,
                "link": reverse("lobby:lobby", args=[uidb]),
            },
        )

        if (  # If form 1 was submitted(tab 1 on modal window)
            form_type == "form1" and self.common_settings_form.is_valid()
        ):
            form = self.common_settings_form

            number_of_tasks = form.cleaned_data.get("tasks")
            diff = form.cleaned_data.get("difficulty")

            tasks = problems.models.Problem.objects.filter(
                difficulty=diff,
            )[:number_of_tasks]

            new_duel = duel.models.Duel.objects.create(
                uuid=uidb,
            )
            new_duel.problems.set(tasks)
            new_duel.save()

            return success_json

        if (
            form_type == "form2"
        ):  # If form 2 was submitted(tab 2 on modal window)
            if self.detailed_settings_form.is_valid():
                form = self.detailed_settings_form

                easy = form.cleaned_data.get("easy_tasks")
                medium = form.cleaned_data.get("medium_tasks")
                hard = form.cleaned_data.get("hard_tasks")

                e_tasks = problems.models.Problem.objects.filter(
                    difficulty="easy",
                )[:easy]
                m_tasks = problems.models.Problem.objects.filter(
                    difficulty="medium",
                )[:medium]
                h_tasks = problems.models.Problem.objects.filter(
                    difficulty="hard",
                )[:hard]

                tasks = e_tasks | m_tasks | h_tasks

                new_duel = duel.models.Duel.objects.create(
                    uuid=uidb,
                )
                new_duel.problems.set(tasks)
                new_duel.save()

                return success_json

            # Flag to know which tab on modal window is should be active
            checked_first = False

        return self.get(request, checked_first=checked_first)


__all__ = [LobbyView]
