from django.contrib.humanize.templatetags.humanize import  intcomma
from django.shortcuts import redirect
from django.views import generic
from ..models import Blog, Post
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .constants import BROWSE, BLOG, NEW_BLOG, SUBSCRIBED
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc
from django.db.models import Exists, OuterRef


class BlogDetail(generic.ListView):
    
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'blog/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs['pk']
        blog = Blog.objects.get(pk=blog_id)

        if self.request.user.is_authenticated:
            if self.request.user == blog.author or self.request.user in blog.moderators.all():
                context['active_tab'] = BLOG + blog_id
            elif self.request.user in blog.subscribers.all() and self.request.user not in blog.moderators.all():
                context['active_tab'] = SUBSCRIBED + blog_id
            else:
                context['active_tab'] = BROWSE
        else:
            context['active_tab'] = BROWSE

        context['blog'] = blog
        return context

    def get_queryset(self):
        blog_id = self.kwargs['pk']
        return  Post.objects.annotate(like_count=Count('likes', distinct=True), 
                                        comment_count=Count('comment', distinct=True),
                                        interactions=Count('likes', distinct=True)+Count('comment', distinct=True),  
                                        liked=Exists(Post.likes.through.objects.filter(
                                                        post_id = OuterRef('pk'),
                                                        user_id = self.request.user.id
                                                        )
                                                    )
                                    ).filter(blog__id = blog_id
                                    ).order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')  

class BlogCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Blog
    fields = ['title','category','image', 'description', 'moderators']
    template_name = "blog/add.html"
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        self.object.subscribers.add(self.request.user)

        return super(BlogCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['active_tab'] = NEW_BLOG
        return context 

class BlogUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Blog
    template_name = "blog/edit.html"
    fields = ['title', 'category', 'image', 'description']
    raise_exception = True

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != self.request.user:
            return redirect("blog:index")
        return super(BlogUpdate, self).get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != self.request.user:
            return redirect("blog:index")
        return super(BlogUpdate, self).post(self, request, *args, **kwargs)

class BlogDelete(LoginRequiredMixin ,DeleteView):
    login_url = reverse_lazy('login')
    model = Blog
    success_url = reverse_lazy('blog:index')
    
    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != self.request.user:
            return redirect("blog:index")
        return super(BlogDelete, self).post(self, request, *args, **kwargs)

class BlogSubscribe(LoginRequiredMixin , generic.View):
    login_url = reverse_lazy('login')
    def get(self, request, *args, **kwargs): 
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            blog_id =self.kwargs['pk']
            blog = Blog.objects.get(pk = blog_id)

            if self.request.user in blog.subscribers.all():
                blog.subscribers.remove(request.user)
                status = 'unsubbed'
            else:
                blog.subscribers.add(request.user)
                status = 'subbed'

            data = {
                'blog' : blog.title,
                'subscribers' : intcomma(blog.subscribers.all().count()),
                'request_user': request.user.username,
                'status' : status
            }
            return JsonResponse(data)

class AddModerators(LoginRequiredMixin , generic.View):

    template_name = 'blog/add_moderators.html'

    def get(self, request , *args, **kwargs):
        blog_id =self.kwargs['pk']
        blog = Blog.objects.get(pk=blog_id)
        if blog.author != self.request.user:
            return redirect("blog:index")
        return render(request, self.template_name, {'blog': blog})

    def post(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=self.kwargs['pk'])
        if blog.author != self.request.user:
            return redirect("blog:index")

        moderators = request.POST.getlist("moderators")
        if len(moderators) > 0 :
            for id in moderators : 
                user = User.objects.get(pk = id)
                blog.moderators.add(user)
                blog.subscribers.add(user)

        return redirect("blog:blog_detail", self.kwargs['pk'])

class RemoveModerator(LoginRequiredMixin, generic.View): 
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            blog = Blog.objects.get(id=self.kwargs['pk'])
        
            if blog.author != request.user:
                return redirect("blog:index")
            moderator = User.objects.get(id=self.kwargs['moderator_pk'])
            
            blog.moderators.remove(moderator)
            blog.subscribers.remove(moderator)
            data = {
                'status' : 'success'
            }
            return JsonResponse(data)
        