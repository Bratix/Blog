# chat_name/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from requests import request
from .models import Chat, Message
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.timezone import now

import sys
sys.path.append("..")
from blogapp.models import Notification
from blogapp.views import NOTIFICATION_CHAT

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        chat_id = self.scope['url_route']['kwargs']['pk']
        self.chat_name = 'chat_%s' % chat_id
        self.chat = Chat.objects.get(pk=chat_id)
        self.url = self.scope["url_route"]
        self.current_user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, closing_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        url = text_data_json['url']
        user = User.objects.get(pk = user_id)

        chat_message = Message.objects.create(
            chat = self.chat,
            user = user,
            text = message
        )
        self.chat.last_message = chat_message.time
        self.chat.save()

        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id
            }
        )

        if self.current_user == self.chat.user1:
            notify_user = self.chat.user2
            thumb_image = self.chat.user1.profile.image.url
        else:
            notify_user = self.chat.user1
            thumb_image = self.chat.user2.profile.image.url
        
        notification = Notification.objects.filter(Q(type=NOTIFICATION_CHAT) & Q(url = url)).first()
        
        if notification:
            notification.text = self.current_user.username + ": " + message
            notification.created_at = now()
            notification.save()
            
        else: 
            Notification.objects.create(
                user = notify_user,
                thumb_image = thumb_image,
                title = "New message",
                url = url,
                text = self.current_user.username + ": " + message,
                type = NOTIFICATION_CHAT
            )

    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']

        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
        }))