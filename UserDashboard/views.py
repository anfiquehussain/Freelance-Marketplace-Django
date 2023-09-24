from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

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



def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser,login_url='IntroHome')
def Admin_Dashboard(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    return render(request, 'admin_dashboard.html', context)
