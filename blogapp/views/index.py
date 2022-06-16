from django.views import generic
from ..models import Post, Category
from django.db.models import Count
from django.db.models import Exists, OuterRef
from django.db.models import DateTimeField
from django.db.models.functions import Trunc


class IndexView(generic.ListView):
    model = Post 
    paginate_by = 10
    context_object_name = 'all_posts'
    template_name = 'index/index.html'
    ordering = ['-likes']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'browse'
        context['all_categories'] = Category.objects.all
        return context

    def get_queryset(self):

        if self.request.user.is_authenticated:
            qs = Post.objects.select_related('author__profile').prefetch_related("tags").annotate(like_count=Count('likes', distinct=True), 
                                        comment_count=Count('comment', distinct=True), 
                                        interactions=Count('likes', distinct=True)+Count('comment', distinct=True), 
                                        liked=Exists(Post.likes.through.objects.filter(
                                                            post_id = OuterRef('pk'),
                                                            user_id = self.request.user.id
                                                            )
                                                    )
                                        ).filter(blog__in = self.request.user.subscribers.all()
                                        ).order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')  
        else:
            qs = Post.objects.select_related('author__profile').prefetch_related("tags").annotate(like_count=Count('likes', distinct=True), 
                                    comment_count=Count('comment', distinct=True), 
                                    interactions=Count('likes', distinct=True)+Count('comment', distinct=True), 
                                    liked=Exists(Post.likes.through.objects.filter(
                                                        post_id = OuterRef('pk'),
                                                        user_id = self.request.user.id
                                                        )
                                                )
                                    ).all().order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')  
        return qs


class Popular(generic.ListView):
    model = Post 
    paginate_by = 10
    context_object_name = 'all_posts'
    template_name = 'index/popular.html'
    ordering = ['-likes']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'popular'
        context['all_categories'] = Category.objects.all
        return context

    def get_queryset(self):

        if self.request.user.is_authenticated:
            qs = Post.objects.select_related('author__profile').prefetch_related("tags").annotate(like_count=Count('likes', distinct=True), 
                                        comment_count=Count('comment', distinct=True), 
                                        interactions=Count('likes', distinct=True)+Count('comment', distinct=True), 
                                        liked=Exists(Post.likes.through.objects.filter(
                                                            post_id = OuterRef('pk'),
                                                            user_id = self.request.user.id
                                                            )
                                                    )
                                        ).all(
                                        ).order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')  
        else:
            qs = Post.objects.select_related('author__profile').prefetch_related("tags").annotate(like_count=Count('likes', distinct=True), 
                                    comment_count=Count('comment', distinct=True), 
                                    interactions=Count('likes', distinct=True)+Count('comment', distinct=True), 
                                    liked=Exists(Post.likes.through.objects.filter(
                                                        post_id = OuterRef('pk'),
                                                        user_id = self.request.user.id
                                                        )
                                                )
                                    ).all().order_by(Trunc('creation_date', 'day', output_field=DateTimeField()).desc(), '-interactions')  

        return qs