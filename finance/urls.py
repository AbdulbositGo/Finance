from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('transactions', views.transactions_list, name="transactions-list"),
    path('transactions/create', views.create_transaction, name="create-transaction"),
]
