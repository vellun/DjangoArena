import django.core.cache
import django.http
import django.shortcuts
import django.views.decorators.http

import lobby.forms


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
            "title": "Главная",
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
            django.urls.reverse("duel:duel", kwargs={"uidb": uidb_url}),
        )


class GameplaySettingsView(django.views.View):
    def dispatch(self, request, *args, **kwargs):
        self.form = lobby.forms.GameplaySettingsForm(request.POST or None)
        print(1)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        print(2)
        context = {
            "form": self.form,
        }

        return django.shortcuts.render(
            request,
            "includes/duel-popup.html",
            context,
        )


__all__ = [LobbyView]
