from django.contrib import admin

from chat.models import Room, GroupMessage

# Register your models here.

admin.site.register(Room)
admin.site.register(GroupMessage)