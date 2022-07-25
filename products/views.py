from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
import re
from carts.models import cart, cart_item
from django.core.exceptions import ObjectDoesNotExist
from carts.views import cart_id

from products.models import categories, products


# Create your views here.
def index_page(request):
    # if 'username' in request.session:
    # try:

    #     if request.user.is_authenticated:
    #         carts_item = cart_item.objects.filter(
    #             user=request.user, is_active=True
    #         ).order_by("id")

    #     else:
    #         carts = cart.objects.get(cart_id=cart_id(request))
    #         carts_item = cart_item.objects.filter(cart=carts, is_active=True)
    #     total =0
    #     quantity =0
    #     for item in carts_item:
    #         total += item.product.price * item.quantity
    #         print(total)
    #         quantity += item.quantity

    # except ObjectDoesNotExist:
    #     pass
    values = products.objects.all()
    # subcarts = {"total": total, "quantity": quantity, "carts_item": carts_item}
    return render(request,'index.html',{'values':values})

def chair_list(request):
    values = products.objects.all()
    return render(request,'userside_productlist.html',{'values':values})

def bed_list(request):
    values = products.objects.all()
    obj = categories.objects.all()
    return render(request,'userside_productlist.html',{'values':values})
def single_product(request,id):
    values = products.objects.get(id = id )
    return render (request,'single_Product.html',{"values" : values})