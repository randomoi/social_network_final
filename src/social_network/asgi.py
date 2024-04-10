import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

import social.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            social.routing.websocket_urlpatterns
        )
    )
})

# References:
# https://channels.readthedocs.io/en/latest/tutorial/index.html
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_1.html
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_2.html