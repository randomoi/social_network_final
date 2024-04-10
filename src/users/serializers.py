from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# this was created to limit how much is shown in Profile API View
class UserModelSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User # references for User model (Django)
        fields = ['id', 'username', 'email', 'password'] 
        extra_kwargs = {
            'password': {'write_only': True} # password will not display as its  write-only, security feature
        }

    # creates user
    def create(self, validated_data): 
        password = validated_data.pop('password') # gets and removes password 
        user = User(**validated_data) # create User without password
        user.set_password(password) # using Django's set_password method, setting password
        user.save() # save user to DB
        return user


# handles profile serialization for Profile model
class ProfileModelSerializer(serializers.ModelSerializer): 
    user = UserModelSerializer(read_only=True) # UserModelSerializer is read-only to prevent user from making changes, nested view
    friends = UserModelSerializer(many=True, read_only=True) # friends filed is read-only

    class Meta:
        model = Profile 
        fields = ['id', 'image', 'user', 'friends'] 

# References:
# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
# https://www.django-rest-framework.org/api-guide/serializers/
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.User.set_password
# https://www.django-rest-framework.org/api-guide/relations/

# END - code was developed with the help of documentation and other external research, please see referenced links. 