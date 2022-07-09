from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
import re

from products.models import products


# Create your views here.
def products_list(request):
    # if 'username' in request.session:
    values = products.objects.all()
    return render(request,'index.html',{'values':values})