from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AccountForm, WithdrawForm
from .models import Account, TransactionLog


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
            return redirect('atm:account_list')
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
            return redirect('atm:account_list')
    else:
        form = AccountForm(instance=account)
        return render(request, 'atm/edit_account.html', {'account': account, 'form': form})

def delete_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    account.delete()
    messages.success(request, 'Account deleted successfully')
    return redirect('atm:account_list')

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
        if amount > 0:
            info += f'{amount} billete(s) de ${denomination}, '
    return info

def withdraw(request):
    form = WithdrawForm().as_grid()
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        card_pin = request.POST.get('card_pin')
        account =  get_object_or_404(Account, card_pin=card_pin)

        if account.balance >= amount:
            if is_dispensable(amount):
                cash_dispense(amount)
                account.balance -= amount
                account.save()
                create_transaction_log(account, amount, 'withdrawal')
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

def create_transaction_log(account, amount, transaction_type):
    account.transactionlog_set.create(amount=amount, transaction_type=transaction_type)
    account.save()

@login_required
def transaction_logs(request):
    transaction_logs = TransactionLog.objects.all()
    return render(request, 'atm/transaction_logs.html', {'transaction_logs': transaction_logs})