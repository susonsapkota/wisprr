from django.forms import ModelForm
from django import forms
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_img', 'username', 'description']
        widgets = {
            'profile_img': forms.FileInput(),
            'username': forms.TextInput(attrs={'placeholder': 'Add display name'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add information'})
        }
