from django.urls import path

import chatrooms.consumers

websocket_urlpatterns = [
    path("chat/<int:room_id>/", chatrooms.consumers.ChatConsumer.as_asgi()),
]
