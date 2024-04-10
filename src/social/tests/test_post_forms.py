from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from social.forms import CreatePostForm

# START - code was developed with the help of documentation and other external research, please see referenced links.

# tests status posts form for valid data
class StatusPostFormTest(TestCase):
    def test_valid_status_post_form(self):
        valid_data = {
            'content': 'Some post 123',
            'file': SimpleUploadedFile("valid_image.jpg", b"file_content", content_type="image/jpeg"),
        }
    
        form = CreatePostForm(data=valid_data)
        self.assertTrue(form.is_valid())

# References:
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#testcase
# https://docs.djangoproject.com/en/3.2/ref/files/uploads/#django.core.files.uploadedfile.SimpleUploadedFile
# https://stackoverflow.com/questions/63476979/unit-testing-django-model-with-an-image-not-quite-understanding-simpleuploaded

# END - code was developed with the help of documentation and other external research, please see referenced links.
