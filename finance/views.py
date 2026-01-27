from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
 
from .models import Wallet, Transaction, Goal, Category 
from .forms import WalletForm, TransactionForm 
 
 
@login_required 
def dashboard_view(request): 
    return render(request, 'finance/dashboard.html', { 
        'wallets': Wallet.objects.filter(user=request.user), 
        'transactions': Transaction.objects.filter(wallet__user=request.user), 
        'goals': Goal.objects.filter(user=request.user), 
    }) 
 
 
@login_required 
def wallets_view(request): 
    wallets = Wallet.objects.filter(user=request.user) 
    form = WalletForm(request.POST or None) 
 
    if request.method == 'POST' and form.is_valid(): 
        wallet = form.save(commit=False) 
        wallet.user = request.user 
        wallet.save() 
        return redirect('wallets') 
 
    return render(request, 'finance/wallets.html', {'wallets': wallets, 'form': form}) 
 
 
@login_required 
def transactions_view(request): 
    transactions = Transaction.objects.filter(wallet__user=request.user) 
    form = TransactionForm(request.POST or None) 
 
    if request.method == 'POST' and form.is_valid(): 
        form.save() 
        return redirect('transactions') 
 
    return render(request, 'finance/transactions.html', {'transactions': transactions, 'form': form}) 
 
 
@login_required 
def goals_view(request): 
    goals = Goal.objects.filter(user=request.user) 
 
    if request.method == 'POST': 
        Goal.objects.create( 
            user=request.user, 
            title=request.POST['title'], 
            target_amount=request.POST['target_amount'], 
            deadline=request.POST['deadline'], 
            url=request.POST.get('url') 
        ) 
        return redirect('goals') 
 
    return render(request, 'finance/goals.html', {'goals': goals}) 
 
 
@login_required 
def categories_view(request): 
    categories = Category.objects.filter(user=request.user) 
 
    if request.method == 'POST': 
        Category.objects.create( 
            user=request.user, 
            name=request.POST['name'], 
            type=request.POST['type'] 
        ) 
        return redirect('categories') 
 
    return render(request, 'finance/categories.html', {'categories': categories}) 
 
 
def login_view(request): 
    form = AuthenticationForm(request, data=request.POST or None) 
 
    if request.method == 'POST' and form.is_valid(): 
        login(request, form.get_user()) 
        return redirect('dashboard') 
 
    return render(request, 'finance/login.html', {'form': form}) 
 
 
def register_view(request): 
    form = UserCreationForm(request.POST or None) 
 
    if request.method == 'POST' and form.is_valid(): 
        login(request, form.save()) 
        return redirect('dashboard') 
 
    return render(request, 'finance/register.html', {'form': form}) 
 
 
def logout_view(request): 
    logout(request) 
    return redirect('login')