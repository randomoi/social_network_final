from django.apps import AppConfig

# START - code was developed with the help of documentation and other external research, please see referenced links. 
class UsersConfiguration(AppConfig):
    name = 'users' 

    # when Django is ready its called 
    def ready(self):
        import users.signals 

# References:
# https://docs.djangoproject.com/en/4.2/ref/applications/#django.apps.AppConfig.name
# https://docs.djangoproject.com/en/4.2/ref/applications/#django.apps.AppConfig.ready
# https://docs.djangoproject.com/en/4.2/topics/signals/#connecting-receiver-functions

# END - code was developed with the help of documentation and other external research, please see referenced links. 