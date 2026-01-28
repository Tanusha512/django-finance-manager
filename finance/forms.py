from django import forms
from .models import Wallet, Transaction, Category, Goal, Profile

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название кошелька'
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Название',
            'balance': 'Начальный баланс',
            'currency': 'Валюта',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Стандартные валюты
        self.fields['currency'].choices = [
            ('RUB', 'Рубли (RUB)'),
            ('USD', 'Доллары (USD)'),
            ('EUR', 'Евро (EUR)'),
            ('KZT', 'Тенге (KZT)'),
            ('BYN', 'Белорусские рубли (BYN)'),
        ]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['wallet', 'category', 'transaction_type', 'amount', 'date', 'description']
        widgets = {
            'wallet': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание транзакции...'
            }),
        }
        labels = {
            'wallet': 'Кошелек',
            'category': 'Категория',
            'transaction_type': 'Тип',
            'amount': 'Сумма',
            'date': 'Дата и время',
            'description': 'Описание',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Фильтруем кошельки и категории только для текущего пользователя
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название категории'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание категории...'
            }),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о себе...'
            }),
        }
        labels = {
            'avatar': 'Аватар',
            'bio': 'О себе',
        }


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'target_amount', 'current_amount', 'deadline', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название цели'
            }),
            'target_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'current_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Название цели',
            'target_amount': 'Целевая сумма',
            'current_amount': 'Уже накоплено',
            'deadline': 'Срок достижения',
            'category': 'Категория',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)


# Форма для быстрого добавления транзакции (упрощенная)
class QuickTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'category', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма',
                'step': '0.01'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)