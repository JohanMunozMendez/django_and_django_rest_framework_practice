from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AccountForm, WithdrawForm, ClientForm, LoginForm
from .models import Account, TransactionLog, Client

denominations = [10000, 5000, 2000]
denominations.sort(reverse=True)
dispensed = []

def signin(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('atm:account_list')
        else:
            messages.error(request, 'Username and password did not match')
            form = LoginForm().as_grid()
            return render(request, 'atm/login.html', {'form': form})
    else:
        form = LoginForm().as_grid()
        return render(request, 'atm/login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('atm:withdraw')

@permission_required('atm.can_manage_clients')
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'atm/clients/client_list.html', {'clients': clients})

@permission_required('atm.can_manage_clients')
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client created successfully')
            return redirect('atm:client_list')
    else:
        form = ClientForm()
        return render(request, 'atm/clients/create_client.html', {'form': form})

@permission_required('atm.can_manage_clients')
def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente updated successfully')
            return redirect('atm:client_list')
    else:
        form = ClientForm(instance=client)
        return render(request, 'atm/clients/edit_client.html', {'client': client, 'form': form})

@permission_required('atm.can_manage_clients')
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.delete()
    messages.success(request, 'Client deleted successfully')
    return redirect('atm:client_list')

@permission_required('atm.can_manage_clients')
def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'atm/accounts/account_list.html', {'accounts': accounts})

@permission_required('atm.can_manage_clients')
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('atm:account_list')
    else:
        form = AccountForm()
    return render(request, 'atm/accounts/create_account.html', {'form': form})

@permission_required('atm.can_manage_clients')
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
        return render(request, 'atm/accounts/edit_account.html', {'account': account, 'form': form})

@permission_required('atm.can_manage_clients')
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
            info += f'{amount} billetes de {denomination}, '
    return info

def withdraw(request):
    form = WithdrawForm().as_grid()
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        card_pin = request.POST['card_pin']
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