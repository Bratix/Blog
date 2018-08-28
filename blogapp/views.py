from django.views import generic
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Blog, BlogPost, Comment, Category

class CategoryView(generic.ListView):
    template_name = 'blogapp/category.html'

    def get_queryset(self):
        return Category.objects.all()
        
class BlogsbyCategoryView(generic.ListView):
    template_name = 'blogapp/category_detail.html'

    def get_queryset(self):
        current_category = Category.objects.get(id=self.kwargs['pk'])
        return Blog.objects.filter(category = current_category)


class IndexView(generic.ListView):
    template_name = 'blogapp/index.html'

    def get_queryset(self):
        return Blog.objects.all()

class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blogapp/detail.html'






class BlogCreate(CreateView):
    model = Blog
    fields = ['blog_title','category']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BlogCreate, self).form_valid(form)

class BlogUpdate(UpdateView):
    model = Blog
    fields = ['blog_title']

class BlogDelete(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')




class BlogPostCreate(CreateView):
    model = BlogPost
    fields = ['post_title','post_text']

    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.blog = Blog.objects.get(id=self.kwargs['pk'])
        return super(BlogPostCreate, self).form_valid(form)

class BlogPostUpdate(UpdateView):
    model = BlogPost
    fields = ['post_title','post_text']

class BlogPostDelete(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:index')

class BlogsPostSearchByTag(generic.ListView):
    template_name = 'blogapp/search.html'

    def get_queryset(self):
        wanted_tag = self.request.GET.get('tag_search').split()
        return BlogPost.objects.filter(tags__name__in = wanted_tag ).distinct()


class CommentCreate(CreateView):
    model = Comment
    fields = ['comment_text']
    
    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.post = BlogPost.objects.get(id=self.kwargs['pk'])
        return super(CommentCreate, self).form_valid(form)

class CommentUpdate(UpdateView):
    model = Comment
    fields = ['comment_text']

class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('blog:index')