from django.urls import path
from . import views

urlpatterns = [
    path('management_order/<int:transaction_id>', views.order_management,name='order_management'),
    path('submit_requirements/',views.submit_requirements,name='submit_requirements')
]

