from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import JsonResponse
import requests
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response 
from app.serializers import *
from rest_framework import generics, mixins


def index(request):
    endpoint = "http://127.0.0.1:8000/apisf/toutelestransactions/"
    response = requests.get(endpoint)
    transactions = response.json()
    return render(request, 'app/index.html',{'transactions': transactions})

def utilisateurs(request):
    endpoint = "http://127.0.0.1:8000/api/listeutilisateur/"
    response = requests.get(endpoint)
    utilisateurs = response.json()
    return render(request, 'app/pageutilisateurs.html', {'utilisateurs':utilisateurs})

def requettes(request):
    endpoint = "http://127.0.0.1:8000/apisr/toutelesrequete/"
    response = requests.get(endpoint)
    requettes = response.json()
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
    endpoint = "http://127.0.0.1:8000/api/listeutilisateur/"
    response = requests.get(endpoint)
    utilisateurs = response.json()
    
    if request.method == 'POST':
        phone_user = request.POST['telephone']
        password = request.POST['password']
        for utilisateur in utilisateurs:
            if utilisateur['numero_telephone'] == phone_user :
                if check_password(password, utilisateur['password']):
                    print(utilisateur['id_utilisateur'])
                    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(utilisateur['id_utilisateur'])+"/"
                    response = requests.get(endpoint)
                    connected_user = response.json()
                    print(endpoint)
                    print(connected_user)
                    endpoint = "http://127.0.0.1:8000/apisr/utilisateurs/"+str(utilisateur['id_utilisateur'])+"/requetes/"
                    response = requests.get(endpoint)
                    requettes_user = response.json()
                    print(endpoint)
                    print(requettes_user)
                    return render(request, 'app/utilisateur.html', {'connected_user': connected_user, 'requettes_user': requettes_user})
                else:
                    error_message = 'Invalid username or password.'
                    return render(request, 'app/login.html', {'error_message': error_message})   
    else:
        return render(request, 'app/login.html')
    
def transactionuserid(request, id):
    endpoint = "http://127.0.0.1:8000/apisf/transactions/"+str(id)+"/transaction/"
    response = requests.get(endpoint)
    transactions = response.json()

    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(id)+"/"
    response = requests.get(endpoint)
    utilisateur = response.json()
    
    print(utilisateur)
    return render(request, 'app/transactionutilisateur.html', {'utilisateur': utilisateur, 'transactions':transactions} )

def requetteuserid(request, id):
    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(id)+"/"
    response = requests.get(endpoint)
    infoutilisateur = response.json()

    endpoint = "http://127.0.0.1:8000/apisr/utilisateurs/"+str(id)+"/requetes/"
    response = requests.get(endpoint)
    requette_user = response.json()
    return render(request, 'app/requetteutilisateur.html', {'infoutilisateur': infoutilisateur, 'requette_user': requette_user})

