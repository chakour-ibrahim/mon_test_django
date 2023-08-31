from django.db import models
from serviceRequette.models import Requette

# Create your models here.
class Transaction(models.Model):
    id_transaction = models.AutoField(primary_key=True)
    # sender_name = models.CharField(max_length=100, null=True, blank= True)
    # receiver_name = models.CharField(max_length=100, null=True, blank= True)
    # typetransaction = models.CharField(max_length=100, null=True, blank= True)
    # amount = models.DecimalField(max_digits=10, null=True, blank= True, decimal_places=2)
    # timestamp = models.DateTimeField(auto_now_add=True, null=True, blank= True)
    status = models.CharField(max_length=100, default='DEPOT INITIE')#
    requette = models.ForeignKey(Requette, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id_transaction} {self.status} {self.requette}"
    

