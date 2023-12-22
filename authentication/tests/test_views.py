from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SigninViewTest(TestCase):
    def setUp(self):
        # Crie um usuário de teste
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_signin_success(self):

        success = self.client.login(
            username='testuser', password='testpassword'
        )

        self.assertTrue(success)

    def test_expense_index_view_not_authenticated_redirected_to_login(self):
        # Obter a URL reversa para a view
        url = reverse('finances:expense_index')

        # Fazer a solicitação para a view sem autenticar
        response = self.client.get(url)

        # Verificar se o código de status é 302 (redirecionamento)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('authentication:signin') + f'?next={url}'
        )

    def test_signin_view_unauthenticated_user_render_template(self):
        # Fazer a solicitação para a view de signin sem autenticar
        response = self.client.get(reverse('authentication:signin'))

        # Verificar se o código de status é 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar se o template correto está sendo renderizado
        self.assertTemplateUsed(response, 'signin.html')

    def test_signin_view_invalid_credentials(self):
        # Dados inválidos para autenticação
        invalid_credentials = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

        # Fazer a solicitação para a view de signin com credenciais inválidas
        response = self.client.post(
            reverse('authentication:signin'), data=invalid_credentials
        )

        # Verificar se o código de status é 200 (OK) - o usuário não é autenticado
        self.assertEqual(response.status_code, 200)

        # Verificar se o template correto está sendo renderizado
        self.assertTemplateUsed(response, 'signin.html')

        # Verificar se o formulário de autenticação possui erros
        self.assertTrue('form' in response.context)
        self.assertTrue(
            isinstance(response.context['form'], AuthenticationForm)
        )

        self.assertTrue(
            'Please enter a correct username and password.'
            in str(response.context['form'].errors)
        )
