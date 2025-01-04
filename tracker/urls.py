from django.urls import path
from .views import balance_view, transaction_view, dashboard_view, transaction_popup_view

urlpatterns = [
    path('balance/', balance_view, name='balance'),
    path('transaction/', transaction_view, name='transaction'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('transaction-popup/<str:transaction_type>/', transaction_popup_view, name='transaction_popup'),
]