from rest_framework import serializers
from .models import Post

# START - code was developed with the help of documentation and other external research, please see referenced links. 
class StatusPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'file', 'date_posted', 'author', 'comment', 'thumbs_up']

# https://www.django-rest-framework.org/api-guide/serializers/

# END - code was developed with the help of documentation and other external research, please see referenced links. 
