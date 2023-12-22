# expense/forms.py
from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    payment_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'due_date', 'payment_date']
