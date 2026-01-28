# finance/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Transaction, Wallet

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создать профиль при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранить профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    """Обновить баланс кошелька после транзакции"""
    if created:
        wallet = instance.wallet
        if instance.transaction_type == 'income':
            wallet.balance += instance.amount
        else:  # expense
            wallet.balance -= instance.amount
        wallet.save()

@receiver(pre_save, sender=Transaction)
def update_wallet_balance_on_update(sender, instance, **kwargs):
    """Обновить баланс кошелька при изменении транзакции"""
    if instance.pk:  # Если транзакция уже существует (обновление)
        try:
            old_transaction = Transaction.objects.get(pk=instance.pk)
            wallet = instance.wallet
            
            # Отменить старую транзакцию
            if old_transaction.transaction_type == 'income':
                wallet.balance -= old_transaction.amount
            else:
                wallet.balance += old_transaction.amount
            
            # Применить новую транзакцию
            if instance.transaction_type == 'income':
                wallet.balance += instance.amount
            else:
                wallet.balance -= instance.amount
            
            wallet.save()
        except Transaction.DoesNotExist:
            pass