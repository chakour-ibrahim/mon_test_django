from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import *
from decimal import Decimal
from django.http import JsonResponse
import requests
from rest_framework.response import Response 
from serviceFinance.serializers import *
import json
from rest_framework import generics, mixins


class DetailTransactionView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionuserSerializer


class CreateTransactionView(generics.CreateAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionuserSerializer

class UpdateTransactionView(generics.UpdateAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionuserSerializer


class ModifierTransactionView(generics.UpdateAPIView):
    serializer_class = ModificationTransactionuserSerializer
    
    def put(self, request, pk):
        transaction = Transaction.objects.get(id_transaction = pk) 
        transaction.status = serializers.validated_data.get('status')
        print(transaction)
        print(transaction.status)
        print(transaction.requette)
        return Response({'message': 'Statut de la transaction mis à jour avec succès'})

class DeleteTransactionView(generics.DestroyAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionSerializer

class ListeTransactionView(generics.ListAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionuserSerializer

class TransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.select_related('requette')
    serializer_class = TransactionSerializer

class TransactionListUserAPIView(generics.ListAPIView):
    serializer_class = TransactionUserSerializer

    def get_queryset(self):
        utilisateur_id = self.kwargs['utilisateur_id']  # Récupérer l'ID de l'utilisateur à partir des paramètres d'URL
        queryset = Transaction.objects.filter(requette__sender_name__id_utilisateur=utilisateur_id)
        return queryset
   