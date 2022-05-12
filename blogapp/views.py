from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView, RedirectView
from django.urls import reverse_lazy
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

class IndexView(generic.ListView):
    model = Post 
    paginate_by = 4
    context_object_name = 'all_posts'
    template_name = 'index/index.html'
    ordering = ['-likes']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['active_tab'] = 'browse'
        context['all_categories'] = Category.objects.all
        return context

class CategoryView(generic.ListView):
    template_name = 'blogapp/category.html'

    def get_queryset(self):
        return Category.objects.all()

    
class BlogsbyCategoryView(generic.ListView):
    template_name = 'blogapp/category_detail.html'

    def get_queryset(self):
        current_category = Category.objects.get(id=self.kwargs['pk'])
        return Blog.objects.filter(category = current_category)

class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['active_tab'] = 'blog' + str(BlogDetailView.get_object(self).id)
        return context

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blogapp/post_detail.html'

class PostSearchByTag(generic.ListView):
    template_name = 'blogapp/search.html'

    def get_queryset(self):
        wanted_tag = self.request.GET.get('search').split(",")
        return Post.objects.filter(tags__name__in = wanted_tag ).distinct()
        #return Post.objects.filter(functools.reduce(or_, [Q(tags__name__icontains=q) for q in wanted_tag]))

def PostLike(request, **kwargs):

    tab_kw = kwargs.get('pk')
    post = Post.objects.get(id = tab_kw)
    user = request.user
    user_like = False
    if user.is_authenticated:
        if user in post.likes.all() :
            post.likes.remove(user)
            user_like = False
        else:
            post.likes.add(user)
            user_like = True
    
    like_number = post.likes.count()
    data = {
        'like_counter': like_number,
        'user_like' : user_like,
    }
    return JsonResponse(data)




class BlogCreate(CreateView):
    model = Blog
    fields = ['title','category','image', 'description']
    template_name = "blog/add.html"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BlogCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['active_tab'] = "new_blog"
        return context

class BlogUpdate(UpdateView):
    model = Blog
    template_name = "blog/edit.html"
    fields = ['title', 'category', 'image', 'description']

class BlogDelete(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')




class PostCreate(CreateView):
    model = Post
    fields = ['title','text','image','tags']

    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.blog = Blog.objects.get(id=self.kwargs['pk'])
        return super(PostCreate, self).form_valid(form)

class PostUpdate(UpdateView):
    model = Post
    fields = ['title','text','image','tags']
    template_name = "blogapp/update.html"

class PostDelete(DeleteView):
    model = Post
    def get_success_url(self):
        return reverse_lazy('blog:detail',kwargs = {'pk': Post.objects.get(id=self.kwargs['pk']).blog.id})


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
    
