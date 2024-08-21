from django.contrib import admin

from .models import Client, Account, TransactionLog

# Register your models here.

admin.site.register(Client)
admin.site.register(Account)
admin.site.register(TransactionLog)