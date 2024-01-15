from django import forms
from django.core.exceptions import ValidationError

from .models import Expense, Income
from .validators import FileExtensionValidator


class ExpenseForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    payment_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    extensionValidator = FileExtensionValidator(
        ['.pdf', '.png', '.jpeg', '.jpg']
    )
    invoice_file = forms.FileField(
        required=False, validators=[extensionValidator]
    )

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'due_date', 'payment_date', 'invoice_file']


class IncomeForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    expected_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    received_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Income
        fields = ['name', 'amount', 'expected_date', 'received_date']
