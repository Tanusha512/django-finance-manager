from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('wallets/', views.wallets, name='wallets'),
    path('transactions/', views.transactions, name='transactions'),
    path('goals/', views.goals, name='goals'),
    path('categories/', views.categories, name='categories'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]