def updatetransaction(request, id):
    endpoint = "http://127.0.0.1:8000/apisf/detailfinance/"+str(id)+"/"
    response = requests.get(endpoint)
    transaction_en_cour = response.json()
    # print(transaction_en_cour)
    endpoint = "http://127.0.0.1:8000/apisr/detailrequette/"+str(transaction_en_cour['requette'])+"/"
    response = requests.get(endpoint)
    requette_en_cour = response.json()
    print(requette_en_cour)
    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(requette_en_cour['sender_name'])+"/"
    response = requests.get(endpoint)
    sender_user = response.json()
    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(requette_en_cour['receiver_name'])+"/"
    response = requests.get(endpoint)
    receiver_user = response.json()
    print(receiver_user)
    if request.method == "POST":
        if Decimal(sender_user['solde']) >0 and (request.POST['status']=="RDCEI" or request.POST['status']=="RDCET" or request.POST['status']=="DDCDI" or request.POST['status']=="DDCDT" or request.POST['status']=="DEDCD" or request.POST['status']=="DIPDC"): 
            if Decimal(sender_user['solde'])> Decimal(requette_en_cour['amount']) and (request.POST['status']=="RDCEI" or request.POST['status']=="RDCET" or request.POST['status']=="DDCDI" or request.POST['status']=="DDCDT" or request.POST['status']=="DEDCD" or request.POST['status']=="DIPDC"):
                if transaction_en_cour['status'] == "DEPOT INITIE" and request.POST['status']=="RDCEI":
                    data ={'status': "RETRAIT DANS LE COMPTE EXPEDITEUR INITIE",
                        "requette": request.POST['requette']
                    }
                    endpointsf = "http://127.0.0.1:8000/apisf/updatefinance/"+str(transaction_en_cour['id_transaction'])+"/"
                    response = requests.put(endpointsf, data)
                elif transaction_en_cour['status'] == "RETRAIT DANS LE COMPTE EXPEDITEUR INITIE" and request.POST['status']=="RDCET":
                    data ={'status': "RETRAIT DANS LE COMPTE EXPEDITEUR TERNIMER",
                        "requette": request.POST['requette']
                    }
                    new_solde_sender_user = Decimal(sender_user['solde']) - Decimal(requette_en_cour['amount'])
                    senderdata = { "solde": new_solde_sender_user}
                    endpointsender = "http://127.0.0.1:8000/api/updatesoldeutilisateur/"+str(sender_user['id_utilisateur'])+"/" 
                    response = requests.put(endpointsender, senderdata)
                    endpointsf = "http://127.0.0.1:8000/apisf/updatefinance/"+str(transaction_en_cour['id_transaction'])+"/"
                    response = requests.put(endpointsf, data)
                elif transaction_en_cour['status'] == "RETRAIT DANS LE COMPTE EXPEDITEUR TERNIMER" and request.POST['status']=="DDCDI":
                    data ={'status': "DEPOT DANS LE COMPTE DESTINATAIRE INITIE",
                        "requette": request.POST['requette']
                    }
                    endpointsf = "http://127.0.0.1:8000/apisf/updatefinance/"+str(transaction_en_cour['id_transaction'])+"/"
                    response = requests.put(endpointsf, data)
                elif transaction_en_cour['status'] == "DEPOT DANS LE COMPTE DESTINATAIRE INITIE" and request.POST['status']=="DDCDT":
                    data ={'status': "DEPOT DANS LE COMPTE DESTINATAIRE TERMINE",
                        "requette": request.POST['requette']
                    }
                    new_solde_receiver_user = Decimal(receiver_user['solde']) + Decimal(requette_en_cour['amount'])
                    receiverdata = {"solde": str(new_solde_receiver_user)}
                    #print(receiver_user)
                    endpointreceiver = "http://127.0.0.1:8000/api/updatesoldeutilisateur/"+str(receiver_user['id_utilisateur'])+"/" 
                    print(receiver_user['solde'])
                    #print(endpointreceiver)
                    #print(receiverdata)
                    response = requests.put(endpointreceiver, receiverdata)   
                    endpointsf = "http://127.0.0.1:8000/apisf/updatefinance/"+str(transaction_en_cour['id_transaction'])+"/"
                    response = requests.put(endpointsf, data)    
                elif transaction_en_cour['status'] == "DEPOT DANS LE COMPTE DESTINATAIRE TERMINE" and request.POST['status']=="DEDCD":
                    data ={'status': "DEPOT EFFECTUE DANS LE COMPTE DESTINATAIRE",
                        "requette": request.POST['requette']
                    }
                    endpointsf = "http://127.0.0.1:8000/apisf/updatefinance/"+str(transaction_en_cour['id_transaction'])+"/"
                    response = requests.put(endpointsf, data)
                else:
                    error_message = "Pour gerer un depôt les etapes doivent etre suivir et respecter de 1 à 6."
                    return render(request, 'app/transfertupdate.html', {'transaction_en_cour':transaction_en_cour, 'requette_en_cour':requette_en_cour, 'error_message': error_message})
            else :
                data ={'status': "ECHEC: Solde de l'expediteur insufisant",
                    "requette": request.POST['requette']
                }
                endpointsf = "http://127.0.0.1:8000/apisf/updatefinance/"+str(transaction_en_cour['id_transaction'])+"/"
                response = requests.put(endpointsf, data)
        else :
            error_message = "Deconnecter vous et créditer compte."
            return render(request, 'app/transfertupdate.html', {'transaction_en_cour':transaction_en_cour, 'error_message': error_message})
        return redirect('http://127.0.0.1:8000/transactionuserid/'+str(sender_user['id_utilisateur'])+'/')
    return render(request, 'app/transfertupdate.html', {'transaction_en_cour':transaction_en_cour, 'requette_en_cour':requette_en_cour})

def pageuser(request):
    return render(request, 'app/utilisateur.html')   
#@login_required

