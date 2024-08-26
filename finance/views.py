from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import User, Category, Transaction
from .filters import TransactionFilter


def home(request):
    return render(request, 'finance/home.html')


@login_required
def transactions_list(request):
    user = request.user

    transactions = Transaction.objects.filter(user=user).select_related('category')
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=transactions,
    )

    template_name = 'finance/transactions-list.html'
    if request.htmx:
        template_name = 'finance/partial/transactions-container.html'

    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income - total_expenses
    }
    return render(request, template_name, context)