from django.contrib import admin
from .models import Balance, Transaction

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    last_display = ['user', 'amount']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'timestamp']