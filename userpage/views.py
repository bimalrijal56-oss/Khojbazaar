from django.shortcuts import render,redirect,reverse,get_object_or_404
from product.models import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import *

# Create your views here.

def index(request):
    context = {
        'products' : Product.objects.filter(trending = True).order_by('-id')[:4]
    }
    return render(request,'index.html',context)

def product_details(request,product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'item' : product
    }
    return render(request,'productdetails.html',context)

@login_required
def add_to_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    
    existingItem =Cart.objects.filter(product=product,user=user)
    if existingItem:
        messages.error(request,'Item already exists in your cart')
        return redirect('product-details',product_id)
    else:
        Cart.objects.create(user=user,product=product)
        messages.success(request,'Item added to your cart')
        return redirect('carts')
    
    
def products(request):
    context = {
        'products' : Product.objects.all()
    }
    return render(request,'products.html',context)

@login_required
def carts(request):
    cart = Cart.objects.filter(user=request.user)
    
    context = {
        'cartItems' :cart
    }
    return render(request,'allcarts.html',context)

def delete_cart(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    messages.success(request,'Item removed from your cart')
    return redirect('carts')


@login_required
def orderItem(request,cart_id,product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id=cart_id)
    user = request.user
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get('quantity')
            price = product.discount_price
            total_price = int(quantity) * price
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            payment_method = request.POST.get('payment_method')
            order_status = request.POST.get('order_status')
            
            order = Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total_price=total_price,
                phone=phone,
                email=email,
                address=address,
                payment_method=payment_method,
                payment_status=False,
                order_status='In Progress'
            )
            if order.payment_method == 'COD':
                cart = Cart.objects.get(id=cart_id)
                cart.delete()
                messages.success(request,'Order placed successfully')
                return redirect('home')
            elif order.payment_method == 'Card':
                return redirect(reverse('stripe-form') + '?order_id=' + str(order.id) + '&cart_id=' + str(cart.id))
            else:
                messages.error(request,'Invalid payment method')
    else:
        form = OrderForm()
    
    context = {
        'form' : form
    }
    return render(request,'orderform.html',context)

@login_required
def myOrders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders' : orders
    }
    return render(request,'myorders.html',context)


@login_required
def stripeForm(request):
    cart_id = request.GET.get('cart_id')
    order_id = request.GET.get('order_id')
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request,'stripe_checkout.html',{'cart':cart, 'order':order})
 
import os
import stripe
from django.conf import settings

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', os.environ.get('STRIPE_SECRET_KEY', ''))
@login_required
def create_checkout_session(request,order_id,cart_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    checkout_session = stripe.checkout.Session.create(
       payment_method_types=['card'],
       line_items=[
          {
             'price_data': {
                'currency': 'npr',
                'unit_amount': int(order.total_price * 100),
                'product_data': {'name': order.product.title},
             },
             'quantity': 1,
          },
       ],
       metadata={'order_id': order.id, 'cart_id': cart.id},
       mode='payment',
       success_url=request.build_absolute_uri(reverse('success')) + f'?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}&cart_id={cart.id}',
       cancel_url=request.build_absolute_uri(reverse('carts')),
    )
    return redirect(checkout_session.url, code=303)

def stripeSuccess(request):
     session_id = request.GET.get('session_id')
     order_id = request.GET.get('order_id')
     cart_id = request.GET.get('cart_id')
     
     if not session_id or not order_id:
          messages.error(request,'Payment failed.Please try again')
          return redirect('carts')
          
     order = get_object_or_404(Order, id=order_id)
     
     try:
          session = stripe.checkout.Session.retrieve(session_id)
          if session.payment_status == 'paid':
               order.payment_status= True
               order.save()
               if cart_id:
                   Cart.objects.filter(id=cart_id).delete()
               messages.success(request,'Payment successful. Your order has been placed')
               return redirect('home')
          else:
               messages.error(request,'Payment failed.Please try again')
               return redirect('carts')
     except Exception:
          messages.error(request,'Payment failed.Please try again')
          return redirect('carts')