from .models import Category


def menu_categories(request):
    categories = Category.objects.all()#filter(parent=None)

    return {"menu_categories": categories}
