from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import User, Category, Transaction
from .filters import TransactionFilter


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