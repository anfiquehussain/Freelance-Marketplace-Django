from django.urls import path
from . import views

urlpatterns = [
    
    path('overview/<int:overview_id>/<str:username>/', views.payments, name='payments'),
    path('success/<int:transaction_id>/<str:username>/', views.success, name='success'),
]
