import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import duel.urls
import homepage.urls
import lobby.urls
import submissions.urls


urlpatterns = [
    django.urls.path("", django.urls.include(homepage.urls)),
    django.urls.path("duel/", django.urls.include(duel.urls)),
    django.urls.path("play/", django.urls.include(lobby.urls)),
    django.urls.path("submissions/", django.urls.include(submissions.urls)),
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("auth/", django.urls.include(django.contrib.auth.urls)),
]

if django.conf.settings.DEBUG:
    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include("debug_toolbar.urls"),
        ),
    )
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )

__all__ = []
