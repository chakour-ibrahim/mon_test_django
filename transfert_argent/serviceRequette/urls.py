from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('detailrequette/<int:pk>/', DetailRequetteView.as_view(), name="DetailRequetteView"),
    path('createrequette/', CreateRequetteView.as_view(), name="CreateRequetteView"),
    path('updaterequette/<int:pk>/', UpdateRequetteView.as_view(), name="UpdateRequetteView"),
    path('deleterequette/<int:pk>/', DeleteRequetteView.as_view(), name="DeleteRequetteView"),
    path('listerequette/', ListeRequetteView.as_view(), name="ListeRequetteView"),
    path('toutelesrequete/', RequeteListAPIView.as_view(), name="RequeteListAPIView"),
    path('utilisateurs/<int:utilisateur_id>/requetes/', RequeteListUserAPIView.as_view(), name='RequeteListUserAPIView'),
] 