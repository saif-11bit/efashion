from django.contrib import admin
from .models import (
    Category,
    Item,
    OrderItem,
    Order,
    Address,
    CouponCode,
    Refund,
    metaTags,
    Review,
)
# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(CouponCode)
admin.site.register(Refund)
admin.site.register(metaTags)
admin.site.register(Review)