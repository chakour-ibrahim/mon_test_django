# Generated by Django 4.2.4 on 2023-08-22 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequette', '0007_alter_requette_sens_requette_and_more'),
        ('serviceFinance', '0007_remove_transaction_requette'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='requette',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='serviceRequette.requette'),
        ),
    ]
