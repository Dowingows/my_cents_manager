from django.test import TestCase
from django.urls import reverse

from finances.models import Expense

from .mixins import AuthenticationMixin


class ExpenseIndexViewTest(AuthenticationMixin, TestCase):
    def test_expense_index_view_authenticated(self):

        self.authenticate_user()

        url = reverse('finances:expense_index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_expense_index_view_not_authenticated_redirected_to_login(self):

        url = reverse('finances:expense_index')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('authentication:signin') + f'?next={url}'
        )


class ExpenseDetailViewTest(AuthenticationMixin, TestCase):
    def test_expense_detail_view_not_authenticated(self):

        url = reverse('finances:expense_detail', args=(1,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('authentication:signin') + f'?next={url}'
        )

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
