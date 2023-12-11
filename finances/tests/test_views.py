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


class ExpenseUpdateViewTest(TestCase):
    fixtures = ['expenses.json']

    def test_expense_update_view(self):

        # Verifica se a view retorna o código de status 200 (OK) para uma solicitação GET
        url = reverse('finances:edit', args=(1,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Cria um dicionário de dados simulando os dados do formulário para atualização
        updated_data = {
            'name': 'Updated Expense',
            'amount': '75.00',
            'payment_date': '2023-12-15',
            'due_date': '2023-12-20',
        }

        # Envia uma solicitação POST com os dados do formulário para atualização
        response = self.client.post(
            reverse('finances:edit', args=(1,)), data=updated_data
        )

        # Verifica se a view redireciona corretamente após uma atualização bem-sucedida
        self.assertRedirects(response, reverse('finances:index'))


class ExpenseDeleteViewTest(TestCase):
    def setUp(self):
        # Cria uma instância de Expense para ser usada nos testes
        self.expense = Expense.objects.create(
            name='Test Delete',
            amount=50.00,
            due_date='2023-12-31',
            payment_date='2023-12-31',
        )
        # Define a URL de exclusão com base no ID da despesa criada
        self.delete_url = reverse('finances:delete', args=[self.expense.pk])

    def test_expense_delete_view(self):
        # Verifica se a view retorna o código de status 302 (redirecionamento temporário) para uma solicitação GET
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)

        # Verifica se a despesa foi removida do banco de dados
        self.assertFalse(Expense.objects.filter(name='Test Delete').exists())

        # Verifica se a view redireciona corretamente após uma exclusão bem-sucedida
        self.assertRedirects(response, reverse('finances:index'))
