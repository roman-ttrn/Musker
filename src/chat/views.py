from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Chat, Message
from .forms import MessageForm

@login_required
def chat_list(request):
    """Список всех чатов пользователя"""
    chats = request.user.chats.all()
    return render(request, 'chat_list.html', {'chats': chats})

@login_required
def chat_detail(request, chat_id):
    """Просмотр чата и отправка сообщения"""
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all().order_by('timestamp')

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    return render(request, 'chat_detail.html', {'chat': chat, 'messagesss': messages, 'form': form})

@login_required
def start_chat(request, user_id):
    """Создание нового чата (если его нет)"""
    user2 = get_object_or_404(User, id=user_id)

    chat = Chat.objects.filter(participants=request.user).filter(participants=user2).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, user2)

    return redirect('chat_detail', chat_id=chat.id)