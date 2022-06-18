# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<pk>\w+)$', consumers.ChatConsumer.as_asgi()),
    re_path(r'wss/(?P<pk>\w+)$', consumers.ChatConsumer.as_asgi()),
]