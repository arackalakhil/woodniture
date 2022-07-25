from ast import Global
import json
from django.shortcuts import redirect, render
from carts.models import cart, cart_item
from carts.views import cart_id, cart_view
from order.models import order, order_product, payment
from products.models import products
from products.views import index_page
from users.models import address
from datetime import date
import datetime
from users.views import user_profile
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def invoice(request, carts_item=0):
   if request.user.is_authenticated:
      if request.method  == "POST":
         global address_id
         address_id=request.POST.get("address_id")
         global addresss
         addresss=address.objects.get(id = address_id)
         carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
         if not carts_item:
            return render (request,"index.html")

      total=0
      quantity=0
      
      for item in carts_item:
         total += item.product.price * item.quantity
         quantity += item.quantity
   else:
      return redirect()
   client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
   global payments
   payments =client.order.create({"amount":int(total)*100, "currency" : "INR", "payment_capture":1})
   payment_id = payments["id"]
   values ={"addresss":addresss,"carts_item":carts_item,"total":total,"quantity":quantity,"payments":payments,"payment_id":payment_id}
   
   return render (request,"invoice.html",values)



def order_cancel(request,id):
   user =request.user
   if request.user.is_authenticated:
      orders = order.objects.get(id=id)
      orders.status= "cancelled"
      orders.save()
      return redirect(user_profile)

def cod(request):
   user = request.user
   if request.user.is_authenticated:
      carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
      total=0
      quantity=0
      for item in carts_item:
         total += item.product.price * item.quantity
         quantity += item.quantity
      cart_items  = cart_item.objects.filter(user = request.user, is_active = True)
      cart_itemcount = cart_items.count()
      if cart_itemcount <= 0 :
         return render(request,'index.html')
      order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
      dates =date.today()
      payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
      amount = total
      payment_method="cashondelivery"
      
      payments = payment(user=user,payment_id=payment_id,payment_method=payment_method,amount=amount,date=dates)
      payments.save()
      orders = order(user=user,order_id=order_id_generated,address=addresss,total=total,date=dates,payment=payments)
      orders.save()
      carts_item = cart_item.objects.filter(
                 user=request.user, is_active=True
             ).order_by("id")
      for x in carts_item:
         orderproduct = order_product(order=orders,user=user,quantity=quantity)
         orderproduct.product=x.product
         orderproduct.product_price=x.product.price
         orderproduct.save() 
      return redirect(order_conforme)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def order_conforme(request):
   if request.user.is_authenticated:
     
        
      carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
      
      total=0
      quantity=0
      
      for item in carts_item:
         total += item.product.price * item.quantity
         quantity += item.quantity
      carts_item.delete()
   else:
      return redirect()
   dates =date.today()
   
   order_products=order_product.objects.filter(user=request.user)
   print(dates)
   values ={"addresss":addresss,"order_product":order_products,"total":total,"quantity":quantity,"dates":dates}

   return render (request,"order_conforme.html",values)
   

#---------------------------------------------------------------------------------------\razopay/---------------------------------------------------------------------------------------------------



# authorize razorpay client with API Keys.
# def razorpay(request):
#    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#    payment = client

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def razorpay_sucess(request):
   # order_id = request.GET.get("order_id")
   user =request.user
   carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
   total=0
   quantity=0
   for item in carts_item:
      total += item.product.price * item.quantity
      quantity += item.quantity
   order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
   dates =date.today()
   amount = total
   payment_method="razorpay"
   payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
   payments = payment(user=user,payment_id=payment_id,payment_method=payment_method,amount=amount,date=dates)
   payments.save()
   orders = order(user=user,order_id=order_id_generated,address=addresss,total=total,date=dates,payment=payments)
   orders.save()
   carts_item.delete()
   return HttpResponse ("Payment success thanks for the order")












# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# def paypal(request):
#     total = 0
#     quantity = 0
#     cart_items =None
#     tax = 0
#     grand_total =0
#     if request.user.is_authenticated:
#         try:

#             details = address.objects.get(id = address_id ) #passed that spesific address in the details variable
#             order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
#             user =  request.user
#             cart_items  = cart_item.objects.filter(user = request.user, is_active = True)
#             cart_itemcount = cart_items.count()
#             if cart_itemcount <= 0 :
#                 return render(request,'nothing.html')
#             for carts_item in cart_items:
#                 total += (int(carts_item.product.price) * int(carts_item.quantity))
                
#             oder = order(user=user,address=details ,total = total,order_id =order_id_generated)
#             oder.save()

            
#             cart_items  = cart_item.objects.filter(user = request.user, is_active = True)

            
            

#         except ObjectDoesNotExist: 
#             pass #just ignore

        
        

#     else:
#         return redirect(cart_view)
        
#     orders = order.objects.get(order_id = order_id_generated)
#     Orderproduct = order_product.objects.filter(order=orders)
#     for cart_items in Orderproduct:
#         total += (cart_items.price * cart_items.quantity)
#         quantity += cart_item.quantity
#     # tax = (2*total)/100
#     tax = 0
#     grand_total = total + tax
            
#     context = {
#     'cart_items':cart_items,
#     'order' :order,
#     "order_id_generated" :order_id_generated,
#     'total':total,
#     'quantity':quantity,
#     'Orderproduct':Orderproduct,
#     'tax':tax,
#     'grand_total':grand_total,
#     'details':details,
        
#         }
#     return render(request, 'paypal.html',context)
    



# def payments(request):
#     body = json.loads(request.body)
#     orders = order.objects.get(orderid = body['orderID'] )
#     payments = payment(

