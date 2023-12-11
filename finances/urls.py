from django.urls import path

from . import views

app_name = 'finances'

urlpatterns = [
    path('expense', views.IndexView.as_view(), name='index'),
    path('expense/new', views.expense_create, name='create'),
    path('expense/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('expenses/<int:pk>/edit/', views.edit, name='edit'),
    path('expenses/<int:pk>/delete/', views.delete, name='delete'),
]
