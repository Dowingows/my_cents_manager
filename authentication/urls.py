from django.urls import path

from . import views

app_name = 'authentication'


urlpatterns = [
    path('', views.home, name='home'),
    path(
        'signin',
        views.SigninView.as_view(),
        name='signin',
    ),
    path('signup', views.SignupView.as_view(), name='signup'),
]
