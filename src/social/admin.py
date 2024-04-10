from django.contrib import admin
from .models import Post, Friend, Comment, GalleryImageItem, Message

admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(Comment)

admin.site.register(GalleryImageItem)
admin.site.register(Message)



