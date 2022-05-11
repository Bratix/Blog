from django.db import models
from django.urls import reverse
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings
from taggit.managers import TaggableManager

class Category(models.Model):
    name = models.CharField(max_length = 30)
    picture = models.FileField(null = True, blank = True)
    
    def __str__(self):
        return self.name

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.TextField(default="")
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    blog_title = models.CharField(max_length = 50)
    picture = models.FileField(null = True, blank = True)
    tags = TaggableManager()
    creation_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.blog_title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk}) 
    

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) 
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    post_title = models.CharField(max_length = 50)
    post_text = models.TextField()
    tags = TaggableManager()
    picture = models.FileField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add = True)
    
   
    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse("blog:blogpost_detail", kwargs={"pk": self.id}) 

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
    comment_text = models.CharField(max_length = 3000)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return reverse("blog:blogpost_detail", kwargs={"pk": self.post.id})
    

