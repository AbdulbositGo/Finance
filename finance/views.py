from django.shortcuts import render
from .models import User, Category, Transaction
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'finance/home.html')


@login_required
def transactions_list(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).select_related('category')

    context = {
        'transactions': transactions
    }

    return render(request, 'finance/transactions-list.html', context)