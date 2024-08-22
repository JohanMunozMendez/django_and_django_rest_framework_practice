from django.urls import path

from . import views
app_name = 'atm'

urlpatterns = [
    path('office-users', views.office_user_list, name='office_user_list'),
    path('office-users/create', views.create_office_user, name='create_office_user'),
    path('office-users/<int:office_user_id>', views.edit_office_user, name='edit_office_user'),
    path('clients', views.ClientListView.as_view(), name='client_list'),
    path('clients/create', views.CreateClientView.as_view(), name='create_client'),
    path('clients/<int:pk>', views.EditClientView.as_view(), name='edit_client'),
    path('clients/<int:pk>/delete', views.DeleteClientView.as_view(), name='delete_client'),
    path('accounts', views.AccountListView.as_view(), name='account_list'),
    path('accounts/create', views.CreateAccountView.as_view(), name='create_account'),
    path('accounts/<int:pk>', views.EditAccountView.as_view(), name='edit_account'),
    path('accounts/<int:pk>/delete', views.DeleteAccountView.as_view(), name='delete_account'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('transaction-logs', views.transaction_logs, name='transaction_logs'),
]