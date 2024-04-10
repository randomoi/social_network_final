from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# START - code was developed with the help of documentation and other external research, please see referenced links. 
# model for status posts
# https://docs.djangoproject.com/en/4.2/ref/models/fields/
class Post(models.Model):
    content = models.TextField(blank=True, null=True)  # text section can be empty
    file = models.FileField(upload_to='post_files', blank=True, null=True)  # optional file 
    date_posted = models.DateTimeField(default=timezone.now)  # post creation date 
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # author reference
    comment = models.TextField(blank=True, null=True)  # optional comment
    thumbs_up = models.ManyToManyField(User, related_name='favorite_posts') # to give thumbs up for post which has many-to-many relationship with User

# model to show user relationships
# code was copied from these resources  
# https://python.plainenglish.io/creating-a-friend-request-model-in-django-640257b2c67f
# https://stackoverflow.com/questions/63351685/how-can-you-add-to-a-manytomanyfield-extension-of-the-default-django-user-model
class Friend(models.Model):
    users = models.ManyToManyField(User)  # many-to-many relationship 
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)  # current user reference
    
    # creates a new friendship
    @classmethod
    def befriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)
        # add new friend to current_user's profile friends 
        current_user.profile.friends.add(new_friend)

    # removes a friendship
    @classmethod
    def unfriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
        # remove friend from current_user's profile friends 
        current_user.profile.friends.remove(new_friend)

# model for comment on status post
# code was adopted from these resources
# https://medium.com/@nutanbhogendrasharma/creating-a-comment-system-to-the-article-in-django-part-8-ba9d8067bb2
# https://medium.com/strategio/my-django-blog-project-5ac08d84b0f8
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # reference to status post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # reference auther to comment 
    content = models.TextField()  # text in the comment
    date_posted = models.DateTimeField(default=timezone.now)  # when comment was posted
    likes = models.ManyToManyField(User, related_name='liked_comments')  # users liked comment

    # represents comment as a string
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'

    # increments likes for comment
    def increment_comment_likes(self):
        self.likes.add(self.author)
        self.save()

    # decrements likes for comment
    def decrement_comment_likes(self):
        self.likes.remove(self.author)
        self.save()

# model for image gallery
# code was adopted from these resources
# https://bharathurs.in/2021/03/06/django-models/
# https://github.com/divanov11/ecommerce_django_mod4/blob/master/store/models.py
class GalleryImageItem(models.Model):
    title = models.CharField(max_length=100, default='Untitled Image')  # title with default name, user can change it
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery')  # reference user to uploaded image 
    file = models.FileField(upload_to='gallery/')  # FileField for image, used FileField in case I would implement video upload as well (next iteration)
    date_uploaded = models.DateTimeField(auto_now_add=True)  # when image was uploaded

      # represents image as a string
    def __str__(self):
        return f"GalleryImageItem {self.id}"

# model for chat message
# code was adopted from these resources
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_1.html
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_2.html
# https://github.com/mirumee/django-messages/blob/master/django_messages/models.py
# https://forum.djangoproject.com/t/django-filter-query-to-get-chat-messages-among-two-friends/18868
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # reference user to message
    username = models.CharField(max_length=255, null=True)  # username
    room = models.CharField(max_length=255)  # chat room where message was sent from
    content = models.TextField()  # text of message
    timestamp = models.DateTimeField(auto_now_add=True)  # date sent
    file = models.FileField(upload_to='chat_images/', null=True, blank=True)  # field for image, used FileField for when I will add video upload functionality

    # handles ordering messages by time/date
    class Meta:
        ordering = ('timestamp',)  

# https://docs.djangoproject.com/en/3.2/topics/db/models/
# https://docs.djangoproject.com/en/3.2/ref/models/fields/
# https://docs.djangoproject.com/en/3.2/topics/db/models/#relationships
# https://docs.djangoproject.com/en/3.2/topics/db/models/#methods
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#datetimefield
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#manytomanyfield
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#foreignkey
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_1.html
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_2.html
# https://github.com/mirumee/django-messages/blob/master/django_messages/models.py
# https://forum.djangoproject.com/t/django-filter-query-to-get-chat-messages-among-two-friends/18868
# https://bharathurs.in/2021/03/06/django-models/
# https://github.com/divanov11/ecommerce_django_mod4/blob/master/store/models.py
# https://medium.com/@nutanbhogendrasharma/creating-a-comment-system-to-the-article-in-django-part-8-ba9d8067bb2
# https://medium.com/strategio/my-django-blog-project-5ac08d84b0f8
# https://medium.com/@nutanbhogendrasharma/creating-a-comment-system-to-the-article-in-django-part-8-ba9d8067bb2
# https://medium.com/strategio/my-django-blog-project-5ac08d84b0f8
# https://python.plainenglish.io/creating-a-friend-request-model-in-django-640257b2c67f
# https://stackoverflow.com/questions/63351685/how-can-you-add-to-a-manytomanyfield-extension-of-the-default-django-user-model
# https://docs.djangoproject.com/en/4.2/ref/models/fields/

# END - code was developed with the help of documentation and other external research, please see referenced links. 