from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_imgs/', blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        if self.username:
            return self.username
        else:
            return self.user.username

    @property
    def avatar(self):
        if self.profile_img:
            return self.profile_img.url
        else:
            return f'{settings.STATIC_URL}images/avatar.svg'
