from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

# Create your views here.
def Seller_Dashboard(request,username):
    user = get_object_or_404(User, username=username)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return redirect('IntroHome')
    context = {
        'user':user
    }

    return render(request,'seller_dashboard.html',context)

def Buyer_Dashboard(request,username):
    user = get_object_or_404(User, username=username)
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return redirect('IntroHome')

    context = {
        'user':user
    }
        
    return render(request,'buyer_dashboard.html')
