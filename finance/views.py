from django.shortcuts import render
from .models import Wallet, Transaction, Goal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("Финансовый менеджер работает!")

@login_required
def dashboard(request):
    user = request.user
    wallets = Wallet.objects.filter(user=user)
    transactions = Transaction.objects.filter(wallet__user=user).order_by('-date')[:10]
    goals = Goal.objects.filter(user=user)

    context = {
        'wallets': wallets,
        'transactions': transactions,
        'goals': goals,
    }
    return render(request, 'finance/dashboard.html', context)