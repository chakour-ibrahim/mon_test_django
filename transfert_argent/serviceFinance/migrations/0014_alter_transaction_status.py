# Generated by Django 4.2.4 on 2023-08-23 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceFinance', '0013_alter_transaction_requette'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(default='DEPOT INITIE', max_length=100),
        ),
    ]
