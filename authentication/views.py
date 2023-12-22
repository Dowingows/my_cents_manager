from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class SigninView(LoginView):
    template_name = 'signin.html'
    next_page = reverse_lazy('finances:home')


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('authentication:signin')


def signout(request):
    logout(request)

    return redirect(f'{settings.LOGOUT_REDIRECT_URL}')
