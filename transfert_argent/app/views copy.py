from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from django.contrib.auth import authenticate
#from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from serviceRequette.models import *
from serviceFinance.models import *
from decimal import Decimal
from django.http import JsonResponse
import requests
# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response 
from app.serializers import UtilisateurSerializer
import json
import psycopg2
from django.core.serializers import serialize
from django.db.models import F
def index(request):
    endpoint = "http://127.0.0.1:8000/apisf/toutelestransactions/"
    response = requests.get(endpoint)
    transactions = response.json()
    print(transactions)
    # endpoint = "http://127.0.0.1:8000/apisf/listefinance/"
    # response = requests.get(endpoint)
    # transactions = response.json()
    # resultats = Transaction.objects.select_related('requette').values('requette__sender_name__numero_telephone', 'requette__sender_name__nom_utilisateur', 'requette__receiver_name__numero_telephone', 'requette__receiver_name__nom_utilisateur', 'requette__amount', 'status', 'requette__timestamp').annotate(
    #                                                 numero_expediteur=F('requette__sender_name__numero_telephone'),
    #                                                 nom_expediteur=F('requette__sender_name_id__nom_utilisateur'),
    #                                                 numero_destinataire=F('requette__receiver_name_id__numero_telephone'),
    #                                                 nom_destinataire=F('requette__receiver_name_id__nom_utilisateur'),
    #                                                 montant=F('requette__amount'),
    #                                                 statut=F('status'),
    #                                                 date=F('requette__timestamp'),
    #                                             )
    return render(request, 'app/index.html',{'transactions': transactions})

def utilisateurs(request):
    endpoint = "http://127.0.0.1:8000/api/listeutilisateur/"
    response = requests.get(endpoint)
    utilisateurs = response.json()
    return render(request, 'app/pageutilisateurs.html', {'utilisateurs':utilisateurs})

def requettes(request):
    endpoint = "http://127.0.0.1:8000/apisr/listerequette/"
    response = requests.get(endpoint)
    requettes = response.json()
    print(requettes)
    
    for requette in requettes:
        print(requette['sender_name'])
        requette['sender_name'] = (Utilisateur.objects.get(id_utilisateur=requette['sender_name'])).numero_telephone
        requette['receiver_name'] = Utilisateur.objects.get(id_utilisateur=requette['receiver_name']).numero_telephone
    return render(request, 'app/pagerequettes.html', {'requettes':requettes})

def login(request):
    return render(request, 'app/login.html')

def register(request):
    if request.method == "POST":
        endpoint = "http://127.0.0.1:8000/api/creatreutilisateur/"
        response = requests.post(endpoint, json={'nom_utilisateur': request.POST['nomutilisateur'],
                                                'numero_telephone': request.POST['telephone'],
                                                'password': make_password(request.POST['password']),
                                                'courriel': request.POST['email'],
                                                'operateur': request.POST['operateur'],
                                                'solde': request.POST['montantsolde']
                                            })
        return redirect('http://127.0.0.1:8000/utilisateurs/')
    return render(request, 'app/login.html')

def connexion(request):
    if request.method == 'POST':
        telephone = request.POST['telephone']
        password = request.POST['password']
        utilisateur = Utilisateur.objects.get(numero_telephone=telephone)
        # print(utilisateur)
        # endpoint = "http://127.0.0.1:8000/api/listeutilisateur/"
        # response = requests.get(endpoint)
        # utilisateursendpoint = response.json()
        # for utilisateur in utilisateurendpoint:
        #     if utilisateur['numero_telephone'] == telephone :
        #         utilisateurconnecter = utilisateur

        if check_password(password, utilisateur.password):
            infoutilisateur = get_object_or_404(Utilisateur, numero_telephone=telephone)
            #print(infoutilisateur.id_utilisateur)
           # print(Requette)
            requettes_user = Requette.objects.filter(sender_name=infoutilisateur.id_utilisateur)
            return render(request, 'app/utilisateur.html', {'infoutilisateur': infoutilisateur, 'requettes_user': requettes_user})
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'app/login.html', {'error_message': error_message})
    else:
        return render(request, 'app/login.html')
    
def transactionuserid(request, id):
    infoutilisateur = Utilisateur.objects.get(id_utilisateur=id)
    resultats = Transaction.objects.select_related('requette').values('id_transaction', 'requette__receiver_name__numero_telephone', 'requette__receiver_name__nom_utilisateur', 'requette__amount', 'status', 'requette__timestamp', 'requette__typerequette').filter(requette__sender_name=id).annotate(
                                                    numero_destinataire=F('requette__receiver_name_id__numero_telephone'),
                                                    nom_destinataire=F('requette__receiver_name_id__nom_utilisateur'),
                                                    montant=F('requette__amount'),
                                                    statut=F('status'),
                                                    date=F('requette__timestamp'),
                                                    typederequetes=F('requette__typerequette'),
                                                    idtransaction=F('id_transaction')
                                                )
    #print(resultats)
    return render(request, 'app/transactionutilisateur.html', {'infoutilisateur': infoutilisateur, 'resultats':resultats} )

