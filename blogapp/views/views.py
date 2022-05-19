from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView, RedirectView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
import json
from django.core import serializers
from django.http import JsonResponse
# from operator import and_, or_
# import functools
# from django.db.models import Q


BROWSE = 'browse'
BLOG = 'blog'
NEW_BLOG = 'new_blog'


class CategoryView(generic.ListView):
    template_name = 'blogapp/category.html'

    def get_queryset(self):
        return Category.objects.all()

    
class BlogsbyCategoryView(generic.ListView):
    template_name = 'blogapp/category_detail.html'

    def get_queryset(self):
        current_category = Category.objects.get(id=self.kwargs['pk'])
        return Blog.objects.filter(category = current_category)






    
