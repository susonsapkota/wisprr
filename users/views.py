from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from users.forms import ProfileForm


# Create your views here.

@login_required
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile_onboarding'):
        profile_onboard = True
    else:
        profile_onboard = False

    return render(request, 'users/profile_edit.html', {'form': form, 'onboarding ': profile_onboard})


def profile_delete(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, we all will miss you... ')
        return redirect('home')
    return render(request, 'users/profile_delete.html')
