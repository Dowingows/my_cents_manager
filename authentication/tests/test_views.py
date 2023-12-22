from django.conf import settings
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


class SignupViewTest(TestCase):
    def test_signup_view_valid_data(self):
        # Dados válidos para criar um novo usuário
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        # Fazer a solicitação para a view de signup com dados válidos
        response = self.client.post(
            reverse('authentication:signup'), data=form_data
        )

        # Verificar se o código de status é 302 (redirecionamento) para a página configurada em success_url
        self.assertEqual(response.status_code, 302)

        # Verificar se o usuário foi criado corretamente
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'testuser')

        # Verificar se o redirecionamento ocorre para a página configurada em success_url
        self.assertRedirects(response, reverse('authentication:signin'))

    def test_signup_view_invalid_data(self):
        # Dados inválidos (password1 e password2 não correspondem)
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }

        # Fazer a solicitação para a view de signup com dados inválidos
        response = self.client.post(
            reverse('authentication:signup'), data=form_data
        )

        # Verificar se o código de status é 200 (OK) - o formulário é inválido
        self.assertEqual(response.status_code, 200)

        # Verificar se o template correto está sendo renderizado
        self.assertTemplateUsed(response, 'signup.html')

        # Verificar se há erros específicos no formulário (neste caso, relacionados às senhas)
        self.assertIn('password2', response.context['form'].errors)
        self.assertIn(
            'The two password fields didn’t match.',
            response.context['form'].errors['password2'][0],
        )


class SignoutViewTest(TestCase):
    def setUp(self):
        # Crie um usuário de teste
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_signout_authenticated_user_logout(self):
        # Autenticar o usuário
        self.client.login(username='testuser', password='testpassword')

        # Fazer a solicitação para a view de logout (signout)
        response = self.client.get(reverse('authentication:signout'))

        # Verificar se o código de status é 302 (redirecionamento) para a página configurada em settings.LOGOUT_REDIRECT_URL
        self.assertEqual(response.status_code, 302)

        # Verificar se o usuário foi desautenticado
        self.assertEqual(str(response.wsgi_request.user), 'AnonymousUser')

        # Verificar se o redirecionamento ocorre para a página configurada em settings.LOGOUT_REDIRECT_URL
        self.assertRedirects(response, settings.LOGOUT_REDIRECT_URL)
