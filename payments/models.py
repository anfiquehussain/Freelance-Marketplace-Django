from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    overview = models.IntegerField(blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    package_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Transaction from {self.sender} to {self.receiver} - {self.amount}"

class SellerAccountBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=3, default='INR')
