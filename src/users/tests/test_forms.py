from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from users.forms import UserAccountCreationForm, UpdateUserInfoForm, UpdateUserProfileForm
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# tests User Register Form for invalid data
class UserRegisterFormTestCase(TestCase):

    def test_user_register_form_has_invalid_data(self):
        form = UserAccountCreationForm(data={
            'username': 'sometestuser',
            'email': 'invalid_email',
            'password1': 'sometestpassword',
            'password2': 'another_password',
        })
        self.assertFalse(form.is_valid())  # [2]
        self.assertEqual(len(form.errors['email']), 1)  # [3]
        self.assertEqual(len(form.errors['password2']), 1) 


# tests User Update Form for valid and invalid data
class UserUpdateFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sometestuser', email='sometestuser@somedomain.com', password='sometestpassword')  # [4]

    # test form validation for valid data
    def test_user_update_form_for_valid_data(self):
        form = UpdateUserInfoForm(data={
            'username': 'updated_user',
            'email': 'updated@somedomain.com',
        }, instance=self.user)  # [5]
        self.assertTrue(form.is_valid())

    # tests form validation with invalid email and blank username 
    def test_user_update_form_invalid_data(self):
        form = UpdateUserInfoForm(data={
            'username': '',
            'email': 'invalid_email',
        }, instance=self.user) 
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors['username']), 1) 
        self.assertEqual(len(form.errors['email']), 1) 


# tests Profile Update Form for valid and invalid data
class ProfileUpdateFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sometestuser', email='sometestuser@somedomain.com', password='sometestpassword')  # [4]

     # tests for valide data
    def test_profile_update_form_for_valid_data(self):
        image = Image.new('RGB', (100, 100), color='red')  # [6]
        image_file = io.BytesIO()
        image.save(image_file, 'JPEG')  # [7]
        image_file.seek(0)

        form_data = {'image': SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg')}  # [8]
        form = UpdateUserProfileForm(data=form_data, files=form_data, instance=self.user.profile)  # [9]
        self.assertTrue(form.is_valid())

    def test_profile_update_form_for_invalid_data(self):
        text_file = io.BytesIO(b'test_image_content')

        form_data = {'image': SimpleUploadedFile('some_test_image.txt', text_file.read(), content_type='text/plain')}  # [8]
        form = UpdateUserProfileForm(data=form_data, files=form_data, instance=self.user.profile)  
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1) 

# References:
# [1]: https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.is_valid
# [2]: https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.errors
# [3]: https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.cleaned_data
# [4]: https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user-model
# [5]: https://docs.djangoproject.com/en/stable/ref/forms/api/#binding-form-data-to-a-form
# [6]: https://pillow.readthedocs.io/en/stable/releasenotes/7.0.0.html#improved-documentation
# [7]: https://pillow.readthedocs.io/en/stable/releasenotes/6.0.0.html#new-image-save-reducing-keyword
# [8]: https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.SimpleUploadedFile
# [9]: https://docs.djangoproject.com/en/stable/topics/forms/modelforms/#modelform

# END - code was developed with the help of documentation and other external research, please see referenced links. 
