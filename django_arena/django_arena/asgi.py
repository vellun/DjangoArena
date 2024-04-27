import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import chatrooms.routing
import duel.routing
import lobby.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_arena.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    lobby.routing.websocket_urlpatterns
                    + chatrooms.routing.websocket_urlpatterns
                    + duel.routing.websocket_urlpatterns,
                ),
            ),
        ),
    },
)
