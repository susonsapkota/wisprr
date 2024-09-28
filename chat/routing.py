from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/room/<chatroom_name>", ChatConsumer.as_asgi()),
    #path("ws/online-status/", OnlineStatsConsumer.as_asgi()),
]
