from django.contrib import admin
from .models import Category
from .models import UserRegistration, BecomeSeller, Category, Brand, Merchant, Product, ProductImage, Coupon, Reward, Cart, CartItem, Inventory, AddProductRequest, Shipping, Order, OrderItem, CategoryTax, Payment, Billing, Cancellation, Refund, Return, Contact

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'modified_by', 'created', 'modified', 'level')
    list_display = ('category_name', 'created_by', 'modified_by', 'created', 'modified')

    def get_readonly_fields(self, request, obj=None):
        # Make fields read-only
        if obj:  # Editing an existing object
            return self.readonly_fields + ('created_by', 'modified_by')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'modified_by', 'created', 'modified')
    list_display = ('product_name', 'price', 'description', 'category_id', 'merchant_id', 'brand_id', 'created_by', 'created', 'modified_by', 'modified')

    def get_readonly_fields(self, request, obj=None):
        # Make fields read-only
        if obj:  # Editing an existing object
            return self.readonly_fields + ('created_by', 'modified_by')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'order_date', 'amount', 'address', 'order_status')
    list_filter = ('order_status',)
    search_fields = ('order_id', 'user_id__username', 'address')
    ordering = ('-order_date',)
    list_editable = ('order_status',)  # Make order_status editable in list display
    
    # Optionally, customize the form layout
    fieldsets = (
        (None, {
            'fields': ('user_id', 'order_date', 'paypal_payment_id', 'amount', 'address', 'order_status')
        }),
    )

admin.site.register(UserRegistration)
admin.site.register(BecomeSeller)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Merchant)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Coupon)
admin.site.register(Reward)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Inventory)
admin.site.register(AddProductRequest)
admin.site.register(Shipping)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(CategoryTax)
admin.site.register(Payment)
admin.site.register(Billing)
admin.site.register(Cancellation)
admin.site.register(Refund)
admin.site.register(Return)
admin.site.register(Contact)