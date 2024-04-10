from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Profile
from .factories import UserModelFactory
from django.contrib.messages import get_messages

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# tests list view for all profiles
# https://www.django-rest-framework.org/api-guide/testing/#apiclient
# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#user-model
# https://docs.djangoproject.com/en/3.2/topics/db/queries/
class DRFProfileViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient() 
        self.user = User.objects.create_user(username='sometestuser', password='sometestpassword') 
        self.staff = User.objects.create_user(username='somestaff', password='sometestpassword', is_staff=True) 
        self.superuser = User.objects.create_user(username='somesuperuser', password='sometestpassword', is_superuser=True)  
        self.profile_user = Profile.objects.get(user_id=self.user.id)  
        self.profile_staff = Profile.objects.get(user_id=self.staff.id)
        self.profile_superuser = Profile.objects.get(user_id=self.superuser.id)

    # tests get queryset authenticated drf
    # https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
    def test_get_queryset_authenticated_drf(self):
        self.client.force_authenticate(user=self.user) 
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(len(response.data), 1)  

    # tests get queryset unauthenticated drf
    # https://docs.djangoproject.com/en/3.2/ref/urlresolvers/#reverse
    # https://www.django-rest-framework.org/api-guide/status-codes/
    def test_get_queryset_unauthenticated_drf(self):
        response = self.client.get(reverse('profile-list'))  
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    # tests get queryset for staff drf
    def test_get_queryset_for_staff_drf(self):
        self.client.force_authenticate(user=self.staff) 
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  

    # tests get queryset for superuser drf
    def test_get_queryset_for_superuser(self):
        self.client.force_authenticate(user=self.superuser) 
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  

# tests standard user's profile page
# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#user-model
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.Client
# https://docs.djangoproject.com/en/3.2/ref/urlresolvers/
class StandardProfileViewTestCaseDjangoView(TestCase):
    def setUp(self):
        self.client = Client()  
        self.test_user = User.objects.create_user(username='sometestuser', password='password12345')  
        self.profile_url = reverse('profile') 
    
    # tests redirection if user not logged in
    # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.Client.get
    # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase.assertRedirects
    def test_redirection_if_user_not_logged_in(self):
        response = self.client.get(self.profile_url) 
        self.assertRedirects(response, f"{reverse('login')}?next={self.profile_url}")  
    
    # tests standard profile view with authenticated user
    # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.Client.login
    # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase.assertTemplateUsed
    def test_standard_profile_view_with_authenticated_user(self):
        self.client.login(username='sometestuser', password='password12345') 

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'users/profile.html') 
    
    # tests standard user profile update with valid data
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    # https://docs.djangoproject.com/en/3.2/ref/models/instances/#refreshing-objects-from-database
    def test_standard_user_profile_update_with_valid_data(self):
        self.client.login(username='sometestuser', password='password12345')

        response = self.client.post(self.profile_url, {
            'username': 'somenewuser',
            'email': 'somenewuser@somedomain.com',
        })

        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, self.profile_url)  

        self.test_user.refresh_from_db() 
        self.assertEqual(self.test_user.username, 'somenewuser') 
        self.assertEqual(self.test_user.email, 'somenewuser@somedomain.com') 

    # tests standard user profile update with invalid_data
    # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase.assertFormError
    def test_standard_user_profile_update_with_invalid_data(self):
        self.client.login(username='sometestuser', password='password12345')

        response = self.client.post(self.profile_url, {
            'username': '',
            'email': 'somenewuser@somedomain.com',
        })

        self.assertEqual(response.status_code, 200) 
        self.assertFormError(response, 'user_form', 'username', 'This field is required.')  

# References:
# https://www.django-rest-framework.org/api-guide/testing/#apiclient
# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#user-model
# https://docs.djangoproject.com/en/3.2/topics/db/queries/
# https://docs.djangoproject.com/en/3.2/ref/urlresolvers/#reverse
# https://www.django-rest-framework.org/api-guide/status-codes/
# https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
# https://factoryboy.readthedocs.io/en/latest/
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.Client
# https://docs.djangoproject.com/en/3.2/ref/urlresolvers/
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.Client.get
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase.assertRedirects
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.Client.login
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase.assertTemplateUsed
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
# https://docs.djangoproject.com/en/3.2/ref/models/instances/#refreshing-objects-from-database
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase.assertFormError

# END - code was developed with the help of documentation and other external research, please see referenced links. 
