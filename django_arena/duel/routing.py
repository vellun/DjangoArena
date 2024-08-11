from django.urls import path

import duel.consumers

websocket_urlpatterns = [
    path(
        "testing/<uidb>/<int:task_num>/<int:user_id>/",
        duel.consumers.SubmissionTestingConsumer.as_asgi(),
    ),
]
