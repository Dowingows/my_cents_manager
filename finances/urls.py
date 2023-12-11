from django.urls import path

from . import views

app_name = 'finances'

urlpatterns = [
    path('expense', views.IndexView.as_view(), name='index'),
    path('expense/<int:pk>/', views.DetailView.as_view(), name='detail'),
]
