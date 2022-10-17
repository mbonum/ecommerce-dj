from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocker import AllowedHostsOriginValidator, OriginValidator

import chat.routing as c

application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(c.websocket_urlpatterns)),
        )
    }
)
