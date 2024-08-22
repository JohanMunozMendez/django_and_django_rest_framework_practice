import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from djgentelella.decorators.perms import all_permission_required

from .forms import AccountForm, WithdrawForm, ClientForm, OfficeUserForm
from .models import Account, TransactionLog, Client, OfficeUser

denominations = [10000, 5000, 2000]
denominations.sort(reverse=True)
dispensed = []
logger = logging.getLogger("django")

@permission_required('atm.view_officeuser')
def office_user_list(request):
    office_users = OfficeUser.objects.all()
    return render(request, 'atm/office_users/office_user_list.html', {'office_users': office_users})
@all_permission_required(['atm.add_officeuser', 'atm.view_officeuser'])
def create_office_user(request):
    if request.method == 'POST':
        form = OfficeUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                try:
                    user = User.objects.create_user(username=username, password=password1)
                    permission = Permission.objects.get(codename='can_manage_clients')
                    user.user_permissions.add(permission)
                    user.save()
                    OfficeUser.objects.create(user=user)
                    messages.success(request, 'Office user created successfully')
                    return redirect('atm:create_office_user')
                except IntegrityError:
                    messages.error(request, 'Username already taken')
                    return render(request, 'atm/office_users/create_office_user.html', {'form': OfficeUserForm()})
            else:
                messages.error(request, 'Passwords do not match')
                logger.error('Passwords do not match')
                return render(request, 'atm/office_users/create_office_user.html', {'form': OfficeUserForm()})
        else:
            messages.error(request, form.errors)
            return render(request, 'atm/office_users/create_office_user.html', {'form': OfficeUserForm()})
    else:
        return render(request, 'atm/office_users/create_office_user.html', {'form': OfficeUserForm()})

def edit_office_user(request, office_user_id):
    pass

# @permission_required('atm.can_manage_clients')
class ClientListView(generic.ListView):
    model = Client
    template_name = 'atm/clients/client_list.html'
    queryset = Client.objects.all()
    context_object_name = 'clients'

# @permission_required('atm.can_manage_clients')
class CreateClientView(generic.CreateView):
    form_class = ClientForm
    template_name = 'atm/clients/create_client.html'
    success_url = reverse_lazy('atm:client_list')

# @permission_required('atm.can_manage_clients')
class EditClientView(generic.UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'atm/clients/edit_client.html'
    success_url = reverse_lazy('atm:client_list')

# @permission_required('atm.can_manage_clients')
class DeleteClientView(generic.DeleteView):
    model = Client
    template_name = 'atm/clients/confirm_delete.html'
    success_url = reverse_lazy('atm:client_list')

# @permission_required('atm.can_manage_clients')
class AccountListView(generic.ListView):
    model = Account
    template_name = 'atm/accounts/account_list.html'
    queryset = Account.objects.all()
    context_object_name = 'accounts'

# @permission_required('atm.can_manage_clients')
class CreateAccountView(generic.CreateView):
    form_class = AccountForm
    template_name = 'atm/accounts/create_account.html'
    success_url = reverse_lazy('atm:account_list')

# @permission_required('atm.can_manage_clients')
class EditAccountView(generic.UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'atm/accounts/edit_account.html'
    success_url = reverse_lazy('atm:account_list')

# @permission_required('atm.can_manage_clients')
class DeleteAccountView(generic.DeleteView):
    model = Account
    template_name = 'atm/accounts/confirm_delete.html'
    success_url = reverse_lazy('atm:account_list')

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