import datetime
import uuid

import django.http
import django.shortcuts
import django.views.decorators.http

import core.models
import notes.models


class HomeView(django.views.View):
    def get(self, *args, **kwargs):
        a_week_ago = django.utils.timezone.now() - datetime.timedelta(weeks=1)
        note_of_a_week = notes.models.Note.objects.filter(
            created_at__gte=a_week_ago,
        ).order_by("-likes").first()
        top_users = core.models.User.objects.order_by("-rating")[:5]
        context = {
            "title": "Главная",
            "link": uuid.uuid4().hex,
            "top_users": top_users,
            "note_of_a_week": note_of_a_week,
        }
        return django.shortcuts.render(
            self.request,
            template_name="homepage/main.html",
            context=context,
        )


__all__ = []
