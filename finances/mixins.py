from abc import ABC, abstractmethod

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Transaction


class UserFilteredMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TransactionMixinBase(ABC):
    @abstractmethod
    def get_date_field(self, form):
        pass

    @abstractmethod
    def get_signed_amount(self, form):
        pass

    def process_transaction(self, form, transaction_type):
        """
        Processa a transação associada a uma despesa ou receita.
        """
        date_field = self.get_date_field(form)

        if getattr(form.instance, date_field) is None:
            if form.instance.transaction:
                form.instance.transaction.delete()
                form.instance.transaction = None

            form.instance.save()

            return

        if form.instance.transaction:
            # Se já existe uma transação, atualiza seus dados
            form.instance.transaction.name = form.instance.name
            form.instance.transaction.amount = self.get_signed_amount(form)
            setattr(
                form.instance.transaction,
                'transaction_date',
                getattr(form.instance, date_field),
            )
            form.instance.transaction.transaction_type = transaction_type
            form.instance.transaction.save()
        else:
            # Se não existe uma transação, cria uma nova
            transaction = Transaction.objects.create(
                user=form.instance.user,
                name=form.instance.name,
                amount=self.get_signed_amount(form),
                transaction_date=getattr(form.instance, date_field),
                transaction_type=transaction_type,
            )
            form.instance.transaction = transaction
            form.instance.save()


class ExpenseTransactionMixin(TransactionMixinBase):
    def get_date_field(self, form):
        return 'payment_date'

    def get_signed_amount(self, form):
        amount = form.instance.amount
        return -abs(amount)


class IncomeTransactionMixin(TransactionMixinBase):
    def get_date_field(self, form):
        return 'received_date'

    def get_signed_amount(self, form):
        amount = form.instance.amount
        return abs(amount)


class FilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(user=user)

        search_input = self.request.GET.get('search-field') or ''
        if search_input:
            queryset = self.filter_by_search(queryset, search_input)

        return queryset

    def filter_by_search(self, queryset, search_input):
        """
        Filtra o queryset com base no campo de pesquisa.
        """
        raise NotImplementedError(
            'Subclasses of FilterMixin must provide a filter_by_search method.'
        )
