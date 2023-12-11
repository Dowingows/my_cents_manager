from django.views import generic

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
