from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# tests signals for create and save user profile and create authentication token signal
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.get_user_model
# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.save
# https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.refresh_from_db
# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
class SignalsTestCase(TestCase):
    # tests create user profile signals
    def test_create_user_profile_signals(self):
        user = User.objects.create_user(username='sometestuser', email='sometestuser@somedomain.com', password='sometestpassword')  
        self.assertTrue(hasattr(user, 'profile')) 
        self.assertEqual(user.profile.user, user)  
    
    # tests save user profile signals
    def test_save_user_profile_signals(self):
        user = User.objects.create_user(username='sometestuser', email='sometestuser@somedomain.com', password='sometestpassword')  
        profile = user.profile

        user.username = 'updated_user123'
        user.save()  
        profile.refresh_from_db()  
        self.assertEqual(profile.user.username, 'updated_user123')
    
    # tests crreate authentication token signals
    def test_create_authentication_token_signals(self):
        user = User.objects.create_user(username='sometestuser', email='sometestuser@somedomain.com', password='sometestpassword')  

        token = Token.objects.get(user=user)  
        self.assertIsNotNone(token)  

# References:
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.get_user_model
# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.save
# https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.refresh_from_db
# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

# END - code was developed with the help of documentation and other external research, please see referenced links. 