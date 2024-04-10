from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


# START - code was developed with the help of documentation and other external research, please see referenced links. 

class UsersAPITestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username="sometestuser", password="sometestpassword")    # [1]
        try:  # if a token already exists for the user
            self.token = Token.objects.get(user=self.test_user).key
        except Token.DoesNotExist: # otherwise generate a new token [2]
            self.token = Token.objects.create(user=self.test_user).key

        # API client [3]
        self.client = APIClient()

        # set API token in the headers [4]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    # tests users API endpoint
    def test_api_for_users(self):
        response = self.client.get('/api/users/')  # [5]
        self.assertEqual(response.status_code, 200)  # [6]

    # tests profile API endpoint - for 200 code
    def test_api_for_profile_response_200(self):
        response = self.client.get('/api/profile/')  
        self.assertEqual(response.status_code, 200)  

    # tests profile API endpoint - isInstance
    def test_api_for_profile_instance(self):
        response = self.client.get('/api/profile/')  
        self.assertIsInstance(response.data, list)  # [7]

    # tests profile API endpoint - equal
    def test_api_for_profile_equal(self):
        response = self.client.get('/api/profile/')  
        self.assertEqual(len(response.data), 1) 

     # tests profile API endpoint - user_data is not none
    def test_api_for_profile_data_IsNotNone(self):
        response = self.client.get('/api/profile/')  
        profile_data = response.data[0]
        # get user's key from the profile_data 
        user_data = profile_data.get('user', None)
        self.assertIsNotNone(user_data)  # confirm that user_data is not None

    # tests profile API endpoint - user_data exists
    def test_api_for_profile_username_exists(self):
        response = self.client.get('/api/profile/')  
        profile_data = response.data[0]
        # get user's key from the profile_data 
        user_data = profile_data.get('user', None)
        # get username key from user_data
        self.assertIn('username', user_data)  # confirm username key exists in user_data [8]
 
     # tests profile API endpoint - validate username
    def test_api_for_profile_confirm_username(self):
        response = self.client.get('/api/profile/')  
        profile_data = response.data[0]
        # get user's key from the profile_data 
        user_data = profile_data.get('user', None)
        self.assertEqual(user_data['username'], self.test_user.username)  # confirm username [9]

# References:
# [1]: https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# [2]: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
# [3]: https://www.django-rest-framework.org/api-guide/testing/#apiclient
# [4]: https://www.django-rest-framework.org/api-guide/testing/#setting-the-authorization-header
# [5]: https://www.django-rest-framework.org/api-guide/testing/#making-requests
# [6]: https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.assertEqual
# [7]: https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertIsInstance
# [8]: https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertIn
# [9]: https://docs.djangoproject.com/en/stable/ref/contrib/auth/#fields
# https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/user/tests/test_user_api.py

# END - code was developed with the help of documentation and other external research, please see referenced links. 