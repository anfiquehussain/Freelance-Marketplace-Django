from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/seller_dashboard/', views.Seller_Dashboard, name='seller_dashboard'),
    path('<str:username>/buyer_dashboard/', views.Buyer_Dashboard, name='buyer_dashboard'),
    path('<str:username>/admin_dashboard/', views.Admin_Dashboard, name='admin_dashboard'),
]