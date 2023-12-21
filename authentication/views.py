from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


def home(request):
    return render(request, 'home.html')


class SigninView(LoginView):
    template_name = 'signin.html'
    next_page = reverse_lazy('authentication:home')


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('authentication:signin')
