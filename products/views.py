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
)
from .forms import CheckoutForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
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
    if query.lower() in item.p_name.lower() or query.lower() in item.category.lower() or query.lower() in item.p_desc.lower():
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
    return render(request, 'search.html', context)


# Prodcut detail
def product_detail(request, id):
    item = Item.objects.get(id=id)
    tags = metaTags.objects.all()
    context = {
        'item' :item,
        'tag': tags,
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

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


# Checkout
class CheckoutView(LoginRequiredMixin,View):
    def get(self,*args, **kwargs):
        # form
        form = CheckoutForm()

        try:
            order= Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'form': form,
                'order':order,
                # 'couponForm':CouponForm(),
            }

            address_qs = Address.objects.filter(
                user=self.request.user,
                default=True,
            )
            
            if address_qs.exists():
                context.update( {'default_address': address_qs.last()} )

            return render(self.request, 'checkout-page.html', context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You donot have an active order!")
            return redirect('products:checkout')


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_address = form.cleaned_data.get('use_default_address')
                if use_default_address:
                    print('Using default address!')
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True,
                    )
                    if address_qs.exists():
                        address = address_qs.first()
                        order.address=address
                        order.save()						
                    else:
                        messages.info(self.request, 'No default address available!')
                        return redirect('checkout')
                else:
                    # print('user is entering new shipping address!')
                    street_address = form.cleaned_data.get('street_address')
                    address_line2 = form.cleaned_data.get('address_line2')
                    state = form.cleaned_data.get('state')
                    city = form.cleaned_data.get('city')
                    pin_code = form.cleaned_data.get('pin_code')
                    

                    if is_valid_form([street_address,state,city,pin_code]):		

                        address=Address(
                            user=self.request.user,street_address=street_address,address_line2=address_line2,state=state,city=city,pin_code=pin_code
                        )
                        address.save()

                        order.address=address
                        order.save()

                        set_default_address = form.cleaned_data.get('set_default_address')
                        if set_default_address:
                            address.default = True
                            address.save()

                    else:
                        messages.info(self.request, 'Please fill required Address fields!')

                return redirect('/')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You donot have an active order")
            return redirect("/")


# check if coupon exists
def get_coupon(request, code):
    now = timezone.now()
    coupon = CouponCode.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now,active=True)
    if coupon.exists():
        return coupon


# add Coupon
def add_coupon(request):
    try:
        coupon = request.POST['coupon']
        coup = get_coupon(coupon)
        order= Order.objects.get(user=request.user, ordered=False)
        order.coupon = coup
        order.save()
        messages.success(request, "Successfully Added Coupon!")
        return redirect("products:checkout")
    except ObjectDoesNotExist:
        messages.info(request, "You donot have an active order!")
        return redirect("products:checkout")

def SignUpSystem(request):
    if request.user.is_authenticated:
        return redirect('landing')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account Successfully created for ' + user)

                return redirect('Login')

        context = {'form':form}
    return render(request, 'signup.html', context)

def LoginSystem(request):
    if request.user.is_authenticated:
        return redirect('landing')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
    
            if user is not None:
                login(request, user)
                return redirect('landing')
            else:
                messages.info(request, 'Email or password is incorrect')

        context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('Login')