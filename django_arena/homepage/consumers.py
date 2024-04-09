import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.lobby_id = f'lobby_id_{self.scope["url_route"]["kwargs"]["uidb"]}'

        async_to_sync(self.channel_layer.group_add)(
            self.lobby_id,
            self.channel_name,
        )

        self.accept()

    def disconnect(self):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_id,
            self.channel_name,
        )
        raise StopConsumer()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.lobby_id,
            {"type": "lobby.message", "message": message},
        )

    # Receive message from room group
    def lobby_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


__all__ = [LobbyConsumer]
