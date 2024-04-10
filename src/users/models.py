from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
# from django.dispatch import receiver


# START - code was developed with the help of documentation and other external research, please see referenced links. 
# model for profile creation
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # relationship with User model = one-to-one 
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') # image with default name and upload location
    friends = models.ManyToManyField(User, related_name='friends', blank=True) # relationship with User model = many-to-many 

    # model in string 
    def __str__(self):
        return f'{self.user.username} Profile' 

    # saves image in DB
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # save method that calls parent class

        if self.image: # confirm if image exists
            if not self.image.closed and self.image._committed:
                self.resize_profile_img() # resize image using custom method
    
    # resizes image if size is above specified
    def resize_profile_img(self):
        image = Image.open(self.image.path) # open image 

        # resize image if its above specified dimensions
        if image.height > 500 or image.width > 500:
            output_size = (500, 500)
            image.thumbnail(output_size) # thumbnail method to resize image
            image.save(self.image.path) # save resized image

# References:
# https://docs.djangoproject.com/en/stable/ref/models/fields/#onetoonefield
# https://docs.djangoproject.com/en/stable/ref/models/fields/#imagefield
# https://docs.djangoproject.com/en/stable/ref/models/fields/#filefield
# https://docs.djangoproject.com/en/stable/ref/models/fields/#manytomanyfield
# https://pillow.readthedocs.io/en/stable/releasenotes/6.0.0.html#image-open
# https://forum.djangoproject.com/t/django-how-to-connect-user-profile-model-with-comment-model-for-showing-data-from-user-profile/9134
# https://dev.to/earthcomfy/django-user-profile-3hik
# https://www.fullstackpython.com/django-db-models-imagefield-examples.html
# https://www.horilla.com/blogs/how-to-implement-user-authentication-authorization-in-django-2023/
# https://rohitlakhotia.com/blog/django-custom-user-model/
# https://www.devhandbook.com/django/user-profile/

# END - code was developed with the help of documentation and other external research, please see referenced links. 
