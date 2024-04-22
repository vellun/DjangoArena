import uuid

import django.http
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


__all__ = []
