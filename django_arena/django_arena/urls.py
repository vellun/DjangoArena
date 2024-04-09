import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import homepage.urls


urlpatterns = [
    django.urls.path("", django.urls.include(homepage.urls)),
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