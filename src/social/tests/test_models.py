from django.test import TestCase
from django.contrib.auth.models import User
from social.models import Post, Friend, Comment, GalleryImageItem, Message

# START - code was developed with the help of documentation and other external research, please see referenced links.
# tests status post model
class StatusPostModelTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="sometestuser", password="sometestpassword")
        self.post = Post.objects.create(content="Some content", author=self.author)

    def test_status_post_model(self):
        self.assertEqual(self.post.content, "Some content")
        self.assertEqual(self.post.author, self.author)

# tests friend model
class FriendModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="someuser1", password="sometestpassword")
        self.user2 = User.objects.create_user(username="someuser2", password="sometestpassword")
        self.friend = Friend.objects.create(current_user=self.user1)

    def test_user_friend_model(self):
        self.friend.users.add(self.user2)
        self.assertIn(self.user2, self.friend.users.all())

# tests Comment model
class CommentModelTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="sometestuser", password="sometestpassword")
        self.post = Post.objects.create(content="Some content", author=self.author)
        self.comment = Comment.objects.create(post=self.post, author=self.author, content="Some comment")

    def test_user_comment_model(self):
        self.assertEqual(str(self.comment), f'Comment by {self.author.username} on {self.post}')
        self.comment.increment_comment_likes()
        self.assertIn(self.author, self.comment.likes.all())
        self.comment.decrement_comment_likes()
        self.assertNotIn(self.author, self.comment.likes.all())

# tests Image Item model
class ImageItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sometestuser", password="sometestpassword")
        self.gallery_image_item = GalleryImageItem.objects.create(title="Some Image Item", user=self.user, file="somepath/to/test_file.jpg")

    def test_user_gallery_item_model(self):
        self.assertEqual(self.gallery_image_item.title, "Some Image Item")
        self.assertEqual(self.gallery_image_item.user, self.user)

# tests Chat Message model
class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sometestuser", password="sometestpassword")
        self.message = Message.objects.create(user=self.user, username="sometestuser", room="sometestroom", content="Some message")

    def test_chat_message_model(self):
        self.assertEqual(self.message.user, self.user)
        self.assertEqual(self.message.username, "sometestuser")
        self.assertEqual(self.message.room, "sometestroom")
        self.assertEqual(self.message.content, "Some message")

# References:
# https://docs.djangoproject.com/en/4.2/topics/auth/default/
# https://stackoverflow.com/questions/74603423/create-users-before-running-tests-drf
# https://stackoverflow.com/questions/10120518/create-a-simple-password-for-unittest-user-using-password-hashers

# END - code was developed with the help of documentation and other external research, please see referenced links.
