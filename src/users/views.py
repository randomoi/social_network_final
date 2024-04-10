from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserAccountCreationForm, UpdateUserInfoForm, UpdateUserProfileForm
from .models import Profile
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserModelSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Profile
from .serializers import ProfileModelSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# START - code was developed with the help of documentation and other external research, please see referenced links.

# handles CRUD operations for User objects
# https://www.django-rest-framework.org/api-guide/viewsets/
# https://docs.djangoproject.com/en/stable/topics/db/queries/
# https://www.django-rest-framework.org/api-guide/serializers/
# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() # queryset to retrieve all users 
    serializer_class = UserModelSerializer # handles serialization of User 
    authentication_classes = [TokenAuthentication] # uses token authentication 

    # queryset to handle user permissions
    def get_queryset(self):
        if not self.request.user.is_authenticated: # if user is not authenticated
            return User.objects.none() # return None users
        elif self.request.user.is_staff or self.request.user.is_superuser: # if user is staff or superuser
            return User.objects.all() # return all users
        else:
            return User.objects.filter(id=self.request.user.id) # othereise return only authenticated user

    # permissions based on action
    # https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated
    def get_permissions(self):
        if self.action in ['create']: # anyone can create user
            return [AllowAny()]
        return [IsAuthenticated()] # must be authenticated to do anything else  

    # handles user creation
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # serialize requested data
        if serializer.is_valid(): # if data is valid
            user = serializer.save() # save user object
            user.set_password(serializer.validated_data['password']) # set password
            user.save() # save user object again
            return Response(serializer.data, status=status.HTTP_201_CREATED) # return 201 response for success
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # return 400 response if data is invalid

    # handles token creation for staff and superusers
    def perform_create(self, serializer):
        user = serializer.save() # save user object
        if user.is_staff or user.is_superuser: # if the user is staff or superuser
            Token.objects.create(user=user) # create a token 
        return user 

# handles user registration with Django Forms
# code was copied from following resources
# https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/11-Pagination/django_project/users/views.py
# https://docs.djangoproject.com/en/stable/ref/contrib/messages/
# https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#render
# https://forum.djangoproject.com/t/how-to-request-existing-files-from-a-form-in-django/11292
def register(request):
    if request.method == 'POST': # if request is POST 
        form = UserAccountCreationForm(request.POST) # add POST data to the form 
        if form.is_valid(): # if form data is valid
            form.save() # save user object
            username = form.cleaned_data.get('username') # get username from the form
            messages.success(request, f'Your account has been setup!  You can now access the website.') # success message 
            return redirect('login') # redirect to login page
    else:
        form = UserAccountCreationForm() # create an empty form for GET requests
    return render(request, 'users/register.html', {'form': form}) # render registration page 

# handles redirection based on user authentication status
# https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#redirect
def index_redirect(request):
    if request.user.is_authenticated: # if user is authenticated
        return redirect('social-home') # redirect to home page 
    else:
        return redirect('login') # if user is not logged in, redirect to login page 

# handles CRUD operations for Profile objects
# https://www.django-rest-framework.org/api-guide/viewsets/
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileModelSerializer
    authentication_classes = [TokenAuthentication]

    # queryset to handle permissions
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Profile.objects.none()
        elif self.request.user.is_staff or self.request.user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user_id=self.request.user.id)

    # permissions based on action
    # https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated
    def get_permissions(self):
        if self.action in ['create']:  # anyone can create profile
            return [AllowAny()]
        return [IsAuthenticated()] # must be authenticated to do anything else  


# handles user profile viewing and updating
# code was copied from following resources
# https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/11-Pagination/django_project/users/views.py
# https://docs.djangoproject.com/en/stable/topics/auth/default/#the-login-required-decorator
@login_required # user must be logged in to view 
def profile(request):
    Profile.objects.get_or_create(user=request.user) # get or create user's profile
    if request.method == 'POST': # if the request is POST
        user_form = UpdateUserInfoForm(request.POST, instance=request.user) # create form for updating user information
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile) # create form for updating profile information
        if user_form.is_valid() and profile_form.is_valid(): # validate both forms
            user_form.save() # save user updates
            profile_form.save() # save profile updates
            messages.success(request, f'Your account has been succesfully updated!') # success message to display to user
            return redirect('profile') # redirect to profile page

    else: # owtherwise, get current user and profile data
        user_form = UpdateUserInfoForm(instance=request.user) 
        profile_form = UpdateUserProfileForm(instance=request.user.profile) 
    context_data = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context_data ) # render profile page with two forms

# References:
# https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/11-Pagination/django_project/users/views.py
# https://www.django-rest-framework.org/api-guide/viewsets/
# https://docs.djangoproject.com/en/stable/topics/db/queries/
# https://www.django-rest-framework.org/api-guide/serializers/
# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
# https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated
# https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/11-Pagination/django_project/users/views.py
# https://docs.djangoproject.com/en/stable/ref/contrib/messages/
# https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#render
# https://forum.djangoproject.com/t/how-to-request-existing-files-from-a-form-in-django/11292
# https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#redirect
# https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated
# https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/11-Pagination/django_project/users/views.py
# https://docs.djangoproject.com/en/stable/topics/auth/default/#the-login-required-decorator
# https://www.django-rest-framework.org/api-guide/generic-views/#createapimixin
# https://www.django-rest-framework.org/api-guide/generic-views/#createmodelmixin
# https://www.django-rest-framework.org/api-guide/permissions/
# https://www.django-rest-framework.org/api-guide/filtering/#filtering

# END - code was developed with the help of documentation and other external research, please see referenced links.
