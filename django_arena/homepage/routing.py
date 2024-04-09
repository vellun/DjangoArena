from django.urls import path

from homepage import consumers

websocket_urlpatterns = [
    path("play/<uidb>/", consumers.LobbyConsumer.as_asgi()),
]
