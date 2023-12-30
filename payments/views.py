from audioop import reverse
from django.shortcuts import render, get_object_or_404
from Services.models import Overview, BasicPackage, StandardPackage, PremiumPackage
from Home.models import UserProfile
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
import stripe
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from Orders.models import Order
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect
import razorpay
from django.http import HttpResponseBadRequest
stripe.api_key = settings.STRIPE_SECRET_KEY


client = razorpay.Client(auth=(settings.REZORPAY_PUBLISHABLE_KEY, settings.REZORPAY_SECRET_KEY))

@login_required
def payments(request, overview_id,username):
    overview = get_object_or_404(Overview, pk=overview_id)
    user = get_object_or_404(User, username=username)

    current_user = request.user

    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    
    additional_data = request.GET.get('additional_data')
    additional_data2 = request.GET.get('additional_data2')
    user_profile = UserProfile.objects.get(user=overview.user.id)
    basic_packages = BasicPackage.objects.filter(overview=overview)
    standard_packages = StandardPackage.objects.filter(overview=overview)
    premium_packages = PremiumPackage.objects.filter(overview=overview)

    price = None
    transaction_id = None
    package_name = ""
    package_discription = ""
    buyer_fee = 0
    seller_fee = 0
    service_fee = 0
    actual_price_fee_added = 0


    if additional_data2 == '1':
        for bp in basic_packages:

            
            
            bayer_fee = bp.Basic_price * (5/100)
            seller_fee = bp.Basic_price * (20/100)
            service_fee = buyer_fee + seller_fee

           

            price = (bp.Basic_price + bayer_fee)
            
            actual_price = bp.Basic_price
            actual_price_fee_added = bp.Basic_price + seller_fee

            
            data = { "amount": price * 100, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            API_KRY = settings.REZORPAY_PUBLISHABLE_KEY
            order_id = payment['id']
            
            package_discription = bp.Basic_description

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=order_id,
                package_name='basic_package',
                service_fee=service_fee
            )
            transaction_id = transaction.id  
    elif additional_data2 == '2':
        for bp in standard_packages:
            bayer_fee = bp.Standard_price * (5/100)
            seller_fee = bp.Standard_price * (20/100)
            service_fee = buyer_fee + seller_fee

           

            price = (bp.Standard_price + bayer_fee)
            
            actual_price = bp.Standard_price
            actual_price_fee_added = bp.Standard_price + seller_fee

            
            data = { "amount": price * 100, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            API_KRY = settings.REZORPAY_PUBLISHABLE_KEY
            order_id = payment['id']
            
            package_discription = bp.Standard_description

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=order_id,
                package_name='standard_package',
                service_fee=service_fee
            )
            transaction_id = transaction.id  

    elif additional_data2 == '3':
        for bp in premium_packages:
            bayer_fee = bp.Premium_price * (5/100)
            seller_fee = bp.Premium_price * (20/100)
            service_fee = buyer_fee + seller_fee

           

            price = (bp.Premium_price + bayer_fee)
            
            actual_price = bp.Premium_price
            actual_price_fee_added = bp.Premium_price + seller_fee

            
            data = { "amount": price * 100, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            API_KRY = settings.REZORPAY_PUBLISHABLE_KEY
            order_id = payment['id']
            
            package_discription = bp.Premium_description

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=order_id,
                package_name='premium_package',
                service_fee=service_fee
            )
            transaction_id = transaction.id 

    print(payment['id'])
        
    context = {
        'user':user,
        'overview': overview,
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'actual_price': actual_price,
        'package_price': price,
        'user_email': request.user.email,
        'user_username': request.user.username,
        'transaction_id': transaction_id,
        'package_name' : transaction.package_name,
        'package_discription':package_discription,
        'service_fee' :  service_fee,
        'actual_price_fee_added':actual_price_fee_added,
        'order_id':order_id,
        'payment' : payment,
        'API_KRY' : API_KRY,
        'order_id' : order_id,
    }
    return render(request, 'payment.html', context)

@login_required()
def success(request, transaction_id, username):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    user = get_object_or_404(User, username=username)
    current_user = request.user
    seller_user = None  
    context = {} 

    if username == current_user.username and transaction.sender == current_user:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    transaction.payment_status = True
    overview = transaction.overview
    overview_id = Overview.objects.get(pk=overview)
    transaction.save()
    
    if transaction.package_name == "basic_package":
        basic_package = BasicPackage.objects.get(overview=overview_id)
        Basic_delivery_time = basic_package.Basic_delivery_time
        delivery_date = timezone.now() + timedelta(days=Basic_delivery_time)
            
    elif transaction.package_name == "standard_package":
        standard_package = StandardPackage.objects.get(overview=overview_id)
        Standard_delivery_time = standard_package.Standard_delivery_time
        delivery_date = timezone.now() + timedelta(days=Standard_delivery_time)
            
    elif transaction.package_name == "premium_package":
        delivery_date =None
        premium_package = PremiumPackage.objects.get(overview=overview_id)
        premium_delivery_time = premium_package.Premium_delivery_time
        delivery_date = timezone.now() + timedelta(days=premium_delivery_time)

    seller_user = transaction.receiver 
    print(delivery_date)

    order = Order.objects.create(
        buyer=current_user,
        service=overview_id,
        status='pending',
        transaction=transaction,
        delivery_date=delivery_date,
        seller=seller_user,
    )

    context = {
            'transaction_id': transaction_id,
        }

    return render(request, 'package_selection.html', context)




from django.contrib import messages 

import stripe
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import razorpay

import requests

@login_required
def withdrawal(request, username):
    client = razorpay.Client(auth=(settings.REZORPAY_PUBLISHABLE_KEY, settings.REZORPAY_SECRET_KEY))
    account_data = {
    "type": "bank_account",  # Specify the type of account (e.g., "bank_account")
    "contact": {
        "name": "John Doe",  # Name of the account holder
        "email": "john.doe@example.com",  # Email address of the account holder
        "phone": "1234567890",  # Phone number of the account holder
    },
    "bank_account": {
        "account_number": "1234567890",  # Account number
        "ifsc": "ABCD1234567",  # IFSC code of the bank branch
        "beneficiary_name": "John Doe",  # Name of the account holder (again)
        },
    }
    linked_account = client.account.create(data=account_data)

    linked_accounts = client.account.create()
    return render(request, "withdrawal.html")
    







    