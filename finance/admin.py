from django.contrib import admin
from .models import Profile, Wallet, Category, Transaction, Goal

# Для каждой модели добавим отображение полей в списке
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'category', 'amount', 'date')
    list_filter = ('wallet', 'category', 'date')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'target_amount', 'deadline', 'url')
    list_filter = ('user', 'deadline')