from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from models import Post

class Post(forms.ModelForm):
    
    text = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
