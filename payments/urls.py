from django.urls import path
from . import views

urlpatterns = [
    
    path('overview/<int:overview_id>/<str:username>/', views.payments, name='payments'),
    path('success/<int:transaction_id>/<str:username>/', views.success, name='success'),
    path('withdrawal/<str:username>/', views.withdrawal, name='withdrawal'),
    path('conform_withdrawal/<str:username>/', views.Conform_withdrawal, name='conform_withdrawal'),
    path('withdraw_list/<str:username>/', views.List_withdrawal, name='withdraw_list'),
path('details_of_withdrawal/<str:username>/<int:withdrawal_id>/', views.Details_of_withdrawal, name='details_of_withdrawal')
]
