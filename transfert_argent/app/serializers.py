from .models import *
from rest_framework.serializers import ModelSerializer


class UtilisateurSerializer(ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id_utilisateur', 'nom_utilisateur', 'numero_telephone', 'password', 'courriel', 'operateur', 'solde']


class UtilisateurSoldeSerializer(ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id_utilisateur', 'solde']

class UtilisateurSerializercompte(ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id_utilisateur', 'nom_utilisateur', 'numero_telephone', 'courriel', 'operateur', 'solde']
