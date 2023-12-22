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


class ExpenseUpdateViewTest(AuthenticationMixin, TestCase):
    def test_expense_update_view_not_authenticated(self):

        url = reverse('finances:expense_edit', args=(1,))

        self.assertRequiresAuthentication(url)

    def test_expense_update_view_authenticated(self):

        expense = Expense.objects.create(
            user=self.test_user,
            name='Test Expense',
            amount=50.00,
            due_date='2023-12-31',
            payment_date='2023-12-30',
        )

        self.authenticate_user()

        url = reverse('finances:expense_edit', args=(expense.pk,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        updated_data = {
            'name': 'Updated Expense',
            'amount': 75.00,
            'due_date': '2023-02-01',
            'payment_date': '2024-01-01',
        }

        response = self.client.post(url, data=updated_data)

        self.assertRedirects(response, reverse('finances:expense_index'))

        updated_expense = Expense.objects.get(pk=expense.pk)

        self.assertEqual(updated_expense.name, updated_data['name'])
        self.assertEqual(updated_expense.amount, updated_data['amount'])
        self.assertEqual(
            str(updated_expense.due_date), updated_data['due_date']
        )
        self.assertEqual(
            str(updated_expense.payment_date), updated_data['payment_date']
        )


class ExpenseDeleteViewTest(AuthenticationMixin, TestCase):
    def setUp(self):

        super().setUp()

        self.expense = Expense.objects.create(
            name='Test Delete',
            amount=50.00,
            due_date='2023-12-31',
            payment_date='2023-12-31',
            user=self.test_user,
        )

        self.url = reverse('finances:expense_delete', args=[self.expense.pk])

    def test_expense_delete_view_not_authenticated(self):
        self.assertRequiresAuthentication(self.url)

    def test_expense_delete_view_authenticated(self):

        self.authenticate_user()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Expense.objects.filter(pk=self.expense.pk).exists())
