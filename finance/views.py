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

    context = {
        'filter': transaction_filter
    }
    return render(request, 'finance/transactions-list.html', context)