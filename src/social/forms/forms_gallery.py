from django import forms
from social.models import GalleryImageItem
from django.core.exceptions import ValidationError
import os

# START - code was developed with the help of documentation, please see referenced links.

# handles validation of the image 
def validate_image_format(value):
    if value is not None:  # check if there is a file
        # supported image format
        supported_image_format = [".jpg"]

        # get extension of file
        extension = os.path.splitext(value.name)[1]

        # if extension is not supported raise an error 
        if not extension.lower() in supported_image_format:
            raise ValidationError(u'Invalid file extension. Please upload .jpg file format.')

# class to handle image submission to the user gallery 
# https://docs.djangoproject.com/en/3.2/topics/forms/
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
class GalleryImageSubmissionForm(forms.ModelForm):
    class Meta:
        model = GalleryImageItem
        fields = ['title', 'file']

    # validation method for fields
    # https://docs.djangoproject.com/en/3.2/ref/forms/validation/
    def clean(self):
        sanitized_data = super().clean()
        file = self.cleaned_data.get('file')
        title = self.cleaned_data.get('title')

        # validate file by using custom validate_image_format if the file has been submitted
        if file:
            validate_image_format(file)

        # if file field is empty raise an error  
        if not file and not title:
            raise forms.ValidationError("Please add an image.")

        return sanitized_data

    #  save_image_for_user image and associate it with user who is submitting the file 
    def save(self, commit=True, user=None):
        image_instance = super().save(commit=False)
        if user:
            image_instance.user = user
        if commit:
            image_instance.save()
        return image_instance

# References:
# https://docs.djangoproject.com/en/3.2/ref/forms/validation/
# https://docs.djangoproject.com/en/3.2/topics/forms/
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
# https://stackoverflow.com/questions/45923410/override-the-save-method-in-django-modelform-to-create-or-update
# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
# https://dev.to/daveson217/how-to-use-autosavefalse-in-cloudinaryfilefield-when-using-django-forms-30c6
# https://hugsformybugs.medium.com/saving-data-using-django-model-form-7ec9d8471ccf
# https://stackoverflow.com/questions/65243073/key-error-on-self-cleaned-data-getfile
# https://djangospirit.readthedocs.io/en/latest/ref/forms/validation.html

# END - code was developed with the help of documentation, please see referenced links.