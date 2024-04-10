from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from social.models import GalleryImageItem
from django.core.files.uploadedfile import SimpleUploadedFile
import os

# START - code was developed with the help of documentation and other external research, please see referenced links.
# tests Image Gallery View
class ImgGalleryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sometestuser', password='sometestpasswaord')
        self.gallery_image_item = GalleryImageItem.objects.create(user=self.user, file='somepath/to/test_image.jpg')
        self.file_path = os.path.join(os.path.dirname(__file__), 'media', 'images', 'test_image.jpg')
        self.form_data = {
            'file': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        }

    # tests user gallery view for authenticated user
    def test_user_gallery_view_for_authenticated_user(self):
        self.client.login(username='sometestuser', password='sometestpasswaord')
        url = reverse('user-gallery', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_image.jpg')  

    # tests user gallery view for unauthenticated user
    def test_user_gallery_view_for_unauthenticated_user(self):
        url = reverse('user-gallery', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'test_image.jpg')  
    
    # tests delete gallery item for authenticated user
    def test_delete_gallery_item_for_authenticated_user(self):
        self.client.login(username='sometestuser', password='sometestpasswaord')
        url = reverse('delete-gallery-item', args=[self.gallery_image_item.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(GalleryImageItem.objects.filter(id=self.gallery_image_item.id).exists())
   
    # tests delete gallery item for unauthenticated user
    def test_delete_gallery_item_for_unauthenticated_user(self):
        url = reverse('delete-gallery-item', args=[self.gallery_image_item.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(GalleryImageItem.objects.filter(id=self.gallery_image_item.id).exists())

    # tests delete gallery item for unauthorized user
    def test_delete_gallery_item_for_unauthorized_user(self):
        unauthorized_user = User.objects.create_user(username='unauthorized', password='sometestpasswaord')
        self.client.login(username='unauthorized', password='sometestpasswaord')
        url = reverse('delete-gallery-item', args=[self.gallery_image_item.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(GalleryImageItem.objects.filter(id=self.gallery_image_item.id).exists())


# References:
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#testcase
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Client
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user
# https://docs.djangoproject.com/en/stable/ref/urlresolvers/#reverse
# https://docs.djangoproject.com/en/stable/topics/http/file-uploads/
# https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.SimpleUploadedFile
# https://docs.djangoproject.com/en/stable/topics/testing/tools/#assertions

# END - code was developed with the help of documentation and other external research, please see referenced links.