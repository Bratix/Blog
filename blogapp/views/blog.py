from audioop import reverse
from django.shortcuts import redirect
from django.views import generic
from ..models import Blog, Post
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .views import BROWSE, BLOG, NEW_BLOG
from django.contrib.auth.mixins import LoginRequiredMixin



class BlogDetail(generic.ListView):
    
    model = Post
    paginate_by = 4
    context_object_name = 'posts'
    template_name = 'blog/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs['pk']
        context['active_tab'] = BLOG + blog_id
        context['blog'] = Blog.objects.get(pk=blog_id)
        return context

    def get_queryset(self):
        blog_id = self.kwargs['pk']
        return Post.objects.filter(blog__id = blog_id).order_by('-title')

class BlogCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Blog
    fields = ['title','category','image', 'description']
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