from django.db import models
from django.urls import reverse
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=50)
    #picture = models.FileField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk}) 
    

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_title = models.CharField(max_length = 50)
    creation_date = models.DateTimeField(auto_now_add=True)
    post_text = models.CharField(max_length = 50000)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.blog.id}) 

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
    comment_text = models.CharField(max_length = 3000)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.post.blog.id})
    

