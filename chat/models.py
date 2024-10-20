from django.contrib.auth.models import User
from django.db import models
import shortuuid


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True, default=shortuuid.uuid)
    online_users = models.ManyToManyField(User, related_name='online_users', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    room = models.ForeignKey(Room, related_name='chat_messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.body[:30]}'

    class Meta:
        ordering = ['-created_at']
