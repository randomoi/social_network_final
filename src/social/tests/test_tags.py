from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from social.templatetags.social_custom_tags import have_file_extension

# START - code was developed with the help of documentation and other external research, please see referenced links.

# tests file for for validextension
class CustomTagTests(TestCase):
    def test_have_file_ext(self):
        file_mock = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        result = have_file_extension(file_mock, "txt")
        self.assertTrue(result)

        # tests for invalid extension
        result = have_file_extension(file_mock, "jpg")
        self.assertFalse(result)

        # tests for missing field
        result = have_file_extension(None, "txt")
        self.assertFalse(result)

# References:
# https://docs.djangoproject.com/en/4.2/ref/files/uploads/#django.core.files.uploadedfile.SimpleUploadedFile
# https://docs.djangoproject.com/en/4.2/topics/forms/
# https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/

# END - code was developed with the help of documentation and other external research, please see referenced links.