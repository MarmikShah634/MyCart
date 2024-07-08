from django.utils import timezone
from django.db import models
from django.conf import settings

#For registering Customer
class UserRegistration(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    email = models.CharField(max_length=16)
    phone_no = models.CharField(max_length=15)
    user_address = models.CharField(max_length=80)
    joined_date = models.DateField(auto_now_add=True)
    is_seller = models.BooleanField(default=False)
    is_prime = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_name

class BecomeSeller(models.Model):
    application_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(UserRegistration, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=16)
    business_email = models.CharField(max_length=16)
    business_phone_no = models.CharField(max_length=15)
    business_address = models.CharField(max_length=80)
    items_to_sell = models.CharField(max_length=200, null=True)
    application_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name
    
class Category(models.Model):

    def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/shop/images/<product_id>/<filename>
        return f'shop/images/{instance.category_name}/{filename}'
    
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)
    category_image = models.ImageField(upload_to=product_directory_path, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='category_created_by', editable=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='category_modified_by', editable=False, null=True, blank=True)
    level = models.PositiveIntegerField(default=0, editable=False)
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        if not self.pk and not self.created_by_id:  # Check if it's a new instance
            self.created_by = current_user
        self.modified_by = current_user

        if self.parent_category:
            self.level = self.parent_category.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(null=False, max_length=30)

    def __str__(self):
        return self.brand_name

class Merchant(models.Model):
    merchant_id = models.AutoField(primary_key=True)
    merchant_name = models.CharField(max_length=20, null=True)
    user_id = models.OneToOneField(UserRegistration, on_delete=models.CASCADE)
    email = models.CharField(max_length=16)
    phone_no = models.CharField(max_length=15)
    merchant_address = models.CharField(max_length=80)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.merchant_name

class Product(models.Model):

    def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/shop/images/<product_id>/<filename>
        return f'shop/images/{instance.product_name}/{filename}'
    
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    price = models.IntegerField(null=False)
    description = models.TextField(max_length=900)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    merchant_id = models.ForeignKey(Merchant, on_delete=models.CASCADE, null=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(upload_to=product_directory_path, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_created_by', editable=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_modified_by', editable=False, null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created
            if hasattr(self, 'request') and self.request.user:
                self.created_by = self.request.user
        self.modified_by = self.request.user if hasattr(self, 'request') and self.request.user else None
        self.modified = timezone.now()
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    
    def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/shop/images/<product_id>/<filename>
        return f'shop/images/{instance.product_id}/{filename}'
    
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='images')
    images = models.ImageField(upload_to=product_directory_path, null=True)

    def __str__(self):
        return f"Image for {self.product_id.product_name}"

class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_name = models.CharField(max_length=30)
    coupon_code = models.CharField(max_length=20)
    coupon_description = models.CharField(max_length=100)
    discount_amount = models.CharField(max_length=4)
    expiry_date = models.DateField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.coupon_name

class Reward(models.Model):
    reward_id = models.AutoField(primary_key=True)
    reward_description = models.CharField(max_length=100)
    points = models.CharField(max_length=5)
    expiry_date = models.DateField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.points

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return str(self.cart_id)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, null=True)

    def __str__(self):
        return f'{self.quantity} of {self.product_id.product_name}'

    def get_total_price(self):
        return self.quantity * self.product_id.price

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product_id = models.ManyToManyField(Product)
    location = models.CharField(null=False, max_length=70)
    quantity = models.CharField(max_length=5)

    def __str__(self):
        return self.location

class AddProductRequest(models.Model):
    add_product_request_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 300)
    price = models.IntegerField(null=False)
    stock = models.BooleanField()
    category_id = models.OneToOneField(Category, on_delete=models.CASCADE)
    merchant_id = models.OneToOneField(Merchant, on_delete=models.CASCADE)
    brand_id = models.OneToOneField(Brand, on_delete=models.CASCADE)
    approval_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField()
    created_by = models.CharField(max_length=30)
    modified_by = models.CharField(max_length=30)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
    
class Shipping(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    address = models.CharField(max_length=70)
    date = models.DateField(auto_now_add=True)
    cost = models.CharField(max_length=4)
    estimated_arrival = models.DateTimeField()
    shipping_method = models.CharField(max_length=10)
    shipping_status = models.CharField(max_length=10)

    def __str__(self):
        return self.shipping_id

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    paypal_payment_id = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    address = models.CharField(max_length=70)
    order_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return str(self.order_id)

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=3)
    price = models.CharField(max_length=5)

    def __str__(self):
        return self.order_item_id

#tax for categories
class CategoryTax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    category_id = models.OneToOneField(Category, on_delete=models.CASCADE)
    tax_rate = models.CharField(max_length=2)
    effective_date = models.DateField(null=False) # from when tax is applied on category
    end_date = models.DateField() # current tax ended and new tax added

    def __str__(self):
        return self.tax_id

# About payments of order
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.CharField(max_length=5)
    method = models.CharField(max_length=10)
    status = models.BooleanField(null=False)
    transaction_id = models.CharField(max_length=15) # Transaction ID provided by the payment gateway

    def __str__(self):
        return self.payment_id
    

# About billings of order
class Billing(models.Model):
    billing_id = models.AutoField(primary_key=True)
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.CharField(max_length=5)
    method = models.CharField(max_length=10)
    address = models.CharField(max_length=70)
    status = models.BooleanField(null=False)
    transaction_id = models.CharField(max_length=15) # Transaction ID provided by the payment gateway

    def __str__(self):
        return self.billing_id
    

class Cancellation(models.Model):
    cancellation_id = models.AutoField(primary_key=True)
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    cancellation_request_date = models.DateField(auto_now_add=True)
    reason = models.CharField(max_length=50)
    status = models.BooleanField(null=False)

    def __str__(self):
        return self.cancellation_id + " " + self.reason

class Refund(models.Model):
    refund_id = models.AutoField(primary_key=True)
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.CharField(max_length=5)
    date = models.DateField(null=False)
    reason = models.CharField(max_length=50)
    status = models.BooleanField(null=False)

    def __str__(self):
        return self.refund_id + " " + self.reason


class Return(models.Model):
    return_id = models.AutoField(primary_key=True)
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(null=False)

    def __str__(self):
        return self.return_id + " " + self.reason
    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length = 300)

    def __str__(self):
        return self.description
    
""" class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=500)
    amount = models.IntegerField(null=False)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(null=False)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:10] + "..." """