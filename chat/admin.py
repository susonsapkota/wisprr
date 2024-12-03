from django.contrib import admin

from chat.models import Room, GroupMessage

# Register your models here.

import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Room, GroupMessage  # Import your models


# Custom Admin for GroupMessage
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_private')
    search_fields = ('name',)
    actions = ['export_room_messages']

    def export_room_messages(self, request, queryset):
        """
        Custom admin action to export all messages for selected rooms as a CSV file.
        """
        # Prepare the HTTP response with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="room_messages.csv"'

        # Create a CSV writer
        writer = csv.writer(response)
        # Write the header row
        writer.writerow(['Room', 'User', 'Message', 'Created At'])

        # Write the data rows
        for room in queryset:
            messages = GroupMessage.objects.filter(room=room)
            for message in messages:
                writer.writerow([room.name, message.user.username, message.body, message.created_at])

        return response

    export_room_messages.short_description = "Export messages for selected rooms"


# Register the models with the custom admin
admin.site.register(Room,RoomAdmin)
admin.site.register(GroupMessage)
