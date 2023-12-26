from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Transaction


class UserFilteredMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TransactionMixin:
    def process_transaction(self, form, transaction_type):
        """
        Processa a transação associada a uma despesa ou receita.
        """

        # Verifica se o payment_date é nulo
        if form.instance.payment_date is None:
            # Se já existe uma transação, remova-a
            if form.instance.transaction:
                form.instance.transaction.delete()
                form.instance.transaction = None

            form.instance.save()

            return  # Early return

        if form.instance.transaction:
            # Se já existe uma transação, atualiza seus dados
            form.instance.transaction.name = form.instance.name
            form.instance.transaction.amount = form.instance.amount
            form.instance.transaction.transaction_date = (
                form.instance.payment_date
            )
            form.instance.transaction.transaction_type = transaction_type
            form.instance.transaction.save()
        else:
            # Se não existe uma transação, cria uma nova
            transaction = Transaction.objects.create(
                user=form.instance.user,
                name=form.instance.name,
                amount=form.instance.amount,
                transaction_date=form.instance.payment_date,
                transaction_type=transaction_type,
            )
            form.instance.transaction = transaction
            form.instance.save()
