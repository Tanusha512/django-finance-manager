from django.urls import path
from . import views

urlpatterns = [
    path('wallets/', views.wallets_view, name='wallets'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('goals/', views.goals_view, name='goals'),
    path('categories/', views.categories_view, name='categories'),
]