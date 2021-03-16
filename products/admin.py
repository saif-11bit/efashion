from django.contrib import admin
from .models import (
    Available_For,
    Category,
    Item,
    OrderItem,
    Order,
    Address,
    CouponCode,
    metaTags,
    Review,
    Crousal,
	EmailNewsletter,
)
# Register your models here.

def make_refund_accepted(ModelAdmin, request, queryset):
	queryset.update(refund_requested=False, refund_granted=True)
make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderAdmin(admin.ModelAdmin):
	list_display = [
		'user', 'ordered', 'being_delivered', 'recieved','refund_requested','refund_granted','address','payment','coupon'
	]

	list_display_links = [
		'user',
		'address',
		'payment',
		'coupon',
	]
	list_filter = [
		'user', 'ordered', 'being_delivered', 'recieved','refund_requested','refund_granted'
	]

	search_fields = [
		'user__username',
		'ref_code',
	]

	actions = [make_refund_accepted]

class AddressAdmin(admin.ModelAdmin):
	list_display = [
		'user',
        'name',
        'phone_n',
		'street_address',
		'state',
		'city',
		'pin_code',
	]

	list_filter = [
		'state',
		'pin_code',
	]

	search_fields = [
		'user__username',
		'street_address',
		'state',
		'city',
		'pin_code',
	]


admin.site.register(Available_For)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(CouponCode)
admin.site.register(metaTags)
admin.site.register(Review)
admin.site.register(Crousal)
admin.site.register(EmailNewsletter)