from django.db import models
from django.contrib.auth.models import User



class Transaction(models.Model):
    overview = models.IntegerField(blank=True, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_transactions')
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


class PaymentWithdrawal(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdrawal_method = models.CharField(max_length=255, choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
    ], default='bank_transfer')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentMethod(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='withdrawal_method')
    withdrawal_method = models.CharField(max_length=255, choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
    ], default='bank_transfer')


class Upi_id(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='upi_ids')
    upi = models.CharField(max_length=255)


class Bank(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='bank_details')
    account_number = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=255)

class Refund_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField('Orders.Order', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ], default='pending')
    refund_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


