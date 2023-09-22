# views.py

from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Order_Requirements
from .forms import OrderRequirementsForm
from Services.models import Overview
from payments.models import Transaction
from Services.models import Question

@login_required
def submit_requirements(request, transaction_id,username):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    user = get_object_or_404(User, username=username)

    order = Order.objects.get(transaction = transaction_id)

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
        return redirect('details_of_the_order', order_id=order.id,username=current_user.username)
    else:
        forms = [OrderRequirementsForm() for order in orders]

    context = {
        'orders': orders,
        'forms': forms,
        'service_provide_question_1':service_provide_question_1
    }

    return render(request, 'submit_requirements.html', context)





@login_required()
def Details_of_the_order(request,order_id,username):
    user = get_object_or_404(User, username=username)
    orders = Order.objects.filter(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    
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
        'orders_services_transactions': orders_services_transactions,  # Include transactions
    }
    
    
    
    return render(request,'details_of_the_order.html',context)


from django.contrib.auth.models import User
from payments.models import Transaction

def List_all_orders(request, username):
    user = get_object_or_404(User, username=username)
    orders = Order.objects.filter(buyer__user=user)


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
        'orders_services_transactions': orders_services_transactions,  # Include transactions
    }
    return render(request, 'list_all_orders.html', context)
