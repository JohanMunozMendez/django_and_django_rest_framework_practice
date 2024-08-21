from django.contrib.auth.models import User
from django.db import models

class OfficeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [('can_manage_clients', 'Can manage clients')]

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    card_pin = models.IntegerField()

    def __str__(self):
        return self.client.name + ' - ' + str(self.balance)

class TransactionLog(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=15)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.client.name + ' - ' + str(self.amount) + ' - ' + self.transaction_type