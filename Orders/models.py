from django.db import models
from Home.models import UserProfile
from Services.models import Overview
from payments.models import Transaction
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='buyer_orders')
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Overview, on_delete=models.CASCADE)
    transaction = models.OneToOneField('payments.Transaction', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'),('in_progress','In Progress'),('cancelled', 'Cancelled'),('expired', 'Expired'),('return', 'Return'),('delivered', 'Delivered'),('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)

class Order_Requirements(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    description = models.TextField()
    answer_1 = models.TextField()
    example_image = models.ImageField(upload_to='requirements/', blank=True, null=True)

class DeliveryDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_transit', 'In Transit'),('return', 'Return'), ('delivered', 'Delivered'), ('failed', 'Failed')], default='pending')
    delivery_notes = models.TextField(blank=True, null=True)
    delivery_modifcation_note = models.TextField(blank=True, null=True)
    order_delivered_date = models.DateField(null=True, blank=True)
    delivery_file = models.FileField(upload_to='delivery_files/', blank=True, null=True)

