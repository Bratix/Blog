# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['pk']
        self.chat = 'chat_%s' % self.chat_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.chat,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
        }))