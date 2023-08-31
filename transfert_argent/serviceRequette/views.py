from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import  get_object_or_404
from .models import *
from decimal import Decimal
from django.http import JsonResponse
import requests
from rest_framework.response import Response 
from serviceRequette.serializers import *
import json
import psycopg2
from rest_framework import generics, mixins

class DetailRequetteView(generics.RetrieveAPIView):
    queryset = Requette.objects.all() 
    serializer_class = RequetteSerializer


class CreateRequetteView(generics.CreateAPIView):
    queryset = Requette.objects.all() 
    serializer_class = RequetteSerializer

class UpdateRequetteView(generics.UpdateAPIView):
    queryset = Requette.objects.all() 
    serializer_class = RequetteSerializer
    

class DeleteRequetteView(generics.DestroyAPIView):
    queryset = Requette.objects.all() 
    serializer_class = RequetteSerializer

class ListeRequetteView(generics.ListAPIView):
    queryset = Requette.objects.all() 
    serializer_class = RequetteSerializer

class RequeteListAPIView(generics.ListAPIView):
    queryset = Requette.objects.select_related('sender_name', 'receiver_name')
    serializer_class = RequeteSerializer

class RequeteListUserAPIView(generics.ListAPIView):
    serializer_class = RequeteUserSerializer

    def get_queryset(self):
        utilisateur_id = self.kwargs['utilisateur_id']  # Récupérer l'ID de l'utilisateur à partir des paramètres d'URL
        queryset = Requette.objects.filter(sender_name_id=utilisateur_id)  # Filtrer les requêtes par ID de l'émetteur
        return queryset


