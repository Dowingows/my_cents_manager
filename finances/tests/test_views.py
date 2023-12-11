from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from finances.models import Expense


class ExpenseDetailViewTest(TestCase):
    def setUp(self):
        # Crie uma despesa para usar nos testes
        future_due_date = timezone.now().date() + timezone.timedelta(days=7)
        self.expense = Expense.objects.create(
            name='Future Expense',
            amount=50.00,
            due_date=future_due_date,
            payment_date=None,
        )

    def test_detail_view_for_pending_expense(self):
        # Acesse a página de detalhes da despesa
        response = self.client.get(
            reverse('finances:detail', args=(self.expense.id,))
        )

        # Verifique se a resposta é bem-sucedida (status code 200)
        self.assertEqual(response.status_code, 200)

        # Verifique se a despesa está no contexto
        self.assertEqual(response.context['expense'], self.expense)

        # Verifique se o template correto está sendo usado
        self.assertTemplateUsed(response, 'expense/detail.html')

    def test_detail_view_for_nonexistent_expense(self):
        # Acesse a página de detalhes de uma despesa inexistente
        response = self.client.get(reverse('finances:detail', args=(999,)))

        # Verifique se a resposta retorna um status code 404, pois a despesa não existe
        self.assertEqual(response.status_code, 404)
