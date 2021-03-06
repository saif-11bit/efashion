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
    payment,
    response,
    success,
    myorders,
    returnorder,
    trackorder,
    aboutUs,
    contactUs,
    privacy_policy,
    terms_con,
    refund_return,
)



urlpatterns = [
    path('', landing, name="landing"),
    path('search/', search_item, name="search"),
    path('cart/', cart_view, name="cart"),
    path('payment/', payment,name="payment"),
    path('success/<int:id>', success,name="success"),
    path('response/', response, name="response"),
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
    path('track/', trackorder, name="track"),
    path('contact/', contactUs, name="contact"),
    path('about/', aboutUs, name="about"),
    path('privacy_policy/', privacy_policy, name="policy"),
    path('terms/', terms_con, name="terms"),
    path('return_policy/', refund_return, name="returnPolicy"),
    # Authentication System 
    # path('signup/', SignUpSystem, name="Signin"),
    # path('login/', LoginSystem, name="Login"),
    # path('logout/', logoutUser, name="Logout")

]
