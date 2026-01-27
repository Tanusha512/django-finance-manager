from django import forms
from .models import Wallet, Transaction, Category, Goal

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

 
@login_required 
def goals_view(request): 
    goals = Goal.objects.filter(user=request.user) 
 
    if request.method == 'POST': 
        title = request.POST.get('title') 
        target_amount = request.POST.get('target_amount') 
        deadline = request.POST.get('deadline') 
        url = request.POST.get('url') 
 
        if title and target_amount and deadline: 
            Goal.objects.create( 
                user=request.user, 
                title=title, 
                target_amount=target_amount, 
                deadline=deadline, 
                url=url 
            ) 
            return redirect('goals') 
 
    return render(request, 'finance/goals.html', {'goals': goals}) 
 
 
@login_required 
def categories_view(request): 
    categories = Category.objects.filter(user=request.user) 
 
    if request.method == 'POST': 
        name = request.POST.get('name') 
        type_ = request.POST.get('type') 
 
        if name and type_: 
            Category.objects.create( 
                user=request.user, 
                name=name, 
                type=type_ 
            ) 
            return redirect('categories') 
 
    return render(request, 'finance/categories.html', {'categories': categories})