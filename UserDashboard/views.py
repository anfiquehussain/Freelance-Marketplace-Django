from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from Home.models import UserProfile
from payments.models import Transaction, SellerAccountBalance, PaymentWithdrawal, Refund_details, PaymentWithdrawal
from Orders.models import Order
from Services.models import Overview
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum


def Seller_Dashboard(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.filter(user=user)
    service_overview = Overview.objects.filter(user=user)
    orders = Order.objects.filter(seller=user)
    withdrawal = PaymentWithdrawal.objects.filter(user=user)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    current_user = request.user
    if username != current_user.username:
        return redirect('IntroHome')

    overview_totals = {}
    overview_counts = {}

    overview_total_counts = {}

    for i in withdrawal:
        print(i)

    for order in orders:
        transaction = Transaction.objects.filter(order=order).first()
        if transaction:
            overview = order.transaction.overview
            overview_total_counts[overview] = overview_total_counts.get(
                overview, 0) + 1

        if order.status == "completed" and transaction:
            overview = transaction.overview
            amount_earned = transaction.amount

            overview_totals[overview] = overview_totals.get(
                overview, 0) + amount_earned
            overview_counts[overview] = overview_counts.get(overview, 0) + 1

    # Add additional information to each service_overview object
    for s_overview in service_overview:
        s_overview.amount_earned = overview_totals.get(s_overview.id, 0)
        s_overview.order_completed = overview_counts.get(s_overview.id, 0)
        s_overview.total_orders = overview_total_counts.get(s_overview.id, 0)

    order_counts = Order.objects.filter(seller=user).aggregate(
        all_count=Count('id'),
        pending_count=Count('id', filter=Q(status='pending')),
        active_count=Count('id', filter=Q(status='in_progress')),
        return_count=Count('id', filter=Q(status='return')),
        expired_count=Count('id', filter=Q(status='expired')),
        delivered_count=Count('id', filter=Q(status='delivered')),
        completed_count=Count('id', filter=Q(status='completed')),
        cancelled_count=Count('id', filter=Q(status='cancelled'))
    )

    earned_total = sum(overview_totals.values())

    account_balance_queryset = SellerAccountBalance.objects.filter(user=user)
    seller_balance_total = 0
    orders = Order.objects.filter(seller=user)

    # Calculate the total amount in withdrawals for the user
    withdrawal_total = sum(withdrawal.values_list('amount', flat=True))

    for order in orders:
        transaction = Transaction.objects.filter(order=order).first()
        if order.status == "completed" and transaction:
            overview = transaction.overview
            amount_earned = transaction.amount
            fee = amount_earned * 10 / 100
            seller_balance_total = seller_balance_total + amount_earned - fee

    # Subtract the withdrawal amount from the earned amount outside the loop
    withdrawal_total = sum(withdrawal.filter(
        status='completed').values_list('amount', flat=True))
    seller_balance_total -= withdrawal_total

    # Update the seller's balance in the database
    if account_balance_queryset.exists():
        account_balance = account_balance_queryset.first()
        account_balance.balance_amount = seller_balance_total
        account_balance.save()
    else:
        create_account_balance = SellerAccountBalance.objects.create(
            user=user,
            balance_amount=seller_balance_total,
        )

    context = {
        'user': user,
        "user_profile": user_profile,
        "service_overview": service_overview,
        'order_counts': order_counts,
        'seller_balance_total': seller_balance_total
    }

    return render(request, 'seller_dashboard.html', context)


def Buyer_Dashboard(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.filter(user=user)
    service_overview = Overview.objects.filter(user=user)
    orders = Order.objects.filter(buyer=user)



    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return redirect('IntroHome')

    orders_services_transactions = []

    for order in orders:
        service = Overview.objects.get(pk=order.service_id)
        transactions = Transaction.objects.filter(overview=order.service_id)

        orders_services_transactions.append((order, service, transactions))

    order_counts = Order.objects.filter(buyer=user).aggregate(
        all_count=Count('id'),
        pending_count=Count('id', filter=Q(status='pending')),
        active_count=Count('id', filter=Q(status='in_progress')),
        return_count=Count('id', filter=Q(status='return')),
        expired_count=Count('id', filter=Q(status='expired')),
        delivered_count=Count('id', filter=Q(status='delivered')),
        completed_count=Count('id', filter=Q(status='completed')),
        cancelled_count=Count('id', filter=Q(status='cancelled'))
    )
    context = {
        'user': user,
        'user_profile': user_profile,
        "service_overview": service_overview,
        'orders_services_transactions': orders_services_transactions,
        'order_counts': order_counts,
    }

    return render(request, 'buyer_dashboard.html', context)

# Function to check if the user is a superuser
def is_superuser(user):
    return user.is_superuser



# Add this decorator to restrict access to superusers only
@user_passes_test(is_superuser, login_url='IntroHome')
def Admin_Dashboard(request, username):
    """
    View for displaying the buyer dashboard.
    Access is restricted to superusers.
    """
    user = get_object_or_404(User, username=username)
    all_user = User.objects.all()
    all_services = Overview.objects.all()
    all_order = Order.objects.all()
    pending_orders_count = all_order.filter(status='pending').count()
    active_orders_count = all_order.filter(status='in_progress').count()
    return_orders_count = all_order.filter(status='return').count()
    expired_orders_count = all_order.filter(status='expired').count()
    delivered_orders_count = all_order.filter(status='delivered').count()
    completed_orders_count = all_order.filter(status='completed').count()
    cancelled_orders_count = all_order.filter(status='cancelled').count()
    
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")    

    all_refund = Refund_details.objects.all()
    all_refunds_count = all_refund.count()
    pending_refunds_count = all_refund.filter(status='pending').count()
    approved_refunds_count = all_refund.filter(status='processing').count()
    rejected_refunds_count = all_refund.filter(status='rejected').count()
    refunded_refunds_count = all_refund.filter(status='refunded').count()

    all_withdrawals = PaymentWithdrawal.objects.all()

    # Get counts for each withdrawal status
    all_withdrawals_count = all_withdrawals.count()
    pending_withdrawals_count = all_withdrawals.filter(
        status='pending').count()
    approved_withdrawals_count = all_withdrawals.filter(
        status='processing').count()
    rejected_withdrawals_count = all_withdrawals.filter(
        status='rejected').count()
    completed_withdrawals_count = all_withdrawals.filter(
        status='completed').count()

    search_results = None
    if request.method == 'POST':
        if 'search_user' in request.POST:
            search_query = request.POST.get('search_query')
            if search_query:
                search_results = User.objects.filter(
                    Q(username__icontains=search_query))
            else:
                pass

    context = {
        'user': user,
        'all_user': all_user,
        'search_results': search_results,
        'all_services': all_services,
        'all_order': all_order,
        'pending_orders_count': pending_orders_count,
        'active_orders_count': active_orders_count,
        'return_orders_count': return_orders_count,
        'expired_orders_count': expired_orders_count,
        'delivered_orders_count': delivered_orders_count,
        'completed_orders_count': completed_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'all_refund': all_refund,
        'all_refunds_count': all_refunds_count,
        'pending_refunds_count': pending_refunds_count,
        'approved_refunds_count': approved_refunds_count,
        'rejected_refunds_count': rejected_refunds_count,
        'refunded_refunds_count': refunded_refunds_count,
        'all_withdrawals': all_withdrawals,
        'all_withdrawals_count': all_withdrawals_count,
        'pending_withdrawals_count': pending_withdrawals_count,
        'approved_withdrawals_count': approved_withdrawals_count,
        'rejected_withdrawals_count': rejected_withdrawals_count,
        'completed_withdrawals_count': completed_withdrawals_count,
    }
    return render(request, 'admin_dashboard.html', context)
