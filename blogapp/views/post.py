from django.views import generic, View
from ..models import Post, Blog, Comment
from django.contrib.humanize.templatetags.humanize import intcomma
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import JsonResponse
from .views import BROWSE, BLOG, NEW_BLOG


class PostDetail(generic.ListView):
    model = Comment
    paginate_by = 6
    context_object_name = 'comments'
    template_name = 'post/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['pk']
        context['active_tab'] = BROWSE
        context['post'] = Post.objects.get(pk=post_id)
        return context

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post__id = post_id).order_by('-edit_date')

class PostSearchByTag(generic.ListView):
    template_name = 'blogapp/search.html'

    def get_queryset(self):
        wanted_tag = self.request.GET.get('search').split(",")
        return Post.objects.filter(tags__name__in = wanted_tag ).distinct()
        #return Post.objects.filter(functools.reduce(or_, [Q(tags__name__icontains=q) for q in wanted_tag]))

class PostLike(View):
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            post_id = kwargs.get('pk')
            post = Post.objects.get(id = post_id)
            user = request.user
            user_like = False
            if user.is_authenticated:
                if user in post.likes.all() :
                    post.likes.remove(user)
                    user_like = False
                else:
                    post.likes.add(user)
                    user_like = True
            
            like_number = intcomma(post.likes.count())
            data = {
                'like_counter': like_number,
                'user_like' : user_like,
            }
            return JsonResponse(data)
    

class PostCreate(CreateView):
    model = Post
    fields = ['title','text','image','tags']
    template_name = "post/add.html"

    def get(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=self.kwargs['blog_pk'])
        print(self.request.user != blog.author )
        if self.request.user != blog.author and self.request.user not in blog.moderators.all() :
            return redirect("blog:index")
        return super(PostCreate, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=self.kwargs['blog_pk'])
        if self.request.user != blog.author and self.request.user not in blog.moderators.all() :
            return redirect("blog:index")
        return super(PostCreate, self).post(self, request, *args, **kwargs)

    def form_valid(self, form): 
        self.object = form.save(commit=False)
        self.object.blog = Blog.objects.get(id=self.kwargs['blog_pk'])
        self.object.author = self.request.user
        return super(PostCreate, self).form_valid(form)

class PostUpdate(UpdateView):
    model = Post
    fields = ['title','text','image','tags']
    template_name = "post/edit.html"

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect("blog:index")
        return super(PostUpdate, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect("blog:index")
        return super(PostUpdate, self).post(self, request, *args, **kwargs)

class PostDelete(DeleteView):
    model = Post
    def get_success_url(self):
        return reverse_lazy('blog:blog_detail',kwargs = {'pk': Post.objects.get(id=self.kwargs['pk']).blog.id})

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != self.request.user:
            return redirect("blog:index")
        return super(PostDelete, self).post(self, request, *args, **kwargs)








