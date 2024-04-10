from django.test import TestCase
from django.contrib.auth.models import User
from social.models import Friend, Post
from django.template import Template, Context

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.get_user_model
# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/4.2/ref/templates/api/#django.template.Template
# https://docs.djangoproject.com/en/4.2/ref/templates/api/#django.template.Template.render
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#assertions
class CountTemplateTagsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sometestuser', email='sometestuser@somedomain.com', password='testpassword')  
    
    # tests friend count tag
    def test_friend_count_tag(self):
        somefriend1 = User.objects.create_user(username='friend_test1', email='somefriend1@somedomain.com', password='sometestpassword')
        somefriend2 = User.objects.create_user(username='friend_test2', email='somefriend2@somedomain.com', password='sometestpassword')
        friend = Friend.objects.create(current_user=self.user) 
        friend.users.add(somefriend1)
        friend.users.add(somefriend2)

    # tests post count tag
    def test_post_count_tag(self):
        Post.objects.create(author=self.user, content='SomeTestPost 1')  
        Post.objects.create(author=self.user, content='SomeTestPost 2')

        template_string = "{% load count_tags %}{% post_count user %}"
        t = Template(template_string) 
        c = Context({'user': self.user})
        rendered_output = t.render(c)  

        expected_output = '2' 
        self.assertEqual(rendered_output, expected_output)  

# References:
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.get_user_model
# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user
# https://docs.djangoproject.com/en/4.2/ref/templates/api/#django.template.Template
# https://docs.djangoproject.com/en/4.2/ref/templates/api/#django.template.Template.render
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#assertions

# END - code was developed with the help of documentation and other external research, please see referenced links. 