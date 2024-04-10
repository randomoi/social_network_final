from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from social.models import Message

# START - code was developed with the help of documentation and other external research, please see referenced links.

# tests chat view functionality
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client
# https://docs.djangoproject.com/en/stable/topics/testing/advanced/#django.test.RequestFactory
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user-objects
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.force_login
# https://docs.djangoproject.com/en/stable/ref/urlresolvers/#reverse
# https://docs.djangoproject.com/en/stable/ref/exceptions/#objectdoesnotexist
class ChatWithUsersViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username='sometestuser1', password='sometestpass1')
        self.user2 = User.objects.create_user(username='sometestuser2', password='sometestpass2')
        self.friend = User.objects.create_user(username='somefrienduser', password='somefriendpass')

    # tests room view for authenticated user
    def test_room_view_for_authenticated_user(self):
        self.client.force_login(self.user1)
        private_chat_room_name = f"chat_{self.user1.pk}_{self.user2.pk}"
        url = reverse('room', args=[private_chat_room_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test schat search view for authenticated user
    def test_chat_search_view_for_authenticated_user(self):
        self.client.force_login(self.user1)
        url = reverse('chat-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # tests chat with friend view for authenticated user
    def test_chat_with_friend_view_for_authenticated_user(self):
        self.client.force_login(self.user1)
        url = reverse('chat_with_users', args=[self.friend.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
         
    # tests chat with friend view for authenticated user post
    def test_chat_with_friend_view_for_authenticated_user_post(self):
        self.client.force_login(self.user1)
        url = reverse('chat_with_users', args=[self.friend.pk])
        message_content = "Hello, friend!"
        response = self.client.post(url, {'message': message_content})
        self.assertEqual(response.status_code, 302)  
        try:
            message = Message.objects.get(content=message_content)
            self.assertEqual(message.room, f"chat_{self.user1.pk}_{self.friend.pk}")
            self.assertEqual(message.user, self.user1)
        except ObjectDoesNotExist:
            self.fail("Sorry,chat message was not created in the database.")

# References:
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client
# https://docs.djangoproject.com/en/stable/topics/testing/advanced/#django.test.RequestFactory
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user-objects
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.force_login
# https://docs.djangoproject.com/en/stable/ref/urlresolvers/#reverse
# https://docs.djangoproject.com/en/stable/ref/exceptions/#objectdoesnotexist

# END - code was developed with the help of documentation and other external research, please see referenced links.
