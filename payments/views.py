# Import necessary decorators and modules from Django
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from datetime import datetime 
import razorpay
# Import models from the current app and other related apps
from .models import Upi_id, Bank, SellerAccountBalance, PaymentWithdrawal, PaymentMethod, Transaction, Refund_details
from Services.models import Overview, BasicPackage, StandardPackage, PremiumPackage
from Home.models import UserProfile
from Orders.models import Order
# Configure Razorpay client with API keys from Django settings
client = razorpay.Client(
    auth=(settings.REZORPAY_PUBLISHABLE_KEY, settings.REZORPAY_SECRET_KEY))

# View function for handling payments
@login_required
def payments(request, overview_id, username):
    # Retrieve overview and user objects from the database
    overview = get_object_or_404(Overview, pk=overview_id)
    user = get_object_or_404(User, username=username)

# Retrieve the current user
    current_user = request.user
# Check if the requested username matches the current user's username
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

# Retrieve additional data from the request URL
    additional_data = request.GET.get('additional_data')
    additional_data2 = request.GET.get('additional_data2')
    # Retrieve user profile and packages associated with the overview
    user_profile = UserProfile.objects.get(user=overview.user.id)
    basic_packages = BasicPackage.objects.filter(overview=overview)
    standard_packages = StandardPackage.objects.filter(overview=overview)
    premium_packages = PremiumPackage.objects.filter(overview=overview)

# Initialize variables for pricing and transaction details
    price = 0
    transaction_id = None
    package_name = ""
    package_discription = ""
    buyer_fee = 0
    seller_fee = 0
    service_fee = 0
    actual_price_fee_added = 0

# Handle different additional data scenarios
    if additional_data2 == '1':
        for bp in basic_packages:

         # Calculate fees and price for basic package
            buyer_fee = bp.Basic_price * (5/100)
            seller_fee = bp.Basic_price * (10/100)
            service_fee = buyer_fee + seller_fee

            price = (bp.Basic_price + buyer_fee)
            actual_price = bp.Basic_price
            actual_price_fee_added = price

            # Create Razorpay order for payment
            data = {"amount": price * 100, "currency": "INR",
                    "receipt": "order_rcptid_11"}
            payment = client.order.create(data=data)
            API_KRY = settings.REZORPAY_PUBLISHABLE_KEY
            order_id = payment['id']

            package_discription = bp.Basic_description
            # Create transaction record
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
            buyer_fee = bp.Standard_price * (5/100)
            seller_fee = bp.Standard_price * (10/100)

            service_fee = buyer_fee + seller_fee

            price = (bp.Standard_price + buyer_fee)

            actual_price = bp.Standard_price
            actual_price_fee_added = bp.Standard_price + buyer_fee

            data = {"amount": price * 100, "currency": "INR",
                    "receipt": "order_rcptid_11"}
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
            buyer_fee = bp.Premium_price * (5/100)
            seller_fee = bp.Premium_price * (10/100)
            service_fee = buyer_fee + seller_fee

            price = (bp.Premium_price + buyer_fee)

            actual_price = bp.Premium_price
            actual_price_fee_added = bp.Premium_price + buyer_fee

            data = {"amount": price * 100, "currency": "INR",
                    "receipt": "order_rcptid_11"}
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
        'user': user,
        'overview': overview,
        'actual_price': actual_price,
        'package_price': price,
        'user_email': request.user.email,
        'user_username': request.user.username,
        'transaction_id': transaction_id,
        'package_name': transaction.package_name,
        'package_discription': package_discription,
        'service_fee':  service_fee,
        'buyer_fee': buyer_fee,
        'actual_price_fee_added': actual_price_fee_added,
        'order_id': order_id,
        'payment': payment,
        'API_KRY': API_KRY,
        'order_id': order_id,
        'price': price,
    }
    return render(request, 'payment.html', context)


