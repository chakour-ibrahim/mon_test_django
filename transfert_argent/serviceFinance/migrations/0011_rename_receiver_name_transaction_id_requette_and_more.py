# Generated by Django 4.2.4 on 2023-08-22 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serviceFinance', '0010_alter_transaction_typetransaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='receiver_name',
            new_name='id_requette',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='sender_name',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='sens_transaction',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='typetransaction',
        ),
    ]
