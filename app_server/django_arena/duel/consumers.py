import channels.generic.websocket

import duel.code_tester


class SubmissionTestingConsumer(
    channels.generic.websocket.AsyncWebsocketConsumer,
):
    async def connect(self):
        self.duel_uuid = self.scope["url_route"]["kwargs"]["uidb"]
        self.task_num = self.scope["url_route"]["kwargs"]["task_num"]
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]

        self.room_name = (
            f"testing_{self.duel_uuid}_{self.task_num}_{self.user_id}"
        )

        self.code_tester = duel.code_tester.CodeTester(
            self.duel_uuid,
            self.user_id,
        )

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"testing_{self.duel_uuid}_{self.task_num}_{self.user_id}",
            self.channel_name,
        )

    async def tests_result(self, event):
        result = event["result"]
        print(result)
        await self.send(
            text_data=result,
        )


__all__ = [SubmissionTestingConsumer]
