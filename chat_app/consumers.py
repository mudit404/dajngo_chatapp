# chat_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from channels.db import database_sync_to_async

import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("WebSocket connect initiated.")
        self.other_user = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_name = f'chat_{min(self.user.username, self.other_user)}_{max(self.user.username, self.other_user)}'
        self.room_group_name = f'chat_{self.room_name}'
        # self.room_group_name = f'chat_{min(self.user.username, self.other_username)}_{max(self.user.username, self.other_username)}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"[CONNECT] {self.user.username} connected to {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Disconnected from {self.room_group_name}")

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Save message to the database
        await self.save_message(self.scope['user'], self.other_user, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver_username, content):
        try:
            receiver = User.objects.get(username=receiver_username)
            message = Message(sender=sender, receiver=receiver, content=content)
            message.save()
            print(f"[SAVE_MESSAGE] Message saved: {message}")
        except Exception as e:
            print(f"[ERROR] Could not save message: {e}")