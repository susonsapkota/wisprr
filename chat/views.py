from lib2to3.fixes.fix_input import context

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from chat.models import Room
from chat.forms import MessageForm


# Create your views here.

@login_required
def chat(request, room_name='public'):
    room = get_object_or_404(Room, name=room_name)
    chat_messages = room.chat_messages.all()[:30]
    form = MessageForm()

    other_user = None
    if room.is_private:
        if request.user not in room.members.all():
            raise Http404()
        for member in room.members.all():
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.room = room
            message.save()
            form = MessageForm()
            context = {
                'message': message,
                'user': request.user,
                'form': form,
            }
            return render(request, 'chat/partial/msg_p.html', context)

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': room.name,
        'chat_group': room_name
    }

    return render(request, 'chat/chat.html', context)


@login_required
def get_or_create_room(request, username):
    if request.user.username == username:
        return redirect('home')

    chat_user = User.objects.get(username=username)

    if chat_user:
        print(f"FOUND {chat_user}")
    else:
        print(f"NOT FOUND {chat_user}")

    user_room = request.user.chat_groups.filter(is_private=True)

    if user_room.exists():
        for chatroom in user_room:
            if chat_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                print("SUS:1")
                chatroom = Room.objects.create(is_private=True)
                chatroom.members.add(chat_user, request.user)
    else:
        print("SUS:2")
        chatroom = Room.objects.create(is_private=True)
        chatroom.members.add(chat_user, request.user)

    return redirect('chat_room', chatroom.name)
