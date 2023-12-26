from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTestMixin:
    def setUp(self):
        # Cria um usuário de teste
        self.test_user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def authenticate_user(self):
        # Autentica o usuário
        self.client.login(username='testuser', password='testpassword')

    def assertRequiresAuthentication(self, url):

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('authentication:signin') + f'?next={url}'
        )
