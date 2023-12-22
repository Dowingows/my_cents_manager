from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ExpenseIndexViewTest(TestCase):
    fixtures = ['users.json', 'expenses.json']

    def test_expense_index_view_authenticated(self):
        # cria usuário de teste
        User.objects.create_user(username='testuser', password='testpassword')

        # Autenticar o usuário
        self.client.login(username='testuser', password='testpassword')

        # Obter a URL reversa para a view
        url = reverse('finances:expense_index')

        # Fazer a solicitação para a view autenticada
        response = self.client.get(url)

        # Verificar se o código de status é 200 (OK)
        self.assertEqual(response.status_code, 200)
