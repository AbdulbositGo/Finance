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

    context = {
        'filter': transaction_filter
    }
    return render(request, template_name, context)