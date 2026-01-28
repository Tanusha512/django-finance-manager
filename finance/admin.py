from django.contrib import admin
from django.utils.html import format_html
from .models import Wallet, Category, Transaction, Goal, Profile

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance', 'currency', 'created_at')
    list_filter = ('currency', 'created_at', 'user')
    search_fields = ('name', 'user__username')
    date_hierarchy = 'created_at'
    
    # Русские названия полей в админке
    list_display_labels = {
        'name': 'Название',
        'user': 'Пользователь',
        'balance': 'Баланс',
        'currency': 'Валюта',
        'created_at': 'Дата создания',
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'short_description')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')
    
    def short_description(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    short_description.short_description = 'Описание'
    
    # Русские названия
    list_display_labels = {
        'name': 'Название',
        'user': 'Пользователь',
        'short_description': 'Описание',
    }


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('formatted_amount', 'transaction_type_display', 'user', 
                    'wallet', 'category', 'date', 'short_description')
    list_filter = ('transaction_type', 'date', 'category', 'wallet', 'user')
    search_fields = ('description', 'user__username', 'wallet__name', 'category__name')
    date_hierarchy = 'date'
    ordering = ('-date',)
    
    def formatted_amount(self, obj):
        color = 'green' if obj.transaction_type == 'income' else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, obj.amount, obj.wallet.currency
        )
    formatted_amount.short_description = 'Сумма'
    
    def transaction_type_display(self, obj):
        display_text = obj.get_transaction_type_display()
        color = 'success' if obj.transaction_type == 'income' else 'danger'
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, display_text
        )
    transaction_type_display.short_description = 'Тип'
    
    def short_description(self, obj):
        if obj.description:
            return obj.description[:30] + '...' if len(obj.description) > 30 else obj.description
        return '-'
    short_description.short_description = 'Описание'
    
    # Русские названия
    list_display_labels = {
        'formatted_amount': 'Сумма',
        'transaction_type_display': 'Тип',
        'user': 'Пользователь',
        'wallet': 'Кошелек',
        'category': 'Категория',
        'date': 'Дата',
        'short_description': 'Описание',
    }


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'target_amount', 'current_amount', 'deadline', 'category')
    list_filter = ('deadline', 'category', 'user')
    search_fields = ('title', 'user__username')
    date_hierarchy = 'deadline'
    
    # Русские названия
    list_display_labels = {
        'title': 'Название',
        'user': 'Пользователь',
        'target_amount': 'Целевая сумма',
        'current_amount': 'Накоплено',
        'deadline': 'Срок',
        'category': 'Категория',
    }


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_bio', 'avatar_preview')
    search_fields = ('user__username', 'bio')
    
    def short_bio(self, obj):
        if obj.bio:
            return obj.bio[:50] + '...' if len(obj.bio) > 50 else obj.bio
        return '-'
    short_bio.short_description = 'О себе'
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%;" />',
                obj.avatar.url
            )
        return '-'
    avatar_preview.short_description = 'Аватар'
    
    # Русские названия
    list_display_labels = {
        'user': 'Пользователь',
        'short_bio': 'О себе',
        'avatar_preview': 'Аватар',
    }


# Настройки админки на русском
admin.site.site_header = '💰 Финансовый менеджер - Администрирование'
admin.site.site_title = 'Финансовый менеджер'
admin.site.index_title = 'Панель управления'