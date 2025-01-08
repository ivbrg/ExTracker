from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import TransactionForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Balance, Transaction, User
from django.db.models import Sum
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard after login
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'tracker/login.html', {'form': form})

@login_required
def dashboard_view(request):
    transactions_list = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    items_per_page = int(request.GET.get('items_per_page', 10))  # Default to 10 items per page
    paginator = Paginator(transactions_list, items_per_page)

    # Handle pagination
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'balance': request.user.balance.amount if hasattr(request.user, 'balance') else 0.00, 
        'page_obj': page_obj,  # Pass the paginated transactions to the template
        'items_per_page': items_per_page,
    }

    return render(request, 'tracker/dashboard.html', context)

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