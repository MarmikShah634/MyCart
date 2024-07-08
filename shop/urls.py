from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.login, name='Login'),
    path('signin/', views.signin, name='Signin'),
    path('index/', views.index, name='ShopHome'),
    path('upload/', views.upload_product_images, name='upload_product_images'),
    path('become_a_seller/', views.become_a_seller, name='become_a_seller'),
    path('category/<int:category_id>', views.categoryView, name='categoryView'),
    path('quick_review_of_<str:product_name>/<int:product_id>', views.productView, name='productView'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update_cart/<int:cart_item_id>/<int:quantity>/', views.update_cart, name='update_cart'),
    path('cart/update_quantity/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('payment/<int:cart_id>/', views.create_payment, name='create_payment'),
    path('payment/execute/', views.execute_payment, name='execute_payment'),
    path('payment/success/', views.payment_success, name='success'),
    path('payment/error/', views.payment_error, name='error'),
    path('order_history/', views.order_history, name='order_history'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='AboutUs'),
    path('search/', views.search, name='Search'),
    # path('contact/', views.contact, name='ContactUs'),
    # path('products/<int:myid>', views.productView, name='ProductView'),
    # path('checkout/', views.checkout, name='Checkout'),
    # path('user-profile/', views.user_profile, name='UserProfile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)