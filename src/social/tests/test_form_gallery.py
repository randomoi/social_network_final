from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.test import TestCase
from django.contrib.auth.models import User
from social.forms import GalleryImageSubmissionForm

# START - code was developed with the help of documentation and other external research, please see referenced links.
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user-objects
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.login
class GalleryImageSubmissionFormTest(TestCase):
    def setUp(self):

        self.username = 'sometestuser'
        self.password = 'sometestpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
    
    # tests for invalid form
    # https://docs.python.org/3/library/os.path.html
    # https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.is_valid
    # https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.SimpleUploadedFile
    def test_invalid_image_form(self):
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_media/invalid_file.png")

        with open(image_path, 'rb') as image_file:
            some_invalid_data = {
                'title': 'Some Random Gallery',
                # https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.SimpleUploadedFile
                'file': SimpleUploadedFile("invalid_file.png", image_file.read(), content_type="image/png"),
            }
            image_form = GalleryImageSubmissionForm(data=some_invalid_data)
            
            self.assertFalse(image_form.is_valid())

# References: 
# https://docs.python.org/3/library/os.path.html
# https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.is_valid
# https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.SimpleUploadedFile
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user-objects
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client.login

# END - code was developed with the help of documentation and other external research, please see referenced links.