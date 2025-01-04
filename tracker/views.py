from django.shortcuts import render, redirect
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def balance_view(request):
    balance = request.user.balance.amount if hasattr(request.user, 'balance') else 0.0
    return render(request, 'tracker/balance.html', {'balance':balance})

@login_required
def transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('balance')
    else:
        form = TransactionForm()
    
    return render(request, 'tracker/transaction.html', {'form':form})

@login_required
def dashboard_view(request):
    balance = request.user.balance.amount if hasattr(request.user, 'balance') else 0.00
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'tracker/dashboard.html', {'balance': balance, 'transactions': transactions})

@login_required
def transaction_popup_view(request, transaction_type):
    if transaction_type not in ['deposit', 'withdrawal']:
        return JsonResponse({'success': False, 'error': 'Invalid transaction type.'})

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = transaction_type
            transaction.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TransactionForm()
        html_form = render_to_string('tracker/transaction_form.html', {'form': form, 'transaction_type': transaction_type}, request=request)
        return JsonResponse({'html_form': html_form})