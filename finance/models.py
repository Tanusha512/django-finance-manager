from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=50, verbose_name="Название кошелька")
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Баланс")
    currency = models.CharField(max_length=10, default="RUB", verbose_name="Валюта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency})"
    
    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"
        ordering = ['-created_at']


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=50, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=100, verbose_name="Название цели")
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Целевая сумма")
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Накоплено")
    deadline = models.DateField(null=True, blank=True, verbose_name="Срок")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"
        ordering = ['-deadline', 'title']


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Доход'),
        ('expense', 'Расход')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="Кошелек")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="Тип")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    date = models.DateTimeField(default=timezone.now, verbose_name="Дата")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.get_transaction_type_display()} {self.amount} {self.wallet.currency}"
    
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-date']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    bio = models.TextField(blank=True, verbose_name="О себе")

    def __str__(self):
        return f"Профиль {self.user.username}"
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