# Decorator to ensure that the user is logged in to access this view
@login_required()
def success(request, transaction_id, username):
    # Retrieving the Transaction and User objects based on provided IDs
    transaction = get_object_or_404(Transaction, id=transaction_id)
    user = get_object_or_404(User, username=username)
    current_user = request.user
    seller_user = None
    context = {}
    # Checking if the logged-in user matches the provided username and is the sender of the transaction
    if username == current_user.username and transaction.sender == current_user:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    transaction.payment_status = True
    overview = transaction.overview
    overview_id = Overview.objects.get(pk=overview)
    transaction.save()

    # Determining the delivery date based on the package name in the transaction
    if transaction.package_name == "basic_package":
        basic_package = BasicPackage.objects.get(overview=overview_id)
        Basic_delivery_time = basic_package.Basic_delivery_time
        delivery_date = timezone.now() + timedelta(days=Basic_delivery_time)
    elif transaction.package_name == "standard_package":
        standard_package = StandardPackage.objects.get(overview=overview_id)
        Standard_delivery_time = standard_package.Standard_delivery_time
        delivery_date = timezone.now() + timedelta(days=Standard_delivery_time)

    elif transaction.package_name == "premium_package":
        delivery_date = None
        premium_package = PremiumPackage.objects.get(overview=overview_id)
        premium_delivery_time = premium_package.Premium_delivery_time
        delivery_date = timezone.now() + timedelta(days=premium_delivery_time)
    # Getting the seller user from the transaction
    seller_user = transaction.receiver
    print(delivery_date)
    # Creating an Order object with the provided details
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


@login_required()
def withdrawal(request, username):

    user = get_object_or_404(User, username=username)
    current_user = request.user
    account_balance = SellerAccountBalance.objects.filter(user=user)
    withdrawal_exist = PaymentWithdrawal.objects.filter(user=user)
    payment_method, created = PaymentMethod.objects.get_or_create(user=user)
    upi, created = Upi_id.objects.get_or_create(user=user)
    bank_details, created = Bank.objects.get_or_create(user=user)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    

    if request.method == "POST":
        withdraw_method = request.POST.get('withdraw_method')

        # Handle the payment method selection form
        if withdraw_method:
            payment_method.withdrawal_method = withdraw_method
            payment_method.save()

        # Handle the UPI form
        elif 'upi_id' in request.POST:
            upi_id = request.POST.get('upi_id')
            # Process the UPI form data as needed
            upi_code = upi.upi = upi_id
            upi.save()
        # Handle the bank details form
        elif 'account_number' in request.POST:
            account_number = request.POST.get('account_number')
            ifsc_code = request.POST.get('ifsc_code')
            bank_name = request.POST.get('bank_name')

            bank_details.account_number = account_number
            bank_details.ifsc_code = ifsc_code
            bank_details.bank_name = bank_name
            bank_details.save()
            print(account_number)

    check_withdrawal_flag = True
    for j in withdrawal_exist:
        if j.status == "pending" or j.status == "processing":
            check_withdrawal_flag = False
        else:
            check_withdrawal_flag = True

    print(check_withdrawal_flag)

    amount = 0
    for i in account_balance:
        amount = i.balance_amount

    # if check_withdrawal_flag:
    #     withdrawal = PaymentWithdrawal.objects.create(
    #         user=user,
    #         amount=amount,
    #         withdrawal_method=payment_method.withdrawal_method,
    #     )
    # else:
    #     print("withdrawal existed")

    context = {
        'payment_method': payment_method,
        'upi': upi,
        'user': user,
        'bank_details': bank_details,
        'amount': amount,
        'check_withdrawal_flag': check_withdrawal_flag
    }
    return render(request, "withdrawal.html", context)


