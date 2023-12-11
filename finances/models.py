from django.db import models
from django.utils import timezone


class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()

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
