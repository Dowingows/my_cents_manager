from django.urls import path

from . import views

app_name = 'finances'

urlpatterns = [
    path('', views.MonthlyView.as_view(), name='home'),
    path('expense', views.IndexView.as_view(), name='expense_index'),
    path(
        'expense/new', views.ExpenseCreateView.as_view(), name='expense_create'
    ),
    path(
        'expense/monthly',
        views.ExpenseMonthlyView.as_view(),
        name='expense_monthly',
    ),
    path(
        'expense/<int:pk>/', views.DetailView.as_view(), name='expense_detail'
    ),
    path(
        'expenses/<int:pk>/edit/',
        views.ExpenseUpdateView.as_view(),
        name='expense_edit',
    ),
    path(
        'expenses/<int:pk>/delete/',
        views.ExpenseDeleteView.as_view(),
        name='expense_delete',
    ),
    path('income', views.IncomeIndexView.as_view(), name='income_index'),
    path('income/new', views.IncomeCreateView.as_view(), name='income_create'),
    path(
        'incomes/<int:pk>/edit/',
        views.IncomeUpdateView.as_view(),
        name='income_edit',
    ),
    path(
        'incomes/<int:pk>/delete/',
        views.IncomeDeleteView.as_view(),
        name='income_delete',
    ),
]
