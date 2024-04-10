from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# handles form creation for user account creation 
# code was adopted from following resources
# https://forum.djangoproject.com/t/adding-extra-fields-to-a-register-form/14922
# https://django-oscar.readthedocs.io/en/3.0.0/_modules/django/contrib/auth/forms.html
# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
# https://docs.djangoproject.com/en/4.2/ref/forms/fields/#emailfield
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#user-objects
# https://docs.djangoproject.com/en/4.2/ref/forms/validation/
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-filters
# https://docs.djangoproject.com/en/4.2/ref/forms/api/#raising-validation-error
# https://stackoverflow.com/questions/71862671/django-custom-registration-form-which-inherits-from-usercreationform
# https://django.cowhite.com/blog/django-form-validation-and-customization-adding-your-own-validation-rules/
class UserAccountCreationForm(UserCreationForm):
    # email field to be included on the form
    email = forms.EmailField() 

    class Meta:
        model = User  
        fields = ['username', 'email', 'password1', 'password2']

    # validation method for email 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  
            raise forms.ValidationError("You can not use this email to register. It's already in the system.")  
        return email


# handles form creation to update the user's information
# code was adopted from following resources
# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
# https://django.cowhite.com/blog/django-form-validation-and-customization-adding-your-own-validation-rules/
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#exclude
class UpdateUserInfoForm(forms.ModelForm): 
    # email field to be included on the form
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    # validation method for email to check if it already in the DB excluding current user
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():  
            raise forms.ValidationError("This email address has already been used.")
        return email

# handles form creation to update user's profile
# code was adopted from following resources
# https://forum.djangoproject.com/t/adding-extra-fields-to-a-register-form/14922
# https://django-oscar.readthedocs.io/en/3.0.0/_modules/django/contrib/auth/forms.html
# https://docs.djangoproject.com/en/4.2/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile.content_type
# https://www.reddit.com/r/djangolearning/comments/pr82lc/image_field_on_form/?rdt=33481
class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    # validation method to check supported image format 
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            try:
                image_format = image.content_type  
                if image_format in ['image/jpeg', 'image/png']:
                    # if validated, return image 
                    return image
                else:
                    raise forms.ValidationError('This file is not supported. Please use .jpg or .png')
            except AttributeError:
                # if file type is not available
                return image

# References:
# https://forum.djangoproject.com/t/adding-extra-fields-to-a-register-form/14922
# https://django-oscar.readthedocs.io/en/3.0.0/_modules/django/contrib/auth/forms.html
# https://docs.djangoproject.com/en/4.2/ref/forms/fields/#emailfield
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#user-objects
# https://docs.djangoproject.com/en/4.2/ref/forms/validation/
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-filters
# https://docs.djangoproject.com/en/4.2/ref/forms/api/#raising-validation-error
# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#exclude
# https://docs.djangoproject.com/en/4.2/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile.content_type


# END - code was developed with the help of documentation and other external research, please see referenced links. 