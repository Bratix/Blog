from django.contrib import admin
from .models import Blog, Notification, Post, Comment, Category, Friend_Request, Profile, Notification

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Friend_Request)
admin.site.register(Profile)
admin.site.register(Notification)