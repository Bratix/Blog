from django.db import models
from django.urls import reverse
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])])
    first_name = models.CharField(max_length = 15)
    last_name = models.CharField(max_length = 15)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)


class Friend_Request(models.Model):
    submitter = models.ForeignKey(User, related_name="submitter", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name="reciever", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    send_date = models.DateTimeField(auto_now_add = True)


class Category(models.Model):
    name = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name="subscribers")
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    title = models.CharField(max_length = 50, unique=True, default="")
    description = models.TextField()
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])])
    creation_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk}) 


class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE) 
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_likes")
    title = models.CharField(max_length = 50)
    text = models.TextField()
    tags = TaggableManager()
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])])
    creation_date = models.DateTimeField(auto_now_add = True)
    
   
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.id}) 


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    text = models.CharField(max_length = 3000, default="")
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("blog:Post_detail", kwargs={"pk": self.post.id})
    

