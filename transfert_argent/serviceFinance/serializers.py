from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class TransactionuserSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id_transaction', 'status', 'requette']

class ModificationTransactionuserSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id_transaction', 'status']

class TransactionSerializer(serializers.ModelSerializer):
    expediteur_name = serializers.CharField(source='requette.sender_name.nom_utilisateur')
    expediteur_numero = serializers.CharField(source='requette.sender_name.numero_telephone')
    type_requete = serializers.CharField(source='requette.typerequette', max_length=100, default='DEPOT')
    destinataire_name = serializers.CharField(source='requette.receiver_name.nom_utilisateur')
    destinataire_numero = serializers.CharField(source='requette.receiver_name.numero_telephone')
    montant_requete = serializers.DecimalField(source='requette.amount', max_digits=100, decimal_places=2)
    statut = serializers.CharField(source='status', max_length=100, default='DEPOT INITIE')
    date = serializers.DateTimeField(source='requette.timestamp')

    class Meta:
        model = Transaction
        fields = ['id_transaction', 'expediteur_name', 'expediteur_numero', 'type_requete', 'destinataire_name', 'destinataire_numero', 'montant_requete', 'statut', 'date']


class TransactionUserSerializer(serializers.ModelSerializer):
    destinataire_name = serializers.CharField(source='requette.receiver_name.nom_utilisateur')
    destinataire_numero = serializers.CharField(source='requette.receiver_name.numero_telephone')
    type_requete = serializers.CharField(source='requette.typerequette', max_length=100, default='DEPOT')
    montant_requete = serializers.DecimalField(source='requette.amount', max_digits=100, decimal_places=2)
    statut = serializers.CharField(source='status', max_length=100, default='DEPOT INITIE')
    date = serializers.DateTimeField(source='requette.timestamp')

    class Meta:
        model = Transaction
        fields = ['id_transaction', 'destinataire_name', 'destinataire_numero', 'type_requete', 'montant_requete', 'statut', 'date']