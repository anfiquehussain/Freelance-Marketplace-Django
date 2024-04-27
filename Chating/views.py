# Importing necessary modules and models
from Orders.models import Order  # Importing Order model
from django.contrib.auth.models import User  # Importing User model
from django.shortcuts import get_object_or_404, render, redirect  # Importing necessary shortcuts
from .forms import MessageForm  # Importing MessageForm from current directory
from Home.models import UserProfile  # Importing UserProfile model from Home app
from .models import Message  # Importing Message model from current directory
from django.http import JsonResponse
import datetime

# View function for handling user chat
def Userchat(request, order_id, username):
    # Getting the user and order objects based on the given IDs
    user = get_object_or_404(User, username=username)
    order = get_object_or_404(Order, id=order_id)
    form = MessageForm()  # Creating a MessageForm instance
    current_user = request.user
    if username == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    # Determining the receiver based on the order and user roles
    if user == order.seller:
        receiver = order.buyer
    else:
        receiver = order.seller

    # Getting receiver and sender profiles
    reciver_profile = UserProfile.objects.filter(user=receiver)
    sender_profile = UserProfile.objects.filter(user=user)

    # Handling form submission
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            # Saving the message object
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.service = order.service
            message.order = order
            message.save()
            # Retrieving messages related to the order
            messages = Message.objects.filter(order=order)
            # Redirecting to the chat page after message submission

            return redirect('userchat', order.id, request.user)

    # Retrieving messages related to the order
    messages = Message.objects.filter(order=order)
    
    # Context data for rendering the chat template
    context = {
        'order': order,
        'user': user,
        'form': form,
        'receiver': receiver,
        'messages': messages,
        'reciver_profile': reciver_profile,
        'sender_profile': sender_profile
    }
   
    return render(request, 'Userchat.html', context)

# Function to fetch messages for a specific order
def get_messages(request, order_id):
    # Getting the order object based on the given ID
    order = get_object_or_404(Order, id=order_id)
    # Retrieving messages related to the order
    messages = Message.objects.filter(order=order)
    message_data = []

    # Iterating through messages and formatting data
    for message in messages:
        timestamp = datetime.datetime.now()
        formatted_timestamp =  message.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Determining the class based on the sender of the message
        if request.user == message.sender:
            message_data.append(f"<p class='message sender'><span class='username'>{formatted_timestamp}</span><br>{message.message}</p>")
        else:
            message_data.append(f"<p class='message receiver'><span class='username'>{formatted_timestamp}</span> <br> {message.message}</p>")

    # Returning JSON response containing formatted message data
    return JsonResponse({"messages": "\n".join(message_data)})
