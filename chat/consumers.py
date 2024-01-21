from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from chat.models import ChatMessage, ChatRoom
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self, *args, **kwargs):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, *args, **kwargs):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await self.accept()

    async def receive(self, text_data):
        body = json.loads(text_data)
        message = body.get("message")
        username = body.get("username")
        room = body.get("room")
        await self.save_message(username, room, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "room": room,
            },
        )

    # save message into db
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        chat_room = ChatRoom.objects.get(slug=room)
        ChatMessage.objects.create(user=user, room=chat_room, message=message)

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room = event["room"]
        await self.send(
            text_data=json.dumps(
                {"message": message, "username": username, "room": room}
            )
        )
