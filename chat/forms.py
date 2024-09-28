from django.forms import ModelForm
from django import forms

from chat.models import GroupMessage


class MessageForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Add message ...',
                       'autofocus': True, "id": "messageInput"})
        }
        labels = {
            'body': '',
        }
