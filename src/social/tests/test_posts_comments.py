from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from social.models import Post, Comment
from social.views.views_post import UserPostListView, validate_media_format
from social.forms import CreatePostForm
import os
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import PostFactory, UserModelFactory

# START - code was developed with the help of documentation and other external research, please see referenced links.
# test for authenticated and unauthenticated user for posts
class UserPostListViewTestCase1(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='sometestuser', password='sometestpassword')
        self.post = Post.objects.create(author=self.user, content='Some Post Content')

    # tests the UserPostListView for authenticated user
    def test_post_list_view_for_authenticated_user(self):
        request = self.factory.get(reverse('social-home'))
        request.user = self.user
        response = UserPostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Some Post Content')

   # tests post list view for unauthenticated user
    def test_post_list_view_for_unauthenticated_user(self):
        response = self.client.get(reverse('social-home'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/home/', fetch_redirect_response=False)

class CreatePostViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sometestuser', password='sometestpassword')
        self.file_path = os.path.join(os.path.dirname(__file__), 'test_media', 'default.jpg')

    # tests CreatePostView for auth user with a valid file
    def test_create_post_view_for_authenticated_user_with_valid_file(self):
        self.client.login(username='sometestuser', password='sometestpassword')
        with open(self.file_path, 'rb') as file:
            data = {'content': 'Some Post', 'file': file}
            response = self.client.post(reverse('post-create'), data, format='multipart')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Post.objects.count(), 1)
            self.assertEqual(Post.objects.first().author, self.user)
            self.assertEqual(Post.objects.first().content, 'Some Post')

    # tests CreatePostView for unauth user
    def test_create_post_view_for_unauthenticated_user(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url) 

    # tests the validate_media_format with valid file ext
    def test_validate_media_format_withvalid_extension(self):
        file = SimpleUploadedFile('some_test_image.jpg', b'Some test image', content_type='image/jpeg')
        try:
            validate_media_format(file)
        except ValidationError:
            self.fail("validate_media_format raised ValidationError.")
    
    # tests validate_media_format with unsupport file extension
    def test_validate_media_file_unsupported_extension(self):
        file = SimpleUploadedFile('some_test_file.txt', b'Some test text file.', content_type='text/plain')
        with self.assertRaises(ValidationError):
            validate_media_format(file)

# tests likes and unlikes for comments
class LikeUnlikeCommentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sometestuser', password='sometestpassword')
        self.post = Post.objects.create(author=self.user, content='Some Post Content')
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Some comment')
    
    # tests likes for comments
    def test_like_comment(self):
        self.client.login(username='sometestuser', password='sometestpassword')
        url = reverse('like-comment', kwargs={'comment_id': self.comment.pk})
        referrer_url = reverse('social-home')
        response = self.client.post(url, HTTP_REFERER=referrer_url)

        self.assertEqual(response.status_code, 302) 
        self.assertTrue(self.user in self.comment.likes.all())

    # tests unlikes for comments
    def test_unlike_comment(self):
        self.comment.likes.add(self.user)
        self.client.login(username='sometestuser', password='sometestpassword')
        url = reverse('like-comment', kwargs={'comment_id': self.comment.pk})
        referrer_url = reverse('social-home')
        response = self.client.post(url, HTTP_REFERER=referrer_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user not in self.comment.likes.all())

# tests delete comment functionality
class DeleteCommentFromPostsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sometestuser', password='sometestpassword')
        self.post = Post.objects.create(author=self.user, content='Some Post Content')
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Some comment')
    
    # tests delete comment functionality
    def test_delete_comment_from_posts(self):
        self.client.login(username='sometestuser', password='sometestpassword')
        url = reverse('delete-comment', kwargs={'comment_id': self.comment.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

# tests submit functionality for comment with data and empty
class SubmitCommentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sometestuser', password='sometestpassword')
        self.post = Post.objects.create(author=self.user, content='Some Post Content')

# tests submit functionality for comment with data  
    def test_submit_comment_with_data(self):
        self.client.login(username='sometestuser', password='sometestpassword')
        url = reverse('submit-comment', kwargs={'id_post': self.post.pk})
        data = {'comment': 'Some comment content'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND) 
        self.assertEqual(self.post.comments.count(), 1)
# tests submit functionality for empty comment 
    def test_submit_comment_without_data(self):
        self.client.login(username='sometestuser', password='sometestpassword')
        url = reverse('submit-comment', kwargs={'id_post': self.post.pk})
        data = {'comment': ''}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(self.post.comments.count(), 0)

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
