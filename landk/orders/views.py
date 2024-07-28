from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Order, OrderItem, ShippingAddress
from .forms import ShippingForm
from products.models import Product

#@login_required
def checkout(request, product_id=None):
    cart = request.session.get('cart', {})
    
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        cart = {str(product_id): 1}
    
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_item_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_item_price
        })
        total_price += total_item_price
    
    form = ShippingForm()
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'orders/checkout.html', context)

#@login_required
@require_POST
def place_order(request):
    form = ShippingForm(request.POST)
    if form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.save()
        
        cart = request.session.get('cart', {})
        total_price = sum(Product.objects.get(id=product_id).price * quantity 
                          for product_id, quantity in cart.items())
        
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            total_price=total_price,
            status='pending'
        )
        
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
        
        # Clear the cart
        request.session['cart'] = {}
        
        return redirect('order_confirmation', order_id=order.id)
    else:
        # If the form is not valid, redirect back to checkout
        return redirect('checkout')

#@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})