from django.shortcuts import render, redirect
from .forms import RegistrationForm,LoginForm
from django.contrib.auth import login
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('IntroHome')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home', identifier=user.username)  # Replace 'home' with the desired URL after login
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

