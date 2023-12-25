from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_delayed(self):
        return (
            self.payment_date is None
            and self.due_date <= timezone.now().date()
        )

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

    def __str__(self):
        return self.name + ' (R$ {})'.format(self.amount)

    class Meta:
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'
