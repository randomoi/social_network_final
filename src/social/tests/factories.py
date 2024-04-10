import factory
from faker import Faker
from django.contrib.auth.models import User
from social.models import Friend, Post
from social.models import Comment, GalleryImageItem, Message
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

# START - code was developed with the help of documentation and other external research, please see referenced links.

fake = Faker()

# https://factoryboy.readthedocs.io/en/stable/reference.html#sequence
# https://factoryboy.readthedocs.io/en/stable/reference.html#factory.PostGenerationMethodCall
class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "User %d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')

# https://factoryboy.readthedocs.io/en/stable/reference.html#subfactory
class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    current_user = factory.SubFactory(UserModelFactory)

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserModelFactory)
    content = factory.Faker('text')

# https://factoryboy.readthedocs.io/en/stable/reference.html#factory.post_generation
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(UserModelFactory)
    post = factory.SubFactory(PostFactory)

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.likes.add(user)

# https://factoryboy.readthedocs.io/en/stable/recipes.html#file-fields
class ImageItemFactory(DjangoModelFactory):
    class Meta:
        model = GalleryImageItem

    title = factory.Faker('sentence')
    user = factory.SubFactory(UserModelFactory)

    file = factory.django.ImageField()
    date_uploaded = factory.Faker('date_time')

class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    user = factory.SubFactory(UserModelFactory)
    username = factory.Faker('user_name')
    room = factory.Faker('word')
    content = factory.Faker('sentence')
    timestamp = factory.Faker('date_time')

# References:
# https://faker.readthedocs.io/en/master/
# https://factoryboy.readthedocs.io/en/stable/reference.html#sequence
# https://factoryboy.readthedocs.io/en/stable/reference.html#factory.PostGenerationMethodCall
# https://factoryboy.readthedocs.io/en/stable/reference.html#subfactory
# https://factoryboy.readthedocs.io/en/stable/reference.html#factory.post_generation
# https://factoryboy.readthedocs.io/en/stable/recipes.html#file-fields

# END - code was developed with the help of documentation and other external research, please see referenced links.