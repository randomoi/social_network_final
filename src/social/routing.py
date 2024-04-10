from django.urls import path
from . import consumers
# START - code was developed with the help of documentation and other external research, please see referenced links. 
websocket_urlpatterns = [
    path('ws/<str:private_chat_room_name>/', consumers.ChatConsumer.as_asgi()),
]

# References:
# https://channels.readthedocs.io/en/latest/tutorial/index.html
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_1.html
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_2.html

# END - code was developed with the help of documentation and other external research, please see referenced links. 