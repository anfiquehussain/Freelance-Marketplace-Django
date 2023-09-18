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
                amount=int(price),
                currency='inr',
                payment_method_types=['card']
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
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    
    transaction.payment_status = True
    overview = transaction.overview
    overview_id = Overview.objects.get(pk=overview)
    transaction.save()
    order = Order.objects.create(
        buyer=request.user.userprofile, 
        service=overview_id,
        status='pending',  
        transaction=transaction,
    )
   
    context = {
        'transaction_id' : transaction_id,
    }
    return render(request, 'package_selection.html',context)


