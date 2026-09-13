from django.urls import *
from .views import *

urlpatterns = [
    path("",index,name='home'),
    path('products',products,name='products'),
    path('product-details/<int:product_id>/',product_details,name='product-details'),
    path('addtocart/<int:product_id>',add_to_cart,name='addtocart'),
    path('carts',carts,name='carts'),
    path('delete-cart/<int:cart_id>',delete_cart,name='delete-cart'),
    path('orderitem/<int:cart_id>/<int:product_id>',orderItem,name='orderitem'),
    path('stripe-form',stripeForm,name='stripe-form'),
    path('create-checkout-session/<int:order_id>/<int:cart_id>',create_checkout_session,name='create-checkout-session'),
    path('success',stripeSuccess,name='success'),
    path('success/',stripeSuccess,name='success_slash'),
    path('my-orders',myOrders,name='my-orders'),
]