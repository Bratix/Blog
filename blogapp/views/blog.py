from django.views import generic
from ..models import Blog, Post
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

class BlogDetail(generic.ListView):
    model = Post
    paginate_by = 4
    context_object_name = 'posts'
    template_name = 'blog/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs['pk']
        context['active_tab'] = 'blog' + blog_id
        context['blog'] = Blog.objects.get(pk=blog_id)
        return context

    def get_queryset(self):
        blog_id = self.kwargs['pk']
        return Post.objects.filter(blog__id = blog_id).order_by('title')

class BlogCreate(CreateView):
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
        context['active_tab'] = "new_blog"
        return context 

class BlogUpdate(UpdateView):
    model = Blog
    template_name = "blog/edit.html"
    fields = ['title', 'category', 'image', 'description']

class BlogDelete(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')