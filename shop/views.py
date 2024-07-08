from math import ceil
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from .models import UserRegistration, BecomeSeller, Category, Brand, Merchant, Product, ProductImage, Coupon, Reward, Cart, CartItem, Inventory, AddProductRequest, Shipping, Order, OrderItem, CategoryTax, Payment, Billing, Cancellation, Refund, Return, Contact, Cart
from .forms import ProductImageForm
from django.views.decorators.cache import never_cache
from django.db.models import Max
import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            user = UserRegistration.objects.get(email=email)
        except UserRegistration.DoesNotExist:
            user = None
        
        if user:
            # Check if the provided password matches the hashed password in the database
            if check_password(password, user.password):
                # Passwords match, login successful
                request.session['email'] = email
                return redirect('shop:ShopHome')
            else:
                # Passwords do not match
                return render(request, 'shop/login.html', {'error': True})
        else:
            # User with the provided email does not exist
            return render(request, 'shop/login.html', {'error': True})
    
    # Render the login form for GET requests
    return render(request, 'shop/login.html')

def signin(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name', '')
        password = make_password(request.POST.get('password', ''))
        email = request.POST.get('email', '')
        phone_no = request.POST.get('phone_no', '')
        user_address = request.POST.get('user_address', '')

        if UserRegistration.objects.filter(email=email).exists():
            raise Exception("Email is already registerd") # make a template for this
        
        if UserRegistration.objects.filter(phone_no=phone_no).exists():
            raise Exception("Phone number is already registerd") # make a template for this

        user_registration = UserRegistration(user_name=user_name, password=password, email=email, phone_no=phone_no, user_address=user_address)
        user_registration.save()
        return redirect('/')
    return render(request, 'shop/signin.html')

def user_profile(request):
    user = UserRegistration.objects.filter(user_id =request.user.id).first()

@never_cache
def index(request):
    email = request.session.get('email')
    if email:
        try:
            user = UserRegistration.objects.get(email=email)
        except UserRegistration.DoesNotExist:
            return redirect('/')
        
        root_categories = Category.objects.filter(parent_category__isnull=True)
        level1_category_items = Category.objects.filter(level=1)
        level2_category_items = Category.objects.filter(level=2)

        level1_category = {}
        level2_category = {}

        for category in root_categories:
            level1_category[category] = Category.objects.filter(parent_category=category)
        
        for category in level1_category_items:
            level2_category[category] = Category.objects.filter(parent_category=category)

        return render(request, 'shop/index.html', {
            'root_categories': root_categories,
            'level1_category': level1_category,
            'level2_category': level2_category
        })

    return redirect('/')

def upload_product_images(request):
    if 'email' in request.session:
        if request.method == 'POST':
            form = ProductImageForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.cleaned_data['product_id']
                images = request.FILES.getlist('images')
                for image in images:
                    ProductImage.objects.create(product_id=product, images=image)
                return HttpResponse('Images uploaded successfully') # Redirect to a success page or another view
        else:
            form = ProductImageForm()
        return render(request, 'shop/upload_product_images.html', {'form': form})
    return redirect('/')
    

def become_a_seller(request):
    if 'email' in request.session:
        if request.method == 'POST':
            user_id = UserRegistration.objects.filter(email=request.session['email']).first()
            business_name = request.POST.get('business_name', '')
            business_email = request.POST.get('business_email', '')
            business_phone_no = request.POST.get('business_phone_no', '')
            business_address = request.POST.get('business_address', '')
            items_to_sell = request.POST.get('items_to_sell', '')

            if BecomeSeller.objects.filter(business_email=business_email).exists():
                return render(request, 'shop/becomeASeller.html', {'business_email_error' : True})
            
            if BecomeSeller.objects.filter(business_phone_no=business_phone_no).exists():
                return render(request, 'shop/becomeASeller.html', {'business_phone_no_error' : True})
            
            if BecomeSeller.objects.filter(business_address=business_address).exists():
                return render(request, 'shop/becomeASeller.html', {'business_address_error' : True})

            req = BecomeSeller(user_id=user_id, business_name=business_name, business_email=business_email, business_phone_no=business_phone_no, business_address=business_address, items_to_sell=items_to_sell)
            req.save()
            return render(request, 'shop/becomeASeller.html', {'success' : True})
        return render(request, 'shop/becomeASeller.html')
    return redirect('/')

@never_cache
def categoryView(request, category_id):
    if 'email' in request.session:
        allCategoryItems = Product.objects.filter(category_id=category_id)
        return render(request, 'shop/categoryItems.html', {'allCategoryItems' : allCategoryItems})
    return redirect('/')

def productView(request, product_name, product_id):
    if 'email' in request.session:
        if request.method == 'POST':
            quantity = request.POST.get('quantity', 1)
            size = request.POST.get('size', '')
            product = get_object_or_404(Product, product_id=product_id)
            user_email = request.session['email']
            user = UserRegistration.objects.filter(email=user_email).first()
            cart, created = Cart.objects.get_or_create(user_id=user, is_paid=False)
            cart_item, created = CartItem.objects.get_or_create(cart_id=cart, product_id=product)
            if created:
                cart_item.quantity = quantity
                cart_item.size = size
            else:
                cart_item.quantity += int(quantity)
                cart_item.size = size
            cart_item.save()
            
            # Calculate and update the total price of the cart
            cart.total_price = cart.get_total_price()
            cart.save()

            return HttpResponseRedirect(request.path_info)

        product = Product.objects.get(product_id=product_id)
        return render(request, 'shop/quickReviewProduct.html', {'product': product})
    return redirect('/')

def view_cart(request):
    if 'email' in request.session:
        user_email = request.session['email']
        user = UserRegistration.objects.filter(email=user_email).first()
        cart = Cart.objects.filter(user_id=user, is_paid=False).first()
        if cart:
            items = CartItem.objects.filter(cart_id=cart)
        else:
            items = []
        return render(request, 'shop/cart.html', {'items': items, 'cart' : cart})
    return redirect('/')

def update_cart(request, cart_item_id, quantity):
    if 'email' in request.session:
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('view_cart')
    return redirect('/')

def update_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect('shop:view_cart')
    item.save()
    return redirect('shop:view_cart')


def create_payment(request, cart_id):
    cart = Cart.objects.get(cart_id=cart_id)
    address = request.POST.get('address', '')
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('shop:execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('shop:error'))
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"Order {cart_id}",
                    "sku": f"order_{cart_id}",
                    "price": str(cart.get_total_price()),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(cart.get_total_price()),
                "currency": "USD"
            },
            "description": f"Payment for Order {cart_id}"
        }]
    })

    if payment.create():
        user = UserRegistration.objects.get(email=request.session['email'])
        if not address:
            address = user.user_address
        order = Order.objects.create(user_id=user, amount=cart.get_total_price(), address=address, paypal_payment_id=payment.id)

        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return redirect('shop:error')

    return redirect('shop:view_cart')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'shop/success.html', {'transaction_id' : payment_id})
    else:
        return redirect('shop:error')

def payment_success(request):
    return render(request, 'shop/success.html')

def payment_error(request):
    return render(request, 'shop/error.html')

def order_history(request):
    if 'email' in request.session:
        user = UserRegistration.objects.filter(email=request.session['email']).first()
        orders = Order.objects.filter(user_id=user)
        return render(request, 'shop/orderHistory.html', {'orders' : orders})
    return redirect('/')

def contact(request):
    if 'email' in request.session:
        if request.method == 'POST':
            user = UserRegistration.objects.get(email=request.session['email'])
            description = request.POST.get('description', '')

            req = Contact(user_id=user, description=description)
            req.save()
            return render(request, 'shop/contact.html', {'success' : True})
        return render(request, 'shop/contact.html')
    return redirect('/')

def about(request):
    return render(request, 'shop/about.html')

def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('/') 


def searchMatch(query, item):
    if query in item.description.lower() or query in item.product_name.lower() or query in str(item.category_id).lower():
        return True
    else:
        return False

def search(request):
    if 'email' in request.session:
        query = request.GET.get('search', '')
        allProducts = Product.objects.all()
        items = [item for item in allProducts if searchMatch(query, item)]
        return render(request, 'shop/search.html', {'items' : items})
    return redirect('/')