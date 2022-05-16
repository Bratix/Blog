from django.views import generic
from ..models import Post, Category

class IndexView(generic.ListView):
    model = Post 
    paginate_by = 4
    context_object_name = 'all_posts'
    template_name = 'index/index.html'
    ordering = ['-likes']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'browse'
        context['all_categories'] = Category.objects.all
        return context