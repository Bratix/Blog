from django.views import generic
from django.shortcuts import render
from ..models import Blog, Post, Profile
from django.db.models import Q, Count, DateTimeField
from django.db.models.functions import Trunc
from django.db.models import Exists, OuterRef
from .constants import MY_POSTS

class IndexSearch(generic.View):
    def get(self, request):
        search_param = self.request.GET.get('param')
        context = { 
            'blogs' : Blog.objects.filter(title__contains = search_param).annotate(subscriber_count=Count('subscribers')).order_by('-subscriber_count')[:3], 
            'posts': Post.objects.filter(Q(title__contains = search_param) | Q(subtitle__contains = search_param)).annotate(comment_count=Count('comment', distinct=True), 
                                    interactions=Count('likes', distinct=True)+Count('comment', distinct=True), 
                                    liked=Exists(Post.likes.through.objects.filter(
                                                        post_id = OuterRef('pk'),
                                                        user_id = self.request.user.id
                                                        )
                                                )
                                    ).order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')[:3], 
            'profiles': Profile.objects.filter(
                Q(user__username__icontains = search_param) | 
                Q(first_name__icontains = search_param) |
                Q(last_name__icontains = search_param))[:3],
            'search_param': "param=" + search_param
        }
        return render(request, 'search/index.html', context )

 
class BlogSearch(generic.ListView):
    model = Blog
    paginate_by = 10
    context_object_name = 'blogs'
    template_name = 'search/blog.html'

    def get_queryset(self):
        search_param = self.request.GET.get('param')
        return Blog.objects.filter(title__contains = search_param).annotate(subscriber_count=Count('subscribers')).order_by('-subscriber_count')

class PostSearch(generic.ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'search/post.html'

    def get_context_data(self, **kwargs):
        search_param = self.request.GET.get('param')
        context = super().get_context_data(**kwargs)
        context['search_param'] =search_param
        return context

    def get_queryset(self):
        search_param = self.request.GET.get('param')
        return Post.objects.filter((Q(title__contains = search_param) | Q(subtitle__contains = search_param))
                                    ).annotate(like_count=Count('likes', distinct=True), 
                                    comment_count=Count('comment', distinct=True), 
                                    interactions=Count('likes', distinct=True)+Count('comment', distinct=True), 
                                    liked=Exists(Post.likes.through.objects.filter(
                                                        post_id = OuterRef('pk'),
                                                        user_id = self.request.user.id
                                                        )
                                                )
                                    ).order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')

class ProfileSearch(generic.ListView):
    model = Profile
    paginate_by = 21
    context_object_name = 'profiles'
    template_name = 'search/profile.html'

    def get_context_data(self, **kwargs):
        search_param = self.request.GET.get('param')
        context = super().get_context_data(**kwargs)
        context['search_param'] =search_param
        return context

    def get_queryset(self):
        search_param = self.request.GET.get('param')
        return Profile.objects.filter(Q(user__username__icontains = search_param) | 
                Q(first_name__icontains = search_param) |
                Q(last_name__icontains = search_param)).order_by("user__username")


class TagSearch(generic.ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'search/post.html'

    def get_context_data(self, **kwargs):
        search_param = self.request.GET.get('param')
        context = super().get_context_data(**kwargs)
        context['search_param'] =search_param
        return context

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Post.objects.filter(tags__name=tag
                                    ).annotate(like_count=Count('likes', distinct=True), 
                                    comment_count=Count('comment', distinct=True), 
                                    interactions=Count('likes', distinct=True)+Count('comment', distinct=True), 
                                    liked=Exists(Post.likes.through.objects.filter(
                                                        post_id = OuterRef('pk'),
                                                        user_id = self.request.user.id
                                                        )
                                                )
                                    ).filter(
                                    ).order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')

class UserPostSearch(generic.ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'search/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = MY_POSTS
        return context

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author = user
                                    ).annotate(like_count=Count('likes', distinct=True), 
                                    comment_count=Count('comment', distinct=True), 
                                    interactions=Count('likes', distinct=True)+Count('comment', distinct=True), 
                                    liked=Exists(Post.likes.through.objects.filter(
                                                        post_id = OuterRef('pk'),
                                                        user_id = self.request.user.id
                                                        )
                                                )
                                    ).order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')