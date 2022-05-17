from django.views import generic, View
from ..models import Post, Blog
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post/detail.html'

class PostSearchByTag(generic.ListView):
    template_name = 'blogapp/search.html'

    def get_queryset(self):
        wanted_tag = self.request.GET.get('search').split(",")
        return Post.objects.filter(tags__name__in = wanted_tag ).distinct()
        #return Post.objects.filter(functools.reduce(or_, [Q(tags__name__icontains=q) for q in wanted_tag]))

class PostLike(View):
    def get(self, request, *args, **kwargs):
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
        
        like_number = post.likes.count()
        data = {
            'like_counter': like_number,
            'user_like' : user_like,
        }
        return JsonResponse(data)

class PostCreate(CreateView):
    model = Post
    fields = ['title','text','image','tags']
    template_name = "post/add.html"

    def form_valid(self, form): 
        self.object = form.save(commit=False)
        self.object.blog = Blog.objects.get(id=self.kwargs['blog_pk'])
        self.object.author = self.request.user
        return super(PostCreate, self).form_valid(form)

class PostUpdate(UpdateView):
    model = Post
    fields = ['title','text','image','tags']
    template_name = "post/edit.html"

class PostDelete(DeleteView):
    model = Post
    def get_success_url(self):
        return reverse_lazy('blog:detail',kwargs = {'pk': Post.objects.get(id=self.kwargs['pk']).blog.id})

""" def PostLike(request, **kwargs):

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
    return JsonResponse(data) """








