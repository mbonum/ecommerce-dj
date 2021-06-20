from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocker import AllowedHostsOriginValidator, OriginValidator

# import home.routing

# application = ProtocolTypeRouter({
#     "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(
#         URLRouter(
#             home.routing.websocket_urlpatterns
#         )
#     ),)
# })