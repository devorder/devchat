from django.shortcuts import render
from chat import models
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    rooms = models.ChatRoom.objects.all()
    ctx = {"rooms": rooms}
    return render(request, "chat/room.html", context=ctx)

@login_required(login_url='admin/login')
def chat(request, slug):
    chat = models.ChatRoom.objects.get(slug=slug)
    messages = models.ChatMessage.objects.filter(room=chat)
    ctx = {"chat": chat, "messages": messages}
    return render(request, "chat/chat.html", context=ctx)
