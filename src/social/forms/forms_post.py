from django import forms
from django.core.exceptions import ValidationError
from social.models import Post
import os

# START - code was developed with the help of documentation, please see referenced links.

# handles media file validation 
def validate_media_format(value):
    if value:
        # supported file format
        supported_image_format = [".jpg", ".jpeg", ".png"]
        supported_video_format = [".mp4"]

        # get extension of uploaded file
        extension = os.path.splitext(value.name)[1]

        # concatenate supported image and video extensions
        supported_extensions = supported_image_format + supported_video_format

        # if extension is not supported raise an error 
        if not extension.lower() in supported_extensions:
            raise ValidationError(u'Invalid file extension. Please upload .jpg, .jpeg, .png or .mp4 file format.')

# class for creating a new post
# https://docs.djangoproject.com/en/3.2/topics/forms/
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
# https://docs.djangoproject.com/en/3.2/ref/forms/validation/
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'file']

    # validation method for form fields
    def clean(self):
        sanitized_data = super().clean()
        text = sanitized_data.get("content")
        file = sanitized_data.get("file")

        # if both text field and file are empty and there are not errors, raise an error 
        if not file and not text and not self.errors:
            raise ValidationError("Please add text or upload .jpg, .jpeg, .png or .mp4 file format.")

    # validation method for the media file field
    def clean_file(self):
        media_file = self.cleaned_data.get('file', False)
        if media_file:
            try:
                # verify uploaded file with validate_media_format
                validate_media_format(media_file)
            except ValidationError as e:
                # error for form's file field
                self.add_error('file', e)
                # no file title if unspported file format is uploaded 
                return None
        return media_file


# References:
# https://docs.djangoproject.com/en/3.2/topics/forms/
# https://docs.djangoproject.com/en/3.2/ref/forms/validation/
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
# https://stackoverflow.com/questions/61917459/django-validate-filefield-within-the-form
# https://djangosnippets.org/snippets/338/raw/
# https://www.youtube.com/watch?v=UcUm82jWeKc

# END - code was developed with the help of documentation, please see referenced links.