def requetteuserid(request, id):
    infoutilisateur = Utilisateur.objects.get(id_utilisateur=id)
    requette_user = Requette.objects.filter(sender_name=infoutilisateur.id_utilisateur)
    return render(request, 'app/requetteutilisateur.html', {'infoutilisateur': infoutilisateur, 'requette_user': requette_user})

def updatetransaction(request, id):
    transaction = Transaction.objects.get(id_transaction=id)
    id=transaction.id_transaction 
    idr=transaction.requette.id_requette
    id_user_sender = transaction.requette.sender_name.id_utilisateur
    id_user_receiver = transaction.requette.receiver_name.id_utilisateur
    user_sender = get_object_or_404(Utilisateur, id_utilisateur = id_user_sender)
    user_receiver = get_object_or_404(Utilisateur, id_utilisateur = id_user_receiver)
    solde_sender_user = transaction.requette.sender_name.solde
    solde_sender_user_init = transaction.requette.sender_name.solde
    solde_receiver_user = transaction.requette.sender_name.solde
    montant_requette = transaction.requette.amount
    statut_transaction = transaction.status
    print(statut_transaction)
    print(idr)
    print(id_user_sender)
    print(id_user_receiver)
    print(solde_sender_user)
    print(solde_sender_user_init)
    print(user_sender)
    print(user_receiver.solde)
    print(solde_receiver_user)
    print(montant_requette)
    # utilisateur = Utilisateur.objects.get(id_utilisateur=transaction.sender_name)
    if request.method == "POST":
        if solde_sender_user>0 and (request.POST['status']=="RDCEI" or request.POST['status']=="RDCET" or request.POST['status']=="DDCDI" or request.POST['status']=="DDCDT" or request.POST['status']=="DEDCD" or request.POST['status']=="DIPDC"): 
            #print(data)
            if solde_sender_user>montant_requette and (request.POST['status']=="RDCEI" or request.POST['status']=="RDCET" or request.POST['status']=="DDCDI" or request.POST['status']=="DDCDT" or request.POST['status']=="DEDCD" or request.POST['status']=="DIPDC"):
                if transaction.status == "DEPOT INITIE" and request.POST['status']=="RDCEI":
                    data ={'status': "RETRAIT DANS LE COMPTE EXPEDITEUR INITIE",
                        "requette": request.POST['requette']
                    }
                    print(data)
                    user_sender.solde -= montant_requette
                    user_sender.save()
                    print(solde_sender_user_init)
                    print(transaction.status)
                elif transaction.status == "RETRAIT DANS LE COMPTE EXPEDITEUR INITIE" and request.POST['status']=="RDCET":
                    data ={'status': "RETRAIT DANS LE COMPTE EXPEDITEUR TERNIMER",
                        "requette": request.POST['requette']
                    }
                    # if solde_sender_user != solde_sender_user_init and request.POST['status']=="RDCET": 
                    #     data ={'status': "RETRAIT DANS LE COMPTE EXPEDITEUR TERMINER",
                    #             "requette": request.POST['requette']
                    #         }
                    print(data)
                elif transaction.status == "RETRAIT DANS LE COMPTE EXPEDITEUR TERNIMER" and request.POST['status']=="DDCDI":
                    data ={'status': "DEPOT DANS LE COMPTE DESTINATAIRE INITIE",
                        "requette": request.POST['requette']
                    }
                    # if solde_sender_user != solde_sender_user_init and request.POST['status']=="RDCET": 
                    #     data ={'status': "RETRAIT DANS LE COMPTE EXPEDITEUR TERMINER",
                    #             "requette": request.POST['requette']
                    #         }
                    print(data)

                elif transaction.status == "DEPOT DANS LE COMPTE DESTINATAIRE INITIE" and request.POST['status']=="DDCDT":
                    data ={'status': "DEPOT DANS LE COMPTE DESTINATAIRE TERMINE",
                        "requette": request.POST['requette']
                    }
                    user_receiver.solde += montant_requette
                    user_receiver.save()
                    # if solde_sender_user != solde_sender_user_init and request.POST['status']=="RDCET": 
                    #     data ={'status': "RETRAIT DANS LE COMPTE EXPEDITEUR TERMINER",
                    #             "requette": request.POST['requette']
                    #         }
                    print(data)
                elif transaction.status == "DEPOT DANS LE COMPTE DESTINATAIRE TERMINE" and request.POST['status']=="DEDCD":
                    data ={'status': "DEPOT EFFECTUE DANS LE COMPTE DESTINATAIRE",
                        "requette": request.POST['requette']
                    }
                    # if solde_sender_user != solde_sender_user_init and request.POST['status']=="RDCET": 
                    #     data ={'status': "RETRAIT DANS LE COMPTE EXPEDITEUR TERMINER",
                    #             "requette": request.POST['requette']
                    #         }
                    print(data)
                else:
                    error_message = "Pour gerer un depôt les etapes doivent etre suivir et respecter de 1 à 6."
                    return render(request, 'app/transfertupdate.html', {'transaction':transaction, 'error_message': error_message})
            else :
                data ={'status': "ECHEC: Solde de l'expediteur insufisant",
                    "requette": request.POST['requette']
                }
                print(data)
        else :
            error_message = "Deconnecter vous et créditer compte."
            return render(request, 'app/transfertupdate.html', {'transaction':transaction, 'error_message': error_message})
        
        endpointsf = "http://127.0.0.1:8000/apisf/updatefinance/"+str(id)+"/"
        print(endpointsf)
        response = requests.put(endpointsf, data)
       
        return redirect('http://127.0.0.1:8000/transactionuserid/'+str(id_user_sender)+'/')
    return render(request, 'app/transfertupdate.html', {'transaction':transaction})

