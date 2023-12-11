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


class ExpenseCreateViewTest(TestCase):
    def test_expense_create_view(self):
        # Verifica se a view retorna o código de status 200 (OK) para uma solicitação GET
        response = self.client.get(reverse('finances:create'))
        self.assertEqual(response.status_code, 200)

        # Cria um dicionário de dados simulando os dados do formulário
        form_data = {
            'name': 'Test Expense',
            'amount': '100.00',
            'payment_date': '2023-12-15',
            'due_date': '2023-12-20',
        }

        # Envia uma solicitação POST com os dados do formulário
        response = self.client.post(reverse('finances:create'), data=form_data)

        # Verifica se a view redireciona corretamente após uma submissão bem-sucedida
        self.assertRedirects(response, reverse('finances:index'))

        # Verifica se um novo objeto Expense foi criado no banco de dados
        self.assertTrue(Expense.objects.filter(name='Test Expense').exists())

        # Verifica se o objeto Expense criado tem os dados corretos
        expense = Expense.objects.get(name='Test Expense')
        self.assertEqual(expense.amount, 100.00)
        self.assertEqual(str(expense.payment_date), '2023-12-15')
        self.assertEqual(str(expense.due_date), '2023-12-20')
