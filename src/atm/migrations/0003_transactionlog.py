# Generated by Django 5.0 on 2024-08-19 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0002_alter_account_card_pin'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('transaction_type', models.CharField(max_length=15)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atm.account')),
            ],
        ),
    ]
