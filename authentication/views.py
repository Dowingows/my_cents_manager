from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy


def home(request):
    return render(request, 'home.html')


class SigninView(LoginView):
    template_name = 'signin.html'
    next_page = reverse_lazy('authentication:home')


def signup(request):
    return render(request, 'signup.html')
