from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Balance (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__ (self):
        return f"{self.user.username}'s balance {self.amount}"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type}: {self.amount}"
    
@receiver(post_save, sender=Transaction)
def update_balance(sender, instance, created, **kwargs):
    if created:
        balance = instance.user.balance
        if instance.transaction_type == 'deposit':
            balance.amount += instance.amount
        elif instance.transaction_type == 'withdrawal':
            balance.amount -= instance.amount
        balance.save()