# Generated by Django 4.2.4 on 2023-08-23 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequette', '0012_alter_requette_amount_alter_requette_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requette',
            name='status',
        ),
    ]