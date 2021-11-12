import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.consumer import SyncConsumer
from django.utils.translation import gettext_lazy as _
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    # https://channels.readthedocs.io/en/latest/topics/consumers.html
    async def connect(self):
        self.room = self.scope["url_route"]["kwargs"]["room"]
        self.room_group = f"chat_{self.room}"
        # Join room
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        # self.channel_name points to the channel layer instance and the channel name that will reach the consumer
        await self.accept()

        # Send message when a user connects
        # await self.channel_layer.group_send(
        #     self.room_group,
        #     {
        #         "type": "chat_text",
        #         "user": "clavem",
        #         "text": _(
        #             "Hi, please keep open or save this page in bookmarks. We will answer you as soon as possible."
        #         ),  # You will receive an email.
        #     },
        # )

    # Leave room
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    # Receive message from webSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        usr = data["user"]
        room = data["room"]
        msg = data["text"]

        await self.save_message(usr, room, msg)

        # Send message to room
        await self.channel_layer.group_send(
            self.room_group,
            {"type": "chat_text", "text": msg, "user": usr},
        )

    # Receive message from room
    async def chat_text(self, event):
        usr = event["user"]
        msg = event["text"]

        await self.send(text_data=json.dumps({"user": usr, "text": msg}))

    @sync_to_async
    def save_message(self, usr, room, msg):
        Message.objects.create(username=usr, room=room, text=msg)


# class OpenConsumer(SyncConsumer):
#     # Send message when a user connects
#     def websocket_connect(self, event):
#         self.send(
#             {
#                 "type": "websocket.accept",
#                 "text": _(
#                     "Hi, please keep open or save this page in bookmarks. We will answer you as soon as possible."
#                 ),  # You will receive an email.
#             }
#         )

#     def websocket_receive(self, event):
#         self.send(
#             {"type": "websocket.send", "text": event["text"], "user": "Clavem team"}
#         )