from django.views import generic
from django.shortcuts import render
from ..models import Blog, Post, Profile
from django.db.models import Q


class IndexSearch(generic.View):
    def get(self, request):
        search_param = self.request.GET.get('param')
        context = { 
            'blogs' : Blog.objects.filter(title__contains = search_param)[:3], 
            'posts': Post.objects.filter(title__contains = search_param)[:3], 
            'profiles': Profile.objects.filter(
                Q(user__username__contains = search_param) | 
                Q(first_name__contains = search_param) |
                Q(last_name__contains = search_param))[:3],
            'search_param': "param=" + search_param
        }
        return render(request, 'search/index.html', context )


class BlogSearch(generic.ListView):
    model = Blog
    paginate_by = 4
    context_object_name = 'blogs'
    template_name = 'search/blog.html'

    def get_queryset(self):
        search_param = self.request.GET.get('param')
        return Blog.objects.filter(title__contains = search_param).order_by("title")

class PostSearch(generic.ListView):
    model = Post
    paginate_by = 4
    context_object_name = 'posts'
    template_name = 'search/post.html'

    def get_context_data(self, **kwargs):
        search_param = self.request.GET.get('param')
        context = super().get_context_data(**kwargs)
        context['search_param'] =search_param
        return context

    def get_queryset(self):
        search_param = self.request.GET.get('param')
        return Post.objects.filter(title__contains = search_param).order_by("title")