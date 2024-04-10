from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .factories import UserModelFactory

# START - code was developed with the help of documentation and other external research, please see referenced links.

# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.login
# https://docs.djangoproject.com/en/stable/ref/request-response/#httpresponse.status_code
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.assertContains
# https://docs.djangoproject.com/en/stable/ref/request-response/#httpresponse-redirect

class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sometestuser', password='sometestpassword')
   
    # tests user profile view auth user status code
    def test_user_profile_view_auth_user_status_code(self):
        self.client.login(username='sometestuser', password='sometestpassword')
        response = self.client.get(reverse('user-profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)

    # test for auth user's username
    def test_profile_view_auth_user_content(self):
        self.client.login(username='sometestuser', password='sometestpassword')
        response = self.client.get(reverse('user-profile', kwargs={'pk': self.user.pk}))
        self.assertContains(response, self.user.username)


    # tests for unauth user
    def test_profile_view_for_unauth_user(self):
        response = self.client.get(reverse('user-profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)

    # tests for non-existent user profile
    def test_profile_view_non_existent_user(self):
        dont_exist_pk = self.user.pk + 100
        response = self.client.get(reverse('user-profile', kwargs={'pk': dont_exist_pk}))
        self.assertEqual(response.status_code, 302)


# tests user profile view with factories
class FactoryUserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = UserModelFactory()

    # tests for auth user with factory
    def test_profile_view_auth_user_with_factory(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(reverse('user-profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)

    # test for unautht user with factory
    def test_profile_view_unauth_user_with_factory(self):
        response = self.client.get(reverse('user-profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)

    # tests for non-existent user profile with factory
    def test_profile_view_nonexistent_user_factory(self):
        dont_exist_pk = self.user.pk + 100
        response = self.client.get(reverse('user-profile', kwargs={'pk': dont_exist_pk}))
        self.assertEqual(response.status_code, 302)

# References: 
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.login
# https://docs.djangoproject.com/en/stable/ref/request-response/#httpresponse.status_code
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.assertContains
# https://docs.djangoproject.com/en/stable/ref/request-response/#httpresponse-redirect

# END - code was developed with the help of documentation and other external research, please see referenced links.