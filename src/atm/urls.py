from django.urls import path

from . import views

app_name = 'atm'
urlpatterns = [
    path('clients', views.client_list, name='client_list'),
    path('create/client', views.create_client, name='create_client'),
    path('<int:client_id>', views.edit_client, name='edit_client'),
    path('<int:client_id>/delete', views.delete_client, name='delete_client'),
    path('accounts', views.account_list, name='account_list'),
    path('create/account', views.create_account, name='create_account'),
    path('<int:account_id>', views.edit_account, name='edit_account'),
    path('<int:account_id>/delete', views.delete_account, name='delete_account'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('transaction-logs', views.transaction_logs, name='transaction_logs'),
]