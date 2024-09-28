import json

from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404

from chat.models import Room, GroupMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        print('here')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room = get_object_or_404(Room, name=self.room_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']

        msg = GroupMessage.objects.create(
            room=self.room,
            user=self.user,
            body=message,
        )
