from django.urls import path

import lobby.consumers

websocket_urlpatterns = [
    path("play/<uidb>/", lobby.consumers.LobbyConsumer.as_asgi()),
]
