from django.test import TestCase
from django.utils import timezone

from finances.models import Expense


class ExpenseModelTest(TestCase):
    def test_is_delayed(self):
        # Crie uma despesa com uma data de vencimento futura
        future_due_date = timezone.now().date() + timezone.timedelta(days=7)
        expense_future = Expense(
            name='Future Expense',
            amount=50.00,
            due_date=future_due_date,
            payment_date=None,
        )

        self.assertFalse(
            expense_future.is_delayed(), 'Despesa não está atrasada'
        )

        # Crie uma despesa com uma data de vencimento passada
        past_due_date = timezone.now().date() - timezone.timedelta(days=7)
        expense_past = Expense(
            name='Past Expense',
            amount=30.00,
            due_date=past_due_date,
            payment_date=None,
        )

        self.assertTrue(expense_past.is_delayed(), 'Despesa está atrasada')

    def test_str_representation(self):
        # Create an Expense instance
        expense = Expense(
            name='Test Expense',
            amount=100.50,
            payment_date=None,
            due_date=timezone.now().date(),
        )

        # Check if the __str__ method returns the expected string
        expected_str = 'Test Expense (R$ 100.5)'
        self.assertEqual(str(expense), expected_str)
