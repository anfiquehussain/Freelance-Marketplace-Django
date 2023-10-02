from django.db import models
from django.contrib.auth.models import User
from Services.models import Overview
from Orders.models import Order

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='messages_received', on_delete=models.CASCADE)
    service = models.ForeignKey(Overview, related_name='service_profile', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, related_name='order_of_user',on_delete=models.CASCADE)
    message = models.TextField()
    status = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)
    video = models.FileField(upload_to='message_videos/', null=True, blank=True)
