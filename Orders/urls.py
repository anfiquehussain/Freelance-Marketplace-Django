from django.urls import path
from . import views

urlpatterns = [
    path('management_order/<int:transaction_id>', views.order_management,name='order_management'),
]

