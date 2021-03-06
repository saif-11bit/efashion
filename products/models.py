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
metaTags
Review
'''

class Available_For(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='Available For', null=True)

    def __str__(self):
     return self.title

class Category(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='Category Poster', null=True)
    _for = models.ForeignKey(Available_For, on_delete=models.CASCADE, null=True)

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
    second_img = models.ImageField(upload_to='Second Img', null=True, blank=True)
    third_img = models.ImageField(upload_to='Third Img', null=True, blank=True)
    p_price = models.IntegerField()
    p_dis_price = models.IntegerField(null=True, blank=True)
    p_desc = models.TextField()
    thirty_four_size = models.BooleanField(null=True)
    small_size = models.BooleanField(null=True)
    medium_size = models.BooleanField(null=True)
    large_size = models.BooleanField(null=True)
    xl_size = models.BooleanField(null=True)
    xxl_size = models.BooleanField(null=True)
    p_slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.p_name


class OrderItem(models.Model):
    SIZE_OPTION = [
        ('34','34'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('2XL', '2XL'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderitems')
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=100, choices=SIZE_OPTION, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.p_name} at {self.created_at}"

    # def no_item_in_cart(self):
    #     self.no_ord_cart = OrderItem.objects.filter(user=self.request.user,ordered=False)
    #     return self.no_ord_cart

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

    class Meta:
        ordering = ['-created_at']
# vAe1x741Tf
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cartitems")
    ref_code = models.CharField(max_length=20,null=True,blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey('CouponCode', on_delete=models.SET_NULL, null=True, blank=True)
    being_delivered = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_requested_reason = models.CharField(max_length=200, null=True, blank=True)
    refund_granted = models.BooleanField(default=False)
    track_order = models.CharField(max_length=80, null=True, blank=True)
    
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
    name = models.CharField(max_length=200)
    phone_n = models.IntegerField(null=True)
    street_address = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=50,null=True)
    city = models.CharField(max_length=50,null=True)
    pin_code = models.CharField(max_length=6,null=True)

    def __str__(self):
        return self.street_address

    class Meta:
        verbose_name_plural = 'Addresses'


class CouponCode(models.Model):
    code = models.CharField(max_length=15, unique=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    amount = models.FloatField()
    active = models.BooleanField(default=True)
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.code

class metaTags(models.Model):
    keyword = models.TextField()
    desc = models.TextField()

    def __str__(self):
        return "Keywords:" + self.keyword

class Review(models.Model):
    image = models.ImageField(upload_to="Customer_review")
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

class EmailNewsletter(models.Model):
    email = models.CharField(max_length=60)
    def __str__(self):
        return self.email

class About(models.Model):
    desc = models.TextField()
    
    def __str__(self):
        return self.desc

class EcomfashionContactDetails(models.Model):
    address = models.TextField()
    phone_num = models.CharField(max_length=50)
    gmail = models.CharField(max_length=50)

    def __str__(self):
        return self.gmail

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=11)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} {self.phone_num}"

class PrivacyPolicy(models.Model):
    desc = models.TextField()

class TermsCondition(models.Model):
    desc = models.TextField()

class ReturnPolicy(models.Model):
    desc = models.TextField()
