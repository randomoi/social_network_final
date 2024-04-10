from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from social.models import Post
from social.views.views_post import UserPostListView, validate_media_format
import os
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import PostFactory, UserModelFactory

# START - code was developed with the help of documentation and other external research, please see referenced links.
# tests get response for all posts
class GetAPIPostViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserModelFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_response_for_all_posts(self):
        url = reverse('posts-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# tests get and delete for Post Detail API View
class StatusPostDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserModelFactory()
        self.post = PostFactory(author=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_request_post_detail(self):
        url = reverse('post-detail-api', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # tests deletion of the post and validates it's no longer in the DB
    def test_delete_status_post_from_db(self):
        url = reverse('post-detail-api', args=[self.post.pk])
        self.client.delete(url)
        self.assertEqual(Post.objects.count(), 0)

    # tests deletion of post and checks the response code
    def test_delete_status_post_response(self):
        url = reverse('post-detail-api', args=[self.post.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 



# References
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#testcase
# https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#django.test.RequestFactory
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.Client
# https://www.django-rest-framework.org/api-guide/testing/#apitestcase
# https://docs.djangoproject.com/en/3.2/ref/urlresolvers/#reverse
# https://docs.djangoproject.com/en/3.2/ref/files/uploads/#django.core.files.uploadedfile.SimpleUploadedFile
# https://docs.python.org/3/library/os.path.html#os.path.join
# https://www.django-rest-framework.org/api-guide/status-codes/
# https://docs.djangoproject.com/en/3.2/ref/exceptions/#django.core.exceptions.ValidationError
# https://stackoverflow.com/questions/72305478/django-test-unit-logged-in-user
# https://github.com/encode/django-rest-framework/blob/master/tests/test_testing.py
# https://github.com/django/djangopeople/blob/master/tests/tests_views.py
# https://django.readthedocs.io/en/1.5.x/topics/testing/advanced.html
# http://www.tomchristie.com/rest-framework-2-docs/api-guide/testing
# https://www.ianlewis.org/en/testing-django-views-without-using-test-client
# https://books.agiliq.com/projects/django-api-polls-tutorial/en/latest/testing-and-ci.html

# END - code was developed with the help of documentation and other external research, please see referenced links.
