from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse
from social.models import Post, Friend
from users.models import Profile

# START - code was developed with the help of documentation and other external research, please see referenced links.

# https://docs.djangoproject.com/en/4.2/ref/request-response/#attributes-set-by-middleware
# https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.HttpRequest.POST
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#filter
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#first
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#all
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#none
def search_user(request):
    if request.method == "POST":  # if request is HTTP do the following
        searched_term = request.POST['searched_term']  # checking POST data 
        user_profile_list = Profile.objects.filter(user__username__icontains=searched_term).exclude(user=request.user)  # getting user profiles 
        user_friend = Friend.objects.filter(current_user=request.user).first()  # getting user's friend/s 
        id_list = [p.user_id for p in user_profile_list]
        users = User.objects.filter(id__in=id_list)  # getting users 
        if user_friend:
            friends = user_friend.users.all()  # getting all friends 
        else:
            friends = User.objects.none()  # if user has no friends display none 
        context_data = {'searched_term': searched_term, 'user_profile_list': user_profile_list, 'friends': friends, 'users': users}
        return render(request, 'social/friends_current_user.html', context_data)  
    else:
        return render(request, 'social/friends_current_user.html', {})

# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#first
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#all
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#none
def list_users(request):
    user_posts = Post.objects.all().order_by()  # get all posts 
    users = User.objects.exclude(id=request.user.id)  # all users exceot self 
    user_friend = Friend.objects.filter(current_user=request.user).first()  # get friend
    if user_friend:
        friends = user_friend.users.all() # getting all friends
    else:
        friends = User.objects.none()  # if user has no friends display none 
    context = {'posts': user_posts, 'users': users, 'friends': friends}
    return render(request, 'social/friends_current_user.html', context) 

# https://docs.djangoproject.com/en/4.2/ref/models/instances/#get
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#user-objects
# https://docs.djangoproject.com/en/4.2/topics/cache/#django.core.cache.cache.delete
def modify_friends(request, operation, pk):
    user_friend = User.objects.get(pk=pk)  # get user friend 
    if user_friend == request.user:  # if friend same as the user return error 
        return HttpResponse("Sorry, you are not allowed to add or remove yourself.")
    if operation == 'add':
        Friend.befriend(request.user, user_friend)
    elif operation == 'remove':
        Friend.unfriend(request.user, user_friend)
    cache.delete('list_users')  # delete cache for list_users 
    return redirect('list_users') 

# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#first
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#get-object-or-404
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#all
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#none
def display_friends(request, pk):
    user = get_object_or_404(User, pk=pk)  # get user object or raising error 
    user_friend = Friend.objects.filter(current_user=user).first()  # Retrieving friend 
    if user_friend:
        friends = user_friend.users.all()  # get all friends
    else:
        friends = User.objects.none()  # if user has no friends display none 
    context_data = {'user': user, 'friends': friends}
    return render(request, 'social/friends_connections.html', context_data)  

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

# END - code was developed with the help of documentation and other external research, please see referenced links.