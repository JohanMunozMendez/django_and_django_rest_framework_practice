from django.contrib import admin

from .models import OfficeUser, Client, Account, TransactionLog

# Register your models here.
admin.site.register(OfficeUser)
admin.site.register(Client)
admin.site.register(Account)
admin.site.register(TransactionLog)