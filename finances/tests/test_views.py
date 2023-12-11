from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from finances.models import Expense


class ExpenseIndexViewTest(TestCase):
    fixtures = ['expenses.json']

    def test_expense_index_view(self):

        url = reverse('finances:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ExpenseDetailViewTest(TestCase):
    fixtures = ['expenses.json']

    def test_expense_detail_view(self):

        url = reverse('finances:detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
