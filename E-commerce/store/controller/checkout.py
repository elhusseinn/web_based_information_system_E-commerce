




from os import name
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from numpy import product
from django.contrib.auth.models import User

from store.models import Cart, Order, OrderItem, Product, Profile


@login_required(login_url='loginpage')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty
    #Total Number of orders for user
    #cartitem --> products inside the cart (i.e count orderitems for single product in the cart)
    userprofile=Profile.objects.filter(user=request.user).first()
    productnames = OrderItem.objects.raw('SELECT * FROM store_product JOIN store_orderitem ON store_product.id=store_orderitem.product_id JOIN store_order ON store_orderitem.order_id = store_order.id WHERE store_order.user_id = %s ',[request.user.id])
    productprices = Order.objects.raw('SELECT * FROM  store_order  WHERE store_order.user_id = %s ',[request.user.id])
    productnamesarray = []
    productpricesarray = []
    for x in productnames:
        if(x.name in productnamesarray):
            continue
        else:
            productnamesarray.append(x.name)
    for y in productprices:
        productpricesarray.append(y.total_price)
    
    context = {'cartitems': cartitems, 'total_price': total_price ,'userprofile':userprofile, 'productnames': productnames, 'productprices':productprices,'productpricesarray':productpricesarray,'productnamesarray' :productnamesarray}
    return render(request, "store/checkout.html", context)

@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':

        currentuser=User.objects.filter(id=request.user.id).first()
        if not currentuser.first_name :
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name =request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
           userprofile=Profile()
           userprofile.user = request.user
           userprofile.phone = request.POST.get('phone')
           userprofile.address = request.POST.get('address')
           userprofile.city = request.POST.get('city')
           userprofile.state = request.POST.get('state')
           userprofile.country = request.POST.get('country')
           userprofile.pincode = request.POST.get('pincode')
           userprofile.save()
                

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price+item.product.selling_price*item.product_qty
        neworder.total_price = cart_total_price

        trackno = 'ecomerc'+str(random.randint(1111111, 9999999))

        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'ecomerc'+str(random.randint(1111111, 9999999))

        neworder.tracking_no = trackno
        neworder.save()
        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )
        
         # to reduce the product quantity it from available stock
            orderproduct=Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity=orderproduct.quantity - item.product_qty
            orderproduct.save()
        
        Cart.objects.filter(user=request.user).delete()
        
   
        payMode=request.POST.get('payment_mode')
        if(payMode=="Paid by PayPal"):
          return JsonResponse({'status':"Your order has been placed successfully"})
        else:     
         messages.success(request,"Your order has been placed successfully")
            
    return redirect('/')






def orders(request):
    return HttpResponse("My orders Page")