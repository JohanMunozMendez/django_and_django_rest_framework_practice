# Generated by Django 5.0 on 2024-08-22 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0011_alter_client_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='atm.client'),
        ),
        migrations.AlterField(
            model_name='transactionlog',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='atm.account'),
        ),
    ]
