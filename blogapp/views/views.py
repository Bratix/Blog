from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView, RedirectView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Blog, Post, Comment, Category
from django.contrib.auth.models import User
import json
from django.core import serializers
from django.http import JsonResponse
# from operator import and_, or_
# import functools
# from django.db.models import Q





class CategoryView(generic.ListView):
    template_name = 'blogapp/category.html'

    def get_queryset(self):
        return Category.objects.all()

    
class BlogsbyCategoryView(generic.ListView):
    template_name = 'blogapp/category_detail.html'

    def get_queryset(self):
        current_category = Category.objects.get(id=self.kwargs['pk'])
        return Blog.objects.filter(category = current_category)





class CommentCreate(CreateView):
    model = Comment
    fields = ['text']

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response
        
    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        response = super(CommentCreate, self).form_valid(form)

        if self.request.is_ajax():
            data = {
                'pk' : self.object.pk,
                'comment_text' : self.object.comment_text,
                'user' : str(self.object.user),
                'creation_date' : self.object.creation_date,
                'comment_count' : self.object.post.comment_set.count(),
            }
            return JsonResponse(data)
        else:
            return response

        

class CommentUpdate(UpdateView):
    model = Comment
    fields = ['text']
    template_name = "blogapp/comment_update.html"

class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('blog:Post_detail',kwargs = {'pk': Comment.objects.get(id=self.kwargs['pk']).post.id})
    
