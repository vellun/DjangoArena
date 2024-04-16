import django.urls

import duel.views

app_name = "duel"

urlpatterns = [
    django.urls.path(
        "<uidb>/<int:task_num>/",
        duel.views.DuelView.as_view(),
        name="duel",
    ),
    django.urls.path(
        "cache-code/<uidb>/",
        duel.views.CacheCodeView.as_view(),
        name="cache-code",
    ),
]
