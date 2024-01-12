# Generated by Django 5.0 on 2024-01-12 17:19

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0004_expense_transaction_income_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='invoice_file',
            field=models.FileField(default=None, null=True, storage=storages.backends.s3.S3Storage(bucket_name='cents-bucket'), upload_to='expense_invoices/'),
            preserve_default=False,
        ),
    ]
