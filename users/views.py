import code
from multiprocessing import context
import numbers
import optparse
import random
from urllib.request import Request
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.test import Client
from carts.models import cart, cart_item

from carts.views import cart_id, checkout
from order.models import order, order_product
from .models import address, customuser
from django.views.decorators.cache import cache_control
import re
from twilio.rest import Client
from datetime import date
from products.views import index_page


# def index(request):
#     return render(request,'index.html')
def signin(request):
    if "username" in request.session:
        return redirect(index_page)
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)
    
        if user is not None:
            try:
                carts = cart.objects.get(cart_id=cart_id(request))
               # carts_item  = cart_item.objects.filter(cart=carts)
                
                # if carts_item :
                carts_item = cart_item.objects.filter(cart = carts) 
                users_item = cart_item.objects.filter(user = user)
                
                for carts_item in carts_item:#if multiple item in cart 
                    a=0
                    for users_item in users_item:#check each items in users_items 
                        if  carts_item.product == users_item.product:#if product in both carts_items from sessions id and users  product from cart_item(models) matches
                            users_item.quantity += carts_item.quantity#product items quantity will be sum of .....
                            carts_item.delete()#delete the carts_item  
                            users_item.save()
                            a=1
                            break
                        if a==0:# to add if different product to user cart 
                            carts_item.user=user
                            carts_item.save()
            except:
                pass    
            login(request, user)
            request.session["username"] = email
            return redirect(index_page)
        else:
            messages.success(request, "Enter correct deatils")
            return redirect(signin)
    return render(request, "login-register.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            if username == "":
                messages.error(request, "username is empty")
                return render(request, "user-register.html.html")
            elif len(username) < 2:
                messages.error(request, "username is too short")
                return render(request, "user-register.html")
            elif not username.isalpha():
                messages.error(request, "username must contain alphabets")
                return render(request, "user-register.html")
            elif not username.isidentifier():
                messages.error(request, "username start must start with alphabets")
                return render(request, "user-register.html")
            elif customuser.objects.filter(username=username):
                messages.error(request, "username exits")
                return render(request, "user-register.html")
            elif email == "":
                messages.error(request, "email field is empty")
                return render(request, "user-register.html")
            elif len(email) < 2:
                messages.error(request, "email is too short")
                return render(request, "user-register.html")

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')

            elif customuser.objects.filter(email=email):
                messages.error(request, "email already exist try another")
                return render(request, "user-register.html")

            else:
                user1 = customuser.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password1,
                    email=email,
                    phone_number=phone_number,
                )
                user1.save()
                return redirect(signin)
        else:
            messages.success(request, "password does not match")
            return render(request, "user-register.html")
    else:
        return render(request, "user-register.html")

    return render(request, "user-register.html")


def signout(request):
    if "username" in request.session:
        request.session.flush()
    logout(request)
    return redirect("home")


# -------------------------------------------#OTP----------------------------------------------------------
def numb_login(request):
    if request.user.is_authenticated:
        return redirect(index_page)
    if request.method == "POST":
        mobile = "8138873820"
        phone_number = request.POST.get("phone_number")
        # global numb
        # numb = phone_number
        # # if customuser.objects.filter(phone_number=phone_number):
        # print(phone_number )
        if mobile == phone_number:
            # SID Twilio
            account_sid = "AC18894f6eab9a08b51d59cda6416a4f08"
            # auth Twilio
            auth_token = "53ce1b0e50ad8d173299aa4ef67db1c9"

            client = Client(account_sid, auth_token)
            global opt
            opt = str(random.randint(1000, 9999))
            message = client.messages.create(
                # to = "int((str(+91))+(str(phone_number)))",
                to="+918138873820",
                from_="+19705089552",
                body="greeting from woodniture your OTP is " + opt,
            )

            # return render(request,'otp.html')
            return redirect(otp)
        else:
            messages.info(request, "invalid number")
            return redirect(numb_login)

    return render(request, "phone_login.html")


def otp(request):
    if request.method == "POST":
        user = customuser.objects.get(phone_number=8138873820)
        otpvalue = request.POST.get("otp")
        if otpvalue == opt:
            login(request, user)
            messages.success(request, "logged in")
            return redirect(index_page)
        else:
            messages.error(request, "incorrect OTP")
            return render(otp)
    else:
        return render(request, "otp.html")
        

# -------------------------------------------#OTP----------------------------------------------------------
def add_address(request):
    

        if request.method == "POST":
            print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
            name = request.POST["name"]
            email = request.POST["email"]
            phone_number = request.POST["phone_number"]
            user_address = request.POST["user_address"]
            country = request.POST["country"]
            town = request.POST["town"]
            state = request.POST["state"]
            zip_code = request.POST["zip_code"]

            # if name == "":
            #     messages.error(request, "username is empty")
            #     return render(request, "add_address.html")
                

            # elif len(name) < 2:
            #     messages.error(request, "username is too short")
            #     return render(request, "add_address.html")


            # elif not name.isalpha():
            #     messages.error(request, "username must contain alphabets")
            #     return render(request, "add_address.html")


            # elif not name.isidentifier():
            #     messages.error(request, "username start must start with alphabets")
            #     return render(request, "add_address.html")
            # elif address.objects.filter(name=name):
            #     messages.error(request, "username exits")

            #     return render(request, "add_address.html")
            # elif email == "":
            #     messages.error(request, "email field is empty")
            #     return render(request, "add_address.html")
            # elif len(email) < 2:
            #     messages.error(request, "email is too short")
            #     return render(request, "add_address.html")

            # # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            # #     messages.error(request,"email should contain @,.")
            # #     return render(request,'signup.html')

            # elif address.objects.filter(email=email):
            #     messages.error(request, "email already exist try another")
            #     return render(request, "add_address.html")

           
            address_data = address(
                    name=name,
                    email=email,
                    phone=phone_number,
                    address_details=user_address,
                    pincode=zip_code,
                    town=town,
                    state=state,
                    country=country,
                    user=request.user,
                )
            address_data.save()

            # return render(request, "checkout.html")

            return redirect(checkout)

        
        return render(request, "add_address.html")


def user_profile(request):
    
    if request.user.is_authenticated:
        user = request.user
        
        orders = order.objects.filter(user=user)


        return render(request,"user_profile.html",{"orders":orders})  
    else:
        return redirect(index_page)

