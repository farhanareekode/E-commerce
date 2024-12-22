from itertools import product

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import return_None
from home.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *


def c_id(request):
    ct_id = request.session.session_key
    if not ct_id:
        ct_id = request.session.create()
    return ct_id



@login_required(login_url='login')
def add_cart(request, pk):
    product = Product.objects.get(id=pk)
    user = request.user
    try:
        cart_items = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart_items = Cart.objects.create(cart_id=c_id(request), user=user)
        cart_items.save()

    try:
        item_items = Items.objects.get(product=product, cart=cart_items)
        if item_items.quantity < item_items.product.stock:
            item_items.quantity += 1
            # product.stock -= 1
            # product.save()
        item_items.save()
    except Items.DoesNotExist:
        item_items = Items.objects.create(product=product, quantity=1, cart=cart_items)
        # product.stock -= 1
        # product.save()
        item_items.save()
    return redirect('cart_details')




def cart_details(request, total=0, count=0, cart_items=None, item_items=None):
    try:
        user = request.user

        if user.is_authenticated:
            cart_items = Cart.objects.filter(user=user)

        # check the section have any products
        else:
            cart_id = request.session.get('cart_id')
            cart_items = Cart.objects.filter(cart_id=cart_id)

        item_items = Items.objects.filter(cart__in=cart_items, active=True)
        for i in item_items:
            total += (i.product.price * i.quantity)
            count += i.quantity

    except ObjectDoesNotExist:
        return HttpResponse("No products")

    return render(request, 'cart.html', {'item_items': item_items, 'total': total, 'count': count})




def min_cart(request, pk):
    user = request.user
    try:
        if user.is_authenticated:
            cart_items = Cart.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            cart_items = Cart.objects.filter(cart_id=cart_id)

        if cart_items.exists:
            for ct in cart_items:
                product = get_object_or_404(Product, id=pk)
                try:
                    item_items = Items.objects.get(product=product, cart=ct)
                    if item_items.quantity > 1:
                        item_items.quantity -= 1
                        item_items.save()
                    else:
                        item_items.delete()
                except Items.DoesNotExist:
                    pass
    except Cart.DoesNotExist:
        pass
    return redirect('cart_details')


def cart_delete(request, pk):
    user = request.user

    try:
        if user.is_authenticated:
            cart_items = Cart.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            cart_items = Cart.objects.filter(cart_id=cart_id)

        if cart_items.exists:
            for ct in cart_items:
                product = get_object_or_404(Product, id=pk)
                try:
                    item_items = Items.objects.get(product=product, cart=ct)
                    item_items.delete()
                except Items.DoesNotExist:
                    pass
    except Cart.DoesNotExist:
        pass
    return redirect('cart_details')
