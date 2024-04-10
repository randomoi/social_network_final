from django import template
from social.models import Friend
from social.models import Post

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/
register = template.Library()  # library to register tags 

# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#simple-tags
# https://docs.djangoproject.com/en/3.2/topics/db/queries/
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#count
@register.simple_tag  # registers tag 
def friend_count(user):
    user_friend = Friend.objects.filter(current_user=user).first()  # get friends for user 
    if user_friend:
        friends_count = user_friend.users.count()  # calculate friends for user 
        return friends_count
    return 0

# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#simple-tags
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#count
@register.simple_tag # registers tag 
def post_count(user):
    # calculate post for user 
    post_count = Post.objects.filter(author=user).count()
    return post_count

# References:
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#simple-tags
# https://docs.djangoproject.com/en/3.2/topics/db/queries/
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#count
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#count
# https://testdriven.io/tips/topics/django

# END - code was developed with the help of documentation and other external research, please see referenced links. 