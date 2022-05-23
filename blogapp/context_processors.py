from .models import Category

def load_categories(request):
    categories = Category.objects.all().order_by("name")
    return {'categories': categories}