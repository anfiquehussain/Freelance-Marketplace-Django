from django.urls import path
from . import views

urlpatterns = [
    
    path('overview/<int:overview_id>', views.payments, name='payments'),
    path('success/<int:transaction_id>', views.success, name='success')
]
