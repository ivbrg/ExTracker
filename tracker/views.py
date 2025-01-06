from django.shortcuts import render, redirect
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator

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
    
def transaction_list(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')  # Order by most recent

    # Get the number of transactions per page (default to 10 if not specified)
    per_page = request.GET.get('per_page', 10)
    paginator = Paginator(transactions, per_page)

    # Get the current page number (default to 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Contains paginated transactions
        'per_page': per_page,  # Pass this to the template for the dropdown
    }
    return render(request, 'tracker/dashboard.html', context)