from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from social.models import Post, Comment

# START - code was developed with the help of documentation and other external research, please see referenced links.
# handles comment submitting a new comment
@login_required # user must be logged in
def create_comment(request, id_post):
    post = get_object_or_404(Post, pk=id_post)  

    if request.method == 'POST':
        comment_content = request.POST.get('comment')

        if comment_content:
            Comment.objects.create(post=post, author=request.user, content=comment_content)  
            messages.success(request, 'Your comment was added!')  
        else:
            messages.error(request, 'The field cannot be empty. Please add a comment.')  

    # redirect to user profile 
    return redirect('user-profile', pk=post.author.id)  

# handles removal/deletion of comment
@login_required # user must be logged in
def remove_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)  
    # if user is author of the comment, delete the comment
    if comment.author == request.user: 
        comment.delete()  
    # redirect to home page
    return redirect('social-home')  

# handles liking/unliking(heart) of comment
@login_required # user must be logged in
def heart_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id) 
    if request.user in comment.likes.all():  
        # if already liked, remove heart
        comment.likes.remove(request.user) 
    else:
        # if did not like yet, add like
        comment.likes.add(request.user)  

    # redirect to same page to display like 
    return redirect(request.META.get('HTTP_REFERER') + f'?id_post={comment.post.id}')  


# References
# https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.HttpRequest.META
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-get
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#many-to-many-relationships
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#deleting-objects
# https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-editing/#deleteview
# https://docs.djangoproject.com/en/4.2/ref/contrib/messages/
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect

# END - code was developed with the help of documentation and other external research, please see referenced links.