from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Account(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    card_pin = models.IntegerField()

    def __str__(self):
        return self.client.username + ' - ' + str(self.balance)
