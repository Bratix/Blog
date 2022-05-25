from django.contrib import admin
from .models import Blog, Post, Comment, Category, Friend_Request, Profile

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Friend_Request)
admin.site.register(Profile)