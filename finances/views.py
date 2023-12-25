from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import ExpenseForm
from .mixins import UserFilteredMixin
from .models import Expense


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
class ExpenseCreateView(generic.CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/form.html'
    success_url = reverse_lazy('finances:expense_index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ExpenseUpdateView(generic.UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/form.html'
    success_url = reverse_lazy('finances:expense_index')


@method_decorator(login_required, name='dispatch')
class ExpenseDeleteView(generic.DeleteView):
    model = Expense
    template_name = 'expense/confirm_delete.html'
    success_url = reverse_lazy('finances:expense_index')
