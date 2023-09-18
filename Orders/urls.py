from django.urls import path
from . import views

urlpatterns = [
    path('management_order/submit_requirements/<int:transaction_id>/<str:username>/', views.submit_requirements,name='submit_requirements'),
    path('management_order/details_of_the_order/<int:order_id>/<str:username>/',views.Details_of_the_order,name='details_of_the_order'),
    path('management_order/list_all_the_order/<str:username>/',views.List_all_orders,name='list_all_the_order')
]

