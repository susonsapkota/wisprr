from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from chat.models import Room
from chat.forms import MessageForm


# Create your views here.

@login_required
def chat(request):
    room = get_object_or_404(Room, name='public')
    chat_messages = room.chat_messages.all()[:30]
    form = MessageForm()

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

    return render(request, 'chat/chat.html', {'chat_messages': chat_messages, 'form': form})
