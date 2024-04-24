import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import chatrooms.urls
import duel.urls
import groups.urls
import homepage.urls
import lobby.urls
import notes.urls
import notifications.urls
import submissions.urls
import users.urls

urlpatterns = [
    django.urls.path("", django.urls.include(homepage.urls)),
    django.urls.path("users/", django.urls.include(users.urls)),
    django.urls.path(
        "notifications/",
        django.urls.include(notifications.urls),
    ),
    django.urls.path("duel/", django.urls.include(duel.urls)),
    django.urls.path("play/", django.urls.include(lobby.urls)),
    django.urls.path("chat/", django.urls.include(chatrooms.urls)),
    django.urls.path("submissions/", django.urls.include(submissions.urls)),
    django.urls.path("groups/", django.urls.include(groups.urls)),
    django.urls.path("blog/", django.urls.include(notes.urls)),
    django.urls.path("admin/", django.contrib.admin.site.urls),
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
