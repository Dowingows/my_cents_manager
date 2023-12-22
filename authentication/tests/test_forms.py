from django.contrib.auth.models import User
from django.test import TestCase

from authentication.forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    def test_custom_user_creation_form_valid_data(self):
        # Dados válidos para criar um novo usuário
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = CustomUserCreationForm(data=form_data)

        # Verificar se o formulário é válido
        self.assertTrue(form.is_valid())

        # Salvar o usuário (isso geralmente acontece em uma view após a validação do formulário)
        user = form.save()

        # Verificar se o usuário foi criado corretamente
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first(), user)

    def test_custom_user_creation_form_invalid_data(self):
        # Dados inválidos (password1 e password2 não correspondem)
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }

        form = CustomUserCreationForm(data=form_data)

        # Verificar se o formulário é inválido
        self.assertFalse(form.is_valid())

        # Verificar se há erros específicos no formulário (neste caso, relacionados às senhas)
        self.assertIn('password2', form.errors)
        self.assertIn(
            'The two password fields didn’t match.',
            form.errors['password2'][0],
        )
