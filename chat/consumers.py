# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['pk']
        self.chat = 'chat_%s' % self.chat_id

        async_to_sync(self.channel_layer.group_add)(
            self.chat,
            self.channel_name
        )

        self.accept()

    def disconnect(self, closing_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']

        async_to_sync(self.channel_layer.group_send)(
            self.chat,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id
            }
        )

    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']

        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
        }))