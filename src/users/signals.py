from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from rest_framework.authtoken.models import Token
from django.conf import settings

# START - code was developed with the help of documentation and other external research, please see referenced links.

# code was copied from following resources
# signals to create profile when new User is saved
# "post_save" signal is sent when save() method is called
# https://docs.djangoproject.com/en/stable/ref/signals/#post-save
# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
# https://docs.djangoproject.com/en/stable/ref/models/querysets/#create
# https://stackoverflow.com/questions/63962443/create-a-post-save-signal-that-creates-a-profile-object-for-me
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created: # confirms if User was created
        Profile.objects.create(user=instance) # if yes, create Profile for new User 

# code was copied from following resources
# signals to save profile when User is saved
# "post_save" signal is sent when save() method is called
# https://docs.djangoproject.com/en/stable/ref/models/instances/#save
# https://stackoverflow.com/questions/63962443/create-a-post-save-signal-that-creates-a-profile-object-for-me
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  

# code was copied from following resources
# signals to create authentication token when new User is saved by using Django REST Framework's TokenAuthentication
# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
# https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
# https://gist.github.com/rayashi/23e3e04957f96b86fdc80fe2ad08ee44
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created: # confirms if User was created
        Token.objects.create(user=instance) # if yes, create Token for new User 

# References:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
# https://docs.djangoproject.com/en/stable/ref/signals/#post-save
# https://docs.djangoproject.com/en/stable/ref/models/instances/#save
# https://docs.djangoproject.com/en/stable/ref/models/querysets/#create
# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
# https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
# https://gist.github.com/rayashi/23e3e04957f96b86fdc80fe2ad08ee44
# https://stackoverflow.com/questions/63962443/create-a-post-save-signal-that-creates-a-profile-object-for-me

# END - code was developed with the help of documentation and other external research, please see referenced links.