from django.test import TestCase, Client
from django.urls import reverse
from social.models import Friend
from .factories import UserModelFactory, FriendFactory, PostFactory
from social.models import User

# START - code was developed with the help of documentation and other external research, please see referenced links.

# tests user search, list friends, modify friends and display friends functionality
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client
# https://factoryboy.readthedocs.io/en/latest/
# https://factoryboy.readthedocs.io/en/latest/
# https://factoryboy.readthedocs.io/en/latest/
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.force_login
# https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse
# https://docs.djangoproject.com/en/4.2/topics/db/queries/
# https://code.djangoproject.com/ticket/11475
class TestViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()  
        self.user1 = UserModelFactory()  
        self.user2 = UserModelFactory()
        self.user3 = UserModelFactory()
        self.friend = FriendFactory(current_user=self.user1)  
        self.friend.users.add(self.user2)
        self.post = PostFactory(author=self.user1)  
        self.client.force_login(self.user1)  

    # tests search functionality
    def test_user_search_func(self):
        response = self.client.post(reverse('profile-search'), {'searched_term': self.user2.username})  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)

    # test  list_users functionality
    def test_list_users_func(self):
        response = self.client.get(reverse('list_users'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username) 
    
    # tests for adding new friends via modify_friends()
    def test_modify_friends_add_func(self):
        response = self.client.get(reverse('modify_friends', args=['add', self.user3.pk]))  
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user3 in Friend.objects.get(current_user=self.user1).users.all()) 

    # tests for removing friends via modify_friends func
    def test_modify_friends_remove_func(self):
        response = self.client.get(reverse('modify_friends', args=['remove', self.user2.pk])) 
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user2 in Friend.objects.get(current_user=self.user1).users.all())

    # tests for displaying friends
    def test_display_friends(self):
        response = self.client.get(reverse('view-friends', args=[self.user1.pk])) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)


# References:
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client
# https://factoryboy.readthedocs.io/en/latest/
# https://factoryboy.readthedocs.io/en/latest/
# https://factoryboy.readthedocs.io/en/latest/
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.force_login
# https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse
# https://docs.djangoproject.com/en/4.2/topics/db/queries/
# https://code.djangoproject.com/ticket/11475

# END - code was developed with the help of documentation and other external research, please see referenced links.