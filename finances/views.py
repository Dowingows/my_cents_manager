from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View, generic

from finances.models import Transaction

from .forms import ExpenseForm, IncomeForm
from .mixins import (
    ExpenseTransactionMixin,
    IncomeTransactionMixin,
    UserFilteredMixin,
)
from .models import Expense, Income
from django.utils import timezone

def index(request):
    return render(request, 'index.html')


@login_required
def home(request):
    return render(request, 'home.html')


class IndexView(UserFilteredMixin, generic.ListView):
    model = Expense
    template_name = 'expense/index.html'
    context_object_name = 'expenses'


class DetailView(UserFilteredMixin, generic.DetailView):
    model = Expense
    template_name = 'expense/detail.html'


@method_decorator(login_required, name='dispatch')
class ExpenseCreateView(ExpenseTransactionMixin, generic.CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/form.html'
    success_url = reverse_lazy('finances:expense_index')

    def form_valid(self, form):
        form.instance.user = self.request.user

        response = super().form_valid(form)

        self.process_transaction(form, 'expense')

        return response


@method_decorator(login_required, name='dispatch')
class ExpenseUpdateView(ExpenseTransactionMixin, generic.UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/form.html'
    success_url = reverse_lazy('finances:expense_index')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.process_transaction(form, 'expense')
        return response


@method_decorator(login_required, name='dispatch')
class ExpenseDeleteView(generic.DeleteView):
    model = Expense
    template_name = 'expense/confirm_delete.html'
    success_url = reverse_lazy('finances:expense_index')


class IncomeIndexView(UserFilteredMixin, generic.ListView):
    model = Income
    template_name = 'income/index.html'
    context_object_name = 'incomes'


@method_decorator(login_required, name='dispatch')
class IncomeCreateView(IncomeTransactionMixin, generic.CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/form.html'
    success_url = reverse_lazy('finances:income_index')

    def form_valid(self, form):
        form.instance.user = self.request.user

        response = super().form_valid(form)

        self.process_transaction(form, 'income')

        return response


@method_decorator(login_required, name='dispatch')
class IncomeUpdateView(IncomeTransactionMixin, generic.UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/form.html'
    success_url = reverse_lazy('finances:income_index')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.process_transaction(form, 'income')
        return response


@method_decorator(login_required, name='dispatch')
class IncomeDeleteView(generic.DeleteView):
    model = Income
    template_name = 'income/confirm_delete.html'
    success_url = reverse_lazy('finances:income_index')


class MonthlyView(View):
    template_name = 'monthly_view.html'

    def get(self, request, *args, **kwargs):
        month = int(request.GET.get('month', timezone.now().month))
        year = int(request.GET.get('year', timezone.now().year))

        transactions = Transaction.objects.filter(
            user=request.user,
            transaction_date__month=month,
            transaction_date__year=year,
        )

        total_income = (
            transactions.filter(transaction_type='income').aggregate(
                Sum('amount')
            )['amount__sum']
            or 0
        )
        total_expense = (
            transactions.filter(transaction_type='expense').aggregate(
                Sum('amount')
            )['amount__sum']
            or 0
        )
        balance = total_income + total_expense

        # Calcular o próximo mês e o mês anterior
        next_month = (month % 12) + 1
        next_year = year + 1 if next_month == 1 else year
        prev_month = month - 1 if month > 1 else 12
        prev_year = year - 1 if month == 1 else year


        # Calcular links para o próximo e anterior
        next_link = reverse('finances:monthly_view') + f'?month={next_month}&year={next_year}'
        prev_link = reverse('finances:monthly_view') + f'?month={prev_month}&year={prev_year}'

        context = {
            'transactions': transactions,
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'month': month,
            'year': year,
            'next_link': next_link,
            'prev_link': prev_link,
        }

        return render(request, self.template_name, context)
