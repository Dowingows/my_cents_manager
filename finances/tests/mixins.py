from django.contrib.auth.models import User


class AuthenticationMixin:
    def setUp(self):
        # Cria um usuário de teste
        self.test_user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def authenticate_user(self):
        # Autentica o usuário
        self.client.login(username='testuser', password='testpassword')
