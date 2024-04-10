from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# tests user model serializer
# https://www.django-rest-framework.org/api-guide/testing/#apiclient
# https://www.django-rest-framework.org/api-guide/requests/#post
# https://www.django-rest-framework.org/api-guide/status-codes/#successful_2xx
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#get
class UserModelSerializerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient() 

    # tests user model serializer create
    def test_user_model_serializer_create(self):
        data = {
            'username': 'sometestuser',
            'email': 'sometestuser@somedomain.com',
            'password': 'sometestpassword'
        }
        response = self.client.post('/api/users/', data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        user = User.objects.get(username=data['username'])  
        self.assertIsNotNone(user)  
        self.assertEqual(user.email, data['email'])  

    # tests user model serializer create with missing fields
    def test_user_model_serializer_create_with_missing_fields(self):
        data = {
            'username': 'sometestuser',
        }
        response = self.client.post('/api/users/', data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
    
    # tests user model serializer create invalid_data
    def test_user_model_serializer_create_invalid_data(self):
        data = {
            'username': 'sometestuser',
            'email': 'invalid_email',  
            'password': 'sometestpassword'
        }
        response = self.client.post('/api/users/', data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

# tests profile serializer
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.get_user_model
# https://www.django-rest-framework.org/api-guide/testing/#apiclient
# https://www.django-rest-framework.org/api-guide/requests/#post
# https://www.django-rest-framework.org/api-guide/status-codes/#successful_2xx
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#get
class ProfileModelSerializerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='sometestuser', email='sometestuser@somedomain.com', password='sometestpassword')  
    
    # tests profile model serializer create invalid user id
    def test_profile_model_serializer_create_invalid_user_id(self):
        data = {
            'user': 9904945,  
            'image': 'users/tests/test_media/images/default.png',
            'video': 'users/tests/test_media/video/test_video.mp4',
        }
        response = self.client.post('/api/profile/', data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

# References:
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.get_user_model
# https://www.django-rest-framework.org/api-guide/testing/#apiclient
# https://www.django-rest-framework.org/api-guide/requests/#post
# https://www.django-rest-framework.org/api-guide/status-codes/#successful_2xx
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#get

# END - code was developed with the help of documentation and other external research, please see referenced links. 