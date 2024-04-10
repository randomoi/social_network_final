# this script is for demostration purposes, it is not meant to go in production this way.
# this scripts shows that token authentication is working
# order of imports is important, do not change
import os  

# default settings for Django 
# https://docs.djangoproject.com/en/stable/topics/settings/
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

import django 

# https://docs.djangoproject.com/en/stable/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage
django.setup()  

import requests 
from rest_framework.authtoken.models import Token  
from tabulate import tabulate
import json

# START - code was developed with the help of documentation and other external research, please see referenced links.

#  Django settings configuration
def configure_django_settings():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')  
    django.setup()  # setup Django 

def retrieve_api_data(url, token):
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization
    # https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers
    headers = {
        'Authorization': f'Token {token}',  # authorization header 
    }
    response = requests.get(url, headers=headers)  # make GET request 
    return response

def main():
    configure_django_settings()  
    users_api_url = 'http://127.0.0.1:8000/api/users/'
    profile_api_url = 'http://127.0.0.1:8000/api/profile/'
  
    # this is only for demonstration purposes!!! I know that this will make application vulnurable to attacks!!!``
    # token = 'f110de29c8437bd6e0a61cadaecdb87b8842ead4' # charlie token
    # token = '1dfbbe40d28c3fb9e46c3954f755b5933ec287d1' # admin token
    token = 'a81f1052720b32bfafbf9af91f9d715c6939ba00' # token demo user
    
    # make API requests with specified token
    response_for_users = retrieve_api_data(users_api_url, token)  # response for users API
    response_for_profile = retrieve_api_data(profile_api_url, token)  # response for profile API

    users_data = json.loads(response_for_users.text)
    profile_data = json.loads(response_for_profile.text)
  
    # print users API with JSON response 
    # https://docs.python-requests.org/en/latest/user/quickstart/#json-response-content
    # print response data
    print("API Response for User:")
    print(tabulate(users_data[:5], headers="keys", tablefmt="grid"))  # show 1st 5 records

    # print profile API JSON response
    print("\nAPI Response for Profile:")
    print(tabulate(profile_data[:5], headers="keys", tablefmt="grid"))  # show 1st 5 records
    
    # print response status codes
    print("API Response status code for Users:", response_for_users.status_code)  # users API status code
    print("API Response status code for Profile:", response_for_profile.status_code)  # profile API status code

if __name__ == "__main__":
    main()  

# References:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization
# https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers
# https://docs.python-requests.org/en/latest/user/quickstart/#json-response-content
# https://docs.python.org/3/library/__main__.html
# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
# https://docs.djangoproject.com/en/stable/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage
# https://docs.djangoproject.com/en/stable/topics/settings/

# END - code was developed with the help of documentation and other external research, please see referenced links.