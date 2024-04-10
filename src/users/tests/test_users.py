from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# tests different authentications
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.get_user_model
# https://www.django-rest-framework.org/api-guide/testing/#apiclient
# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse
# https://www.django-rest-framework.org/api-guide/status-codes/
# https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication

User = get_user_model() 

class UserViewSetAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()  
        self.user = User.objects.create_user(username='user', password='somepassword')  
        self.staff = User.objects.create_user(username='staff', password='sometestpassword', is_staff=True)
        self.superuser = User.objects.create_user(username='superuser', password='sometestpassword', is_superuser=True)

    # tests for unauthenticated user
    def test_get_queryset_for_unauthenticated_user(self):
        response = self.client.get(reverse('user-list'))  
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    # tests that authenticated users can see user list
    def test_get_queryset_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)  
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # tests user creation for unauthenticated users
    def test_create_for_unauthenticated_user(self):
        response = self.client.post(reverse('user-list'), data={'username': 'somenewuser', 'password': 'sometestpassword'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertTrue(User.objects.filter(username='somenewuser').exists())

    # tests user creation for authenticated users
    def test_create_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('user-list'), data={'username': 'somenewuser2', 'password': 'sometestpassword'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertTrue(User.objects.filter(username='somenewuser2').exists())

# References:
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.get_user_model
# https://www.django-rest-framework.org/api-guide/testing/#apiclient
# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse
# https://www.django-rest-framework.org/api-guide/status-codes/
# https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication

# END - code was developed with the help of documentation and other external research, please see referenced links. 