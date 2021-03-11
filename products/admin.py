from django.contrib import admin
from .models import (
    Available_For,
    Category,
    Item,
    OrderItem,
    Order,
    Address,
    CouponCode,
    Refund,
    metaTags,
    Review,
    Crousal,
)
# Register your models here.

admin.site.register(Available_For)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(CouponCode)
admin.site.register(Refund)
admin.site.register(metaTags)
admin.site.register(Review)
admin.site.register(Crousal)