from django.test import TestCase
from social.serializers import StatusPostSerializer
from .factories import PostFactory
from rest_framework.test import APIRequestFactory

# START - code was developed with the help of documentation and other external research, please see referenced links.
# tests post serializer for empty data
class StatusPostSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.post = PostFactory()

    def test_post_serializer_with_empty_data(self):
        serializer = StatusPostSerializer(data={})
        self.assertFalse(serializer.is_valid())

# References:
# https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/stable/ref/models/querysets/#create
# https://docs.djangoproject.com/en/stable/topics/db/examples/many_to_many/
# https://www.django-rest-framework.org/api-guide/serializers/
# https://docs.python.org/3/library/unittest.html#assert-methods
# https://www.django-rest-framework.org/api-guide/testing/#apirequestfactory
# https://www.django-rest-framework.org/api-guide/testing/
# https://stackoverflow.com/questions/75650569/unittesting-drf-serializer-validators-one-by-one
# https://github.com/encode/django-rest-framework/discussions/7743
# https://github.com/encode/django-rest-framework/blob/master/tests/test_renderers.py

# END - code was developed with the help of documentation and other external research, please see referenced links.