import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.contenttypes.models import ContentType

from .api.serializers import MessageSerializer
from .models import Person, Channel


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        message = await self.save_message(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps(MessageSerializer(message).data))

    @database_sync_to_async
    def save_message(self, message):
        user = self.scope['user']
        channel = Channel.objects.get(pk=self.room_name)
        author = Person.objects.get(user_type=ContentType.objects.get_for_model(user), user_id=user.id)
        return channel.messages.create(author=author, body=message)
