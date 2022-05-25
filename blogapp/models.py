from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])], default='default_user.jpg')
    first_name = models.CharField(max_length = 15)
    last_name = models.CharField(max_length = 15)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
    pending_friends = models.ManyToManyField(User, related_name="pending_friends", blank=True)

    def get_absolute_url(self):
        return reverse("blog:profile_detail", kwargs={"pk": self.pk}) 
    
    def __str__(self):
        return self.user.username


class Friend_Request(models.Model):
    submitter = models.ForeignKey(User, related_name="submitter", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name="reciever", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    send_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "from " + self.submitter.username +" to " + self.reciever.username


class Category(models.Model):
    name = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    moderators = models.ManyToManyField( User, related_name="moderators", blank=True)
    subscribers = models.ManyToManyField(User, related_name="subscribers")
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    title = models.CharField(max_length = 50, unique=True, default="")
    description = models.TextField()
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])])
    creation_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.pk}) 


class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE) 
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    title = models.CharField(max_length = 50)
    text = models.TextField()
    tags = TaggableManager()
    image = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])])
    creation_date = models.DateTimeField(auto_now_add = True)
    
   
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.id}) 
    


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    text = models.CharField(max_length = 3000, default="")
    edited = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(default=now)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.post.id})
    

