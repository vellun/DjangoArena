import django.urls

import duel.views

app_name = "duel"

urlpatterns = [
    django.urls.re_path(
        r"^(?P<uidb>\w+)/(?P<task_num>\d+)/(?P<tab>description|submissions)/$",
        duel.views.DuelView.as_view(),
        name="duel",
    ),
    django.urls.path(
        "<uidb>/results/",
        duel.views.ResultsView.as_view(),
        name="results",
    ),
    django.urls.path(
        "<uidb>/timeout/",
        duel.views.DuelTimerView.as_view(),
        name="timeout",
    ),
    django.urls.path(
        "<uidb>/leave/",
        duel.views.LeaveDuelView.as_view(),
        name="leave",
    ),
    django.urls.path(
        "cache-code/<uidb>/",
        duel.views.CacheCodeView.as_view(),
        name="cache-code",
    ),
    django.urls.path(
        "cache-result/<uidb>/",
        duel.views.CacheTestsResultView.as_view(),
        name="cache-result",
    ),
]
