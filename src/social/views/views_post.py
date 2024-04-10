from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from itertools import chain
import os
from social.models import Post, Friend, Comment, GalleryImageItem
from social.forms import GalleryImageSubmissionForm, CreatePostForm

# START - code was developed with the help of documentation and other external research, please see referenced links.

# handles display of list of posts
class UserPostListView(ListView):
    model = Post
    template_name = 'social/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

# https://medium.com/@hassanraza/what-is-dispatch-used-for-in-django-c29af0653e94
    @method_decorator(login_required)  # login_required to view it
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # https://stackoverflow.com/questions/75696944/how-to-filter-by-request-user-in-django-filter-model
    # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#filter
    # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#first
    def get_queryset(self):
        if self.request.user.is_authenticated:
            # user's friends
            user_friend = Friend.objects.filter(current_user=self.request.user).first() 
            if user_friend:
                friends = user_friend.users.all()
            else:
                friends = User.objects.none()

            # retrieve posts from user and their friends 
            posts_of_friends = Post.objects.filter(author__in=friends) 
            posts_of_user = Post.objects.filter(author=self.request.user)

            # add together posts and sort by post date
            queryset = sorted(chain(posts_of_friends, posts_of_user), key=lambda post: post.date_posted, reverse=True)

            return queryset
        else:
            # empty if user is not logged in
            return Post.objects.none()

    # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#filter
    # https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        list_of_posts = context_data['posts']

        # paginate list of posts
        paginator = Paginator(list_of_posts, self.paginate_by, orphans=1)  

        # current page index from GET request
        page_index= self.request.GET.get('page')
        page_object = paginator.get_page(page_index) 
        context_data['page_obj'] = page_object

        # add GalleryImageSubmissionForm to context_data
        context_data['form'] = GalleryImageSubmissionForm()

        # get user's friends and image gallery items
        user = self.request.user
        user_friend = Friend.objects.filter(current_user=user).first()
        if user_friend:
            friends = user_friend.users.all()
        else:
            friends = User.objects.none()

        # show 2 images from gallery
        image_gallery_items = GalleryImageItem.objects.filter(user=user)[:2] 

        context_data['friends'] = friends
        context_data['first_4_friends'] = friends[:4]
        context_data['image_gallery_items'] = image_gallery_items

        return context_data

# handles validate media files in CreatePostView
def validate_media_format(value):
    if value is not None:  # check is file is not None
        supported_image_format = [".jpg", ".jpeg", ".png"]
        supported_video_format = [".mp4"]
        extension = os.path.splitext(value.name)[1]  
        supported_extensions = supported_image_format + supported_video_format
        if not extension.lower() in supported_extensions:
            raise ValidationError(u'This file has unsupported file extension.')

# handles post creation
class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm  
    model = Post

    # this func overrides form_valid and add custom validation for media files
    def form_valid(self, form):
        file = self.request.FILES.get('file', None)
        try:
            validate_media_format(file)
        except ValidationError:
            form.add_error('file', "Unsupportedfile format. Only .jpg and .mp4 formats are allowed.")
            return self.form_invalid(form)
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # after post creation redirects to home page
    def get_success_url(self):
        return reverse('social-home')  

# retrieve how many users has as friends
def retrieve_total_friend_count(user):
    return user.profile.friends.count()  

# displays user details and total friends
@login_required
def base_view(request):
    user = request.user
    total_friends = retrieve_total_friend_count(user)
    return render(request, 'base.html', {'user': user, 'friends_count': total_friends})

# handls comments for posts
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-get
# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#handling-uploaded-files-with-a-model
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#querysets-and-lookups
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#prefetch-related
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
@login_required
def post_comment_list_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        id_comment = request.POST.get('comment_id')

        if action == 'like':
            post_comment = get_object_or_404(Comment, pk=id_comment)  

            # if the user liked post_comment
            if post_comment.likes.filter(id=request.user.id).exists():  
                # remove like
                post_comment.likes.remove(request.user)
                liked = False
            else: # if the user liked post_comment, add like
                post_comment.likes.add(request.user)
                liked = True

            return JsonResponse({'liked': liked, 'likes_count': post_comment.likes.count()})  

        post_comment = request.POST.get('comment')
        id_post = request.POST.get('id_post')

        status_post = Post.objects.get(pk=id_post)  
        Comment.objects.create(post=status_post, author=request.user, content=post_comment) 

        return redirect('social-home') 

    else:
        posts = Post.objects.all().prefetch_related('comments') 
        context_data = {
            'posts': posts
        }
        return render(request, 'social/home.html', context_data)  

# handls thumbs up for a post
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-get
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#querysets-and-lookups
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#prefetch-related
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
@login_required
def thumbs_up_post(request, id_post):
    status_post = get_object_or_404(Post, pk=id_post)  
    if request.user in status_post.thumbs_up.all(): 
        # if use already gave thumbs up to the post, remove it 
        status_post.thumbs_up.remove(request.user)
    else:
        # if user hasn't given thumbs up to the post yet, add it 
        status_post.thumbs_up.add(request.user)

    # redirect to same page
    return redirect(request.META.get('HTTP_REFERER', 'home'))  # [2]

# View for handling post deletion
# https://stackoverflow.com/questions/52673974/django-2-1-deleteview-only-owner-can-delete-or-redirect
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-get
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#deleting-objects
# https://docs.djangoproject.com/en/4.2/ref/contrib/messages/#messages-tags
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#querysets-and-lookups
class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy('social-home')  

# deletes post  
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object() 

        # if user authenticated and owner of post
        if self.object.author == self.request.user: 
            # delete post and their comments
            self.object.comments.all().delete()  
            self.object.delete() 
            # display success message
            messages.success(request, 'The Post was deleted successfully.', extra_tags='success') 
        else: # display error message
            messages.error(request, 'Sorry, you can not delete this post. Its not your post.', extra_tags='error')  

        return redirect(self.get_success_url())  



# References
# https://docs.djangoproject.com/en/4.2/ref/request-response/#attributes-set-by-middleware
# https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.HttpRequest.POST
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#filter
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#first
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#all
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#none
# https://docs.djangoproject.com/en/4.2/ref/models/instances/#get
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#user-objects
# https://docs.djangoproject.com/en/4.2/topics/cache/#django.core.cache.cache.delete
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#get-object-or-404
# https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.HttpRequest.method
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#get
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-get
# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#handling-uploaded-files-with-a-model
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#count
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#all
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#querysets-and-lookups
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#prefetch-related
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/4.2/ref/contrib/messages/
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#deleting-objects
# https://docs.djangoproject.com/en/4.2/ref/contrib/messages/#messages-tags
# https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-editing/#deleteview

# END - code was developed with the help of documentation and other external research, please see referenced links.