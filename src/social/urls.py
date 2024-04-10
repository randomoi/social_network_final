from django.urls import path
from .views.views_search import search_user, list_users, modify_friends, display_friends
from .views.views_post import UserPostListView, CreatePostView, base_view,  DeletePostView, post_comment_list_view, thumbs_up_post
from .views.views_profile import UserProfileView
from .views.views_post_api import StatusPostAPIView, StatusPostDetailAPIView
from .views.views_comment import create_comment, remove_comment, heart_comment
from .views.views_gallery import image_gallery_upload, ImageGalleryView, delete_image_from_gallery
from .views.views_chat import show_friends, chat_user_search, chat_with_users, room


urlpatterns = [
    # search view
    path('search/', search_user, name='profile-search'),
    
    # profile-related views
    path('userprofile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('friend/', list_users, name='list_users'),
    path('friend/<str:operation>/<int:pk>/', modify_friends, name='modify_friends'),
    path('view-friends/<int:pk>/', display_friends, name='view-friends'),

  
    path('home/', UserPostListView.as_view(), name='social-home'),
    path('base/', base_view, name='base'),

    # post-related views
    path('post/create/', CreatePostView.as_view(), name='post-create'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='post-delete'),
    path('post/comment/', post_comment_list_view, name='post-comment'),
    path('like-post/<int:id_post>/', thumbs_up_post, name='like-post'),

    # comment-related views
    path('submit-comment/<int:id_post>/', create_comment, name='submit-comment'),
    path('comment/delete/<int:comment_id>/', remove_comment, name='delete-comment'),
    path('comment/<int:comment_id>/like/', heart_comment, name='like-comment'),

    # gallery-related views
    path('upload_gallery/', image_gallery_upload, name='upload-gallery'),
    path('usergallery/<int:pk>/', ImageGalleryView.as_view(), name='user-gallery'),
    path('usergallery/<int:item_id>/delete/', delete_image_from_gallery, name='delete-gallery-item'),

    # chat-related views
    path('chat/', show_friends, name='chat-home'),
    path('chat/search/', chat_user_search, name='chat-search'),
    path('chat/with_friend/<int:friend_pk>/', chat_with_users, name='chat_with_users'),
    path('room/<str:private_chat_room_name>/', room, name='room'),

    # API-related views
    path('api/posts/', StatusPostAPIView.as_view(), name='posts-api'),
    path('api/posts/<int:pk>/', StatusPostDetailAPIView.as_view(), name='post-detail-api'),
]