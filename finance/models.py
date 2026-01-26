from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    bio = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def str(self):
        return self.user.username


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Название кошелька")
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Баланс")

    class Meta:
        verbose_name = "Кошелёк"
        verbose_name_plural = "Кошельки"

    def str(self):
        return f"{self.name} — {self.balance}"


class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название категории")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def str(self):
        return self.name


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="Кошелёк")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def str(self):
        return f"{self.amount} — {self.category}"


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Название цели")
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Целевая сумма")
    deadline = models.DateField(verbose_name="Срок достижения")
    url = models.URLField(blank=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def str(self):
        return self.title