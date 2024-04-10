from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.forms import UserAccountCreationForm

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# tests user registration/account creation
# Django test client: https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client
# https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.get
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.SimpleTestCase.assertTemplateUsed
class UserRegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client() 
        self.register_url = reverse('register')  

    # tests register get request
    def test_register_get_request(self):
        response = self.client.get(self.register_url) 
        self.assertEqual(response.status_code, 200) 
        self.assertIsInstance(response.context['form'], UserAccountCreationForm)  
        self.assertTemplateUsed(response, 'users/register.html') 

    # tests register post data invalid form  
    # https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.post
    # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#filter
    # https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.SimpleTestCase.assertFormError
    def test_registration_with_invalid_data(self):
        form_data = {
            'username': '',
            'email': 'sometestuser@somedomain.com',
            'password1': 'mypassword123',
            'password2': 'mypassword123'
        }

        response = self.client.post(self.register_url, data=form_data)  
        self.assertFalse(get_user_model().objects.filter(username='sometestuser').exists()) 
        self.assertEqual(response.status_code, 200)  
        self.assertFormError(response, 'form', 'username', 'This field is required.')  

    # tests user registration with valid data 
    # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#exists
    # https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.3
    # https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.SimpleTestCase.assertRedirects
    def test_user_registration_with_valid_data(self):
        form_data = {
            'username': 'sometestuser',
            'email': 'sometestuser@somedomain.com',
            'password1': 'mypassword123',
            'password2': 'mypassword123'
        }

        initial_user_count = get_user_model().objects.count()  
        response = self.client.post(self.register_url, data=form_data)  

        self.assertEqual(get_user_model().objects.count(), initial_user_count + 1) 
        self.assertTrue(get_user_model().objects.filter(username='sometestuser').exists())  
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('login')) 

        some_new_user = get_user_model().objects.latest('id') 
        self.assertEqual(some_new_user.username, 'sometestuser') 
        self.assertEqual(some_new_user.email, 'sometestuser@somedomain.com')

# References:
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client
# https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.get
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.SimpleTestCase.assertTemplateUsed
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.post
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#filter
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.SimpleTestCase.assertFormError
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#exists
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.3
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.SimpleTestCase.assertRedirects

# END - code was developed with the help of documentation and other external research, please see referenced links. 