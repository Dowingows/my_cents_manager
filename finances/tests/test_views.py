from django.test import TestCase
from django.urls import reverse, reverse_lazy

from finances.models import Expense, Income, Transaction

from .mixins import AuthenticationTestMixin


class ExpenseIndexViewTest(AuthenticationTestMixin, TestCase):
    def test_expense_index_view_not_authenticated(self):

        url = reverse('finances:expense_index')

        self.assertRequiresAuthentication(url)

    def test_expense_index_view_authenticated(self):

        self.authenticate_user()

        url = reverse('finances:expense_index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class ExpenseDetailViewTest(AuthenticationTestMixin, TestCase):
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


class ExpenseCreateViewTest(AuthenticationTestMixin, TestCase):
    def test_expense_create_view_not_authenticated(self):

        url = reverse('finances:expense_create')

        self.assertRequiresAuthentication(url)

    def test_expense_create_view_authenticated_with_payment_date(self):
        self.authenticate_user()

        form_data = {
            'name': 'Test Expense',
            'amount': 100.00,
            'payment_date': '2023-12-15',
            'due_date': '2023-12-20',
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

        # Verifique se uma transação foi criada
        self.assertTrue(expense.transaction is not None)
        self.assertEqual(expense.transaction.name, 'Test Expense')
        self.assertEqual(expense.transaction.amount, -100.00)
        self.assertEqual(
            str(expense.transaction.transaction_date), '2023-12-15'
        )
        self.assertEqual(expense.transaction.transaction_type, 'expense')

    def test_expense_create_view_authenticated_without_payment_date(self):
        self.authenticate_user()

        form_data = {
            'name': 'Test Expense',
            'amount': 100.00,
            'due_date': '2023-12-20',
        }

        response = self.client.post(
            reverse('finances:expense_create'), data=form_data
        )

        self.assertRedirects(response, reverse('finances:expense_index'))

        self.assertTrue(Expense.objects.filter(name='Test Expense').exists())

        expense = Expense.objects.get(name='Test Expense')
        self.assertEqual(expense.amount, 100.00)
        self.assertIsNone(expense.payment_date)
        self.assertEqual(str(expense.due_date), '2023-12-20')

        # Verifique se nenhuma transação foi criada
        self.assertIsNone(expense.transaction)


class ExpenseUpdateViewTest(AuthenticationTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.expense = Expense.objects.create(
            user=self.test_user,
            name='Test Expense',
            amount=50.00,
            due_date='2023-12-31',
            payment_date='2023-12-30',
        )

        self.transaction = Transaction.objects.create(
            user=self.test_user,
            name=self.expense.name,
            amount=self.expense.amount,
            transaction_date=self.expense.payment_date,
            transaction_type='expense',
        )

        self.expense.transaction = self.transaction

        self.expense.save()

        self.url = reverse_lazy(
            'finances:expense_edit', args=(self.expense.pk,)
        )

    def test_expense_update_view_not_authenticated(self):
        self.assertRequiresAuthentication(self.url)

    def test_expense_update_view_authenticated_with_payment_date(self):
        self.authenticate_user()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        updated_data = {
            'name': 'Updated Expense',
            'amount': 75.00,
            'due_date': '2023-02-01',
            'payment_date': '2024-01-01',
        }

        response = self.client.post(self.url, data=updated_data)

        self.assertRedirects(response, reverse('finances:expense_index'))

        updated_expense = Expense.objects.get(pk=self.expense.pk)

        self.assertEqual(updated_expense.name, updated_data['name'])
        self.assertEqual(updated_expense.amount, updated_data['amount'])
        self.assertEqual(
            str(updated_expense.due_date), updated_data['due_date']
        )
        self.assertEqual(
            str(updated_expense.payment_date), updated_data['payment_date']
        )

        # Verifique se a transação foi atualizada
        self.assertEqual(
            updated_expense.transaction.name, updated_data['name']
        )
        self.assertEqual(
            updated_expense.transaction.amount, -updated_data['amount']
        )
        self.assertEqual(
            str(updated_expense.transaction.transaction_date),
            updated_data['payment_date'],
        )

    def test_expense_update_view_authenticated_without_payment_date(self):
        self.authenticate_user()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        updated_data = {
            'name': 'Updated Expense',
            'amount': 75.00,
            'due_date': '2023-02-01',
        }

        response = self.client.post(self.url, data=updated_data)

        self.assertRedirects(response, reverse('finances:expense_index'))

        updated_expense = Expense.objects.get(pk=self.expense.pk)

        self.assertEqual(updated_expense.name, updated_data['name'])
        self.assertEqual(updated_expense.amount, updated_data['amount'])
        self.assertEqual(
            str(updated_expense.due_date), updated_data['due_date']
        )
        self.assertIsNone(updated_expense.payment_date)

        # Verifique se a transação foi removida
        self.assertFalse(
            Transaction.objects.filter(pk=self.transaction.pk).exists()
        )


class ExpenseDeleteViewTest(AuthenticationTestMixin, TestCase):
    def setUp(self):

        super().setUp()

        self.expense = Expense.objects.create(
            name='Test Delete',
            amount=50.00,
            due_date='2023-12-31',
            payment_date='2023-12-31',
            user=self.test_user,
        )

        self.transaction = Transaction.objects.create(
            user=self.test_user,
            name=self.expense.name,
            amount=self.expense.amount,
            transaction_date=self.expense.payment_date,
            transaction_type='expense',
        )

        self.expense.transaction = self.transaction

        self.expense.save()

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
        self.assertFalse(
            Transaction.objects.filter(pk=self.transaction.pk).exists()
        )


class IncomeIndexViewTest(AuthenticationTestMixin, TestCase):
    def test_income_index_view_not_authenticated(self):
        url = reverse('finances:income_index')
        self.assertRequiresAuthentication(url)

    def test_income_index_view_authenticated(self):
        self.authenticate_user()

        url = reverse('finances:income_index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class IncomeCreateViewTest(AuthenticationTestMixin, TestCase):
    def test_income_create_view_not_authenticated(self):
        url = reverse('finances:income_create')
        self.assertRequiresAuthentication(url)

    def test_income_create_view_authenticated_with_received_date(self):
        self.authenticate_user()

        response = self.client.get(reverse('finances:income_create'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'name': 'Test Income',
            'amount': 150.00,
            'received_date': '2023-12-10',
            'expected_date': '2023-12-15',
            'user_id': self.test_user.pk,
        }

        response = self.client.post(
            reverse('finances:income_create'), data=form_data
        )

        self.assertRedirects(response, reverse('finances:income_index'))

        self.assertTrue(Income.objects.filter(name='Test Income').exists())

        income = Income.objects.get(name='Test Income')
        self.assertEqual(income.amount, 150.00)
        self.assertEqual(str(income.received_date), '2023-12-10')
        self.assertEqual(str(income.expected_date), '2023-12-15')

        # Verifique se uma transação foi criada
        self.assertTrue(income.transaction is not None)
        self.assertEqual(income.transaction.name, form_data['name'])
        self.assertEqual(income.transaction.amount, form_data['amount'])
        self.assertEqual(
            str(income.transaction.transaction_date),
            form_data['received_date'],
        )
        self.assertEqual(income.transaction.transaction_type, 'income')


class IncomeUpdateViewTest(AuthenticationTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.income = Income.objects.create(
            user=self.test_user,
            name='Test Income',
            amount=75.00,
            expected_date='2023-12-31',
            received_date='2023-12-30',
        )

        self.transaction = Transaction.objects.create(
            user=self.test_user,
            name=self.income.name,
            amount=self.income.amount,
            transaction_date=self.income.received_date,
            transaction_type='income',
        )

        self.income.transaction = self.transaction

        self.income.save()

        self.url = reverse_lazy('finances:income_edit', args=(self.income.pk,))

    def test_income_update_view_not_authenticated(self):
        url = reverse('finances:income_edit', args=(1,))
        self.assertRequiresAuthentication(url)

    def test_income_update_view_authenticated_with_received_date(self):

        self.authenticate_user()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        updated_data = {
            'name': 'Updated Income',
            'amount': 100.00,
            'expected_date': '2024-02-01',
            'received_date': '2024-01-01',
        }

        response = self.client.post(self.url, data=updated_data)

        self.assertRedirects(response, reverse('finances:income_index'))

        updated_income = Income.objects.get(pk=self.income.pk)

        self.assertEqual(updated_income.name, updated_data['name'])
        self.assertEqual(updated_income.amount, updated_data['amount'])
        self.assertEqual(
            str(updated_income.expected_date), updated_data['expected_date']
        )
        self.assertEqual(
            str(updated_income.received_date), updated_data['received_date']
        )

        # Verifique se a transação foi atualizada
        self.assertEqual(updated_income.transaction.name, updated_data['name'])
        self.assertEqual(
            updated_income.transaction.amount, updated_data['amount']
        )
        self.assertEqual(
            str(updated_income.transaction.transaction_date),
            updated_data['received_date'],
        )


class IncomeDeleteViewTest(AuthenticationTestMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.income = Income.objects.create(
            name='Test Delete',
            amount=50.00,
            expected_date='2023-12-31',
            received_date='2023-12-31',
            user=self.test_user,
        )

        self.url = reverse('finances:income_delete', args=[self.income.pk])

    def test_income_delete_view_not_authenticated(self):
        self.assertRequiresAuthentication(self.url)

    def test_income_delete_view_authenticated(self):
        self.authenticate_user()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Income.objects.filter(pk=self.income.pk).exists())
