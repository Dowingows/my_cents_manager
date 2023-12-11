from django.shortcuts import redirect, render
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
