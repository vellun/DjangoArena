import json

import channels.generic.websocket
import django.core.cache
from django.urls import reverse


class LobbyConsumer(channels.generic.websocket.AsyncWebsocketConsumer):
    async def connect(self):
        self.uidb = self.scope["url_route"]["kwargs"]["uidb"]
        self.room_id = f"lobby_id_{self.uidb}"
        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_id,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json["command"]

        if command == "disconnect_user":
            user_id = text_data_json["user_id"]
            uidb = text_data_json["uidb"]
            username = text_data_json["username"]

            cur_lobby = set(
                django.core.cache.cache.get("lobby_users_" + uidb) or [],
            )
            cur_lobby = cur_lobby.discard(user_id)
            django.core.cache.cache.set(
                "lobby_users_" + uidb,
                cur_lobby,
                3600 * 10,
            )

            are_you_leader = django.core.cache.cache.get(
                "lobby_leader_" + uidb,
            ) == int(user_id)

            await self.channel_layer.group_send(
                self.room_id,
                {
                    "type": "del_player",
                    "is_leader": are_you_leader,
                    "todo": "del_user",
                    "username": username,
                },
            )

            await self.disconnect("")

        elif command == "start":
            await self.channel_layer.group_send(
                self.room_id,
                {
                    "type": "start",
                    "todo": "start_game",
                    "game_url": reverse(
                        "duel:duel",
                        args=[self.uidb, 1, "description"],
                    ),
                },
            )

    async def add_player(self, event):
        username = event["username"]
        image = event["image"]
        await self.send(
            text_data=json.dumps(
                {
                    "username": username,
                    "image": image,
                },
            ),
        )

    async def del_player(self, event):
        username = event["username"]
        todo = event["todo"]
        is_leader = event["is_leader"]
        await self.send(
            text_data=json.dumps(
                {
                    "username": username,
                    "todo": todo,
                    "is_leader": is_leader,
                },
            ),
        )

    async def start(self, event):
        todo = event["todo"]
        game_url = event["game_url"]
        await self.send(
            text_data=json.dumps(
                {
                    "todo": todo,
                    "game_url": game_url,
                },
            ),
        )


__all__ = [LobbyConsumer]