def pageuser(request):
    return render(request, 'app/utilisateur.html')   
#@login_required

def deconnexion(request):
    logout(request)
    #messages.success(request, 'logout successfully!')
    return redirect('http://127.0.0.1:8000/')

#@login_required
def update(request, id):
    utilisateur = Utilisateur.objects.get(id_utilisateur=id)
    id=utilisateur.id_utilisateur 
    if request.method == "POST":
        endpoint = "http://127.0.0.1:8000/api/updateutilisateur/"+str(id)+"/"
        print(endpoint)
        response = requests.put(endpoint, json={'nom_utilisateur': request.POST['nomutilisateur'],
                                                'numero_telephone': request.POST['telephone'],
                                                'password': make_password(request.POST['password']),
                                                'courriel': request.POST['email'],
                                                'operateur': request.POST['operateur'],
                                                'solde': request.POST['montantsolde']
                                            })
        return redirect('http://127.0.0.1:8000/utilisateurs/')
    return render(request, 'app/update.html', {'utilisateur':utilisateur})

def delete(request, id):
    utilisateur = Utilisateur.objects.get(id_utilisateur=id)
    id=utilisateur.id_utilisateur 

    endpoint = "http://127.0.0.1:8000/api/deleteutilisateur/"+str(id)+"/"
    print(endpoint)
    response = requests.delete(endpoint)
    return redirect('http://127.0.0.1:8000/utilisateurs/')
     
def pageutilisateurs(request):
#     utilisateurs = Utilisateur.objects.all()

    return render(request, 'app/pageutilisateurs.html')

def pagerequettes(request):
     return render(request, 'app/pagerequettes.html')

def envoilarequette(request, phone_sender):
    utilisateur = Utilisateur.objects.get(numero_telephone=phone_sender)
    id_user_sender = utilisateur.id_utilisateur
    if request.method == "POST":
        user_reciver= Utilisateur.objects.get(numero_telephone= request.POST['numeroreciver'])
        id_user_reciver = user_reciver.id_utilisateur
        endpoint = "http://127.0.0.1:8000/apisr/createrequette/"
        response = requests.post(endpoint, json={'sender_name': id_user_sender,
                                                'receiver_name': id_user_reciver,
                                                'typerequette': request.POST['typerequette'],
                                                'amount': request.POST['montant'],
                                                #'status': 'Dépôt Initié',
                                                'sens_requette': request.POST['typenvoi'],
                                            })
       
        requette = Requette.objects.latest('id_requette')
        print(requette.id_requette)
    
        endpointsf = "http://127.0.0.1:8000/apisf/creatrefinance/"
        response = requests.post(endpointsf, json={'status': 'DEPOT INITIE',
                                                    'requette': requette.id_requette,
                                            })
        print(id_user_sender)
        print(id_user_reciver)
        return redirect('http://127.0.0.1:8000/transactionuserid/'+str(utilisateur.id_utilisateur)+"/")
    return render(request, 'app/transfert.html', {'utilisateur':utilisateur})

# def utilisateur(request):
#     return render(request, 'app/utilisateur.html')

# def initrequettes(request, phone_sender):
#     utilisateur = Utilisateur.objects.get(numero_telephone=phone_sender)
#     return render(request, 'app/transfert.html', {'utilisateur':utilisateur})

#@api_view(['POST'])


