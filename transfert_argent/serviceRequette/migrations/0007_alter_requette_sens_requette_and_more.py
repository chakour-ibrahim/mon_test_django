# Generated by Django 4.2.4 on 2023-08-21 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequette', '0006_rename_receiver_number_requette_receiver_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requette',
            name='sens_requette',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='requette',
            name='typerequette',
            field=models.CharField(default='Depôt', max_length=100),
        ),
    ]
