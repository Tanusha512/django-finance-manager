from django import forms
from .models import Wallet, Transaction, Category

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance']
        labels = {
            'name': 'Название кошелька',
            'balance': 'Баланс',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['wallet', 'category', 'amount', 'comment']
        labels = {
            'wallet': 'Кошелёк',
            'category': 'Категория',
            'amount': 'Сумма',
            'comment': 'Комментарий',
        }
        widgets = {
            'wallet': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        } 