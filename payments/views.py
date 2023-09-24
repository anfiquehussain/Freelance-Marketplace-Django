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


# import razorpay

# client = razorpay.Client(auth=(settings.REZORPAY_PUBLISHABLE_KEY, settings.REZORPAY_SECRET_KEY))

stripe.api_key = settings.STRIPE_SECRET_KEY



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
            # data = { "amount": bp.Basic_price * 100, "currency": "INR", "receipt": "order_rcptid_11" }
            
            bayer_fee = bp.Basic_price * (5/100)
            seller_fee = bp.Basic_price * (20/100)
            service_fee = buyer_fee + seller_fee
            
            price = (bp.Basic_price + seller_fee) * 100
            actual_price = bp.Basic_price
            actual_price_fee_added = bp.Basic_price + seller_fee

            
            payment_intent = stripe.PaymentIntent.create(
                amount=int(actual_price_fee_added * 100),
                currency='inr',
                payment_method_types=['card'],
                description=bp.Basic_description,
                receipt_email=request.user.email,
                
                 
                metadata={
                    'overview_id': overview.id,
                    'package_name': 'basic_package',
                }
            )
            payment_id = payment_intent.id
            
            
            
            package_discription = bp.Basic_description

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=payment_id,
                package_name='basic_package',
                service_fee=service_fee
            )
            transaction_id = transaction.id  
    elif additional_data2 == '2':
        for sp in standard_packages:

            bayer_fee = sp.Standard_price * (5/100)
            seller_fee = sp.Standard_price * (20/100)
            service_fee = buyer_fee + seller_fee

            price = (sp.Standard_price + seller_fee) * 100
            actual_price = sp.Standard_price
            actual_price_fee_added = sp.Standard_price + seller_fee

            payment_intent = stripe.PaymentIntent.create(
                amount=int(price),
                currency='inr',
                payment_method_types=['card']
            )
            payment_id = payment_intent.id
            package_discription = sp.Standard_description

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=payment_id,
                package_name='standard_package',
                service_fee=service_fee
            )
            transaction_id = transaction.id
    elif additional_data2 == '3':
        for pp in premium_packages:

            bayer_fee = pp.Premium_price * (5/100)
            seller_fee = pp.Premium_price * (20/100)
            service_fee = buyer_fee + seller_fee

            price = (pp.Premium_price + seller_fee) * 100
            actual_price = pp.Premium_price
            actual_price_fee_added = pp.Premium_price + seller_fee

            print(actual_price_fee_added)
            payment_intent = stripe.PaymentIntent.create(
                amount=int(price),
                currency='inr',
                payment_method_types=['card']
            )
            payment_id = payment_intent.id
            package_discription = pp.Premium_description

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=payment_id,
                package_name='premium_package',
                service_fee=service_fee
            )
            transaction_id = transaction.id
            
            

    # payment = client.order.create(data=data)
    # API_KRY = settings.REZORPAY_PUBLISHABLE_KEY
    # order_id = payment['id']

   
    print(package_discription)
        
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

        # 'payment' : payment,
        # 'API_KRY' : API_KRY,
        # 'order_id' : order_id,
    }
    return render(request, 'payment.html', context)

@login_required()
def success(request, transaction_id,username):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    user = get_object_or_404(User, username=username)
    
    

    current_user = request.user

    if username == current_user.username and transaction.sender == current_user:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
        
    payment_intent = stripe.PaymentIntent.retrieve(transaction.payment_id)
    

    
    try:
        # Retrieve the PaymentIntent
        payment_intent = stripe.PaymentIntent.retrieve(transaction.payment_id)
        

        # Replace 'tok_12345' with the actual token generated on the client-side
        stripe_token = request.POST.get('stripeToken')
        
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "token": stripe_token
            }
        )

        # The payment method ID is available as payment_method.id
        actual_payment_method_id = payment_method.id
        stripe_url_webhook = None
        if payment_intent.status == 'requires_payment_method':
            # Modify the PaymentIntent with the new payment method
            payment_intent = stripe.PaymentIntent.modify(
                payment_intent.id,
                payment_method=actual_payment_method_id
            )

            
            # Confirm the PaymentIntent
            payment_intent.confirm()
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
                delivery_date = timezone.now() + timedelta(Standard_delivery_time)
            
            elif transaction.package_name == "premium_package":
                premium_package = PremiumPackage.objects.get(overview=overview_id)
                Premium_delivery_time = premium_package.Premium_delivery_time
                delivery_date = timezone.now() + timedelta(Premium_delivery_time)

            seller_user = transaction.receiver 
            
            order = Order.objects.create(
                buyer=request.user.userprofile,
                service=overview_id,
                status='pending',
                transaction=transaction,
                delivery_date=delivery_date,
                seller=seller_user,
            )


            print(f"PaymentIntent confirmed. Status: {payment_intent.status}")
        else:
            print(f"PaymentIntent status: {payment_intent.status}")
        

        if payment_intent.status == 'requires_action' and 'next_action' in payment_intent:
            next_action = payment_intent['next_action']

           
            if next_action.get('type') == 'use_stripe_sdk':

                source = next_action['use_stripe_sdk']['source']
                stripe_js_url = next_action['use_stripe_sdk']['stripe_js']
               
                stripe_url_webhook = stripe_js_url
                

            # return redirect(stripe_js_url)

    except stripe.error.StripeError as e:
        # Handle Stripe API errors
        print(f"Stripe error: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
    


   
    context = {
        'transaction_id' : transaction_id,
        'stripe_url_webhook':stripe_url_webhook,
        
    }
    return render(request, 'package_selection.html',context)


