from django.contrib import admin
from .models import Blog, Post, Comment, Category

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)