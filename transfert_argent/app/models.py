from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class Utilisateur(AbstractBaseUser):
    id_utilisateur = models.AutoField(primary_key=True)
    nom_utilisateur = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100) 
    courriel = models.EmailField()
    operateur = models.CharField(max_length=100)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.id_utilisateur} {self.numero_telephone} {self.password} {self.nom_utilisateur} {self.solde} {self.courriel} {self.operateur}"
    