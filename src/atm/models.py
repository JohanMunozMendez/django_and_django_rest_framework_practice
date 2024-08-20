from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Account(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    card_pin = models.IntegerField()

    def __str__(self):
        return self.client.username + ' - ' + str(self.balance)

class TransactionLog(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=15)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.client.username + ' - ' + str(self.amount) + ' - ' + self.transaction_type