# @api_view(['POST'])
# def send_data(request):
#     # Récupérer les données depuis la requête
#     data = request.data

#     # Envoyer les données à l'application réceptrice
#     response = requests.post('http://localhost:8000/receiver/', data=data)

#     # Traiter la réponse de l'application réceptrice
#     # ...

#     # Renvoyer une réponse
#     return Response({'message': 'Données envoyées avec succès'})


# @api_view(['POST'])
# def envoilarequette(request, phone_sender):
#     utilisateur = Utilisateur.objects.get(numero_telephone=phone_sender)  
#     if request.method =='POST':    
#         numerosender = request.POST['numerosender']
#         numeroreciver = request.POST['numeroreciver']
#         typenvoi = request.POST['typenvoi']
#         montant = Decimal(request.POST['montant'])  
#         sender_user = get_object_or_404(Utilisateur, numero_telephone=numerosender)
#         receiver_user = get_object_or_404(Utilisateur, numero_telephone=numeroreciver)              
#     # Récupérer les données depuis la requête
#     data = request.data

#     # Envoyer les données à l'application réceptrice
#     response = request.post('http://localhost:8000/requettes/', data=data)

#     # Traiter la réponse de l'application réceptrice
#     # ...

#     # Renvoyer une réponse
#     return render(request, 'app/transfert.html', {'utilisateur':utilisateur})


# def updatetransaction(request):
#     if request.method == 'POST':
#         numerosender = request.POST['numerosender']
#         numeroreciver = request.POST['numeroreciver']
#         typenvoi = request.POST['typenvoi']
#         montant = Decimal(request.POST['montant'])
        
#         sender_user = get_object_or_404(Utilisateur, numero_telephone=numerosender)
#         receiver_user = get_object_or_404(Utilisateur, numero_telephone=numeroreciver)
#         print(sender_user.solde)
#         print(receiver_user.solde)
#         if sender_user.solde > montant:
#             sender_user.solde -= montant
#             sender_user.save()
            
#             receiver_user.solde += montant
#             receiver_user.save()
            
#             transaction = Transaction(sender_name=sender_user.nom_utilisateur, receiver_name=receiver_user.nom_utilisateur, amount=montant, status='Reussie', typetransaction=typenvoi)
        
#             # Enregistrez l'utilisateur dans la base de données
#             transaction.save()
            
#             return redirect('/')
#         elif sender_user.solde == montant:
#                 transaction = Transaction(sender_name=sender_user.nom_utilisateur, receiver_name=receiver_user.nom_utilisateur, amount=montant, status='Encour...', typetransaction=typenvoi)
#                 transaction.save()
#                 return redirect('/')
#         else:
#             transaction = Transaction(sender_name=sender_user.nom_utilisateur, receiver_name=receiver_user.nom_utilisateur, amount=montant, status='Echec...', typetransaction=typenvoi)
#             transaction.save()
#             return render(request, '/')
    
#     return render(request, 'app/transfert.html')

 
class UtilisateurViewset(ReadOnlyModelViewSet):
    serializer_class = UtilisateurSerializer
    def get_queryset(self):
        return Utilisateur.objects.all()
    

def send_data_to_receiver(data):
    url = 'http://127.0.0.1:8000/api/utilisateurs/'
    response = requests.get(url, data=data)
    # Traiter la réponse si nécessaire
    print(response)

from django.forms.models import model_to_dict
@api_view(['GET'])
def api_view(request, *args, **kwargs):
  query = Utilisateur.objects.all().order_by('?').first()
  data ={}
  if query:
      data = UtilisateurSerializer(query).data
  return Response(data)
# Création d'un dictionnaire vide
# mon_dictionnaire = {}

# # Tuple
# mon_tuple = ('valeur1', 'valeur2')

# # Clés correspondantes pour chaque élément du tuple
# cles = ['cle1', 'cle2']

# # Ajout des éléments du tuple avec leurs clés dans le dictionnaire
# for i in range(len(cles)):
#     mon_dictionnaire[cles[i]] = mon_tuple[i]

# print(mon_dictionnaire)
# # Sortie : {'cle1': 'valeur1', 'cle2': 'valeur2'}
from rest_framework import generics, mixins

class detailUtilisateurView(generics.RetrieveAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer


class CreateUtilisateurView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer

class UpdateUtilisateurView(generics.UpdateAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer


class DeleteUtilisateurView(generics.DestroyAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer

class ListeUtilisateurView(generics.ListAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer


class UtilisateurMixinsViews(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    lookup_field = 'pk'
    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = name
        serializer.save(content=content)

    def perform_update(self, serializer):
        name = serializer.validated_data.get('name')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = name
        serializer.save(content=content)  

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)   


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)             
