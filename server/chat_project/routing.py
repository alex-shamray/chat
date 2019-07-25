from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

import chat.routing
import notifications.routing
from household_budget.consumers import EchoConsumer
from oauth.channels.auth import JSONWebTokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': JSONWebTokenAuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns + notifications.routing.websocket_urlpatterns + [
            url(r'^ws/echo/$', EchoConsumer),
        ])
    ),
})
