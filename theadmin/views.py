from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
import re
from products.models import products, categories

import users
from users.models import customuser



def signin_admins(request):
    if 'username' in request.session:
         return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate ( email = email, password = password )

        if user is not None and user.is_superuser:
            
            request.session['username']=email
            login(request,user) 
            return redirect(home_admin)
        else:
            messages.error(request,'Enter correct admin deatils')
            return redirect(signin_admins)

    return render(request,'adminlogin.html')

def home_admin(request):
    if 'username' in request.session:
        return render(request,'adminindex.html')

def data_admin(request):
    if 'username' in request.session:
        values = customuser.objects.all()
    return render(request,'user_data_table.html',{'values':values})


def signout_admin(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(signin_admins)
    
def list_products(request):
    if 'username' in request.session:
        values = products.objects.all()
    return render(request,'admin_products.html',{'values':values})

def cat_products(request):
    # if 'username' in request.session:
    values = categories.objects.all()
    
    return render(request,'cat_products.html',{'values':values})

# def delete_user(request,id):
#     del_user = User.objects.get(id=id)
#     del_user.delete()
#     return redirect(data_admin)

# def update_user(request,id):
#     obj =  User.objects.get(id = id )
#     if request.method == "POST":
#         username = request.POST.get('username')
#         name = request.POST.get('name')
#         emailid = request.POST.get('email')
#         obj.first_name = username
#         obj.name = name
#         obj.email = emailid
#         obj.save()
#         return redirect(data_admin) 
#     return render(request,'update_user.html',{'user':obj})


def delete_products(request,id):
    delete_product = products.objects.get(id=id)
    delete_product.delete()
    return redirect(list_products)
    
def update_products(request,id):
    objs =  products.objects.get(id = id )
    values = categories.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        des = request.POST.get('des')
        img =request.POST.get('img')
        price= request.POST.get('price')
        stock=request.POST.get('stock')
        cat = request.POST.get('cat')
        obj =  products.objects.get(id = id )
        obj.name = name
        obj.des = des
        obj.img = img
        obj.price = price
        obj.stock = stock
        obj.cat   = cat
        obj.save()
        return redirect(list_products) 
    return render(request,'update_products.html',{'products':objs,'values':values})

def add_products(request):
    values = categories.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        des = request.POST.get('des')
        img= request.POST.get('img')
        price= request.POST.get('price')
        stock=request.POST.get('stock')
        cat = request.POST.get('cat')
        product =products(name = name, des = des, img = img, price = price, stock = stock)
        product.cats  = categories.objects.get(id=cat)
        product.save()
        return redirect(list_products) 
    return render(request,'add_products.html',{'values':values})


def add_category(request):
    
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        des = request.POST.get('des')
        stock=request.POST.get('stock')
        category =categories(category_name = category_name, des = des, stock = stock)
        category.save()
        return redirect(cat_products) 
    return render(request,'add_category.html')

def delete_category(request,id):
    del_category = categories.objects.get(id=id)
    del_category.delete()
    return redirect(cat_products)

def update_category(request,id):
    
    obj = categories.objects.get(id=id)
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        des = request.POST.get('des')
        stock=request.POST.get('stock')
       
        values =  categories.objects.get(id = id )
        values.name = category_name
        values.des = des
        values.stock = stock
        values.save()
        return redirect(cat_products) 
    return render(request,'update_category.html',{'categories':obj})
    
def block_user(request,id):
    user = customuser.objects.get(id = id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(data_admin)