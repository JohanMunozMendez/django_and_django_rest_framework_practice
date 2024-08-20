from django import forms
from djgentelella.widgets import core as genwidgets
from djgentelella.forms.forms import GTForm

from .models import Account

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