#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         amount_paid = orders.ordertotal,
#         status = body['status'],
#     )
#     payments.save()
#     print(body)
#     orders.payment = payment
#     orders.is_ordered =True
#     orders.save()
#     #MOVE THE CART ITEMS TO ORDER PRODUCTS TABLE
#     cart_items  = cart_item.objects.filter(user = request.user, is_active = True)
#     for x in cart_items:
                
#         Orderproduct = order_product(order=order)
#         Orderproduct.product = x.product
#         Orderproduct.quantity = x.quantity
#         Orderproduct.product_price = x.product.price
#         Orderproduct.save()
#     #REDUCE THE QUANTITY OF STOCK

#         product = product.objects.get(id = x.product.id)
#         product.stock -= x.quantity
#         product.save()
#     #CLEAR CART
#     for x in cart_items:
#         x.delete()

#     #SEND ORDER RECIEVED EMAIL TO CUSTOMER




#     #SEND ORDER NUMBER AND TRANSACTION ID BACK TO SEND DATA METHOD VIA JASON RESPONDS
#     data = {
#         "orderID":order.orderid,
#         "transID":payment.payment_id,
#     }


#     return JsonResponse(data)




# def order_complete(request):
#     total = 0
#     quantity = 0
#     cart_items =None
#     tax = 0
#     grand_total =0
#     order_number    = request.GET.get("orderID")
#     transID         = request.GET.get("transID")
#     print(order_number)

#     try:
#         dates =date.today()   
#         details = address.objects.get(id = address_id )
#         orders = order.objects.get(orderid = order_number)
#         ordered_products = order_product.objects.filter(order = orders)
#         Orderproduct = order_product.objects.filter(order=orders)
#         for cart_item in Orderproduct:
#             total += (cart_item.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         # tax = (2*total)/100
#         tax = 0
#         grand_total = total + tax

#         context = {
#             "order":orders,
#             "ordered_products":ordered_products,
#             "orderID":orders.orderid,
#             "details":details,
#             "transID":transID,
#             "dates":dates,
#             "grand_total":grand_total,
#             "tax":tax,
#             "total":total
#         }
#         return render(request,"order_complete.html",context)

#     except (payment.DoesNotExist,order.DoesNotExist):
#         return redirect("userhome")


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def paypal(request):
    if request.user.is_authenticated:
        try:
        
            carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
            if not carts_item:
                return render (request,"index.html")
            cart_itemcount = carts_item.count()
            if cart_itemcount <= 0 :
                return render(request,'index.html')
            total=0
            quantity=0
      
            for item in carts_item:
                total += item.product.price * item.quantity
                quantity += item.quantity
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            dates =date.today()
            orders = order(user=request.user,address=addresss ,total = total,order_id =order_id_generated,date=dates)
            order_products = order_product.objects.filter(order=orders)
            orders.save()
        except ObjectDoesNotExist:
               pass #just ignore
    else:
        return redirect(cart_view)

   
    values ={"carts_item":carts_item,"total":total,"quantity":quantity,"orders":orders,"order_products":order_products}
   
    return render (request,"paypal.html",values)

# ///////////////////////////////////////////////////////////////////////////////////


def payments(request):
    body = json.loads(request.body)
    print("dhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    print(body['orderID'])

    orders = order.objects.get( order_id = body['orderID'] )
    payments = payment(

        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount = orders.total,
        status = body['status'],
    )
    payments.save()
    print(body)
    print(orders.order_id)
    # print(orders.payments.payment_id)

    orders.payment = payments
    orders.is_ordered =True
    orders.save()
    print(orders)       

    print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")

    #MOVE THE CART ITEMS TO ORDER PRODUCTS TABLE
    cart_items  = cart_item.objects.filter(user = request.user)
    print(cart_items)
    for x in cart_items:
        print(orders)       
        Orderproduct = order_product(order=orders)
        print(Orderproduct)
        print("dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")

        Orderproduct.product = x.product
        Orderproduct.quantity = x.quantity
        Orderproduct.product_price = x.product.price
        Orderproduct.save()
    #REDUCE THE QUANTITY OF STOCK

        product = products.objects.get(id = x.product.id)
        product.stock -= x.quantity
        product.save()
    #CLEAR CART

    for x in cart_items:
        x.delete()

    #SEND ORDER RECIEVED EMAIL TO CUSTOMER

    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


    #SEND ORDER NUMBER AND TRANSACTION ID BACK TO SEND DATA METHOD VIA JASON RESPONDS
    data = {
        "orderID":orders.order_id,
        "transID":payments.payment_id,
    }

    print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
    return JsonResponse(data)


    
def order_complete(request):
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    order_number    = request.GET.get("orderID")
    transID         = request.GET.get("transID")
    print(order_number)

    try:
        dates =date.today()   
        details = address.objects.get(id = address_id )
        orders = order.objects.get(order_id = order_number)
        ordered_products = order_product.objects.filter(order = orders)
        Orderproduct = order_product.objects.filter(order=orders)
        for cart_item in Orderproduct:
            total += (cart_item.product_price * cart_item.quantity)
            quantity += cart_item.quantity
        # tax = (2*total)/100
        tax = 0
        grand_total = total + tax
        print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
        context = {
            "order":orders,
            "ordered_products":ordered_products,
            "orderID":orders.order_id,
            "details":details,
            "transID":transID,
            "dates":dates,
            "total":total,
            "tax":tax,
            "total":total
        }
        return render(request,"index.html" )

    except (payment.DoesNotExist,order.DoesNotExist):
        return redirect("userhome")


