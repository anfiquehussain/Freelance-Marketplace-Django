from django.shortcuts import render, get_object_or_404
from payments.models import Transaction
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required()
def order_management(request,transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request,'order_management.html')
