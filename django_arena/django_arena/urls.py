import django.conf
from django.contrib import admin
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import duel.urls
import homepage.urls


urlpatterns = [
    django.urls.path("", django.urls.include(homepage.urls)),
    django.urls.path("duel/", django.urls.include(duel.urls)),
    django.urls.path("admin/", admin.site.urls),
    django.urls.path("auth/", django.urls.include(django.contrib.auth.urls)),
]

if django.conf.settings.DEBUG:
    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include("debug_toolbar.urls"),
        ),
    )

__all__ = []
