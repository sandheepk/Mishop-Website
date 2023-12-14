from home.models import *
from . models import *
from cart.models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect, get_object_or_404

# Create your views here.
def c_id(request):
    ct_id=request.session.session_key
    if not ct_id:
        ct_id=request.session.create()
    return ct_id

@login_required(login_url='signup')
def add_cart(request,product_id):
    prod = product.objects.get(id=product_id)
    user = request.user

    try:
        ct=cartlist.objects.get(user=user)

    except cartlist.DoesNotExist:
        ct=cartlist.objects.create(cart_id=c_id(request),user=user)
        ct.save()

    try:
        c_item=cartitems.objects.get(product=prod,cart=ct)
        if c_item.quantity < c_item.product.stock:
            c_item.quantity+=1
            prod.stock -=1
            prod.save()
            
        c_item.save()
    except cartitems.DoesNotExist:
        c_items=cartitems.objects.create(product=prod,quantity=1,cart=ct)
        c_item.save()
    return redirect('cart')



def cart(request,tot=0,count=0,cart_item=None,ct_items=None):
    try:
        user = request.user

        if user.is_authenticated:
            ct = cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id') #object venda 
            ct = cartlist.objects.filter(cart_id=cart_id)
        ct_items = cartitems.objects.filter(cart__in=ct, available=True)   #active

        for i in ct_items:
            tot += (i.product.price * i.quantity)
            count += i.quantity

    except ObjectDoesNotExist:
        return HttpResponse("<script> alert('Empty Cart');window.location'/';</script>")
    print('hello')
    return render(request,'cart.html',{'ci':ct_items,'t':tot,'cn':count})


@login_required(login_url='signup') #changed
def min_cart(request,product_id):
    user=request.user
    try:
        if user.is_authenticated:
            ct_list = cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            ct_list = cartlist.objects.filter(cart_id=cart_id)

        if ct_list.exists:
            for ct in ct_list:
                prod=get_object_or_404 (product,id=product_id)
                try:
                    c_items=cartitems.objects.get(product=prod, cart=ct)
                    if c_items.quantity>1:
                        c_items.quantity-=1
                        c_items.save()
                    else:
                        c_items.delete()
                except cartitems.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass

    return redirect('cart')

@login_required(login_url='signup')
def cart_delete(request, product_id):
    user = request.user
    try:
        if user.is_authenticated:
            ct_list = cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            ct_list = cartlist.objects.filter(cart_id=cart_id)

        if ct_list.exists():
            for ct in ct_list:
                prod = get_object_or_404(product, id=product_id)
                try:
                    c_items=cartitems.objects.get(product=prod, cart=ct)
                    c_items.delete()
                except cartitems.DoesNotExist:
                    pass

    except cartlist.DoesNotExist:
        pass
    return redirect('cart')

def Checkout(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        country = request.POST['country']
        address = request.POST['address']
        towncity = request.POST['city']
        postcodezip = request.POST['pin']
        phone = request.POST['phone']
        email = request.POST['email']
        cart = cartlist.objects.filter(user=request.user).first()

        checkoutS = checkout(
            user=request.user,
            cart=cart,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            towncity=towncity,
            postcodezip=postcodezip,
            phone=phone,
            email=email
        )
        checkoutS.save()
        return redirect('bank')

    return render(request,'checkout.html')
    

def bank(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        name = request.POST.get('name')
        expiry_month = request.POST.get('expiry_month')
        expiry_year = request.POST.get('expiry_year')
        cvv = request.POST.get('cvv')

        pay = payment(
            user=request.user,
            account_number=account_number,
            name=name,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            cvv=cvv
        )
        pay.save()

        user =request.user
        ct = cartlist.objets.get(user=user, cart_id=c_id(request))
        items.objects.filters(cart=ct).delete()
        return redirect('paymenthandler')
    return render(request,'bank.html')

def success(request):
    return render(request, 'successful.html')

def pay(request):
    return render(request, 'pay.html')

