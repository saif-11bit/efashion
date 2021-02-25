from django.urls import path
from .views import (
    landing,
    category_item,
    product_detail,
    add_to_cart,
    remove_from_cart,
    remove_single_from_cart,
    search_item,
    CheckoutView,
    cart_view,
    add_address,
    add_coupon,
    myorders,
    returnorder,
)



urlpatterns = [
    path('', landing, name="landing"),
    path('search/', search_item, name="search"),
    path('cart/', cart_view, name="cart"),
    path('add-coupon/', add_coupon, name="add-coupon"),
    path('add-address/', add_address, name="add-address"),
    path('category/<int:id>/', category_item, name="category"),
    path('product-detail/<int:id>/', product_detail, name="product-detail"),
    path('add-to-cart/<int:id>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<int:id>/<str:size>', remove_from_cart, name="remove-from-cart"),
    path('remove-single-from-cart/<int:id>/', remove_single_from_cart, name="remove-single-from-cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('myorders/', myorders, name="myorder"),
    path('return/', returnorder, name="return"),
    # Authentication System 
    # path('signup/', SignUpSystem, name="Signin"),
    # path('login/', LoginSystem, name="Login"),
    # path('logout/', logoutUser, name="Logout")

]
