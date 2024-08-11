import json

import asgiref.sync
import channels.generic.websocket
import django.contrib.auth

import chatrooms.models


class ChatConsumer(channels.generic.websocket.AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        await self.channel_layer.group_add(
            f"chat_{self.room_id}",
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"chat_{self.room_id}",
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        user_id = text_data_json["user_id"]
        room = text_data_json["room"]

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            f"chat_{self.room_id}",
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "user_id": user_id,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        user_id = event["user_id"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "user_id": user_id,
                },
            ),
        )

    @asgiref.sync.sync_to_async
    def save_message(self, username, room, message):
        user = django.contrib.auth.get_user_model().objects.get(
            username=username,
        )
        room = chatrooms.models.ChatRoom.objects.get(pk=room)

        chatrooms.models.Message.objects.create(
            user=user,
            room=room,
            content=message,
        )


__all__ = [ChatConsumer]
