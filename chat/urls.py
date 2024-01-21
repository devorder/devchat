from django.urls import path
from chat import views

urlpatterns = [
    path("", views.index,  name="chat"),
    path("<slug:slug>", views.chat,  name="chat-room")
]
