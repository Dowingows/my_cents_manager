from django.db import models


class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return self.name + " (R$ {})".format(self.amount)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"