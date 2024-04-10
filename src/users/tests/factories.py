import factory
from django.contrib.auth.models import User
from users.models import Profile

# START - code was developed with the help of documentation and other external research, please see referenced links. 
# code was adopted from following resources
# https://factoryboy.readthedocs.io/en/stable/recipes.html
class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User  

    username = factory.Sequence(lambda n: f'user{n}')  
    password = factory.PostGenerationMethodCall('set_password', 'password') 

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile  

    user = factory.SubFactory(UserModelFactory)  

# References:
# https://factoryboy.readthedocs.io/en/stable/recipes.html
# https://factoryboy.readthedocs.io/en/latest/orms.html#the-djangomodelfactory-subclass
# https://factoryboy.readthedocs.io/en/latest/reference.html#sequence
# https://factoryboy.readthedocs.io/en/latest/reference.html#postgenerationmethodcall
# https://factoryboy.readthedocs.io/en/latest/reference.html#subfactory

# END - code was developed with the help of documentation and other external research, please see referenced links. 