@login_required()
def Conform_withdrawal(request, username):
    """
    View for confirming withdrawal requests.
        Checks if there are any pending or processing withdrawals for the user. If not, creates a new withdrawal request.

        Args:
        - request: HttpRequest object
        - username: Username of the user making the request

        Returns:
        - Rendered HTML template with confirmation message
    """



    user = get_object_or_404(User, username=username)
    payment_method, created = PaymentMethod.objects.get_or_create(user=user)
    account_balance = SellerAccountBalance.objects.filter(user=user)
    withdrawal_exist = PaymentWithdrawal.objects.filter(user=user)
    amount = 0
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    for i in account_balance:
        amount = i.balance_amount

    check_withdrawal_flag = True
    for j in withdrawal_exist:
        if j.status == "pending" or j.status == "processing":
            check_withdrawal_flag = False
        else:
            check_withdrawal_flag = True

    print(check_withdrawal_flag)

    if check_withdrawal_flag:
        withdrawal = PaymentWithdrawal.objects.create(
            user=user,
            amount=amount,
            withdrawal_method=payment_method.withdrawal_method,
        )
    else:
        print("withdrawal existed")
    return render(request, "conform_withdrawal.html")


def is_superuser(user):
    """
    Function to check if a user is a superuser.

    Args:
    - user: User object to check

    Returns:
    - True if the user is a superuser, False otherwise
    """
    return user.is_superuser


# View for handling withdrawal requests
@user_passes_test(is_superuser, login_url='IntroHome')
def List_withdrawal(request, username):
    """
    Render a list of all withdrawal requests.

    Only accessible by superusers.

    Args:
        request: HttpRequest object
        username: Username of the current user

    Returns:
        Rendered HTML template with withdrawal list and relevant context data
    """
    user = get_object_or_404(User, username=username)
    withdrawal = PaymentWithdrawal.objects.all()
    context = {
        'withdrawal': withdrawal,
    }
    return render(request, "withdraw_list.html", context)

# View for displaying details of a specific withdrawal request


@user_passes_test(is_superuser, login_url='IntroHome')
def Details_of_withdrawal(request, username, withdrawal_id):
    """
    Render details of a specific withdrawal request.

    Only accessible by superusers.

    Args:
        request: HttpRequest object
        username: Username of the current user
        withdrawal_id: ID of the withdrawal request

    Returns:
        Rendered HTML template with withdrawal details and relevant context data
    """
    user = get_object_or_404(User, username=username)
    withdrawal = get_object_or_404(PaymentWithdrawal, pk=withdrawal_id)
    upi = Upi_id.objects.get(user=withdrawal.user)
    bank_details = Bank.objects.get(user=withdrawal.user)

    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    account_balance = SellerAccountBalance.objects.get(user=withdrawal.user)

    upi_bank_withdrawal_user = []
    upi_bank_withdrawal_user.append((user, withdrawal, upi, bank_details))

    if request.method == "POST":
        status_withdraw = request.POST.get('status_withdraw')
        if status_withdraw == 'accept':
            withdrawal.status = 'processing'
            withdrawal.save()
        elif status_withdraw == 'completed':
            withdrawal.status = 'completed'
            withdrawal.save()
            account_balance.balance_amount = 0
            account_balance.save()
        else:
            withdrawal.status = 'rejected'
            withdrawal.save()

    context = {
        'withdrawal': withdrawal,
        'upi_bank_withdrawal_user': upi_bank_withdrawal_user
    }

    return render(request, "details_of_withdrawal.html", context)


@login_required()
def Seller_list_withdrawal(request, username):
    """
    Render a list of withdrawal requests for the current user.

    Args:
        request: HttpRequest object
        username: Username of the current user

    Returns:
        Rendered HTML template with withdrawal list for the current user and relevant context data
    """

    user = get_object_or_404(User, username=username)
    current_user = request.user
    withdrawal = PaymentWithdrawal.objects.filter(user=current_user)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    context = {
        'withdrawal': withdrawal,
    }
    return render(request, "seller_widrawal_list.html", context)


