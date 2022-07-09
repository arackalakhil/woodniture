import numbers
import optparse
import random
from urllib.request import Request
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.test import Client
from .models import customuser
from django.views.decorators.cache import cache_control
import re
from twilio.rest import Client

from products.views import products_list


# def index(request):
#     return render(request,'index.html')
def signin(request):
    if 'username' in request.session:
        return redirect(products_list) 
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate( email = email, password = password )

        if user is not None :
            request.session['username'] = email   
            login(request,user) 

            return redirect(products_list)
        else:
            messages.success(request,'Enter correct deatils')
            return redirect(signin)
    return render(request,'login-register.html')
    
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if username=="":
                messages.error(request,"username is empty")
                return render(request,'login-register.html')
            elif len(username)<2:
                messages.error(request,"username is too short")
                return render(request,'login-register.html')
            elif not username.isalpha():
                messages.error(request,"username must contain alphabets")
                return render(request,'login-register.html')
            elif not username.isidentifier():
                messages.error(request,"username start must start with alphabets")
                return render(request,'login-register.html')
            elif customuser.objects.filter(username = username):
                messages.error(request,"username exits")
                return render(request,'login-register.html')
            elif email=="":
                messages.error(request,"email field is empty")
                return render(request,'login-register.html')
            elif len(email)<2:
                messages.error(request,"email is too short")
                return render(request,'login-register.html')

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')

            elif customuser.objects.filter(email=email):
                messages.error(request,"email already exist try another")
                return render(request,'login-register.html')
                
            else:
                user1 =customuser.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password1,email=email,phone_number = phone_number)
                user1.save()
                return redirect(signup)
        else:
            messages.success(request,"password does not match")
            return render(request,'login-register.html')
    else:
        return render(request,'login-register.html') 
        
    return render(request,'login-register.html') 
def signout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect('home')


# -------------------------------------------#OTP----------------------------------------------------------
def numb_login(request): 
    if request.user.is_authenticated:
        return redirect(products_list)
    if request.method == 'POST':
        mobile = '8138873820'
        phone_number  = request.POST.get('phone_number')
        # global numb
        # numb = phone_number
        # # if customuser.objects.filter(phone_number=phone_number):
        # print(phone_number )
        if mobile == phone_number:   
            # SID Twilio
            account_sid ="AC18894f6eab9a08b51d59cda6416a4f08" 
            #auth Twilio
            auth_token ="53ce1b0e50ad8d173299aa4ef67db1c9"

            client = Client(account_sid, auth_token)
            global opt
            opt = str(random.randint(1000,9999))
            message =client.messages.create(
                # to = "int((str(+91))+(str(phone_number)))",
                to = "+918138873820",
                from_ ="+19705089552",
                body = "greeting from woodniture your OTP is " + opt )

            # return render(request,'otp.html')
            return redirect(otp) 
        else:
            messages.info(request,"invalid number")
            return redirect (numb_login)
    
    return render (request,'phone_login.html')

def otp (request):
    if request.method =="POST":
        user =customuser.objects.get(phone_number = 8138873820)
        otpvalue = request.POST.get('otp')
        if otpvalue == opt:
            login(request,user)
            messages.success(request,'logged in')
            return redirect(products_list)
        else:
            messages.error(request,'incorrect OTP')
            return render(otp)
    else:
        return render(request,'otp.html')