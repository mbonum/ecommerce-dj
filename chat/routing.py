from django.urls import path#, re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r"ws/contact/(?P<room_name>\w+)/$",
    path("ws/contact/<str:room_name>/", consumers.ChatConsumer.as_asgi())
]
