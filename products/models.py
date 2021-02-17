from django.db import models
from django.contrib.auth.models import User
# Create your models here.
'''
category
item
orderitem
order
address
couponcode
refund
'''

class Category(models.Model):
    FOR = [
        ('men', 'men'),
        ('women', 'women'),
        ('kids', 'kids'),
    ]
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='Category Poster', null=True)
    _for = models.CharField(max_length=200, choices=FOR, null=True)

    def __str__(self):
        return f'{self._for}-{self.title}'


class Crousal(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='Crousal Image')

    def __str__(self):
        return self.title

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=200)
    p_image = models.ImageField(upload_to='Items')
    p_price = models.IntegerField()
    p_dis_price = models.IntegerField()
    p_desc = models.TextField()
    p_slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.p_name


class OrderItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} of {self.item.p_name}"

	def get_total_item_price(self):
		return self.quantity * self.item.p_price

	def get_total_discount_item_price(self):
		return self.quantity * self.item.p_dis_price

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_total_discount_item_price()

	def get_final_price(self):
		if self.item.p_dis_price:
			return self.get_total_discount_item_price()
		return self.get_total_item_price()


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ref_code = models.CharField(max_length=20)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
	# payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
	coupon = models.ForeignKey('CouponCode', on_delete=models.SET_NULL, null=True, blank=True)
	being_delivered = models.BooleanField(default=False)
	recieved = models.BooleanField(default=False)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		if self.coupon and total>1:
			total -= self.coupon.amount
		return total

class Address(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	street_address = models.CharField(max_length=200)
	address_line2 = models.CharField(max_length=200)
	state = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	pin_code = models.CharField(max_length=6)
	default = models.BooleanField(default=False)

	def __str__(self):
		return self.street_address

	class Meta:
		verbose_name_plural = 'Addresses'


class CouponCode(models.Model):
	code = models.CharField(max_length=15)
	valid_from = models.DateTimeField(null=True, blank=True)
	valid_to = models.DateTimeField(null=True, blank=True)
	amount = models.FloatField()
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.code


class Refund(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	reason = models.TextField()
	accepted = models.BooleanField(default=False)
	email = models.EmailField()

	def __str__(self):
		return f"{self.pk}"

class metaTags(models.Model):
	keyword = models.TextField()
	desc = models.TextField()

	def __str__(self):
		return "Keywords:" + self.keyword

