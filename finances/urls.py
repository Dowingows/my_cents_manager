from django.urls import path

from . import views

app_name = 'finances'

urlpatterns = [
    path('expense', views.IndexView.as_view(), name='index'),
    path('expense/new', views.ExpenseCreateView.as_view(), name='create'),
    path('expense/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path(
        'expenses/<int:pk>/edit/',
        views.ExpenseUpdateView.as_view(),
        name='edit',
    ),
    path('expenses/<int:pk>/delete/', views.delete, name='delete'),
]
