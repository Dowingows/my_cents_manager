from django.test import TestCase
from django.urls import reverse

from finances.models import Expense

from .mixins import AuthenticationMixin


class ExpenseIndexViewTest(AuthenticationMixin, TestCase):
    def test_expense_index_view_not_authenticated(self):

        url = reverse('finances:expense_index')

        self.assertRequiresAuthentication(url)

    def test_expense_index_view_authenticated(self):

        self.authenticate_user()

        url = reverse('finances:expense_index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class ExpenseDetailViewTest(AuthenticationMixin, TestCase):
    def test_expense_detail_view_not_authenticated(self):

        url = reverse('finances:expense_detail', args=(1,))

        self.assertRequiresAuthentication(url)

    def test_expense_detail_view_authenticated(self):

        expense = Expense.objects.create(
            user=self.test_user,
            name='Test Expense',
            amount=50.00,
            due_date='2023-12-31',
            payment_date='2023-12-30',
        )

        self.authenticate_user()

        url = reverse('finances:expense_detail', args=(expense.pk,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class ExpenseCreateViewTest(AuthenticationMixin, TestCase):
    def test_expense_create_view_not_authenticated(self):

        url = reverse('finances:expense_create')

        self.assertRequiresAuthentication(url)

    def test_expense_create_view_authenticated(self):

        self.authenticate_user()

        response = self.client.get(reverse('finances:expense_create'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'name': 'Test Expense',
            'amount': 100.00,
            'payment_date': '2023-12-15',
            'due_date': '2023-12-20',
            'user_id': self.test_user.pk,
        }

        response = self.client.post(
            reverse('finances:expense_create'), data=form_data
        )

        self.assertRedirects(response, reverse('finances:expense_index'))

        self.assertTrue(Expense.objects.filter(name='Test Expense').exists())

        expense = Expense.objects.get(name='Test Expense')
        self.assertEqual(expense.amount, 100.00)
        self.assertEqual(str(expense.payment_date), '2023-12-15')
        self.assertEqual(str(expense.due_date), '2023-12-20')
