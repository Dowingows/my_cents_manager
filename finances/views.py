from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic

from finances.models import Transaction

from .forms import ExpenseForm, IncomeForm
from .mixins import (
    ExpenseTransactionMixin,
    FileGenerationMixin,
    FilterMixin,
    IncomeTransactionMixin,
    MonthlyMixin,
    UserFilteredMixin,
)
from .models import Expense, Income


def index(request):
    return render(request, 'index.html')


class IndexView(FilterMixin, UserFilteredMixin, generic.ListView):
    model = Expense
    template_name = 'expense/index.html'
    context_object_name = 'expenses'

    def filter_by_search(self, queryset, search_input):
        return queryset.filter(name__contains=search_input)


class DetailView(UserFilteredMixin, generic.DetailView):
    model = Expense
    template_name = 'expense/detail.html'


@method_decorator(login_required, name='dispatch')
class ExpenseCreateView(
    ExpenseTransactionMixin, FileGenerationMixin, generic.CreateView
):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/new.html'
    success_url = reverse_lazy('finances:expense_index')

    def form_valid(self, form):
        form.instance.user = self.request.user

        self.modify_file_name(form, 'invoice_file', 'invoice')
        self.modify_file_name(form, 'receipt_file', 'receipt')

        response = super().form_valid(form)

        self.process_transaction(form, 'expense')

        return response


@method_decorator(login_required, name='dispatch')
class ExpenseUpdateView(
    ExpenseTransactionMixin, FileGenerationMixin, generic.UpdateView
):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/update.html'
    success_url = reverse_lazy('finances:expense_index')

    def form_valid(self, form):

        self.modify_file_name(form, 'invoice_file', 'invoice')
        self.modify_file_name(form, 'receipt_file', 'receipt')

        response = super().form_valid(form)

        self.process_transaction(form, 'expense')
        return response


@method_decorator(login_required, name='dispatch')
class ExpenseDeleteView(generic.DeleteView):
    model = Expense
    template_name = 'expense/confirm_delete.html'
    success_url = reverse_lazy('finances:expense_index')


class IncomeIndexView(FilterMixin, UserFilteredMixin, generic.ListView):
    model = Income
    template_name = 'income/index.html'
    context_object_name = 'incomes'

    def filter_by_search(self, queryset, search_input):
        return queryset.filter(name__contains=search_input)


@method_decorator(login_required, name='dispatch')
class IncomeCreateView(IncomeTransactionMixin, generic.CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/new.html'
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
    template_name = 'income/update.html'
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


@method_decorator(login_required, name='dispatch')
class MonthlyView(MonthlyMixin):
    template_name = 'monthly_view.html'

    def get(self, request, *args, **kwargs):
        month, year = self.get_month_and_year(request)
        transactions = self.get_transactions(request.user, month, year)
        total_income, total_expense, balance = self.calculate_totals(
            transactions
        )

        (
            next_month,
            next_year,
            prev_month,
            prev_year,
        ) = self.calculate_next_and_previous(month, year)
        next_link, prev_link = self.calculate_links(
            reverse('finances:home'),
            next_month,
            next_year,
            prev_month,
            prev_year,
        )

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

    def get_transactions(self, user, month, year):
        return Transaction.objects.filter(
            user=user,
            transaction_date__month=month,
            transaction_date__year=year,
        ).order_by('-transaction_date')

    def calculate_totals(self, transactions):
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
        return total_income, total_expense, balance


@method_decorator(login_required, name='dispatch')
class ExpenseMonthlyView(MonthlyMixin):
    template_name = 'expense/monthly.html'

    def get(self, request, *args, **kwargs):

        month, year = self.get_month_and_year(request)
        expenses = self.get_expenses(request.user, month, year)

        (
            total_expense,
            total_delayed,
            total_unpaid,
            total_paid,
        ) = self.calculate_totals(expenses)

        (
            next_month,
            next_year,
            prev_month,
            prev_year,
        ) = self.calculate_next_and_previous(month, year)

        next_link, prev_link = self.calculate_links(
            reverse('finances:expense_monthly'),
            next_month,
            next_year,
            prev_month,
            prev_year,
        )

        context = {
            'expenses': expenses,
            'total_expense': total_expense,
            'total_delayed': total_delayed,
            'total_unpaid': total_unpaid,
            'total_paid': total_paid,
            'month': month,
            'year': year,
            'next_link': next_link,
            'prev_link': prev_link,
        }

        return render(request, self.template_name, context)

    def get_expenses(self, user, month, year):
        return Expense.objects.filter(
            user=user,
            due_date__month=month,
            due_date__year=year,
        ).order_by('-due_date')

    def calculate_totals(self, expenses):

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_delayed = (
            expenses.filter(
                payment_date__isnull=True, due_date__lte=timezone.now().date()
            )
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_unpaid = (expenses.filter(payment_date__isnull=True)).aggregate(
            Sum('amount')
        )['amount__sum'] or 0

        total_paid = (expenses.filter(payment_date__isnull=False)).aggregate(
            Sum('amount')
        )['amount__sum'] or 0

        return total_expense, total_delayed, total_unpaid, total_paid
