from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import balance_view, transaction_view, dashboard_view, transaction_popup_view, signup

urlpatterns = [
    path('balance/', balance_view, name='balance'),
    path('transaction/', transaction_view, name='transaction'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('transaction-popup/<str:transaction_type>/', transaction_popup_view, name='transaction_popup'),
    path('', LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
]