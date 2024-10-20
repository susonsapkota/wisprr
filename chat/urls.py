"""
URL configuration for winwisprr project.

"""

from django.contrib import admin
from django.urls import path, include
from .views import chat, get_or_create_room

urlpatterns = [
    path('', chat, name='home'),
    path('chat/<username>', get_or_create_room, name='chat'),
    path('room/<room_name>', chat, name='chat_room'),

]
