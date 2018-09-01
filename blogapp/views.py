from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView, RedirectView
from django.urls import reverse_lazy
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Blog, BlogPost, Comment, Category
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse


class IndexView(View):
    def get(self, request):
        context = { 'all_blogs' : Blog.objects.all, 'all_categories': Category.objects.order_by('?')[:3], 'all_posts': BlogPost.objects.order_by('?') }
        return render(request, 'blogapp/index.html', context )
        print("####post_like#####")

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
    template_name = 'blogapp/detail.html'

class BlogPostDetailView(generic.DetailView):
    model = BlogPost
    template_name = 'blogapp/blogpost_detail.html'

class BlogsPostSearchByTag(generic.ListView):
    template_name = 'blogapp/search.html'

    def get_queryset(self):
        wanted_tag = self.request.GET.get('search').split()
        return BlogPost.objects.filter(tags__name__in = wanted_tag ).distinct()

def PostLike(request):
    # def get_redirect_url(self, **kwargs):
    #     tab_kw = self.kwargs.get('pk')
    #     post = get_object_or_404(BlogPost, pk = tab_kw)
    #     user = self.request.user
    #     if user.is_authenticated:
    #         if user in post.likes.all() :
    #             post.likes.remove(user)
    #         else:
    #             post.likes.add(user)

    #     return post.get_absolute_url()
    # tab_kw = self.kwargs.get('pk')
    # post = get_object_or_404(BlogPost, pk = tab_kw)
    # user = self.request.user
    # if user.is_authenticated:
    #     if user in post.likes.all() :
    #         post.likes.remove(user)
    #     else:
    #         post.likes.add(user)

    print("####post_like#####")
    object_ = json.dumps({'like_counter': 999})
    return HttpResponse(object_,content_type='application/json')
    

class TheView(View):

    def options(self, request, id):
        response = HttpResponse()
        response['allow'] = ','.join(['get', 'post', 'put', 'delete', 'options'])
        return response



class BlogCreate(CreateView):
    model = Blog
    fields = ['blog_title','category','picture']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BlogCreate, self).form_valid(form)

class BlogUpdate(UpdateView):
    model = Blog
    fields = ['blog_title', 'category', 'picture']

class BlogDelete(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')




class BlogPostCreate(CreateView):
    model = BlogPost
    fields = ['post_title','post_text','picture','tags']

    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.blog = Blog.objects.get(id=self.kwargs['pk'])
        return super(BlogPostCreate, self).form_valid(form)

class BlogPostUpdate(UpdateView):
    model = BlogPost
    fields = ['post_title','post_text']

class BlogPostDelete(DeleteView):
    model = BlogPost
    def get_success_url(self):
        return reverse_lazy('blog:detail',kwargs = {'pk': BlogPost.objects.get(id=self.kwargs['pk']).blog.id})


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

    def get_success_url(self):
        return reverse_lazy('blog:blogpost_detail',kwargs = {'pk': Comment.objects.get(id=self.kwargs['pk']).post.id})
    
