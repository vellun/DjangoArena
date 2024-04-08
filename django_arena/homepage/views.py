import uuid

from django.core.cache import cache
import django.http
from django.http import HttpResponse
import django.shortcuts
import django.views.decorators.http


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
        # Start duel
        return django.shortcuts.redirect(
            django.urls.reverse("duel:duel", kwargs={"uidb": uidb_url}),
        )


__all__ = []
