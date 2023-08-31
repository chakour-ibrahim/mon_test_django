# Generated by Django 4.2.4 on 2023-08-20 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('serviceRequette', '0003_alter_requette_sens_requette_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requette',
            name='receiver_name',
        ),
        migrations.RemoveField(
            model_name='requette',
            name='sender_name',
        ),
        migrations.AddField(
            model_name='requette',
            name='receiver_number',
            field=models.ForeignKey(default='000000000', on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='app.utilisateur', to_field='numero_telephone'),
        ),
        migrations.AddField(
            model_name='requette',
            name='sender_number',
            field=models.ForeignKey(default='000000000', on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='app.utilisateur', to_field='numero_telephone'),
        ),
    ]