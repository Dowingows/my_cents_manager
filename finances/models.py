from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    transaction_type = models.CharField(
        max_length=7, choices=TRANSACTION_TYPES
    )

    def __str__(self):
        return f'{self.name} ({self.amount})'


class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expense',
    )

    def is_delayed(self):
        return (
            self.payment_date is None
            and self.due_date <= timezone.now().date()
        )

    def is_paid(self):
        return self.payment_date is not None

    def delete(self, *args, **kwargs):
        if self.transaction:
            self.transaction.delete()

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name + ' (R$ {})'.format(self.amount)

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'


class Income(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='income',
    )

    def __str__(self):
        return self.name + ' (R$ {})'.format(self.amount)

    def delete(self, *args, **kwargs):
        if self.transaction:
            self.transaction.delete()

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'
