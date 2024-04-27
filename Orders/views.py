# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Order_Requirements, DeliveryDetails
from .forms import DeliveryDetailsForm
from datetime import datetime
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Order_Requirements, DeliveryDetails
from .forms import OrderRequirementsForm
from Services.models import Overview
from payments.models import Transaction
from Services.models import Question


# View function for submitting requirements for an order
@login_required
def submit_requirements(request, transaction_id, username):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    user = get_object_or_404(User, username=username)

    order = Order.objects.get(transaction=transaction_id)
    existing_requirements = Order_Requirements.objects.filter(order=order)
    existing_requirement_check = False
    if existing_requirements.exists():
        existing_requirement_check = True

    print(order.created_at)
    print(transaction.timestamp)

    tr_payemt_status = transaction.payment_status
    # print(sender_payemt_id)
    # print(transaction.payment_id)

    current_user = request.user

    if username == current_user.username and transaction.sender == current_user and tr_payemt_status == True:
        if current_user == order.buyer:
            pass
    else:
        return HttpResponseForbidden("Access Denied")

    orders = Order.objects.filter(transaction=transaction)
    # Questions = Question.objects.filter(overview=orders.service)
    # print(Questions)

# Fetching questions related to the service
    for ord in orders:
        questions = Question.objects.filter(overview=ord.service)
        # print("Service:", ord.service)

    for question in questions:
        service_provide_question_1 = question.question_text

    if request.method == 'POST':
        for order in orders:

            form = OrderRequirementsForm(request.POST, request.FILES)
            if form.is_valid():
                requirements = form.save(commit=False)
                requirements.order = order
                requirements.save()
        return redirect('details_of_the_order', order_id=order.id, username=current_user.username)
    else:
        forms = [OrderRequirementsForm() for order in orders]

    context = {
        'orders': orders,
        'forms': forms,
        'service_provide_question_1': service_provide_question_1,
        'existing_requirement_check': existing_requirement_check,

    }

    return render(request, 'submit_requirements.html', context)


# View function for displaying details of an order
@login_required()
def Details_of_the_order(request, order_id, username):
    # Retrieving user and order objects
    user = get_object_or_404(User, username=username)
    orders = Order.objects.filter(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    delivary_item = DeliveryDetails.objects.filter(order=order)
    # transation = Transaction.objects.filter(id=order.transaction_id)
    # for i in transation:
    #     print(i.id)
    # Handling cancellation of pending orders
    if (order.status == "pending"):
        if request.method == "POST":
            cencel = request.POST.get("status_order")
            order.status = "cancelled"
            order.save()
 # Handling actions upon order delivery
    if (order.status == 'delivered'):
        if request.method == 'POST':
            ok = request.POST.get('ok')
            no = request.POST.get('no')

            if (ok == 'yes,appove the delivary'):
                for item in delivary_item:
                    item. delivery_status = "completed"
                    item.save()
                order.status = "completed"
                order.save()
            elif (no == 'i am not ready of yet'):
                for item in delivary_item:
                    item. delivery_status = "return"
                    item.save()
                order.status = "return"
                order.save()

    current_user = request.user
    if username == current_user.username and order.buyer.id == current_user.id:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    # for item in delivary_item:
    #     print(item.delivery_file)

    order_requirements_check = 0

    order_requirements = Order_Requirements.objects.all()
    for rq in order_requirements:

        if (rq.order.id == order.id):

            order_requirements_check = rq.order.id
            break
        else:
            order_requirements_check = 0

    if (order_requirements_check):
        order_requirements = Order_Requirements.objects.filter(
            order=order_requirements_check)
        # for orq in order_requirements:
        #     print(orq.id)
    else:
        order_requirements = ''
        # print(order_requirements)

    orders_services_transactions = []

    for order in orders:
        service = Overview.objects.get(pk=order.service_id)
        transactions = Transaction.objects.filter(overview=order.service_id)
        orders_services_transactions.append((order, service, transactions))
    context = {
        'user': user,
        "order_requirements_check": order_requirements_check,
        "order_requirements": order_requirements,
        'orders_services_transactions': orders_services_transactions,
        'delivary_item': delivary_item
    }
    return render(request, 'details_of_the_order.html', context)


# View function for displaying all orders of a user
def List_all_orders(request, username):
    # Retrieving user and associated orders
    user = get_object_or_404(User, username=username)
    orders = Order.objects.filter(buyer=user)

    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    orders_services_transactions = []

    for order in orders:
        service = Overview.objects.get(pk=order.service_id)
        transactions = Transaction.objects.filter(overview=order.service_id)

        # Append a tuple containing order, service, and transactions to the list
        orders_services_transactions.append((order, service, transactions))

    context = {
        'user': user,
        'orders_services_transactions': orders_services_transactions,
    }
    return render(request, 'list_all_orders.html', context)


# View function for displaying all orders of a seller
def Seller_List_all_orders(request, username):
    user = get_object_or_404(User, username=username)
    orders = Order.objects.filter(seller=user)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    # Create a list to store transaction and overview information for each order
    order_info = []

    for order in orders:
        transaction = Transaction.objects.filter(order=order).first()
        overview = Overview.objects.get(pk=order.service.pk)

        current_datetime = timezone.now()
        current_date = current_datetime.date()

        if (order.status == "pending" or order.status == "in_progress"):

            if order.delivery_date < current_date:
                order.status = "expired"
                order.save()

        order_info.append({
            'order': order,
            'transaction': transaction,
            'overview': overview,
        })

    context = {
        'user': user,
        'order_info': order_info,
    }

    return render(request, 'seller_list_all_orders.html', context)


# View function for displaying details of an order for a seller
@login_required
def Seller_Details_of_the_order(request, order_id, username):
    user = get_object_or_404(User, username=username)
    order = get_object_or_404(Order, id=order_id)
    delivary_item = DeliveryDetails.objects.filter(order=order)

    if username != request.user.username or order.seller != user:
        return HttpResponseForbidden("Access Denied")

    existing_delivery_details = DeliveryDetails.objects.filter(
        order=order).first()
    order_requirements = Order_Requirements.objects.filter(order=order)

    if request.method == 'POST':
        form = DeliveryDetailsForm(
            request.POST, request.FILES, instance=existing_delivery_details)
        if form.is_valid():
            delivery_details = form.save(commit=False)
            delivery_details.delivery_status = 'delivered'
            delivery_details.order_delivered_date = timezone.now()
            delivery_details.order = order
            delivery_details.save()
            order.status = 'delivered'
            order.save()

    else:
        if existing_delivery_details:
            form = DeliveryDetailsForm(instance=existing_delivery_details)
        else:
            form = DeliveryDetailsForm()

    accept_order_value = ""
    if request.method == 'POST':
        order_status_value = request.POST.get('status_order')
        if order_status_value == 'accept':
            order.status = "in_progress"
            order.save()
        elif order_status_value == 'cancel':
            order.status = "cancelled"
            order.save()

    for item in delivary_item:
        print(order.status)
        print(item.delivery_status)
        if order.status == "return":
            item.delivery_status = "return"
            item.save()
        else:
            print("bad")
    context = {
        'user': user,
        'order': order,
        'form': form,
        'order_requirements': order_requirements
    }
    return render(request, 'seller_detials_of_order.html', context)
