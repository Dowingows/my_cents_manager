from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage


class FileRemovalMixin:
    def remove_previous_file(self, instance, field_name):
        if instance.id and getattr(instance, field_name):
            try:
                old_instance = instance.__class__.objects.get(id=instance.id)
                old_file = getattr(old_instance, field_name)
                new_file = getattr(instance, field_name)

                if old_file.name != new_file.name:
                    old_file.delete(save=False)

            except instance.__class__.DoesNotExist:
                pass


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


def expense_upload_to(instance, filename):
    return f'expense_documents/{filename}'


def determine_storage():
    return S3Boto3Storage(
        bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        region_name=settings.AWS_S3_REGION_NAME,
    )


class Expense(models.Model, FileRemovalMixin):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    invoice_file = models.FileField(
        upload_to=expense_upload_to, storage=determine_storage, default=None
    )

    receipt_file = models.FileField(
        upload_to=expense_upload_to, storage=determine_storage, default=None
    )

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

        if self.invoice_file:
            self.invoice_file.delete(save=False)

        if self.receipt_file:
            self.receipt_file.delete(save=False)

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        self.remove_previous_file(self, 'invoice_file')
        self.remove_previous_file(self, 'receipt_file')

        super().save(*args, **kwargs)

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
