# Generated by Django 4.2.4 on 2023-08-22 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequette', '0008_alter_requette_id_requette'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requette',
            name='id_requette',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
