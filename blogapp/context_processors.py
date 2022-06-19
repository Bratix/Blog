import os
from .models import Category

def load_categories(request):
    categories = Category.objects.all().order_by("name")
    return {'categories': categories}

def load_url(request):
    ajax_url = os.environ.get('AJAX_URL')
    return {'ajax_url': ajax_url}
