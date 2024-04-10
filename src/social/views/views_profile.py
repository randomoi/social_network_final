from django.shortcuts import render,  get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User
from social.models import Post, Friend, GalleryImageItem
from social.forms import GalleryImageSubmissionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# START - code was developed with the help of documentation and other external research, please see referenced links.
@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        # get user with provided pk from DB or return 404 error
        user = get_object_or_404(User, pk=pk)  

        # get user's posts in descending order
        status_posts = Post.objects.filter(author=user).order_by('-date_posted')  

        # get post count for user
        status_post_count = status_posts.count()  

        # get user's friends
        user_friend = Friend.objects.filter(current_user=user).first()
        if user_friend:
            friends = user_friend.users.all()
        else:
            friends = User.objects.none()

        # get first 4 friends 
        first_4_friends = friends[:4]  

        # get user's image gallery items
        image_gallery_items = GalleryImageItem.objects.filter(user=user) 

        gallery_submission_form = GalleryImageSubmissionForm()

        context_data = {
            'user': user,
            'posts': status_posts,
            'friends': friends,
            'first_4_friends': first_4_friends,
            'form': gallery_submission_form,
            'image_gallery_items': image_gallery_items,
            'post_count': status_post_count, 
        }

        return render(request, 'social/friend_profile.html', context_data)  

# References
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#count
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#field-lookups
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#querysets-and-managers
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-filters
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-get
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#order-by
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#count
# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#handling-uploaded-files-with-a-model
# https://docs.djangoproject.com/en/4.2/ref/forms/api/#django.forms.Form.is_valid
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect

# END - code was developed with the help of documentation and other external research, please see referenced links.