from django import forms
from djgentelella.widgets import core as genwidgets
from djgentelella.forms.forms import GTForm

from .models import Account, Client, OfficeUser

class ClientForm(GTForm, forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            "name": genwidgets.TextInput(),
            "email": genwidgets.EmailInput(),
            "phone": genwidgets.TextInput(),
            "dni": genwidgets.TextInput(),
        }

class AccountForm(GTForm, forms.ModelForm):

    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            "client": genwidgets.Select(),
            "balance": genwidgets.NumberInput(),
            "card_pin": genwidgets.NumberInput(),
        }

class WithdrawForm(GTForm):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, required=True, label='Amount to withdraw', widget=genwidgets.NumberInput())
    card_pin = forms.IntegerField(required=True, label='Card PIN', widget=genwidgets.NumberInput())

class LoginForm(GTForm):
    username = forms.CharField(required=True, label='Username', widget=genwidgets.TextInput())
    password = forms.CharField(required=True, label='Password', widget=genwidgets.PasswordInput())

class OfficeUserForm(GTForm):
    first_name = forms.CharField(required=True, label='First Name', widget=genwidgets.TextInput())
    last_name = forms.CharField(required=True, label='Last Name', widget=genwidgets.TextInput())
    is_admin = forms.BooleanField(required=False, label='Is Admin', widget=genwidgets.CheckboxInput())

    class Meta:
        model = OfficeUser
        fields = []