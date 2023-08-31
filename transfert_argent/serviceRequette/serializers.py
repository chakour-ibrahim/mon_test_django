from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from app.models import Utilisateur

class RequetteSerializer(ModelSerializer):
    class Meta:
        model = Requette
        fields = ['id_requette', 'sender_name', 'receiver_name', 'typerequette', 'amount', 'timestamp', 'sens_requette']

class RequeteSerializer(serializers.ModelSerializer):
    expediteur_name = serializers.CharField(source='sender_name.nom_utilisateur')
    expediteur_numero = serializers.CharField(source='sender_name.numero_telephone')
    type_requete = serializers.CharField(source='typerequette', max_length=100, default='DEPOT')
    destinataire_name = serializers.CharField(source='receiver_name.nom_utilisateur')
    destinataire_numero = serializers.CharField(source='receiver_name.numero_telephone')
    montant_requete = serializers.DecimalField(source='amount', max_digits=100, decimal_places=2)
    date = serializers.DateTimeField(source='timestamp')

    class Meta:
        model = Requette
        fields = ['id_requette', 'expediteur_name', 'expediteur_numero', 'destinataire_name', 'destinataire_numero', 'montant_requete', 'date', 'type_requete']


class RequeteUserSerializer(serializers.ModelSerializer):
    destinataire_name = serializers.CharField(source='receiver_name.nom_utilisateur')
    destinataire_numero = serializers.CharField(source='receiver_name.numero_telephone')
    type_requete = serializers.CharField(source='typerequette', max_length=100, default='DEPOT')
    montant_requete = serializers.DecimalField(source='amount', max_digits=100, decimal_places=2)
    date = serializers.DateTimeField(source='timestamp')

    class Meta:
        model = Requette
        fields = ['id_requette', 'destinataire_name', 'destinataire_numero', 'type_requete', 'montant_requete', 'date']

