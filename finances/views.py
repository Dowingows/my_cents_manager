from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import ExpenseForm
from .models import Expense


class IndexView(generic.ListView):
    model = Expense
    template_name = 'expense/index.html'
    context_object_name = 'expenses'


class DetailView(generic.DetailView):
    model = Expense
    template_name = 'expense/detail.html'


class ExpenseCreateView(generic.CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/form.html'
    success_url = reverse_lazy('finances:index')


class ExpenseUpdateView(generic.UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/form.html'
    success_url = reverse_lazy('finances:index')


class ExpenseDeleteView(generic.DeleteView):
    model = Expense
    template_name = 'expense/confirm_delete.html'
    success_url = reverse_lazy('finances:index')
