from django.shortcuts import render
from .models import (
    Crousal,
    Category,
    Item,
    OrderItem,
    Order,
)
# Create your views here.

# Landing page view
def landing(request):
    crousal = Crousal.objects.all()
    items = Item.objects.all()[:8]
    category = Category.objects.all()
    context = {
        'crousal':crousal,
        'items':items,
        'category':category,
    }
    return render(request, 'landing.html', context)


def category_item(request,id):
    items = Item.objects.filter(category=id)
    context = {
        'items':items,
    }
    return render(request, 'items.html', context)