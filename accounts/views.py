# Import necessary modules and functions
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout

# Define view for user registration


def register(request):
    if request.method == 'POST':
        # Process the registration form if the request method is POST
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the form data if it's valid
            form.save()
            # Redirect to login page after successful registration
            return redirect('login')
    else:
        # Render the registration form for GET requests
        form = RegistrationForm()
    # Render the registration template with the form
    return render(request, 'registration/register.html', {'form': form})

# Define view for user logout


def logout_view(request):
    # Log out the user
    logout(request)
    # Redirect to the home page
    return redirect('IntroHome')

# Define view for user login


def login_view(request):
    if request.method == 'POST':
        # Process the login form if the request method is POST
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Get the authenticated user
            user = form.get_user()
            # Log in the user
            login(request, user)
            # Redirect to home page with user identifier
            return redirect('home', identifier=user.username)
    else:
        # Render the login form for GET requests
        form = LoginForm()
    # Render the login template with the form
    return render(request, 'registration/login.html', {'form': form})
