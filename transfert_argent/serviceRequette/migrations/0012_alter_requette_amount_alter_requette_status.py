# Generated by Django 4.2.4 on 2023-08-23 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequette', '0011_requette_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requette',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
        migrations.AlterField(
            model_name='requette',
            name='status',
            field=models.CharField(max_length=100),
        ),
    ]
