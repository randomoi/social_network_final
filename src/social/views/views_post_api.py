from django.http import Http404
from social.models import Post
from social.serializers import StatusPostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.http import Http404

# START - code was developed with the help of documentation and other external research, please see referenced links.

# handles display of all status posts
class StatusPostAPIView(APIView):
    # permissions based on type of user
    # https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated
    def get_permissions(self):
        if self.request.user.is_superuser:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    # get request
    def get(self, request):
        if request.user.is_superuser: # if user is administrator 
            posts = Post.objects.all()  # show all posts
        else: # otherwise, show only posts for auth user 
            posts = Post.objects.filter(author=request.user)  
        serializer = StatusPostSerializer(posts, many=True)
        return Response(serializer.data)

    # post request
    def post(self, request):
        serializer = StatusPostSerializer(data=request.data)  # instance for receiving data
        if serializer.is_valid():  # validate data 
            serializer.save(author=request.user)  # save data to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# handles display of one status post
class StatusPostDetailAPIView(APIView):
    # https://www.django-rest-framework.org/api-guide/permissions/
    permission_classes = [IsAuthenticated] # this make sures that only authenticated user can see specific post
  
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk, author=self.request.user)  # get one post with the provided pk
        except Post.DoesNotExist:
            raise Http404  # if post is not found, raise 404 error 
    
    # get request
    def get(self, request, pk):
        post = self.get_object(pk)  # get one post with the provided pk
        serializer = StatusPostSerializer(post)  
        return Response(serializer.data)  # return serialized data as API response
    # put request
    def put(self, request, pk):
        post = self.get_object(pk)  # get one post with the provided pk
        serializer = StatusPostSerializer(post, data=request.data)   # instance for receiving data
        if serializer.is_valid():  # validate data 
            serializer.save()  # save updated data to DB
            return Response(serializer.data)  # return serialized data as API response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
   
    # delete request
    def delete(self, request, pk):
        post = self.get_object(pk)  # get one post with the provided pk
        post.delete()  # delete post from DB
        return Response(status=status.HTTP_204_NO_CONTENT) 


# References
# https://www.django-rest-framework.org/api-guide/views/
# https://www.django-rest-framework.org/api-guide/serializers/
# https://www.django-rest-framework.org/api-guide/status-codes/
# https://www.django-rest-framework.org/api-guide/exceptions/#http404
# https://www.django-rest-framework.org/api-guide/pagination/

# END - code was developed with the help of documentation and other external research, please see referenced links.
