from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Wallet, Transaction, Goal, Category, Profile
from .forms import WalletForm, TransactionForm, GoalForm, ProfileForm

# Авторизация, регистрация
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('finance:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'finance/login.html', {'form': form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('finance:login')
    return render(request, 'finance/logout.html')

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('finance:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'finance/register.html', {'form': form})

# Дашборд
@login_required
def dashboard(request):
    wallets = Wallet.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]
    goals = Goal.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    context = {
        'wallets': wallets,
        'transactions': transactions,
        'goals': goals,
        'categories': categories
    }
    return render(request, 'finance/dashboard.html', context)

# Страницы
@login_required
def wallets(request):
    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
            return redirect('finance:wallets')
    else:
        form = WalletForm()
    wallets = Wallet.objects.filter(user=request.user)
    return render(request, 'finance/wallets.html', {'wallets': wallets, 'form': form})

@login_required
def transactions(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('finance:transactions')
    else:
        form = TransactionForm()
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'finance/transactions.html', {'transactions': transactions, 'form': form})

@login_required
def goals(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('finance:goals')
    else:
        form = GoalForm()
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'finance/goals.html', {'goals': goals, 'form': form})

@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'finance/categories.html', {'categories': categories})

@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('finance:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'finance/profile.html', {'form': form})