def deconnexion(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

#@login_required
def update(request, id):
    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(id)+"/"
    response = requests.get(endpoint)
    utilisateur = response.json()
    if request.method == "POST":
        data = {'nom_utilisateur': request.POST['nomutilisateur'],
                'numero_telephone': request.POST['telephone'],
                'courriel': request.POST['email'],
                'operateur': request.POST['operateur'],
                'solde': request.POST['montantsolde']
                }
        endpoint = "http://127.0.0.1:8000/api/updatecompteutilisateur/"+str(id)+"/"
        response = requests.put(endpoint, data)
        return redirect('http://127.0.0.1:8000/utilisateurs/')
    return render(request, 'app/update.html', {'utilisateur':utilisateur})

def delete(request, id):
    endpoint = "http://127.0.0.1:8000/api/deleteutilisateur/"+str(id)+"/"
    print(endpoint)
    response = requests.delete(endpoint)
    return redirect('http://127.0.0.1:8000/utilisateurs/')
     
def pageutilisateurs(request):
    return render(request, 'app/pageutilisateurs.html')

def pagerequettes(request):
     return render(request, 'app/pagerequettes.html')

def envoilarequette(request, id):
    
    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(id)+"/"
    response = requests.get(endpoint)
    utilisateur = response.json()
    if request.method == "POST":
        endpoint = "http://127.0.0.1:8000/api/listeutilisateur/"
        response = requests.get(endpoint)
        utilisateurs = response.json()
        for user in utilisateurs:
            if (user['numero_telephone'] == request.POST['numeroreciver']):
                user_reciver= user
                endpoint = "http://127.0.0.1:8000/apisr/createrequette/"
                response = requests.post(endpoint, json={'sender_name': utilisateur['id_utilisateur'],
                                                        'receiver_name': user_reciver['id_utilisateur'],
                                                        'typerequette': request.POST['typerequette'],
                                                        'amount': request.POST['montant'],
                                                        'sens_requette': request.POST['typenvoi'],
                                                    })
        
                data = {'sender_name': utilisateur['id_utilisateur'],
                        'receiver_name': user_reciver['id_utilisateur'],
                        'typerequette': request.POST['typerequette'],
                        'amount': request.POST['montant'],
                        'sens_requette': request.POST['typenvoi'],
                    }
        
                endpoint = "http://127.0.0.1:8000/apisr/listerequette/"
                response = requests.get(endpoint)
                requetes = response.json()
                for requete in requetes:
                    max_requete_id = 0
                    if requete['id_requette']>max_requete_id:
                        max_requete_id=requete['id_requette']

                        endpoint = "http://127.0.0.1:8000/apisf/creatrefinance/"
                        response = requests.post(endpoint, json={'status': 'DEPOT INITIE',
                                                                'requette': max_requete_id,
                                                            })
                return redirect('http://127.0.0.1:8000/transactionuserid/'+str(utilisateur['id_utilisateur'])+"/")
    return render(request, 'app/transfert.html', {'utilisateur':utilisateur})

def detailrequette(request, id):
    endpoint = "http://127.0.0.1:8000/apisf/listefinance/"
    response = requests.get(endpoint)
    transactions = response.json()
    for transaction in transactions:
        if transaction['requette']==id:
            id_detail = transaction['id_transaction']

    endpoint = "http://127.0.0.1:8000/apisr/listerequette/"
    response = requests.get(endpoint)
    lesrequetes = response.json()
    for requete in lesrequetes:
        if requete['id_requette']==id:
            id_user = requete['sender_name']     

    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(id_user)+"/"
    response = requests.get(endpoint)
    utilisateur = response.json()  
    endpoint = "http://127.0.0.1:8000/apisf/toutelestransactions/"
    response = requests.get(endpoint)
    touteslestransactions= response.json()
    for transactiondetailer in touteslestransactions:
        if transactiondetailer['id_transaction']==id_detail:
            return render(request, 'app/detailrequette.html', {'transactiondetailer':transactiondetailer, 'utilisateur':utilisateur})

def detailrequetteacc(request, id):
    endpoint = "http://127.0.0.1:8000/apisf/listefinance/"
    response = requests.get(endpoint)
    transactions = response.json()
    for transaction in transactions:
        if transaction['requette']==id:
            id_detail = transaction['id_transaction']


    endpoint = "http://127.0.0.1:8000/apisr/listerequette/"
    response = requests.get(endpoint)
    lesrequetes = response.json()
    for requete in lesrequetes:
        if requete['id_requette']==id:
            id_user = requete['sender_name']     

    endpoint = "http://127.0.0.1:8000/api/detailutilisateur/"+str(id_user)+"/"
    response = requests.get(endpoint)
    utilisateur = response.json()  
    endpoint = "http://127.0.0.1:8000/apisf/toutelestransactions/"
    response = requests.get(endpoint)
    touteslestransactions= response.json()
    for transactiondetailer in touteslestransactions:
        if transactiondetailer['id_transaction']==id_detail:
            print(transactiondetailer)
    return render(request, 'app/detailrequetteacc.html', {'transactiondetailer':transactiondetailer, 'utilisateur':utilisateur})



class detailUtilisateurView(generics.RetrieveAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer


class CreateUtilisateurView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer

class UpdateUtilisateurView(generics.UpdateAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer

class UpdateSoldeUtilisateurView(generics.UpdateAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSoldeSerializer


class DeleteUtilisateurView(generics.DestroyAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer

class ListeUtilisateurView(generics.ListAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializer

class UpdateUtilisateurCompteView(generics.UpdateAPIView):
    queryset = Utilisateur.objects.all() 
    serializer_class = UtilisateurSerializercompte

