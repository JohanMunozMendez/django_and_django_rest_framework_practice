from django.contrib import admin

from .models import Account, TransactionLog

# Register your models here.

admin.site.register(Account)
admin.site.register(TransactionLog)