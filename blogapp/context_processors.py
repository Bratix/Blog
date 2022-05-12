from .models import Category

def load_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}