@login_required()
def Save_payement_method(request, username):
    user = get_object_or_404(User, username=username)
    current_user = request.user
    payment_method, created = PaymentMethod.objects.get_or_create(user=user)
    upi, created = Upi_id.objects.get_or_create(user=user)
    bank_details, created = Bank.objects.get_or_create(user=user)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    if request.method == "POST":
        withdraw_method = request.POST.get('withdraw_method')

        # Handle the payment method selection form
        if withdraw_method:
            payment_method.withdrawal_method = withdraw_method
            payment_method.save()

        # Handle the UPI form
        elif 'upi_id' in request.POST:
            upi_id = request.POST.get('upi_id')
            # Process the UPI form data as needed
            upi_code = upi.upi = upi_id
            upi.save()
        # Handle the bank details form
        elif 'account_number' in request.POST:
            account_number = request.POST.get('account_number')
            ifsc_code = request.POST.get('ifsc_code')
            bank_name = request.POST.get('bank_name')

            bank_details.account_number = account_number
            bank_details.ifsc_code = ifsc_code
            bank_details.bank_name = bank_name
            bank_details.save()
            print(account_number)

    context = {
        'payment_method': payment_method,
        'upi': upi,
        'user': user,
        'bank_details': bank_details,
    }
    return render(request, "save_payement_method.html", context)


@login_required()
def Refund(request, username):
    user = get_object_or_404(User, username=username)
    orders = Order.objects.filter(buyer=user)
    refund_created = []  # Initialize as list to handle multiple refunds
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    for index, order in enumerate(orders, start=1):
        if order.status == 'cancelled' or order.status == 'expired':
            refund, created = Refund_details.objects.get_or_create(
                user=user,
                order=order
            )
            refund_created.append({
                'counter': index,
                'user': refund.user.username,
                'created_at': refund.created_at,
                'amount': refund.order.transaction.amount,
                'order_status': refund.order.status,
                'order_id': refund.order.id,
                'refund_status': refund.status,
                'payment_id': refund.order.transaction.payment_id,
            })

    context = {
        'refund_created': refund_created,
    }
    return render(request, "refund.html", context)


@user_passes_test(is_superuser, login_url='IntroHome')
def List_refunds(request, username):
    user = get_object_or_404(User, username=username)
    refunds = Refund_details.objects.all()
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    context = {
        'refund_created': refunds,
    }
    return render(request, "list_refunds.html", context)


# Assuming is_superuser is defined somewhere
# Assuming client is imported from somewhere

@user_passes_test(is_superuser, login_url='IntroHome')
def Details_of_refund(request, username, refund_id):
    user = get_object_or_404(User, username=username)
    refund = get_object_or_404(Refund_details, pk=refund_id)
    upi = Upi_id.objects.get(user=refund.user)
    ord = client.order.payments(refund.order.transaction.payment_id)
    refund_this = client.refund.all(refund.refund_id)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    for item in refund_this['items']:
        refund_status_cehck = item['status']
    payid = ord['items'][0]['id']
    with_fee = refund.order.transaction.amount + \
        refund.order.transaction.amount * Decimal('0.05')
    bank_details = Bank.objects.get(user=refund.user)
    if request.method == "POST":
        status_withdraw = request.POST.get('status_withdraw')
        if status_withdraw == 'accept':
            # Convert to integer before passing to refund function
            with_fee_int = int(with_fee * 100)
            # Generate a unique receipt ID based on refund ID and current timestamp
            receipt_id = f"Receipt-{refund_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            ref = client.payment.refund(payid, {
                "amount": with_fee_int,
                "currency": "INR",
                "speed": "normal",
                "notes": {
                    "notes_key_1": "Beam me up Scotty.",
                    "notes_key_2": "Engage"
                },
                "receipt": receipt_id  # Use the generated unique receipt ID
            })
            print(ref)
            refund.refund_id = ref['id']
            refund.status = 'processing'
            refund.save()
        elif status_withdraw == 'completed':
            refund.status = 'completed'
            refund.save()
        else:
            refund.status = 'rejected'
            refund.save()

    context = {
        'refund': refund,
        'upi': upi,
        'bank_details': bank_details,
        'with_fee': with_fee,
        'refund_status_cehck': refund_status_cehck
    }

    return render(request, "details_of_refund.html", context)
