from .models import Category, Blog
from django.contrib.auth.models import User

def load_categories(request):
    categories = Category.objects.all().order_by("name")
    return {'categories': categories}
