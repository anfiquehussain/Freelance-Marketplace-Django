from django.db import models
from Home.models import UserProfile
from Services.models import Overview
from payments.models import Transaction

# Create your models here.
class Order(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Overview, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)



    def __str__(self):
        return f"Order #{self.pk} - {self.service.title}"

class Order_Requirements(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    description = models.TextField()
    answer_1 = models.TextField()
    example_image = models.ImageField(upload_to='requirements/', blank=True, null=True)

