from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AccountForm, WithdrawForm
from .models import Account

denominations = [10000, 5000, 2000]
denominations.sort(reverse=True)
dispensed = []

# Create your views here.
def accounts(request):
    accounts = Account.objects.all()
    return render(request, 'atm/accounts.html', {'accounts': accounts})

def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('atm:accounts')
    else:
        form = AccountForm()
    return render(request, 'atm/create_account.html', {'form': form})

def edit_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully')
            return redirect('atm:accounts')
    else:
        form = AccountForm(instance=account)
        return render(request, 'atm/edit_account.html', {'account': account, 'form': form})

def delete_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    account.delete()
    messages.success(request, 'Account deleted successfully')
    return redirect('atm:accounts')

def is_dispensable(amount):
    if amount == 0:
        return True
    for denomination in denominations:
        if amount >= denomination and is_dispensable(amount - denomination):
            return True
    return False

def cash_dispense(amount):
    global dispensed
    dispensed = []
    cash_dispensed = 0

    for denomination in denominations:
        while amount >= denomination:
            amount -= Decimal(denomination)
            cash_dispensed += 1

        dispensed.append((cash_dispensed, denomination))
        cash_dispensed = 0

def show_withdrawal_info():
    info = 'Su dinero es '
    for amount, denomination in dispensed:
        info += f'{amount} billetes de {denomination} '
    return info

def withdraw(request):
    form = WithdrawForm().as_grid()
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        card_pin = request.POST.get('card_pin')
        account = Account.objects.get(card_pin=card_pin)

        if account.balance >= amount:
            if is_dispensable(amount):
                cash_dispense(amount)
                account.balance -= amount
                account.save()
                messages.success(request, f'Withdrawal successful {show_withdrawal_info()}')
                return redirect('atm:withdraw')

            else:
                messages.error(request, 'Amount not dispensable')
                return redirect('atm:withdraw')
        else:
            messages.error(request, 'Insufficient funds')
            return redirect('atm:withdraw')
    else:
        return render(request, 'atm/withdraw.html', {'form': form})

