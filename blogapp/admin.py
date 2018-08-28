from django.contrib import admin
from .models import Blog, BlogPost, Comment, Category

admin.site.register(Blog)
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Category)