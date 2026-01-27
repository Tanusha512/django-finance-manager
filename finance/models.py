from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField("Название кошелька", max_length=100)
    balance = models.DecimalField("Баланс", max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"

    def str(self):
        return self.name


class Category(models.Model):
    TYPE_CHOICES = (
        ('income', 'Доход'),
        ('expense', 'Расход'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField("Название категории", max_length=100)
    type = models.CharField("Тип категории", max_length=10, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def str(self):
        return self.name


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="Кошелек")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    amount = models.DecimalField("Сумма", max_digits=12, decimal_places=2)
    comment = models.TextField("Комментарий", blank=True)
    date = models.DateTimeField("Дата и время", auto_now_add=True)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def str(self):
        return f"{self.amount} ₽ — {self.category}"


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField("Название цели", max_length=200)
    target_amount = models.DecimalField("Целевая сумма", max_digits=12, decimal_places=2)
    deadline = models.DateField("Срок достижения")
    url = models.URLField("Ссылка (опционально)", blank=True)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def str(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField("Аватар", upload_to='avatars/', blank=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def str(self):
        return self.user.username