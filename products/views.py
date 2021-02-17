from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

# product list of particular category
def category_item(request,id):
    items = Item.objects.filter(category=id)
    context = {
        'items':items,
    }
    return render(request, 'items.html', context)


# Prodcut detail
def product_detail(request, id):
    item = Item.objects.get(id=id)
    context = {
        'item' :item,
    }
    return render(request, 'product-detail.html', context)



# Add to Cart
@login_required
def add_to_cart(request, id):
	item = get_object_or_404(Item, id=id)
	order_item, created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False
	)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if order items in the order
		if order.items.filter(item__id=item.id).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "The item quantity was updated.")
			return redirect('/')
		else:
			order.items.add(order_item)
			messages.info(request, "This item was added to the cart.")
			return redirect('products:product-detail', id=id)

	else:
		ordered_date = timezone.now()
		order = Order.objects.create(user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request, "This item was added to the cart.")
		return redirect('products:product-detail', id=id)

# Remove from cart
@login_required
def remove_from_cart(request, id):
	item = get_object_or_404(Item, id=id)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if order items in the order
		if order.items.filter(item__id=item.id).exists():
			order_item =OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]

			order_item.quantity = 1
			order_item.save()
            
			order.items.remove(order_item)
			messages.info(request, "This item was removed from your cart.")
			return redirect('/')
		else:
			# order doesn't contain this order item
			messages.info(request, "This item was not in your cart.")
			return redirect('products:product-detail', id=id)
			
	else:
		# user doesn't have an order
		messages.info(request, "You donot have active order.")
		return redirect('products:product-detail', id=id)


# Remove single from cart
@login_required
def remove_single_from_cart(request, id):
	item = get_object_or_404(Item, id=id)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if order items in the order
		if order.items.filter(item__id=item.id).exists():
			order_item =OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
			messages.info(request, "This item quantity was updated!")
			return redirect('/')
		else:
			# order doesn't contain this order item
			messages.info(request, "This item was not in your cart.")
			return redirect('products:product-detail', id=id)
			
	else:
		# user doesn't have an order
		messages.info(request, "You donot have active order.")
		return redirect('products:product-detail', id=id)



# Checkout