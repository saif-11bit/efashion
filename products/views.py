from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Available_For,
    Crousal,
    Category,
    Item,
    OrderItem,
    Order,
    metaTags,
    Address,
    CouponCode,
    Review,
    Payment,
    Refund,
)
from .forms import CheckoutForm
from . import Checksum
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import VerifyPaytmResponse
import requests
# from django.db.models import F
# Create your views here.


# Landing page view
def landing(request):
    crousal = Crousal.objects.all()
    items = Item.objects.all()[:8]
    category = Category.objects.all()
    tags = metaTags.objects.all()
    reviews = Review.objects.all()
    context = {
        'available_for':Available_For.objects.all(),
        'crousal':crousal,
        'items':items,
        # 'category':Category,
        'tag': tags,
        'review': reviews,
    }
    return render(request, 'index.html', context)

# product list of particular category
def category_item(request,id):
    items = Item.objects.filter(category=id)
    cate = Category.objects.get(id=id)
    tags = metaTags.objects.all()
    context = {
        'items':items,
        'tag': tags,
        'cate':cate,
    }
    return render(request, 'product.html', context)

# check if query matches item name or cat or des
def searchMatch(query, item):
    if query.lower() in item.p_name.lower() or query.lower() in item.category.title.lower() or query.lower() in item.p_desc.lower():
        return True
    return False

# search
def search_item(request):
    query = request.GET.get('search')
    all_items = Item.objects.all()
    prod = [item for item in all_items if searchMatch(query, item)]
    context = {
        'prod':prod
    }
    return render(request, 'searchedItem.html', context)


# Prodcut detail
def product_detail(request, id):
    item = Item.objects.get(id=id)
    related_item = Item.objects.exclude(id=id).filter(category=item.category)[:4]
    tags = metaTags.objects.all()


    context = {
        'item' :item,
        'tag': tags,
        'related_item':related_item,
    }
    return render(request, 'productDes.html', context)


# cart
@login_required
def cart_view(request):
    try:
        cart_items = Order.objects.get(user=request.user, ordered=False)
        context = {
            'cart':cart_items,
        }
        return render(request, 'cart.html', context)
    except ObjectDoesNotExist:
        messages.info(request, "No item in your cart!")
        return redirect('/')


# Add to Cart
@login_required
def add_to_cart(request, id):
    if request.method == 'POST':
        p_size = request.POST['p_size']
        p_qty = request.POST['p_qty']
        
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        size=p_size,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order items in the order
        if order.items.filter(item__id=item.id, size=p_size).exists():
            order_item.quantity = int(p_qty)
            order_item.save()
            messages.info(request, "The item updated!")
            return redirect('cart')
        else:
            order_item.quantity = int(p_qty)
            order_item.save()
            order.items.add(order_item)
            messages.info(request, "This item was added to the cart.")
            return redirect('product-detail', id=id)

    else:
        ordered_date = timezone.now()
        order_item.quantity = int(p_qty)
        order_item.size = p_size
        order_item.save()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to the cart.")
        return redirect('product-detail', id=id)


# Remove from cart
@login_required
def remove_from_cart(request, id, size):
    item = get_object_or_404(Item, id=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order items in the order
        if order.items.filter(item__id=item.id).exists():
            order_item =OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
                size=size,
            )[0]

            order_item.quantity = 1
            order_item.save()
            
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect('cart')
        else:
            # order doesn't contain this order item
            messages.info(request, "This item was not in your cart.")
            return redirect('product-detail', id=id)
            
    else:
        # user doesn't have an order
        messages.info(request, "You donot have active order.")
        return redirect('product-detail', id=id)


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
            return redirect('cart')
        else:
            # order doesn't contain this order item
            messages.info(request, "This item was not in your cart.")
            return redirect('products:product-detail', id=id)
            
    else:
        # user doesn't have an order
        messages.info(request, "You donot have active order.")
        return redirect('products:product-detail', id=id)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


# Checkout
class CheckoutView(LoginRequiredMixin,View):
    def get(self,*args, **kwargs):
        try:
            order= Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order':order,
                # 'couponForm':CouponForm(),
            }

            address_qs = Address.objects.filter(
                user=self.request.user,
                # default=True,
            )
            
            if address_qs.exists():
                context.update( {'address': address_qs.all()} )

            return render(self.request, 'checkout.html', context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You donot have an active order!")
            return redirect('checkout')

# ===================

# check if coupon exists
def get_coupon(request, coupon):
    now = timezone.now()
    coupon = CouponCode.objects.filter(code__iexact=coupon, valid_from__lte=now, valid_to__gte=now,active=True).exclude(order__user=request.user)
    if coupon.exists():
        return coupon.first()


# add Coupon
@login_required
def add_coupon(request):
    if request.method=='POST':
        try:
            coupon = request.POST['coupon']
            print(coupon)
            coup = get_coupon(request, coupon)
            order= Order.objects.get(user=request.user, ordered=False)
            order.coupon = coup
            order.save()
            messages.success(request, "Successfully Added Coupon!")
            return redirect("checkout")
        except ObjectDoesNotExist:
            messages.info(request, "You donot have an active order!")
            return redirect("checkout")


@login_required
def add_address(request):
    if request.method=='POST':
        user = request.user
        name = request.POST['name']
        phone_n = request.POST['phone_n']
        street_address = request.POST['street_address']
        city = request.POST['city']
        state = request.POST['state']
        pin_code = request.POST['pin_code']

        address = Address()
        address.user = user
        address.name = name
        address.phone_n = phone_n
        address.street_address = street_address
        address.city = city
        address.state = state
        address.pin_code = pin_code
        address.save()

        return redirect('/checkout/')


def payment(request):
    order = Order.objects.get(user=request.user, ordered=False)
    if request.method == 'POST':
        SelAdressid = request.POST['radioAdressSel']
        address = Address.objects.get(id=SelAdressid)
        order.address = address
        order.save()
    order_id = Checksum.__id_generator__()
    bill_amount = str(order.get_total())
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        # 'MOBILE_NO': '7405505665',
        # 'EMAIL': 'dhaval.savalia6@gmail.com',
        'CUST_ID': 'saif930go@gmail.com',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': bill_amount,
    } # This data should ideally come from database
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'payment.html', context)


@csrf_exempt
def response(request):
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        return redirect('/success/')
        # save success details to db; details in resp['paytm']
        # return HttpResponse("<center><h1>Transaction Successful</h1><br><h3>Return Home</h3><center>", status=200)
    else:
        # check what happened; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)

def success(request):
    order = Order.objects.get(user=request.user, ordered=False)
    payment = Payment()
    payment.user = request.user
    payment.amount = order.get_total()
    payment.save()
    order.payment = payment
    order.ordered = True
    order.save()
    return redirect('/')

@login_required
def myorders(request):
    myorder = OrderItem.objects.filter(user=request.user,ordered=True)
    context = {
        'order': myorder,
    }
    return render(request, 'myorders.html', context)

@login_required
def returnorder(request):
    myorder = OrderItem.objects.filter(user=request.user,ordered=True)
    #Ye Banana hai
    context = {
        'order': myorder,
    }
    return render(request, 'refund.html', context)
