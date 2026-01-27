from django import forms
from .models import Wallet, Transaction

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance']
        labels = {
            'name': 'Название кошелька',
            'balance': 'Баланс',
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['wallet', 'category', 'amount', 'comment']
        labels = {
            'wallet': 'Кошелек',
            'category': 'Категория',
            'amount': 'Сумма',
            'comment': 'Комментарий',
        }