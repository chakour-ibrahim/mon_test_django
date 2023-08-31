from django.db import models
from app.models import *
# Create your models here.

class Requette(models.Model):               
    id_requette = models.AutoField(primary_key=True)
    sender_name = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='receiver')
    typerequette = models.CharField(max_length=100, default='DEPOT')
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    sens_requette = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.id_requette} {self.sender_name} {self.receiver_name} {self.typerequette} {self.amount} {self.timestamp} {self.sens_requette}"