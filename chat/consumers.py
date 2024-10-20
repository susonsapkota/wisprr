import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from chat.models import Room, GroupMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room = get_object_or_404(Room, name=self.room_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name,
        )

        # handling the online user
        if self.user not in self.room.online_users.all():
            self.room.online_users.add(self.user)
            self.update_count()

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        json_body = json.loads(text_data)
        msg_body = json_body['body']
        message = GroupMessage.objects.create(
            room=self.room,
            user=self.user,
            body=msg_body
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }
        html_partial = render_to_string('chat/partial/msg_p.html', context=context)
        self.send(text_data=html_partial)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name)

        self.room.online_users.remove(self.user)
        self.update_count()

    def update_count(self):
        online = self.room.online_users.count() - 1
        event = {
            'type': 'online_count_handler',
            'online_count': online,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, event
        )

    def online_count_handler(self, event):
        online = event['online_count']
        html = render_to_string("chat/partial/count_p.html", {'online_count': online})
        self.send(text_data=html)
