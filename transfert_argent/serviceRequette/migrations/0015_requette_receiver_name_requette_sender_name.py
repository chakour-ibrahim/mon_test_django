# Generated by Django 4.2.4 on 2023-08-30 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('serviceRequette', '0014_remove_requette_receiver_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requette',
            name='receiver_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='app.utilisateur'),
        ),
        migrations.AddField(
            model_name='requette',
            name='sender_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='app.utilisateur'),
        ),
    ]
