from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=50, verbose_name="Название кошелька")
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Баланс")
    currency = models.CharField(max_length=10, default="RUB", verbose_name="Валюта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def str(self):
        return f"{self.name} ({self.balance} {self.currency})"

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=50, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    def str(self):
        return self.name

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=100, verbose_name="Название цели")
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Целевая сумма")
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Накоплено")
    deadline = models.DateField(null=True, blank=True, verbose_name="Срок")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")

    def str(self):
        return self.title

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

    def str(self):
        return f"{self.transaction_type} {self.amount} в {self.wallet.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    bio = models.TextField(blank=True, verbose_name="О себе")

    def str(self):
        return self.user.username