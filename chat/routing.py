from django.urls import path  # , re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r"ws/chat/(?P<room_name>\w+)/$",
    path("ws/contact/<str:room>/", consumers.ChatConsumer.as_asgi())  # room.html js
]
