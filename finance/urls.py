from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'finance'

urlpatterns = [
    # ========== Главная и дашборд ==========
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ========== Кошельки ==========
    path('wallets/', views.wallets, name='wallets'),
    path('wallets/add/', views.wallet_add, name='wallet_add'),
    path('wallets/<int:pk>/edit/', views.wallet_edit, name='wallet_edit'),
    path('wallets/<int:pk>/delete/', views.wallet_delete, name='wallet_delete'),
    
    # ========== Транзакции ==========
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/add/', views.transaction_add, name='transaction_add'),
    path('transactions/<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    
    # ========== Категории ==========
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # ========== Цели ==========
    path('goals/', views.goals, name='goals'),
    path('goals/add/', views.goal_add, name='goal_add'),
    path('goals/<int:pk>/edit/', views.goal_edit, name='goal_edit'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
    
    # ========== Профиль ==========
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # ========== Аутентификация ==========
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Используем кастомный logout
]

# Альтернативно, если хотите использовать встроенный LogoutView:
# path('logout/', auth_views.LogoutView.as_view(next_page='finance:login'), name='logout'),