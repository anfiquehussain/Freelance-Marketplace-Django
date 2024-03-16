from django.urls import path
from . import views

urlpatterns = [
    
    path('overview/<int:overview_id>/<str:username>/', views.payments, name='payments'),
    path('success/<int:transaction_id>/<str:username>/', views.success, name='success'),
    path('withdrawal/<str:username>/', views.withdrawal, name='withdrawal'),
    path('conform_withdrawal/<str:username>/', views.Conform_withdrawal, name='conform_withdrawal'),
    path('withdraw_list/<str:username>/', views.List_withdrawal, name='withdraw_list'),
    path('details_of_withdrawal/<str:username>/<int:withdrawal_id>/', views.Details_of_withdrawal, name='details_of_withdrawal'),
    path('seller_list_withdrawal/<str:username>/', views.Seller_list_withdrawal, name='seller_widrawal_list'),
    path('refund/<str:username>/', views.Refund, name='refund'),
    path('save_payement_method/<str:username>/', views.Save_payement_method, name='save_payement_method'),
    path('list_refunds/<str:username>/', views.List_refunds, name='list_refunds'),
    path('details_of_refund/<str:username>/<int:refund_id>/', views.Details_of_refund, name='details_of_refund'),
]
