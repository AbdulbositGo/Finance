from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import User, Category, Transaction
from .filters import TransactionFilter
from .forms import TransactionForm


def home(request):
    return render(request, 'finance/home.html')


@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()

    template_name = 'finance/transactions-list.html'
    if request.htmx:
        template_name = 'finance/partial/transactions-container.html'

    context = {
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income - total_expenses
    }
    return render(request, template_name, context)


@login_required
def create_transaction(request):
    form = TransactionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "A new transaction created")
            return redirect('transactions-list')    
    context = {
        'form': form
    }
    if request.htmx:
        return render(request, 'finance/partial/create-transaction.html', context)
    return render(request, 'finance/create-transaction.html', context)


@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transactions-list')
        else:
            context = {
                'transaction': transaction,
                'form': TransactionForm(request.POST, instance=transaction)
            }
            return render(request, 'finance/partial/update-transaction.html', context)

    else:
        form = TransactionForm(instance=transaction)

    context = {
        'transaction': transaction,
        'form': form
    }

    if request.htmx:
        return render(request, 'finance/partial/update-transaction.html', context)
    return render(request, 'finance/update-transaction.html', context)


@login_required
@require_http_methods(['DELETE'])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk, user=request.user)
    transaction.delete()
    messages.error(request, f'Transaction of {transaction.amount} on \
                   {transaction.date_time} was deleted ')
    return redirect('transactions-list')
