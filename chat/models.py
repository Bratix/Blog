from django.db import models
from django.contrib.auth.models import User



class Chat(models.Model):
    user1 = models.ForeignKey(User,on_delete = models.CASCADE,  related_name='user1')
    user2 = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user2')
    
    def __str__(self):
        return self.user1.username + self.user2.username

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now_add = True)
    text = models.TextField()

    def __str__(self):
        return self.text
