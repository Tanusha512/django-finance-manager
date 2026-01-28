from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import models
from django.utils import timezone

from .models import Wallet, Transaction, Category, Goal, Profile
from .forms import WalletForm, TransactionForm, CategoryForm, ProfileForm, GoalForm

# ========== Dashboard ==========

@login_required
def dashboard(request):
    """Главная страница"""
    wallets = Wallet.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]
    categories = Category.objects.filter(user=request.user)
    goals = Goal.objects.filter(user=request.user)
    
    # Статистика
    total_balance = sum(wallet.balance for wallet in wallets)
    
    # Доходы и расходы за текущий месяц
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    monthly_income = Transaction.objects.filter(
        user=request.user,
        transaction_type='income',
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    monthly_expense = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    context = {
        'wallets': wallets,
        'transactions': transactions,
        'categories': categories,
        'goals': goals,
        'total_balance': total_balance,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'page_title': 'Главная',
        'page_icon': 'fas fa-tachometer-alt',
    }
    return render(request, 'finance/dashboard.html', context)

# ========== Кошельки ==========

@login_required
def wallets(request):
    """Список кошельков пользователя"""
    wallets_list = Wallet.objects.filter(user=request.user)
    
    total_balance_rub = 0
    currencies_set = set()
    
    for wallet in wallets_list:
        currencies_set.add(wallet.currency)
        # Если хотите считать только рубли
        if wallet.currency == 'RUB':
            total_balance_rub += wallet.balance
    
    # Общее количество кошельков
    wallet_count = wallets_list.count()
    
    # Количество уникальных валют
    currency_count = len(currencies_set)
    
    total_balance_all = sum(w.balance for w in wallets_list)
    
    context = {
        'wallets': wallets_list,
        'wallet_count': wallet_count,
        'total_balance_rub': total_balance_rub,
        'total_balance_all': total_balance_all,
        'currency_count': currency_count,
        'currencies': list(currencies_set),
        'page_title': 'Мои кошельки',
        'page_icon': 'fas fa-wallet',
    }
    return render(request, 'finance/wallets.html', context)

@login_required
def wallet_add(request):
    """Добавление нового кошелька"""
    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
            messages.success(request, f'Кошелек "{wallet.name}" успешно создан!')
            return redirect('finance:wallets')
    else:
        form = WalletForm()
    
    context = {
        'form': form,
        'page_title': 'Новый кошелек',
        'page_icon': 'fas fa-plus-circle',
    }
    return render(request, 'finance/wallet_form.html', context)

@login_required
def wallet_edit(request, pk):
    """Редактирование кошелька"""
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            messages.success(request, f'Кошелек "{wallet.name}" успешно обновлен!')
            return redirect('finance:wallets')
    else:
        form = WalletForm(instance=wallet)
    
    context = {
        'form': form,
        'page_title': 'Редактирование кошелька',
        'page_icon': 'fas fa-edit',
    }
    return render(request, 'finance/wallet_form.html', context)

@login_required
def wallet_delete(request, pk):
    """Удаление кошелька"""
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    
    if request.method == 'POST':
        wallet_name = wallet.name
        wallet.delete()
        messages.success(request, f'Кошелек "{wallet_name}" успешно удален!')
        return redirect('finance:wallets')
    
    context = {
        'wallet': wallet,
        'page_title': 'Удаление кошелька',
        'page_icon': 'fas fa-trash',
    }
    return render(request, 'finance/wallet_confirm_delete.html', context)

# ========== Транзакции ==========

@login_required
def transactions(request):
    """Список транзакций пользователя"""
    transactions_list = Transaction.objects.filter(user=request.user).order_by('-date')
    
    # Статистика
    total_income = Transaction.objects.filter(
        user=request.user,
        transaction_type='income'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    total_expense = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    context = {
        'transactions': transactions_list,
        'total_income': total_income,
        'total_expense': total_expense,
        'page_title': 'Мои транзакции',
        'page_icon': 'fas fa-exchange-alt',
    }
    return render(request, 'finance/transactions.html', context)

@login_required
def transaction_add(request):
    """Добавление новой транзакции"""
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            
            # Обновляем баланс кошелька
            wallet = transaction.wallet
            if transaction.transaction_type == 'income':
                wallet.balance += transaction.amount
            else:  # expense
                wallet.balance -= transaction.amount
            wallet.save()
            
            transaction.save()
            messages.success(request, 'Транзакция успешно добавлена!')
            return redirect('finance:transactions')
    else:
        form = TransactionForm(user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Новая транзакция',
        'page_icon': 'fas fa-plus-circle',
    }
    return render(request, 'finance/transaction_form.html', context)

@login_required
def transaction_edit(request, pk):
    """Редактирование транзакции"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    old_amount = transaction.amount
    old_type = transaction.transaction_type
    old_wallet = transaction.wallet
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            # Восстанавливаем старый баланс
            if old_type == 'income':
                old_wallet.balance -= old_amount
            else:
                old_wallet.balance += old_amount
            old_wallet.save()
            
            # Сохраняем новую транзакцию
            updated_transaction = form.save(commit=False)
            wallet = updated_transaction.wallet
            
            # Применяем новую транзакцию
            if updated_transaction.transaction_type == 'income':
                wallet.balance += updated_transaction.amount
            else:
                wallet.balance -= updated_transaction.amount
            wallet.save()
            
            updated_transaction.save()
            messages.success(request, 'Транзакция успешно обновлена!')
            return redirect('finance:transactions')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Редактирование транзакции',
        'page_icon': 'fas fa-edit',
    }
    return render(request, 'finance/transaction_form.html', context)

@login_required
def transaction_delete(request, pk):
    """Удаление транзакции"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Восстанавливаем баланс кошелька
        wallet = transaction.wallet
        if transaction.transaction_type == 'income':
            wallet.balance -= transaction.amount
        else:
            wallet.balance += transaction.amount
        wallet.save()
        
        transaction.delete()
        messages.success(request, 'Транзакция успешно удалена!')
        return redirect('finance:transactions')
    
    context = {
        'transaction': transaction,
        'page_title': 'Удаление транзакции',
        'page_icon': 'fas fa-trash',
    }
    return render(request, 'finance/transaction_confirm_delete.html', context)

# ========== Категории ==========

@login_required
def categories(request):
    """Список категорий пользователя"""
    categories_list = Category.objects.filter(user=request.user)
    
    context = {
        'categories': categories_list,
        'page_title': 'Мои категории',
        'page_icon': 'fas fa-tags',
    }
    return render(request, 'finance/categories.html', context)

@login_required
def category_add(request):
    """Добавление новой категории"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, f'Категория "{category.name}" успешно создана!')
            return redirect('finance:categories')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'page_title': 'Новая категория',
        'page_icon': 'fas fa-plus-circle',
    }
    return render(request, 'finance/category_form.html', context)

@login_required
def category_edit(request, pk):
    """Редактирование категории"""
    category = get_object_or_404(Category, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Категория "{category.name}" успешно обновлена!')
            return redirect('finance:categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'page_title': 'Редактирование категории',
        'page_icon': 'fas fa-edit',
    }
    return render(request, 'finance/category_form.html', context)

@login_required
def category_delete(request, pk):
    """Удаление категории"""
    category = get_object_or_404(Category, pk=pk, user=request.user)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Категория "{category_name}" успешно удалена!')
        return redirect('finance:categories')
    
    context = {
        'category': category,
        'page_title': 'Удаление категории',
        'page_icon': 'fas fa-trash',
    }
    return render(request, 'finance/category_confirm_delete.html', context)

# ========== Цели ==========

@login_required
def goals(request):
    """Список целей пользователя"""
    goals_list = Goal.objects.filter(user=request.user).order_by('-deadline')
    
    # Статистика
    total_goals = goals_list.count()
    completed_goals = goals_list.filter(current_amount__gte=models.F('target_amount')).count()
    in_progress_goals = goals_list.filter(current_amount__lt=models.F('target_amount')).count()
    
    # Просроченные цели
    overdue_goals = goals_list.filter(
        deadline__lt=timezone.now().date(),
        current_amount__lt=models.F('target_amount')
    ).count()
    
    context = {
        'goals': goals_list,
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'in_progress_goals': in_progress_goals,
        'overdue_goals': overdue_goals,
        'page_title': 'Мои цели',
        'page_icon': 'fas fa-bullseye',
    }
    return render(request, 'finance/goals.html', context)

@login_required
def goal_add(request):
    """Добавление новой цели"""
    if request.method == 'POST':
        form = GoalForm(request.POST, user=request.user)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f'Цель "{goal.title}" успешно создана!')
            return redirect('finance:goals')
    else:
        form = GoalForm(user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Новая цель',
        'page_icon': 'fas fa-plus-circle',
    }
    return render(request, 'finance/goal_form.html', context)

@login_required
def goal_edit(request, pk):
    """Редактирование цели"""
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Цель "{goal.title}" успешно обновлена!')
            return redirect('finance:goals')
    else:
        form = GoalForm(instance=goal, user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Редактирование цели',
        'page_icon': 'fas fa-edit',
    }
    return render(request, 'finance/goal_form.html', context)

@login_required
def goal_delete(request, pk):
    """Удаление цели"""
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        goal_name = goal.title
        goal.delete()
        messages.success(request, f'Цель "{goal_name}" успешно удалена!')
        return redirect('finance:goals')
    
    context = {
        'goal': goal,
        'page_title': 'Удаление цели',
        'page_icon': 'fas fa-trash',
    }
    return render(request, 'finance/goal_confirm_delete.html', context)

# ========== Профиль ==========

@login_required
def profile(request):
    """Страница профиля пользователя"""
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Создаем профиль, если он не существует
        user_profile = Profile.objects.create(user=request.user)
    
    # Статистика пользователя
    wallet_count = Wallet.objects.filter(user=request.user).count()
    transaction_count = Transaction.objects.filter(user=request.user).count()
    goal_count = Goal.objects.filter(user=request.user).count()
    
    context = {
        'profile': user_profile,
        'wallet_count': wallet_count,
        'transaction_count': transaction_count,
        'goal_count': goal_count,
        'page_title': 'Мой профиль',
        'page_icon': 'fas fa-user',
    }
    return render(request, 'finance/profile.html', context)

@login_required
def profile_edit(request):
    """Редактирование профиля"""
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('finance:profile')
    else:
        form = ProfileForm(instance=user_profile)
    
    context = {
        'form': form,
        'page_title': 'Редактирование профиля',
        'page_icon': 'fas fa-edit',
    }
    return render(request, 'finance/profile_form.html', context)

# ========== Аутентификация ==========

def login_view(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('finance:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('finance:dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'page_title': 'Вход в систему',
        'page_icon': 'fas fa-sign-in-alt',
    }
    return render(request, 'finance/login.html', context)

def logout_view(request):
    """Кастомный выход пользователя"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('finance:login')