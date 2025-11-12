from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='createOrder'),
    path('update_order/<int:order_id>/', views.update_order_status, name='updateStatus'),
]
