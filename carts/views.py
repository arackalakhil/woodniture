from itertools import product
from optparse import Values
from pickle import TRUE
from re import T
from django.shortcuts import get_object_or_404, redirect, render
from products.models import products
from carts.models import cart, cart_item
from django.core.exceptions import ObjectDoesNotExist

from users.models import address

# Create your views here.


def cart_id(request):
    session_id = request.session.session_key  # to get session_id(key)/cart id

    if not session_id:  # if session id is not present
        session_id = request.session.create()  # to create a new session
    return session_id


def cat_add(request, id):
    product = products.objects.get(id=id)

    

    # --------------------- to combain the product and cart-----------------
    if request.user.is_authenticated:

        try:
            carts_item = cart_item.objects.get(product=product, user=request.user)
            carts_item.quantity += 1  # present cart_item quantibty + 1
            carts_item.save()
        except cart_item.DoesNotExist:
            carts_item = cart_item.objects.create(
                product=product, user=request.user, quantity=1
            )  # quantity is one since we are creating new cart
            carts_item.save()

    else:
        try:
            carts = cart.objects.get(
            cart_id=cart_id(request)
            )  # to bring cart id from the session
        except cart.DoesNotExist:
            carts = cart.objects.create(cart_id=cart_id(request))
            carts.save()

        try:
            carts_item = cart_item.objects.get(product=product, cart=carts)
            carts_item.quantity += 1
            carts_item.save()

        except cart_item.DoesNotExist:
            carts_item = cart_item.objects.create(
                product=product, cart=carts, quantity=1
            )
            carts_item.save()
    # return render(request,'cart_list.html')
    return redirect(cart_view)


def cart_view(request, total=0, quantity=0, carts_item=0):
    # product =products.objects.all()
    try:

        if request.user.is_authenticated:
            carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")

        else:
            carts = cart.objects.get(cart_id=cart_id(request))
            carts_item = cart_item.objects.filter(cart=carts, is_active=True)

        for item in carts_item:
            total += item.product.price * item.quantity
            print(total)
            quantity += item.quantity

    except ObjectDoesNotExist:
        pass

    values = {"total": total, "quantity": quantity, "carts_item": carts_item}
    return render(request, "cart_list.html", values)


def delete_cart(request, id):
    product = get_object_or_404(products, id=id)
    if request.user.is_authenticated:
        carts_item = cart_item.objects.get(product=product, user=request.user)
    else:
        carts = cart.objects.get(cart_id=cart_id(request))
        carts_item = cart_item.objects.get(product=product, cart=carts)
    carts_item.delete()
    return redirect(cart_view)


def cart_item_remove(request, id):

    product = get_object_or_404(products, id=id)

    if request.user.is_authenticated:
        carts_item = cart_item.objects.get(product=product, user=request.user)

    else:
        carts = cart.objects.get(cart_id=cart_id(request))
        carts_item = cart_item.objects.get(product=product, cart=carts)
    if carts_item.quantity > 1:
        carts_item.quantity -= 1
        carts_item.save()

    else:
        carts_item.delete()
    return redirect(cart_view)


def checkout(
    request,
    total=0,
    quantity=0,
    cars_items=None, 
):
    try:
        if request.user.is_authenticated:
            details = address.objects.filter(user=request.user)
            carts_item = cart_item.objects.filter(user=request.user, is_active=True)

        else:
            return render(request,"login-register")
        for item in carts_item:
            total += item.product.price * item.quantity
            quantity += item.quantity
    except:
        if request.user.is_authenticated:
            pass
        else:
            return render(request,"login-register.html")
    values = {
            "total": total,
            "quantity": quantity,
            "carts_item": carts_item,
            "details": details,
        }

    return render(request, "checkout.html",values)
