from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from social.models import Friend, Message
from django.http import HttpResponseForbidden


# START - code was developed with the help of documentation and other external research, please see referenced links.
# get user's friends 
def retrieve_friends(user):
    # filter friends for the user
    friends_for_user = Friend.objects.filter(current_user=user).first()
    if friends_for_user:
        # if user has friends retrieve them
        return friends_for_user.users.all()
    else:
        # otherwise return empty
        return User.objects.none()

@login_required
def show_friends(request):
    user = request.user # current user
    user_friends = retrieve_friends(user) # retrieve friends
    return render(request, 'chat/chat_search.html', {'friends': user_friends})

# https://stackoverflow.com/questions/71260838/how-to-get-user-object-based-on-username-and-not-the-id-pk-in-django
def room(request, private_chat_room_name):
    # get user IDs by extracting them from room name
    chat_room_part = private_chat_room_name.split('_')
    userOne = User.objects.get(pk=chat_room_part[1])
    userTwo = User.objects.get(pk=chat_room_part[2])

    # validation check to make sure user is part of the chat room,if not, restrict access and show error message 
    if request.user not in [userOne, userTwo]:
        return HttpResponseForbidden("Restricted! This chat room is private. You do not have access to it.")

    # get receiver's username
    receiver_username = userOne.username if userOne != request.user else userTwo.username
    # get messages for the room
    messages = Message.objects.filter(room=private_chat_room_name)
    
    # image messages 
    image_messages = [{
            'message': m,
            'is_file_image': bool(m.file),  # confirm if message has a file 
            'image_url': f"http://127.0.0.1:8000{m.file.url}" if m.file and m.file.url.startswith('/') else None,
        } for m in messages]

    return render(request, 'chat/private_room.html', {
        'private_chat_room_name': private_chat_room_name,
        'username': request.user.username,
        'receiver_username': receiver_username,
        'image_messages': image_messages,
    })

# https://stackoverflow.com/questions/46481016/how-to-find-user-queryset-matching-self-request-user
@login_required
def chat_user_search(request):
    # get searched term from POST request
    searched_term = request.POST.get('searched_term', '').strip()
    user = request.user

    # if term is submitted, search for friends
    search_friends = User.objects.filter(username__icontains=searched_term) if searched_term else User.objects.none()
    # do not include current user in search results
    friends_excluding_self = search_friends.exclude(pk=user.pk)

    context = {
        'searched_term': searched_term,
        'friends': friends_excluding_self,
        'user_friends': retrieve_friends(user), 
    }

    return render(request, 'chat/chat_search.html', context)

@login_required  # check that user is logged in  
# https://docs.djangoproject.com/en/stable/topics/auth/default/#django.contrib.auth.decorators.login_required
def chat_with_users(request, friend_pk):
    # get a friend, if not found return a 404 error  
    # https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#get-object-or-404
    friend = get_object_or_404(User, pk=friend_pk)

    # combine both users and sort in ascending order to make sure both users access the same room 
    user_and_friend_ids = [str(request.user.pk), str(friend.pk)]
    user_and_friend_ids.sort()
    # get room URL from sorting
    chat_room_url = f"chat_{user_and_friend_ids[0]}_{user_and_friend_ids[1]}"

    if request.method == "POST":
        # get text and uploaded image from the POST request
        # https://docs.djangoproject.com/en/stable/topics/http/file-uploads/
        content = request.POST.get('message') # text
        sent_image = request.FILES.get('image')  # uploaded image file 

        # create chat message and use escape() to prevent XSS attacks
        # https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.html.escape
        chat_message = Message(
            user=request.user,
            room=chat_room_url,
            content=escape(content),
            file=sent_image  
        )
        # save chat message to DB 
        # https://docs.djangoproject.com/en/stable/topics/db/queries/#creating-objects
        chat_message.save()  

        return redirect('room', private_chat_room_name=chat_room_url)

    # get all messages for chat room
    all_messages = Message.objects.filter(room=chat_room_url)

    # display template with all details
    # https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#render
    return render(request, 'chat/private_room.html', {
        'private_chat_room_name': chat_room_url,
        'username': request.user.username,
        'receiver_username': friend.username,
        'messages': all_messages,
    })

# References
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_1.html
# https://djangochannelsrestframework.readthedocs.io/en/latest/tutorial/part_2.html
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/ref/models/relations/#django.db.models.ForeignKey
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#filter
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#exclude
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/ref/models/instances/#create
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#get
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#values
# https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.Field.primary_key
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#complex-lookups-with-q
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/stable/topics/db/queries/
# https://docs.djangoproject.com/en/stable/topics/auth/default/#django.contrib.auth.decorators.login_required
# https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#render
# https://stackoverflow.com/questions/75468161/trying-to-get-the-other-user-but-keep-getting-the-current-user

# END - code was developed with the help of documentation and other external research, please see referenced links.