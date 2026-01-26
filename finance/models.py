from django.db import models 
from django.contrib.auth.models import User 
 
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True) 
    bio = models.TextField(blank=True) 
 
    def str(self): 
        return self.user.username 
 
 
class Wallet(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100) 
    balance = models.DecimalField(max_digits=10, decimal_places=2) 
 
    def str(self): 
        return f"{self.name} — {self.balance}" 
 
 
class Category(models.Model): 
    TYPE_CHOICES = [ 
        ('income', 'Доход'), 
        ('expense', 'Расход'), 
    ] 
 
    name = models.CharField(max_length=100) 
    type = models.CharField(max_length=10, choices=TYPE_CHOICES) 
 
    def str(self): 
        return self.name 
 
 
class Transaction(models.Model): 
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    date = models.DateTimeField(auto_now_add=True) 
    comment = models.TextField(blank=True) 
 
    def str(self): 
        return f"{self.amount} — {self.category}" 
 
 
class Goal(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=200) 
    target_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    deadline = models.DateField() 
    url = models.URLField(blank=True) 
 
    def str(self): 
        return self.title