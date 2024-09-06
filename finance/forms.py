from typing import Any
from django import forms
from django.utils.timezone import make_aware, datetime

from .models import Category, Transaction


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect()
    )
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise forms.ValidationError('Amount must be a positive number')
        return amount
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.date_time:
            instance.date_time = make_aware(datetime.now())
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Transaction
        fields = [
            'type',
            'amount',
            'date_time',
            'category'
        ]
