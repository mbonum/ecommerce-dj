import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # self.channel_name=pointer to the channel layer instance and the channel name that will reach the consumer
        await self.accept()
        # Send message when a user connects
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "opener",
                "opener": "Hi, please save in bookmarks this page if you want to contact us directly.",
                "clvm": "CLVM",
            },
        )

    async def opener(self, event):
        message = event["opener"]
        username = event["clvm"]

        await self.send(
            text_data=json.dumps({"opener": message, "clvm": username})
        )

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from webSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        room = data["room"]

        await self.save_message(username, room, message)

        # Send message to room, "username": username
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message},
        )

    # Receive message from room
    async def chat_message(self, event):
        message = event["message"]
        # username = event["username"], "username": username

        await self.send(
            text_data=json.dumps(
                {"type": "chat_message", "message": message}
            )
        )

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)
