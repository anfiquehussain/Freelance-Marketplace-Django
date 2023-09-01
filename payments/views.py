from django.shortcuts import render, get_object_or_404
from Services.models import Overview, BasicPackage, StandardPackage, PremiumPackage
from Home.models import UserProfile
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
import stripe
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# import razorpay

# client = razorpay.Client(auth=(settings.REZORPAY_PUBLISHABLE_KEY, settings.REZORPAY_SECRET_KEY))

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payments(request, overview_id):
    overview = get_object_or_404(Overview, pk=overview_id)
    additional_data = request.GET.get('additional_data')
    additional_data2 = request.GET.get('additional_data2')
    user_profile = UserProfile.objects.get(user=overview.user.id)
    basic_packages = BasicPackage.objects.filter(overview=overview)
    standard_packages = StandardPackage.objects.filter(overview=overview)
    premium_packages = PremiumPackage.objects.filter(overview=overview)

    price = None
    transaction_id = None

    if additional_data2 == '1':
        for bp in basic_packages:
            # data = { "amount": bp.Basic_price * 100, "currency": "INR", "receipt": "order_rcptid_11" }
            price = bp.Basic_price * 100
            actual_price = bp.Basic_price

            payment_intent = stripe.PaymentIntent.create(
                amount=price,
                currency='inr',
            )
            payment_id = payment_intent.id

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=payment_id,
                package_name='basic_package'
            )
            transaction_id = transaction.id  
    elif additional_data2 == '2':
        for sp in standard_packages:
            price = sp.Standard_price * 100
            actual_price = sp.Standard_price

            payment_intent = stripe.PaymentIntent.create(
                amount=price,
                currency='inr',
            )
            payment_id = payment_intent.id

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=payment_id,
                package_name='standard_package'
            )
            transaction_id = transaction.id
    elif additional_data2 == '3':
        for pp in premium_packages:
            price = pp.Premium_price * 100  
            actual_price = pp.Premium_price

            payment_intent = stripe.PaymentIntent.create(
                amount=price,
                currency='inr',
            )
            payment_id = payment_intent.id

            transaction = Transaction.objects.create(
                overview=overview.id,
                sender=request.user,
                receiver=user_profile.user,
                amount=actual_price,
                payment_id=payment_id,
                package_name='premium_package'
            )
            transaction_id = transaction.id

    # payment = client.order.create(data=data)
    # API_KRY = settings.REZORPAY_PUBLISHABLE_KEY
    # order_id = payment['id']
        
    context = {
        'overview': overview,
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'actual_price': actual_price,
        'package_price': price,
        'user_email': request.user.email,
        'user_username': request.user.username,
        'transaction_id': transaction_id,  # Include the transaction id in the context

        # 'payment' : payment,
        # 'API_KRY' : API_KRY,
        # 'order_id' : order_id,


    }
    return render(request, 'payment.html', context)

@login_required()
def success(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.payment_status = True
    transaction.save()
    context = {
        'transaction_id' : transaction_id
    }
    return render(request, 'package_selection.html',context)

