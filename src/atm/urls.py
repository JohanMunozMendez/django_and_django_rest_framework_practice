from django.urls import path

from . import views

app_name = 'atm'
urlpatterns = [
    path('accounts', views.accounts, name='accounts'),
    path('create-account', views.create_account, name='create_account'),
    path('<int:account_id>', views.edit_account, name='edit_account'),
    path('<int:account_id>/delete', views.delete_account, name='delete_account'),
    path('withdraw', views.withdraw, name='withdraw'),
]