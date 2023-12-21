from django.urls import path

from . import views

app_name = 'authentication'


urlpatterns = [
    path('', views.home, name='home'),
    path(
        'signin',
        views.SigninView.as_view(template_name='signin.html'),
        name='signin',
    ),
    path('signup', views.signup, name='signup'),
]
