from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from .forms import ExpenseForm
from .models import Expense


class IndexView(generic.ListView):
    template_name = 'expense/index.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        """Return the last five published questions."""
        return Expense.objects.all()


class DetailView(generic.DetailView):
    model = Expense
    template_name = 'expense/detail.html'


def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('finances:index'))
    else:
        form = ExpenseForm()

    return render(request, 'expense/form.html', {'form': form})


def edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect(reverse('finances:index'))
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense/form.html', {'form': form})


def delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect(reverse('finances:index'))
