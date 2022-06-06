from sre_constants import CATEGORY
from django.views import generic
from .constants import CATEGORY
from ..models import Category, Blog

class CategoryDetail(generic.ListView):
    template_name = 'category/detail.html'
    paginate_by = 4
    context_object_name = 'blogs'

    def get_queryset(self):
        current_category = Category.objects.get(id=self.kwargs['pk'])
        return Blog.objects.filter(category = current_category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        context['active_tab'] = CATEGORY + category_id
        context['category'] = Category.objects.get(pk=category_id)
        return context