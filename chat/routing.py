from django.urls import path
from chat import consumers

web_socket_urlpatterns = [
    path("ws/<str:room_name>/", consumers.ChatConsumer.as_asgi(),  name="chat-room-async")
]
