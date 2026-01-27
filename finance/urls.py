from django.urls import path 
from . import views 
 
urlpatterns = [ 
    path('', views.dashboard_view, name='dashboard'), 
    path('wallets/', views.wallets_view, name='wallets'), 
    path('transactions/', views.transactions_view, name='transactions'), 
    path('goals/', views.goals_view, name='goals'), 
    path('categories/', views.categories_view, name='categories'), 
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'), 
]