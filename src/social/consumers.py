import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from social.models import Message  # Import the Message model
from django.contrib.auth.models import User
import base64
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from channels.db import database_sync_to_async

# START - code was developed with the help of documentation and other external research, please see referenced links.

# handles retrieval of timestamp last sent message
@database_sync_to_async  # makes function into asynchronous DB call
def retrieve_last_timestamp(user):
    last_msg = user.message_set.last()  # retrieve last message sent 
    return last_msg.timestamp if last_msg is not None else "You don't have Messages."  # return timestamp or a placeholder 

# handles WebSocket consumer for chat 
class ChatConsumer(AsyncWebsocketConsumer):
    # handles connecting to WS
    async def connect(self):
        # confirm if user is authenticated
        if not self.scope['user'].is_authenticated:
            await self.close()  # if not authenticated, close connection
        else:
            # retrieve private chat room name from URL and add user to private chat room's WebSocket group
            self.private_chat_room_name = self.scope['url_route']['kwargs']['private_chat_room_name']
            self.room_group_name = f'chat_{self.private_chat_room_name}'

            # separate private_chat_room_name into users and confirm if user belongs to the chat room
            chat_room_part = self.private_chat_room_name.split('_')
            if str(self.scope['user'].pk) not in chat_room_part[1:]:
                await self.close()  # if user doesnt belong to chat, close connection
                return
                
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # handles disconnecting from WS     
    async def disconnect(self, close_code):
        # when disconnected, remove user from WS group 
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # handles receiving data
    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get('username')
        room = data.get('room')
        user = await self.get_or_create_user(username)

        # handles text messages
        message = data.get('message')
        if message:
            timestamp = await retrieve_last_timestamp(user)
            await self.save_text_message(user, room, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_text_message',
                    'message': message,
                    'username': username,
                    'timestamp': str(timestamp),
                }
            )

        # handls image messages
        image_base64 = data.get('image')
        if image_base64:
            message = await self.save_image_message(user, room, image_base64) 
            timestamp = await retrieve_last_timestamp(user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_image_message',
                    'image_url': message.file.url,
                    'username': username,
                    'timestamp': str(timestamp),
                }
            )
    # handles text chat messages
    async def chat_text_message(self, event):
        message = event.get('message')
        username = event.get('username')
        timestamp = event.get('timestamp')  

        if message is not None and username is not None:  # confirm if not None before sending
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'timestamp': str(timestamp),
            }))
        else:
            print('username or text message is None')
    
    # handles image chat messages
    async def chat_image_message(self, event):
            image_url = event.get('image_url')
            username = event.get('username')
            timestamp = event.get('timestamp')  

            print(f"Sending image URL: {image_url}") # print image URL

            if image_url and username:
                await self.send(text_data=json.dumps({
                    'image_url': image_url,
                    'username': username,
                    'timestamp': str(timestamp),
                }))
            else:
                print('username or image is None.')

    @sync_to_async  # makes func into asynchronous DB call
    def get_or_create_user(self, username):
        # get or create user based on specified username
        user, created = User.objects.get_or_create(username=username)
        return user

    # handles saving of text message 
    @sync_to_async
    def save_text_message(self, user, room, content):
        Message.objects.create(
            user=user,
            username=user.username,
            room=room,
            content=content,
        )

    # handles saving of image message 
    @database_sync_to_async
    def save_image_message(self, user, room, image_base64):
        image_data = base64.b64decode(image_base64)
        image_bytes_io = BytesIO(image_data)
        image_file = InMemoryUploadedFile(image_bytes_io, None, 'image.jpg', 'image/jpeg', len(image_data), None)
        return Message.objects.create(
            user=user,
            room=room,
            file=image_file
        )
# References:
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_1.html
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_2.html
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html
# https://channels.readthedocs.io/en/latest/tutorial/index.html
# https://channels.readthedocs.io/en/latest/topics/consumers.html
# https://channels.readthedocs.io/en/latest/topics/channel_layers.html#groups
# https://docs.djangoproject.com/en/3.2/topics/db/queries/
# https://channels.readthedocs.io/en/latest/topics/databases.html
# https://stackoverflow.com/questions/64188904/django-channels-save-messages-to-database
# https://stackoverflow.com/questions/61926359/django-synchronousonlyoperation-you-cannot-call-this-from-an-async-context-u
# https://stackoverflow.com/questions/68546624/using-channels-outside-consumers-py-but-function-in-consumers-not-firing
# https://forum.djangoproject.com/t/websocket-connection-failed-in-production-nginx-gunicorn-daphne-django-react/20683
# https://github.com/LonamiWebs/Telethon/issues/1018
# https://github.com/mitchtabian/Codingwithmitch-Chat/blob/master/chat/consumers.py
# https://testdriven.io/blog/django-channels/
# https://stackoverflow.com/questions/76024087/waiting-for-websocket-connection-in-django-channels-consumer
# https://github.com/django/channels_redis/issues/167
# https://github.com/django/channels/issues/1920
# https://buildmedia.readthedocs.org/media/pdf/channels/latest/channels.pdf
# https://forum.djangoproject.com/t/self-scope-user-always-returns-anonymous-user/17873
# https://github.com/django/channels/issues/718
# https://snyk.io/advisor/python/channels/functions/channels.testing.WebsocketCommunicator

# END - code was developed with the help of documentation and other external research, please see referenced links.