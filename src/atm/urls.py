from django.urls import path

from . import views
app_name = 'atm'

urlpatterns = [
    path('office-users', views.office_user_list, name='office_user_list'),
    path('office-users/create', views.create_office_user, name='create_office_user'),
    path('office-users/<int:office_user_id>', views.edit_office_user, name='edit_office_user'),
    path('clients', views.client_list, name='client_list'),
    path('clients/create', views.create_client, name='create_client'),
    path('clients/<int:client_id>', views.edit_client, name='edit_client'),
    path('clients<int:client_id>/delete', views.delete_client, name='delete_client'),
    path('accounts', views.account_list, name='account_list'),
    path('accounts/create', views.create_account, name='create_account'),
    path('accounts/<int:account_id>', views.edit_account, name='edit_account'),
    path('accounts/<int:account_id>/delete', views.delete_account, name='delete_account'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('transaction-logs', views.transaction_logs, name='transaction_logs'),
]